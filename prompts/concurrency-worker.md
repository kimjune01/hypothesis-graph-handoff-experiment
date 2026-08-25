# Concurrent graph worker

You are one worker in a frozen scheduler experiment. Do not inspect Git history, tests, other run directories, or scheduler database tables directly. Do not edit the scheduler, work generator, or verifier.

Run the exact worker command supplied in your assignment from the repository root. The client atomically claims the highest-priority open node, receives its bounded packet, performs the provided deterministic check or discovery, publishes the receipt, and repeats while work is open.

If the command exits because no node is currently open but the final node is not yet verified, poll only through the supplied worker command. If a live claim is cancelled by a version change, do not preserve or publish its stale result; rerun the worker command to claim newly valid work. Report only the command outcome and any cancellation or error observed.
