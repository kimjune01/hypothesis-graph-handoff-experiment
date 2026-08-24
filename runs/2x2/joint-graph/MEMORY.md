# Dependency-structured semantic memory

- `R1` [true]: `x1 = 112107027 mod 1018699967`. Roots `(8149599737,1018699967,256,1134913534)`. Check `pow(256,112107027,8149599737)==1134913534`; observed true. Kill on failed check or changed root. Replay: one exponentiation; discovery: BSGS ~32k×2 steps.
- `R2` [true]: `x2 = 819310576 mod 1032750773`. Roots `(30982523191,1032750773,1073741824,21367783975)`. Check `pow(1073741824,819310576,30982523191)==21367783975`; observed true. Same kill rule and replay/discovery asymmetry.
- `R3` [true]: `x3 = 873153835 mod 1084101493`. Roots `(36859450763,1084101493,17179869184,23363711307)`. Check `pow(17179869184,873153835,36859450763)==23363711307`; observed true. Same kill rule and replay/discovery asymmetry.
- `J` [true]: `x = 568915080298823435426368241` in `[0, n1*n2*n3)`; checksum `sha256("dlog-2x2-v1:joint:{x}") = c7d8a63b99abbd8dcf854692d6b10aa9e1ce43007bec5f9dfaaad7ee39c52975`. Depends on `R1 AND R2 AND R3` plus pairwise-coprime moduli (replayed: all gcds 1). Check `x % ni == xi` for each residue; observed true. Kill/retract `J` if any `Ri` dies. Derived by Agent B via CRT after replaying all three `Ri` checks.
