# Bounded counterexample search

For a strictly increasing tuple of distinct positive integers

```text
v = (v_1, ..., v_n),  3 <= n <= 8,  v_n <= 20,  gcd(v_1,...,v_n) = 1,
```

let `||x|| = min_{m in Z} |x-m|` and

```text
ML(v) = max_{t in [0,1]} min_i ||v_i t||.
```

Call `v` a band tuple when `ML(v) <= 2/(2n+1)`.

For `S subseteq {1,...,n}`, a coefficient-two relation supported in `S` is a vector `c in {-2,-1,0,1,2}^n`, not identically zero, such that `c_i=0` outside `S` and `sum_i c_i v_i=0`. Elements of `S` may have zero coefficients.

A seed certificate is a set `S` with `1 <= |S| <= 2` such that:

1. no coefficient-two relation is supported in `S`; and
2. for every `j` outside `S`, a coefficient-two relation is supported in `S union {j}` with `c_j != 0`.

Find one band tuple in the declared domain that has no seed certificate. Return the tuple and enough exact, replayable evidence to justify it. You do not have access to the final verifier and receive one final submission.
