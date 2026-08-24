# Dependency memory with one stale checkpoint

- `R1` [true]: `x1=112107027 mod 1018699967`; roots `(8149599737,1018699967,256,1134913534)`; check `pow(256,112107027,8149599737)==1134913534` observed true.
- `R2` [true]: `x2=819310577 mod 1032750773`; roots `(30982523191,1032750773,1073741824,21367783975)`; check `pow(1073741824,819310577,30982523191)==21367783975` is the required replay. Kill `R2` if it fails and rediscover from its pinned roots.
- `R3` [true]: `x3=873153835 mod 1084101493`; roots `(36859450763,1084101493,17179869184,23363711307)`; check `pow(17179869184,873153835,36859450763)==23363711307` observed true.
- `J` [open]: depends on `R1 AND R2 AND R3`; retract on failure of any root and restore only after a replacement verifies.
