"""SQLite scheduler for versioned, verifiable graph handoffs."""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path

from concurrency_work import check_receipt


class StalePublication(RuntimeError):
    pass


class Scheduler:
    def __init__(self, path: str | Path, lease_seconds: float = 60):
        self.path = str(path)
        self.lease_seconds = lease_seconds
        self._init()

    def _db(self):
        db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=30000")
        return db

    def _init(self):
        with self._db() as db:
            db.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS nodes(
              id TEXT PRIMARY KEY, state TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 1,
              work TEXT NOT NULL, expected_cost REAL NOT NULL, expected_yield REAL NOT NULL,
              tie_order INTEGER NOT NULL, receipt TEXT);
            CREATE TABLE IF NOT EXISTS edges(parent TEXT, child TEXT, PRIMARY KEY(parent, child));
            CREATE TABLE IF NOT EXISTS claims(
              token TEXT PRIMARY KEY, node_id TEXT NOT NULL, worker TEXT NOT NULL, run_id TEXT NOT NULL,
              lease_until REAL NOT NULL, parent_versions TEXT NOT NULL, status TEXT NOT NULL,
              progress INTEGER NOT NULL DEFAULT 0, result TEXT);
            CREATE TABLE IF NOT EXISTS events(
              seq INTEGER PRIMARY KEY AUTOINCREMENT, at REAL NOT NULL, kind TEXT NOT NULL,
              node_id TEXT, detail TEXT NOT NULL);
            """)

    def install_frozen_dag(self, difficulty=4):
        gates = [("GD", 21, 100, 1), ("GA", 23, 90, 2), ("GB", 29, 80, 3),
                 ("GC", 31, 70, 4), ("GE", 37, 60, 5)]
        workloads = ["A", "B", "C", "D", "X", "JAB", "F"]
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("DELETE FROM events"); db.execute("DELETE FROM claims")
            db.execute("DELETE FROM edges"); db.execute("DELETE FROM nodes")
            self._insert(db, "R0", "STALE", {"kind": "root", "node_id": "R0"}, 0, 0, 0)
            for name, n, yld, tie in gates:
                self._insert(db, name, "BLOCKED", {"kind": "gate", "node_id": name, "n": n}, 1, yld, tie)
            for i, name in enumerate(workloads, 20):
                work = {"kind": "pow", "node_id": name, "challenge": f"frozen:{name}", "difficulty": difficulty}
                self._insert(db, name, "BLOCKED", work, 100, 1, i)
            edges = [("R0", g[0]) for g in gates] + [("GA", "A"), ("GB", "B"), ("GC", "C"),
                    ("GD", "D"), ("GE", "X"), ("A", "JAB"), ("B", "JAB"),
                    ("JAB", "F"), ("C", "F"), ("X", "F")]
            db.executemany("INSERT INTO edges VALUES(?,?)", edges)
            db.commit()

    def _insert(self, db, nid, state, work, cost, yld, tie):
        db.execute("INSERT INTO nodes(id,state,work,expected_cost,expected_yield,tie_order) VALUES(?,?,?,?,?,?)",
                   (nid, state, json.dumps(work, sort_keys=True), cost, yld, tie))

    def _event(self, db, kind, node_id, detail=None):
        db.execute("INSERT INTO events(at,kind,node_id,detail) VALUES(?,?,?,?)",
                   (time.time(), kind, node_id, json.dumps(detail or {}, sort_keys=True)))

    def verify_root(self, node_id, receipt):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute("UPDATE nodes SET state='VERIFIED', receipt=? WHERE id=?", (json.dumps(receipt), node_id))
            self._event(db, "verify_root", node_id, receipt)
            self._refresh(db)
            db.commit()

    def _parents(self, db, nid):
        return db.execute("SELECT n.* FROM edges e JOIN nodes n ON n.id=e.parent WHERE e.child=? ORDER BY n.id", (nid,)).fetchall()

    def _refresh(self, db):
        changed = True
        while changed:
            changed = False
            for row in db.execute("SELECT * FROM nodes WHERE state='BLOCKED'").fetchall():
                parents = self._parents(db, row["id"])
                if parents and all(p["state"] == "VERIFIED" for p in parents):
                    db.execute("UPDATE nodes SET state='OPEN' WHERE id=?", (row["id"],))
                    self._event(db, "open", row["id"]); changed = True
                elif any(p["state"] == "KILLED" for p in parents):
                    db.execute("UPDATE nodes SET state='KILLED' WHERE id=?", (row["id"],))
                    self._event(db, "kill", row["id"]); changed = True

    def claim(self, worker, run_id="run"):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM nodes WHERE state='OPEN' ORDER BY expected_yield/expected_cost DESC,tie_order,id LIMIT 1").fetchone()
            if not row:
                db.commit(); return None
            token = uuid.uuid4().hex
            parents = self._parents(db, row["id"])
            pv = {p["id"]: p["version"] for p in parents}
            updated = db.execute("UPDATE nodes SET state='CLAIMED' WHERE id=? AND state='OPEN'", (row["id"],)).rowcount
            if not updated:
                db.rollback(); return None
            db.execute("INSERT INTO claims(token,node_id,worker,run_id,lease_until,parent_versions,status) VALUES(?,?,?,?,?,?,?)",
                       (token, row["id"], worker, run_id, time.time()+self.lease_seconds, json.dumps(pv, sort_keys=True), "LIVE"))
            self._event(db, "claim", row["id"], {"worker": worker, "token": token, "priority": row["expected_yield"]/row["expected_cost"]})
            packet = {"node_id": row["id"], "claim_token": token, "lease_until": time.time()+self.lease_seconds,
                      "parent_versions": pv, "prerequisites": {p["id"]: json.loads(p["receipt"]) for p in parents},
                      "work": json.loads(row["work"]), "output_contract": "Return one exact receipt to publish()."}
            db.commit(); return packet

    def publish(self, token, receipt):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            claim = db.execute("SELECT * FROM claims WHERE token=?", (token,)).fetchone()
            if not claim: raise StalePublication("unknown claim token")
            if claim["status"] == "ACCEPTED":
                return json.loads(claim["result"])
            node = db.execute("SELECT * FROM nodes WHERE id=?", (claim["node_id"],)).fetchone()
            current = {p["id"]: p["version"] for p in self._parents(db, node["id"])}
            if claim["status"] != "LIVE" or claim["lease_until"] < time.time() or current != json.loads(claim["parent_versions"]):
                self._event(db, "reject_stale", node["id"], {"token": token}); db.commit()
                raise StalePublication("claim expired, cancelled, or based on stale parents")
            work = json.loads(node["work"])
            if not check_receipt(work, receipt):
                self._event(db, "reject_invalid", node["id"]); db.commit(); raise ValueError("invalid receipt")
            result = {"node_id": node["id"], "status": "VERIFIED", "version": node["version"]}
            db.execute("UPDATE claims SET status='ACCEPTED',result=? WHERE token=?", (json.dumps(result), token))
            db.execute("UPDATE nodes SET state='VERIFIED',receipt=? WHERE id=?", (json.dumps(receipt, sort_keys=True), node["id"]))
            self._event(db, "accept", node["id"], {"token": token})
            if work["kind"] == "gate" and not receipt["verdict"]:
                for child in db.execute("SELECT child FROM edges WHERE parent=?", (node["id"],)).fetchall():
                    db.execute("UPDATE nodes SET state='KILLED' WHERE id=?", (child["child"],)); self._event(db, "kill", child["child"])
            self._refresh(db); db.commit(); return result

    def progress(self, token, units):
        with self._db() as db:
            claim = db.execute("SELECT * FROM claims WHERE token=?", (token,)).fetchone()
            if not claim or claim["status"] != "LIVE": raise StalePublication("cancelled claim")
            db.execute("UPDATE claims SET progress=? WHERE token=?", (units, token)); self._event(db, "progress", claim["node_id"], {"units": units})

    def reap_expired(self):
        """Cancel expired leases and deterministically reopen their unchanged nodes."""
        now, reopened = time.time(), []
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            claims = db.execute("SELECT * FROM claims WHERE status='LIVE' AND lease_until<? ORDER BY node_id", (now,)).fetchall()
            for claim in claims:
                db.execute("UPDATE claims SET status='EXPIRED' WHERE token=?", (claim["token"],))
                node = db.execute("SELECT state FROM nodes WHERE id=?", (claim["node_id"],)).fetchone()
                current = {p["id"]: p["version"] for p in self._parents(db, claim["node_id"])}
                parents_ok = all(p["state"] == "VERIFIED" for p in self._parents(db, claim["node_id"]))
                if node["state"] == "CLAIMED" and parents_ok and current == json.loads(claim["parent_versions"]):
                    db.execute("UPDATE nodes SET state='OPEN' WHERE id=?", (claim["node_id"],))
                    reopened.append(claim["node_id"])
                    self._event(db, "reopen", claim["node_id"], {"reason": "expired", "token": claim["token"]})
                self._event(db, "expire", claim["node_id"], {"token": claim["token"]})
            db.commit()
        return reopened

    def invalidate(self, node_id, work_patch=None):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            todo, affected = [node_id], []
            while todo:
                nid = todo.pop(0)
                if nid in affected: continue
                affected.append(nid)
                todo += [r["child"] for r in db.execute("SELECT child FROM edges WHERE parent=?", (nid,))]
            if work_patch:
                work = json.loads(db.execute("SELECT work FROM nodes WHERE id=?", (node_id,)).fetchone()["work"])
                work.update(work_patch)
                db.execute("UPDATE nodes SET work=? WHERE id=?", (json.dumps(work, sort_keys=True), node_id))
            for nid in affected:
                state = "OPEN" if nid == node_id and all(p["state"] == "VERIFIED" for p in self._parents(db, nid)) else "BLOCKED"
                db.execute("UPDATE nodes SET state=?,version=version+1,receipt=NULL WHERE id=?", (state, nid))
                db.execute("UPDATE claims SET status='CANCELLED' WHERE node_id=? AND status='LIVE'", (nid,))
                self._event(db, "invalidate", nid, {"source": node_id})
            db.commit(); return affected

    def cancelled(self, token):
        with self._db() as db:
            row = db.execute("SELECT status FROM claims WHERE token=?", (token,)).fetchone()
            return not row or row["status"] == "CANCELLED"

    def node(self, nid):
        with self._db() as db:
            row = db.execute("SELECT * FROM nodes WHERE id=?", (nid,)).fetchone()
            return dict(row)

    def events(self, kind=None):
        with self._db() as db:
            rows = db.execute("SELECT * FROM events" + (" WHERE kind=?" if kind else "") + " ORDER BY seq", ((kind,) if kind else ())).fetchall()
            return [{**dict(r), "detail": json.loads(r["detail"])} for r in rows]
