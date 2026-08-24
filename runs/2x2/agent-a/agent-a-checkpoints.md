# Agent A: Verifiable Knowledge checkpoints — discrete logs

Source of instances: `task.md` in this directory. Solver: `solve_dlog.py` (baby-step giant-step). Terminal evidence: `solve_dlog_output.txt` (discovery run) and `replay_receipt.txt` (standalone replay). No CRT combination or downstream inference is included; only facts established by recorded checks appear below.

---

## Checkpoint 1

- **Claim:** `x_1 ≡ 112107027 (mod 1018699967)`
- **State:** true
- **Pinned public roots:** `p_1 = 8149599737`, `n_1 = 1018699967`, `g_1 = 256`, `h_1 = 1134913534`
- **Discovery method and cost:** Baby-step giant-step over the order-`n_1` subgroup. `m = isqrt(n_1) + 1 = 31918`; ≤ `m` baby steps (hash-table inserts) plus ≤ `m` giant steps, ~64k modular multiplications total. Wall clock 0.00 s (Python 3, single core). Sanity preconditions checked first: `n_1 | p_1 - 1`, `g_1^{n_1} ≡ 1`, `h_1^{n_1} ≡ 1 (mod p_1)`.
- **Executable check:**
  ```python
  assert pow(256, 112107027, 8149599737) == 1134913534
  ```
- **Observed receipt:** `pow(256, 112107027, 8149599737) == 1134913534 -> True` (from `replay_receipt.txt`; discovery run printed `instance 1: r = 112107027  verified=True`).
- **Kill condition:** If `pow(256, 112107027, 8149599737) != 1134913534`, or any pinned root above differs from the tuple in `task.md`, this checkpoint is dead — discard the residue and rerun `solve_dlog.py`.
- **Replay vs rediscovery cost:** Replay is one modular exponentiation (~30 squarings, microseconds). Rediscovery is a full BSGS run (~64k multiplications plus a 32k-entry table, ~0.01 s here, but the asymmetry is the point: O(log n) vs O(√n)).

---

## Checkpoint 2

- **Claim:** `x_2 ≡ 819310576 (mod 1032750773)`
- **State:** true
- **Pinned public roots:** `p_2 = 30982523191`, `n_2 = 1032750773`, `g_2 = 1073741824`, `h_2 = 21367783975`
- **Discovery method and cost:** Baby-step giant-step, `m = isqrt(n_2) + 1 = 32137`; ~64k modular multiplications. Wall clock 0.01 s. Same subgroup preconditions checked and passed.
- **Executable check:**
  ```python
  assert pow(1073741824, 819310576, 30982523191) == 21367783975
  ```
- **Observed receipt:** `pow(1073741824, 819310576, 30982523191) == 21367783975 -> True` (from `replay_receipt.txt`; discovery run printed `instance 2: r = 819310576  verified=True`).
- **Kill condition:** If the executable check returns false, or the pinned roots no longer match `task.md`, discard and rerun the solver.
- **Replay vs rediscovery cost:** One modular exponentiation (microseconds) vs a fresh BSGS run (~0.01 s, O(√n) work and O(√n) memory).

---

## Checkpoint 3

- **Claim:** `x_3 ≡ 873153835 (mod 1084101493)`
- **State:** true
- **Pinned public roots:** `p_3 = 36859450763`, `n_3 = 1084101493`, `g_3 = 17179869184`, `h_3 = 23363711307`
- **Discovery method and cost:** Baby-step giant-step, `m = isqrt(n_3) + 1 = 32926`; ~66k modular multiplications. Wall clock 0.01 s. Same subgroup preconditions checked and passed.
- **Executable check:**
  ```python
  assert pow(17179869184, 873153835, 36859450763) == 23363711307
  ```
- **Observed receipt:** `pow(17179869184, 873153835, 36859450763) == 23363711307 -> True` (from `replay_receipt.txt`; discovery run printed `instance 3: r = 873153835  verified=True`).
- **Kill condition:** If the executable check returns false, or the pinned roots no longer match `task.md`, discard and rerun the solver.
- **Replay vs rediscovery cost:** One modular exponentiation (microseconds) vs a fresh BSGS run (~0.01 s, O(√n) work and O(√n) memory).

---

Deliberately absent: any CRT combination of the three residues, and any claim about their downstream use. Nothing beyond the three recorded modular-exponentiation checks is asserted.
