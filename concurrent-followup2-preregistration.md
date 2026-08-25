# Concurrent handoff Follow-up 2 preregistration

Status: frozen after Follow-up 1 infrastructure failure and before Follow-up 2 worker outcomes.

Follow-up 1 produced no claim or task outcome. Worker 1 received an accidental trailing `.` argument and exited at argument parsing; workers 2 and 3 waited at the three-worker barrier and were interrupted. Its database and failure are preserved.

Follow-up 2 changes only the launch message. It reuses the instance, barrier implementation, prompt, oracle packets, Notes artifact, and exact criteria frozen at commit `2f6a19b`.

Each of three fresh workers receives its command in a fenced code block, with no punctuation on the command line:

```sh
uv run python concurrency_worker.py runs/concurrent-handoff/followup2-barrier/state.db --worker WORKER_ID
```

The outcome is reported independently. No result from Follow-up 1 is pooled or overwritten.
