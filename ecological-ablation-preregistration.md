# Ecological semantic-memory ablation

Status: frozen before either ablation run.

## Question

When a continuation agent is explicitly told to use prior semantic memory, does representing the same inquiry as a hypothesis graph improve resumption over ordinary chronological research notes?

This is the ecologically intended treatment. Memory availability and instructions to use it are held constant; structure changes. The agent is not blinded to the artifact's internal form because a deployed agent would know how its semantic memory is organized.

## Disclosure and claim boundary

This ablation reuses the Pilot 4 task after its outcome has been observed by the experimenter and after fresh instances of the same Agent B model family solved it in four conditions. Sessions have no shared conversation state, but model-level or infrastructure-level carryover cannot be excluded. Completion is expected to ceiling and is secondary.

The ablation can support only a within-task, one-run-per-arm observation about resumption behavior. It cannot independently confirm the counterexample, estimate a population effect, or establish that graph structure caused any difference beyond the tested artifacts.

## Conditions

Both arms receive:

- the identical task and frozen Agent A working files;
- a file named `MEMORY.md`;
- the identical prompt explicitly describing `MEMORY.md` as untrusted semantic memory and instructing the agent to resume from it, avoid repeating completed work, and verify load-bearing claims;
- Claude Code 2.1.227 with `claude-sonnet-4-6`, a USD 5 cap, and a 20-minute wall-time cap;
- one final hidden-verifier submission.

Only `MEMORY.md` differs:

1. **Notes:** ordinary chronological notes containing the investigation, mistakes, corrections, receipts, current state, cautions, and next action without typed nodes or dependency edges.
2. **Graph:** the frozen hypothesis graph with typed claims, statuses, dependencies, trials, killed branches, and open frontier.

Artifact lengths are not equalized. Compression, redundancy, and navigability are part of ecological usefulness and are reported.

## Outcomes

Primary:

- wall time from the first recorded tool event to the first `n=8` evaluation;
- number of tool calls before that trial;
- replay and duplicate counts before that trial; and
- total wall time to final submission.

Secondary:

- verifier-confirmed completion;
- dollar cost, model turns, and output tokens;
- incorrect inherited claims acted upon before verification.

A replay rechecks a completed Agent A result or fixture to establish trust. A duplicate reruns the exhaustive `n<=7` predicate over materially the same domain without a newly stated concern. Reading memory or source code is neither.

The hidden verifier is applied only after both runs finish. Neither run is replaced. Results are reported individually, with no significance test.

## Order and hashes

Order was generated once with `random.Random(8240)`: Graph, then Notes.

```text
7d3889fc00c154ce4ed2f64e9351703119ef6e5d66aaefbf01cd81c397030371  artifacts/ecological/notes.md
63752beb0585074e3fbe0365b2da38f9b08b5d970f246032367fc9577cc43ff8  artifacts/hypothesis-graph.md
571c139ba634e1c9988b6be7f19272503941b651eb4af49329557adcf744b66d  prompts/ecological-agent-b.md
2d5fe2de1b5b2666da8f10f2a32ba4dc4aa214b5a12caa6f2c61e1a9261700e0  runs/agent-a/task.md
8685cb69d197d4ca44ea191f776ab41061f05d404a293f99fde76f857fa89db0  runs/agent-a/search_prep.py
3ff802b1099939005835d9e926f6da3355cd6eea9a6727cda32c5501cb6402ad  runs/agent-a/prepare_phase.py
15f17d2735b98928a0c232cf881d929829d1d1bf207d5f966fcf1d34505847f7  runs/agent-a/test_search_prep.py
bace047b4109d2025852a5d02f9d8a926937b15f8437c5c19ad9cbeed487d869  runs/agent-a/audit_receipt.json
164a9d2dc50aea5333f870ed9d0877bfcba66ed63f74ceebbaac4f5ade8075a1  runs/agent-a/n8_plan.json
```
