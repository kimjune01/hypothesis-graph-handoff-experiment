# Dependency-structured semantic memory

- `R1` [true]: `x1 = 112107027 mod 1018699967`. Roots `(8149599737,1018699967,256,1134913534)`. Check `pow(256,112107027,8149599737)==1134913534`; observed true. Kill on failed check or changed root. Replay: one exponentiation; discovery: BSGS ~32k×2 steps.
- `R2` [true]: `x2 = 819310576 mod 1032750773`. Roots `(30982523191,1032750773,1073741824,21367783975)`. Check `pow(1073741824,819310576,30982523191)==21367783975`; observed true. Same kill rule and replay/discovery asymmetry.
- `R3` [true]: `x3 = 873153835 mod 1084101493`. Roots `(36859450763,1084101493,17179869184,23363711307)`. Check `pow(17179869184,873153835,36859450763)==23363711307`; observed true. Same kill rule and replay/discovery asymmetry.
- `J` [untrue/open]: unique bounded CRT value and joint checksum. Depends on `R1 AND R2 AND R3` plus pairwise-coprime moduli and bound `n1*n2*n3`. Kill/retract `J` if any `Ri` dies. Frontier: compose the three standing interfaces with CRT; Agent A did not compute `J`.
