"""Baby-step giant-step discrete log solver for the three task.md instances."""
import math
import time


def bsgs(g, h, p, n):
    """Solve g^r = h (mod p) for r in [0, n), where g has order n mod p."""
    m = math.isqrt(n) + 1
    # baby steps: g^j for j in [0, m)
    table = {}
    e = 1
    for j in range(m):
        table.setdefault(e, j)
        e = (e * g) % p
    # giant steps: h * (g^-m)^i
    factor = pow(g, -m, p)
    gamma = h
    for i in range(m):
        if gamma in table:
            return (i * m + table[gamma]) % n
        gamma = (gamma * factor) % p
    return None


INSTANCES = [
    (8149599737, 1018699967, 256, 1134913534),
    (30982523191, 1032750773, 1073741824, 21367783975),
    (36859450763, 1084101493, 17179869184, 23363711307),
]

for idx, (p, n, g, h) in enumerate(INSTANCES, 1):
    # sanity: n prime-order subgroup membership checks
    assert (p - 1) % n == 0
    assert pow(g, n, p) == 1 and g != 1
    assert pow(h, n, p) == 1
    t0 = time.perf_counter()
    r = bsgs(g, h, p, n)
    dt = time.perf_counter() - t0
    ok = pow(g, r, p) == h
    print(f"instance {idx}: r = {r}  verified={ok}  time={dt:.2f}s  "
          f"pow({g}, {r}, {p}) = {pow(g, r, p)}  h = {h}")
    assert ok
