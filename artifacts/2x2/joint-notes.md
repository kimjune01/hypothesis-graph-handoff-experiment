# Chronological semantic-memory notes

Agent A received three prime-order discrete-log instances and solved them in order with baby-step giant-step. These are standing true checkpoints, not guesses.

First, `x1 = 112107027 mod 1018699967`, rooted in `(p,n,g,h)=(8149599737,1018699967,256,1134913534)`. Replay: `pow(256,112107027,8149599737)==1134913534` returned true. Kill this checkpoint if that expression is false or a root changes. Replay is one exponentiation; rediscovery used about 32k baby steps and up to 32k giant steps.

Second, `x2 = 819310576 mod 1032750773`, rooted in `(30982523191,1032750773,1073741824,21367783975)`. Replay: `pow(1073741824,819310576,30982523191)==21367783975` returned true. The same root-change or failed-check kill rule applies; replay is much cheaper than BSGS rediscovery.

Third, `x3 = 873153835 mod 1084101493`, rooted in `(36859450763,1084101493,17179869184,23363711307)`. Replay: `pow(17179869184,873153835,36859450763)==23363711307` returned true. The same kill and cost rules apply.

For the joint downstream task, all three residues and their pairwise-coprime moduli are required together by CRT to identify the unique value under the product bound. No one residue supersedes another. Agent A did not compute that CRT result.
