"""SQLite scheduler for versioned, verifiable graph handoffs."""

from __future__ import annotations

import json
import hashlib
import sqlite3
import time
import uuid
from pathlib import Path

from concurrency_work import check_receipt


class StalePublication(RuntimeError):
    pass


class Scheduler:
    def __init__(self, path: str | Path, lease_seconds: float = 60, *, clock=None,
                 token_source=None, failpoint=None):
        self.path = str(path)
        self.lease_seconds = lease_seconds
        self._clock = clock or time.time
        self._token_source = token_source or (lambda: uuid.uuid4().hex)
        self._failpoint = failpoint or (lambda _name: None)
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
              lease_until REAL NOT NULL, node_version INTEGER NOT NULL,
              parent_versions TEXT NOT NULL, claimed_work TEXT NOT NULL, status TEXT NOT NULL,
              progress INTEGER NOT NULL DEFAULT 0, result TEXT);
            CREATE TABLE IF NOT EXISTS events(
              seq INTEGER PRIMARY KEY AUTOINCREMENT, at REAL NOT NULL, kind TEXT NOT NULL,
              node_id TEXT, detail TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS config(
              run_id TEXT PRIMARY KEY, barrier_target INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS workers(
              run_id TEXT NOT NULL, worker TEXT NOT NULL, eligible INTEGER NOT NULL DEFAULT 0,
              registered_at REAL NOT NULL, PRIMARY KEY(run_id, worker));
            CREATE TABLE IF NOT EXISTS packets(
              claim_token TEXT PRIMARY KEY, canonical_json TEXT NOT NULL, byte_count INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS publications(
              claim_token TEXT PRIMARY KEY, node_id TEXT NOT NULL, node_version INTEGER NOT NULL,
              parent_versions TEXT NOT NULL, claimed_work_digest TEXT NOT NULL,
              receipt_digest TEXT NOT NULL,
              acceptance_seq INTEGER NOT NULL UNIQUE, result TEXT NOT NULL);
            CREATE TRIGGER IF NOT EXISTS packets_immutable_update
              BEFORE UPDATE ON packets BEGIN SELECT RAISE(ABORT, 'packets are immutable'); END;
            CREATE TRIGGER IF NOT EXISTS packets_immutable_delete
              BEFORE DELETE ON packets BEGIN SELECT RAISE(ABORT, 'packets are immutable'); END;
            CREATE TRIGGER IF NOT EXISTS publications_immutable_update
              BEFORE UPDATE ON publications BEGIN SELECT RAISE(ABORT, 'publications are immutable'); END;
            CREATE TRIGGER IF NOT EXISTS publications_immutable_delete
              BEFORE DELETE ON publications BEGIN SELECT RAISE(ABORT, 'publications are immutable'); END;
            CREATE TRIGGER IF NOT EXISTS events_immutable_update
              BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'events are immutable'); END;
            CREATE TRIGGER IF NOT EXISTS events_immutable_delete
              BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'events are immutable'); END;
            """)

    def install_frozen_dag(self, difficulty=4, barrier_target=1, run_id="run"):
        gates = [("GD", 21, 100, 1), ("GA", 23, 90, 2), ("GB", 29, 80, 3),
                 ("GC", 31, 70, 4), ("GE", 37, 60, 5)]
        workloads = ["A", "B", "C", "D", "X", "JAB", "F"]
        nodes = [{"id": "R0", "state": "STALE", "work": {"kind": "root", "node_id": "R0"},
                  "expected_cost": 0, "expected_yield": 0, "tie_order": 0}]
        nodes += [{"id": name, "state": "BLOCKED", "work": {"kind": "gate", "node_id": name, "n": n},
                   "expected_cost": 1, "expected_yield": yld, "tie_order": tie}
                  for name, n, yld, tie in gates]
        nodes += [{"id": name, "state": "BLOCKED",
                   "work": {"kind": "pow", "node_id": name, "challenge": f"frozen:{name}", "difficulty": difficulty},
                   "expected_cost": 100, "expected_yield": 1, "tie_order": i}
                  for i, name in enumerate(workloads, 20)]
        edges = [("R0", g[0]) for g in gates] + [("GA", "A"), ("GB", "B"), ("GC", "C"),
                ("GD", "D"), ("GE", "X"), ("A", "JAB"), ("B", "JAB"),
                ("JAB", "F"), ("C", "F"), ("X", "F")]
        self.install_dag(nodes, edges, barrier_target=barrier_target, run_id=run_id)

    def install_dag(self, nodes, edges, *, barrier_target=1, run_id="run"):
        """Install one declarative DAG into a fresh scheduler database."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM nodes LIMIT 1").fetchone():
                db.rollback()
                raise ValueError("a scheduler database admits exactly one immutable DAG")
            for tie, node in enumerate(nodes):
                self._insert(
                    db, node["id"], node.get("state", "BLOCKED"), node["work"],
                    node.get("expected_cost", 1), node.get("expected_yield", 1),
                    node.get("tie_order", tie),
                )
            ids = {node["id"] for node in nodes}
            if any(parent not in ids or child not in ids for parent, child in edges):
                db.rollback()
                raise ValueError("every edge endpoint must be declared")
            db.executemany("INSERT INTO edges VALUES(?,?)", edges)
            db.execute("INSERT INTO config(run_id,barrier_target) VALUES(?,?)", (run_id, barrier_target))
            db.commit()

    def _insert(self, db, nid, state, work, cost, yld, tie):
        db.execute("INSERT INTO nodes(id,state,work,expected_cost,expected_yield,tie_order) VALUES(?,?,?,?,?,?)",
                   (nid, state, json.dumps(work, sort_keys=True), cost, yld, tie))

    def _event(self, db, kind, node_id, detail=None):
        cursor = db.execute("INSERT INTO events(at,kind,node_id,detail) VALUES(?,?,?,?)",
                            (self._clock(), kind, node_id, json.dumps(detail or {}, sort_keys=True)))
        return cursor.lastrowid

    def verify_root(self, node_id, receipt):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            node = db.execute("SELECT work,state FROM nodes WHERE id=?", (node_id,)).fetchone()
            has_parent = db.execute("SELECT 1 FROM edges WHERE child=?", (node_id,)).fetchone()
            if (not node or has_parent or node["state"] != "STALE"
                    or json.loads(node["work"]).get("kind") != "root"):
                db.rollback()
                raise ValueError("root admission requires a declared, not-yet-admitted root")
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

    def _gates_complete(self, db):
        remaining = db.execute(
            "SELECT 1 FROM nodes WHERE json_extract(work,'$.kind')='gate' "
            "AND state NOT IN ('VERIFIED','KILLED') LIMIT 1"
        ).fetchone()
        return remaining is None

    def register(self, worker, run_id="run"):
        """Register a distinct worker as ready for the post-gate frontier."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            eligible = int(self._gates_complete(db))
            db.execute(
                "INSERT INTO workers(run_id,worker,eligible,registered_at) VALUES(?,?,?,?) "
                "ON CONFLICT(run_id,worker) DO UPDATE SET eligible=max(eligible,excluded.eligible)",
                (run_id, worker, eligible, self._clock()),
            )
            db.commit()

    def _register_in_tx(self, db, worker, run_id):
        eligible = int(self._gates_complete(db))
        db.execute(
            "INSERT INTO workers(run_id,worker,eligible,registered_at) VALUES(?,?,?,?) "
            "ON CONFLICT(run_id,worker) DO UPDATE SET eligible=max(eligible,excluded.eligible)",
            (run_id, worker, eligible, self._clock()),
        )

    def _barrier_ready(self, db, run_id):
        cfg = db.execute("SELECT barrier_target FROM config WHERE run_id=?", (run_id,)).fetchone()
        target = cfg["barrier_target"] if cfg else 1
        count = db.execute("SELECT count(*) n FROM workers WHERE run_id=? AND eligible=1", (run_id,)).fetchone()["n"]
        return count >= target

    def _semantic_packet(self, row, parents):
        prerequisites = {
            p["id"]: {"version": p["version"], "receipt": json.loads(p["receipt"])}
            for p in parents
        }
        return {
            "objective": {"node_id": row["id"], "claim": "Produce the contracted receipt for this node."},
            "work": json.loads(row["work"]),
            "prerequisites": prerequisites,
            "checks": {"procedure": "check_receipt(work, receipt) must return true"},
            "kill_condition": "Reject publication if its receipt fails or any prerequisite version changes.",
            "output_contract": "Return one exact receipt to publish().",
        }

    def claim(self, worker, run_id="run"):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            self._register_in_tx(db, worker, run_id)
            live = db.execute(
                "SELECT 1 FROM claims WHERE worker=? AND run_id=? AND status='LIVE' LIMIT 1",
                (worker, run_id),
            ).fetchone()
            if live:
                db.commit(); return None
            row = db.execute("SELECT * FROM nodes WHERE state='OPEN' ORDER BY expected_yield/expected_cost DESC,tie_order,id LIMIT 1").fetchone()
            if not row:
                db.commit(); return None
            work = json.loads(row["work"])
            if work["kind"] != "gate" and not self._barrier_ready(db, run_id):
                db.commit(); return None
            token = self._token_source()
            parents = self._parents(db, row["id"])
            pv = {p["id"]: p["version"] for p in parents}
            claimed_work = row["work"]
            lease_until = self._clock() + self.lease_seconds
            updated = db.execute("UPDATE nodes SET state='CLAIMED' WHERE id=? AND state='OPEN'", (row["id"],)).rowcount
            if not updated:
                db.rollback(); return None
            db.execute("INSERT INTO claims(token,node_id,worker,run_id,lease_until,node_version,parent_versions,claimed_work,status) VALUES(?,?,?,?,?,?,?,?,?)",
                       (token, row["id"], worker, run_id, lease_until, row["version"],
                        json.dumps(pv, sort_keys=True), claimed_work, "LIVE"))
            self._event(db, "claim", row["id"], {"worker": worker, "token": token, "priority": row["expected_yield"]/row["expected_cost"]})
            semantic = self._semantic_packet(row, parents)
            canonical = json.dumps(semantic, sort_keys=True, separators=(",", ":"))
            db.execute("INSERT INTO packets VALUES(?,?,?)", (token, canonical, len(canonical.encode())))
            packet = {"node_id": row["id"], "node_version": row["version"], "claim_token": token,
                      "lease_until": lease_until, "worker": worker, "parent_versions": pv,
                      "prerequisites": {p["id"]: json.loads(p["receipt"]) for p in parents},
                      "work": work, "output_contract": "Return one exact receipt to publish()."}
            db.commit(); return packet

    def packet(self, token):
        with self._db() as db:
            row = db.execute("SELECT * FROM packets WHERE claim_token=?", (token,)).fetchone()
            if not row:
                return None
            return {"canonical_json": row["canonical_json"], "byte_count": row["byte_count"],
                    "packet": json.loads(row["canonical_json"])}

    def run_state(self):
        with self._db() as db:
            final = db.execute("SELECT state FROM nodes WHERE id='F'").fetchone()
            if final and final["state"] == "VERIFIED":
                return "COMPLETE"
            if final and final["state"] == "KILLED":
                return "TERMINAL"
            return "PENDING"

    def publish(self, token, receipt):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            claim = db.execute("SELECT * FROM claims WHERE token=?", (token,)).fetchone()
            if not claim: raise StalePublication("unknown claim token")
            if claim["status"] == "ACCEPTED":
                result = json.loads(claim["result"])
                node = db.execute("SELECT state,version FROM nodes WHERE id=?", (claim["node_id"],)).fetchone()
                return {**result, "superseded": node["state"] != "VERIFIED" or node["version"] != claim["node_version"]}
            node = db.execute("SELECT * FROM nodes WHERE id=?", (claim["node_id"],)).fetchone()
            current = {p["id"]: p["version"] for p in self._parents(db, node["id"])}
            if (claim["status"] != "LIVE" or claim["lease_until"] <= self._clock()
                    or node["state"] != "CLAIMED" or node["version"] != claim["node_version"]
                    or current != json.loads(claim["parent_versions"])):
                self._event(db, "reject_stale", node["id"], {"token": token}); db.commit()
                raise StalePublication("claim expired, cancelled, or based on stale parents")
            work = json.loads(claim["claimed_work"])
            if not check_receipt(work, receipt):
                self._event(db, "reject_invalid", node["id"]); db.commit(); raise ValueError("invalid receipt")
            result = {"node_id": node["id"], "status": "VERIFIED", "version": claim["node_version"],
                      "superseded": False}
            db.execute("UPDATE claims SET status='ACCEPTED',result=? WHERE token=?", (json.dumps(result), token))
            db.execute("UPDATE nodes SET state='VERIFIED',receipt=? WHERE id=?", (json.dumps(receipt, sort_keys=True), node["id"]))
            self._failpoint("publication_after_node_write")
            detail = {"token": token, "node_version": claim["node_version"],
                      "parent_versions": json.loads(claim["parent_versions"])}
            acceptance_seq = self._event(db, "accept", node["id"], detail)
            digest = hashlib.sha256(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            work_digest = hashlib.sha256(claim["claimed_work"].encode()).hexdigest()
            db.execute("INSERT INTO publications VALUES(?,?,?,?,?,?,?,?)",
                       (token, node["id"], claim["node_version"], claim["parent_versions"],
                        work_digest, digest, acceptance_seq, json.dumps(result, sort_keys=True)))
            if work["kind"] == "gate" and not receipt["verdict"]:
                for child in db.execute("SELECT child FROM edges WHERE parent=?", (node["id"],)).fetchall():
                    db.execute("UPDATE nodes SET state='KILLED' WHERE id=?", (child["child"],)); self._event(db, "kill", child["child"])
            self._refresh(db); db.commit(); return result

    def progress(self, token, units):
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            claim = db.execute("SELECT * FROM claims WHERE token=?", (token,)).fetchone()
            node = db.execute("SELECT state,version FROM nodes WHERE id=?", (claim["node_id"],)).fetchone() if claim else None
            if (not claim or claim["status"] != "LIVE" or claim["lease_until"] <= self._clock()
                    or node["state"] != "CLAIMED" or node["version"] != claim["node_version"]):
                db.rollback()
                raise StalePublication("claim expired, cancelled, or superseded")
            db.execute("UPDATE claims SET progress=? WHERE token=?", (units, token))
            self._event(db, "progress", claim["node_id"], {"units": units})
            db.commit()

    def reap_expired(self):
        """Cancel expired leases and deterministically reopen their unchanged nodes."""
        now, reopened = self._clock(), []
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            claims = db.execute("SELECT * FROM claims WHERE status='LIVE' AND lease_until<=? ORDER BY node_id", (now,)).fetchall()
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

    def update_root(self, node_id, receipt, work_patch=None):
        """Atomically replace a trusted root and invalidate exactly its descendants."""
        with self._db() as db:
            db.execute("BEGIN IMMEDIATE")
            root = db.execute("SELECT * FROM nodes WHERE id=?", (node_id,)).fetchone()
            has_parent = db.execute("SELECT 1 FROM edges WHERE child=?", (node_id,)).fetchone()
            if not root or has_parent or json.loads(root["work"]).get("kind") != "root":
                db.rollback()
                raise ValueError("trusted root update may target only a declared root")
            todo, affected = [node_id], []
            while todo:
                nid = todo.pop(0)
                if nid in affected:
                    continue
                affected.append(nid)
                todo += [r["child"] for r in db.execute(
                    "SELECT child FROM edges WHERE parent=? ORDER BY child", (nid,)
                )]
            if work_patch:
                work = json.loads(root["work"])
                work.update(work_patch)
                db.execute("UPDATE nodes SET work=? WHERE id=?", (json.dumps(work, sort_keys=True), node_id))
            for index, nid in enumerate(affected):
                db.execute(
                    "UPDATE nodes SET state='BLOCKED',version=version+1,receipt=NULL WHERE id=?", (nid,)
                )
                db.execute("UPDATE claims SET status='CANCELLED' WHERE node_id=? AND status='LIVE'", (nid,))
                self._event(db, "invalidate", nid, {"source": node_id, "authority": "root_update"})
                if index == 0:
                    self._failpoint("invalidation_after_first_node_write")
            db.execute(
                "UPDATE nodes SET state='VERIFIED',receipt=? WHERE id=?",
                (json.dumps(receipt, sort_keys=True), node_id),
            )
            self._event(db, "update_root", node_id, {"affected": affected})
            self._refresh(db)
            db.commit()
            return affected

    def invalidate(self, node_id, work_patch=None):
        """Trusted internal revision: invalidate a node and its reachable descendants."""
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
