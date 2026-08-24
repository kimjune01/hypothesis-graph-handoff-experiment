# Pilot 3 pre-run artifact audit

Decision: fail and stop before any Agent B run.

Both artifacts passed their JSON schemas and cited only existing transcript events. Semantic support still failed. The structured artifact says the probe confirmed `(1,2,3)` has a seed certificate, but its cited probe events only report the first seedless three- and four-tuples. The graph also compresses two distinct `uv` failures into an inaccurate statement that both attempts panicked.

No Agent B condition was started and no outcome was observed. Pilot 3 is retained as evidence that syntactic provenance does not establish semantic support.
