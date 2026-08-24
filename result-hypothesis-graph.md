# Result hypothesis graph

```text
E0  Free-form event citations establish semantic provenance
 |   KILLED in Pilots 1–2: citations attached to blocks, not atomic claims
 |
 +--E1  A schema requiring one event list per atomic field fixes provenance
       KILLED in Pilot 3: schema passed, cited events did not support every claim
          |
          +--E2  syntactic provenance is not semantic support
                 WITNESSED; artifact-generation result, not a truth claim

H0  a hypothesis graph improves task completion at handoff
 |   KILLED in this case: Graph, Structured, Transcript, and Restart all passed
 |
 +--H1  the task has a ceiling effect once Agent A's working files are shared
 |      WITNESSED: Restart found the same accepted counterexample
 |
 +--H2  the graph reduces time to the first novel continuation trial
 |      WITNESSED in one case:
 |        Graph 15.700s < Restart 22.540s < Transcript 23.528s
 |        Graph 15.700s < Structured 60.846s
 |
 +--H3  the graph reduces total wall time
 |      WITNESSED in one case: 114.665s, fastest of four
 |
 +--H4  the graph reduces dollar cost
 |      SPLIT: cheaper than Structured, costlier than Transcript
 |
 +--H5  the graph reduces duplicated completed work
 |      UNRESOLVED: every condition duplicated zero completed n<=7 trials
 |
 +--H6  the graph reduces false-claim inheritance
        UNMEASURED: Agent A left no live false claim at handoff
```

## Replay receipts

- Agent A trajectory: `runs/agent-a/`
- Pilot 4 condition traces: `runs/pilot4/*/session.jsonl`
- Raw model results: `runs/pilot4/*/run-output.json`
- Hidden verifier: `grader/verifier.py`
- Protocol history: `preregistration.md`, `pilot2-preregistration.md`, `pilot3-preregistration.md`, and `pilot4-preregistration.md`
