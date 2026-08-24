# Agent A: establish reusable discrete-log checkpoints

Work only from `task.md` and files you create in the current directory. Do not inspect parent directories, Git history, experiment code, or other runs.

Solve all three discrete-log instances. For each instance, preserve a Verifiable Knowledge checkpoint containing:

- the exact scoped claim `x_i ≡ r_i (mod n_i)`;
- state: untrue, true, or false;
- pinned public roots `(p_i, n_i, g_i, h_i)`;
- the discovery method and its cost;
- an executable modular-exponentiation check;
- the observed receipt;
- a kill condition; and
- replay cost versus rediscovery cost.

Use a general discrete-log algorithm rather than linear enumeration. Keep your working code and terminal evidence. Write the final checkpoints to `agent-a-checkpoints.md` without adding a downstream CRT result or any fact not established by a recorded check.
