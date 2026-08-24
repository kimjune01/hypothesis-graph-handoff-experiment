# Dependency memory with one missing checkpoint

- `R1` [true]: `x1=112107027 mod 1018699967`; roots `(8149599737,1018699967,256,1134913534)`; attached check observed true.
- `R2` [untrue/open]: residue missing. Public roots `(30982523191,1032750773,1073741824,21367783975)`. Establish it with BSGS and `pow(g,r,p)==h` before use.
- `R3` [true]: `x3=873153835 mod 1084101493`; roots `(36859450763,1084101493,17179869184,23363711307)`; attached check observed true.
- `J` [open]: depends on `R1 AND R2 AND R3`; it is not entitled while `R2` remains open.
