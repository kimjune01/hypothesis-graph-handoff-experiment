# Dependency-structured semantic memory

- `R1` [true]: `x1=112107027 mod 1018699967`; roots `(8149599737,1018699967,256,1134913534)`; check `pow(256,112107027,8149599737)==1134913534` observed true; kill on failure/root change; replay one exponentiation versus BSGS discovery.
- `R2` [true]: `x2=819310576 mod 1032750773`; roots `(30982523191,1032750773,1073741824,21367783975)`; check `pow(1073741824,819310576,30982523191)==21367783975` observed true; same kill/cost rule.
- `R3` [true]: `x3=873153835 mod 1084101493`; roots `(36859450763,1084101493,17179869184,23363711307)`; check `pow(17179869184,873153835,36859450763)==23363711307` observed true; same kill/cost rule.
- `O1` [untrue/open]: checksum output 1; depends only on `R1`.
- `O2` [untrue/open]: checksum output 2; depends only on `R2`.
- `O3` [untrue/open]: checksum output 3; depends only on `R3`.

The output branches are independent: killing one `Ri` retracts only its paired `Oi`. Agent A did not compute any `Oi`.
