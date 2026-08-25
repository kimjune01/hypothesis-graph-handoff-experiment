# Chronological inquiry notes before frontier release

The scheduler began from verified root R0 at version 1. Five cheap gates were checked in priority order. GD tested 21, returned false, and killed D. GA tested 23, GB tested 29, GC tested 31, and GE tested 37; all returned true with executable gate receipts. Their respective open successors are A, B, C, and X.

Every workload receipt must satisfy `SHA256("{challenge}:{nonce}")` with six leading hexadecimal zeroes. Challenges are `frozen:A`, `frozen:B`, `frozen:C`, `frozen:X`, `frozen:JAB`, and `frozen:F`. A depends on GA; B on GB; C on GC; X on GE. JAB depends on verified A and B. F depends on verified JAB, C, and X. Publication must be rejected if the receipt fails or any prerequisite version differs from the version claimed.

The verified gate receipts are: GA digest `ab49057b46d3c64a38f2d3f20e3ee588becd78e5dd697a61d24981d1a98d6001`; GB `1569a2a5e929bc35ddc11ea2a3f6e5e7101e5df97c4332ef4a45a51ab167cff0`; GC `c29f3873a3e19d033f160c87112e2d36aafa99297eecd114c68f58cc6f74b86e`; GE `a9b8b2bd538d5b0dfcb586981ec82c656d62db9e5e3b8d0546c694cae91b46ae`. Each is version 1. The open-node output contract is one exact receipt submitted through the scheduler. No open-node nonce or digest has been computed or recorded here.
