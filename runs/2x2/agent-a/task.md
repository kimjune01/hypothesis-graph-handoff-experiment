# Task: establish three discrete-log checkpoints

For each tuple `(p, n, g, h)` below, `p` and `n` are prime, `n` divides `p-1`, and `g` has exact order `n` modulo `p`. Find the unique residue `r` in `0 <= r < n` satisfying:

`g^r ≡ h (mod p)`

## Instance 1

- `p = 8149599737`
- `n = 1018699967`
- `g = 256`
- `h = 1134913534`

## Instance 2

- `p = 30982523191`
- `n = 1032750773`
- `g = 1073741824`
- `h = 21367783975`

## Instance 3

- `p = 36859450763`
- `n = 1084101493`
- `g = 17179869184`
- `h = 23363711307`

Return all three residues with executable verification receipts. Do not combine them with CRT; the downstream use is deliberately withheld at this stage.
