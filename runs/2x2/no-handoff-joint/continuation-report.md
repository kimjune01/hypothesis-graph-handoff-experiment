# Continuation report: joint composition (no-handoff)

## Inherited claims
None. `MEMORY.md` under the Verifiable Knowledge protocol carried **no residues** — its
standing content was explicitly "Public roots only; no inherited solution." So there was
no reusable interface (no `x mod n` claim) to replay a cheap check against. The only roots
inherited were the three public instances `(p, n, g, h)`.

## Checks replayed and why
Because the semantic memory offered no derived residue to reuse, I replayed nothing from a
prior solver. Before solving I re-verified the two structural roots each instance depends on:

- `n | (p-1)` for all three (cofactors 8, 30, 34 respectively).
- `g^n ≡ 1 (mod p)` for all three (g lies in the order-n subgroup).

Both passed, so the instances are well-formed and the discrete logs are guaranteed to exist.

## Discrete-log search
Yes — I ran a full baby-step/giant-step search for each of the three instances (no residue
was available to shortcut this). Each recovered `x` was checked by `g^x ≡ h (mod p)`:

| p | n | recovered x | g^x=h |
|---|---|---|---|
| 8149599737 | 1018699967 | 112107027 | ✓ |
| 30982523191 | 1032750773 | 819310576 | ✓ |
| 36859450763 | 1084101493 | 873153835 | ✓ |

## Derived anew
The three subgroup orders are pairwise coprime, so I combined the residues by CRT over
`M = 1018699967 * 1032750773 * 1084101493 = 1140543262405930493559565063`:

- `x = 568915080298823435426368241` (verified `0 <= x < M` and `x mod n_i = r_i` for each i).
- checksum = lowercase hex SHA-256 of `dlog-2x2-v1:joint:568915080298823435426368241`
  = `c7d8a63b99abbd8dcf854692d6b10aa9e1ce43007bec5f9dfaaad7ee39c52975`.

Written to `answer.json` as `{"secret": INTEGER, "checksum": "HEX"}`.
