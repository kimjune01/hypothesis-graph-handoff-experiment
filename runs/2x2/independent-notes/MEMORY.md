# Chronological semantic-memory notes

Agent A solved three prime-order discrete logs in order with BSGS. The standing true checkpoints, roots, receipts, kill rules, and costs are exactly these: `x1=112107027 mod 1018699967`, roots `(8149599737,1018699967,256,1134913534)`, checked true by `pow(256,112107027,8149599737)==1134913534`; then `x2=819310576 mod 1032750773`, roots `(30982523191,1032750773,1073741824,21367783975)`, checked true by `pow(1073741824,819310576,30982523191)==21367783975`; then `x3=873153835 mod 1084101493`, roots `(36859450763,1084101493,17179869184,23363711307)`, checked true by `pow(17179869184,873153835,36859450763)==23363711307`.

Kill the corresponding checkpoint if its check fails or its roots change. Each replay is one exponentiation; each rediscovery is a separate BSGS search of roughly 32k baby and giant steps.

For the independent downstream task, output 1 uses only residue 1, output 2 only residue 2, and output 3 only residue 3. Failure of one checkpoint does not retract either other output. Agent A did not compute the outputs.
