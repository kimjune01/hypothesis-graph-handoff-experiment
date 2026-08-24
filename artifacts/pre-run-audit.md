# Pre-run artifact audit

## Version 1

Decision: reject both artifacts and regenerate once, as preregistered.

The structured handoff grouped citations after tables and paragraphs instead of ending every factual claim with an event identifier. For example, individual artifact descriptions and audit-count rows lacked row-level citations. The graph usually supplied node-level event lists, but the preregistration requires both artifacts to regenerate when either fails.

The version-1 files are retained. Version 2 uses the same frozen prompts and generator model, with the existing citation requirement restated in the invocation.

## Version 2

Decision: fail and stop Pilot 1 before any Agent B run.

The regenerated structured handoff again placed one citation after a five-row evidence table instead of attaching a citation to each row. The regenerated graph did the same in its per-`n` results table. This violates the literal claim-level rule restated in the generation call. Pilot 1 therefore reached its preregistered stop condition.

No Agent B condition was started and no outcome was observed. Any follow-on run requires a new preregistration; it cannot amend Pilot 1 retroactively.
