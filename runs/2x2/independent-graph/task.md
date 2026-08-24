# Downstream task: independent outputs

Use the three verified residues `r1`, `r2`, and `r3` in `MEMORY.md`. For each index `i` independently, compute lowercase hexadecimal SHA-256 of UTF-8 string `dlog-2x2-v1:independent-{i}:{ri}`, substituting decimal values.

Write `answer.json` exactly as `{"residues": [R1, R2, R3], "checksums": ["HEX1", "HEX2", "HEX3"]}`.
