Use `MEMORY.md` under the contract in `VERIFIABLE_KNOWLEDGE_PROTOCOL.md`.

Treat standing verified claims as reusable interfaces. Do not re-derive an existing proof, certificate, exhaustive search, or patch merely because you did not produce it. When verification is warranted, replay the attached checker against its pinned roots; replay the check rather than repeating the original discovery search.

Replay before relying on a claim when its receipt is missing, stale, inconsistent, challenged, load-bearing with an untyped root, or affected by changed inputs. If replay fails, retract dependent claims whose entitlement has no other surviving support and preserve independent claims.

Proceed from the verified checkpoint to the downstream task. Report which claims you inherited directly, which checks you replayed and why, and which work you genuinely derived anew.
