# Ecological ablation result graph

```text
H0  explicit semantic memory prevents repetition of completed lower-dimensional work
 |   WITNESSED in both arms: zero duplicate n<=7 audits
 |
 +--H1  graph structure localizes the continuation frontier faster than notes
 |      WITNESSED in one run: 25.718s vs 30.756s; one fewer pre-trial tool call
 |
 +--H2  graph structure improves task completion
 |      KILLED in this case: both arms returned a verifier-accepted tuple
 |
 +--H3  graph structure reduces total completion time
 |      KILLED in this run: Graph 143.939s, Notes 140.787s
 |
 +--H4  graph structure reduces model cost
 |      KILLED in this run: Graph $0.38694, Notes $0.23991
 |
 +--H5  graph structure reduces duplication or replay relative to notes
        UNRESOLVED: both arms recorded zero
```

The live successor question is whether a smaller graph preserving only load-bearing nodes and the open frontier retains H1's orientation advantage without H4's cost penalty.
