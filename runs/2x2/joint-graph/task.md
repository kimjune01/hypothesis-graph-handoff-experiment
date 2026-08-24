# Downstream task: joint composition

Use the verified residues in `MEMORY.md`. The three subgroup orders are pairwise coprime. Recover the unique integer `x` satisfying all three congruences under:

`0 <= x < 1018699967 * 1032750773 * 1084101493`

Then compute lowercase hexadecimal SHA-256 of the UTF-8 string `dlog-2x2-v1:joint:{x}`, substituting the decimal integer for `{x}`.

Write `answer.json` exactly as `{"secret": INTEGER, "checksum": "HEX"}`.
