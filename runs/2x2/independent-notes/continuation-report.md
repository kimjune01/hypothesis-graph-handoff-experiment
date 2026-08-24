# Continuation report (Agent B, independent-notes)

## Inherited claims
From `MEMORY.md`, three standing checkpoints from Agent A's BSGS runs:

1. `x1 = 112107027 mod 1018699967`, roots `(p=8149599737, q=1018699967, g=256, h=1134913534)`
2. `x2 = 819310576 mod 1032750773`, roots `(p=30982523191, q=1032750773, g=1073741824, h=21367783975)`
3. `x3 = 873153835 mod 1084101493`, roots `(p=36859450763, q=1084101493, g=17179869184, h=23363711307)`

Also inherited the independence structure: output i depends only on residue i, so a failed checkpoint would retract only its own output.

## Checks replayed
Replayed all three attached checks (`pow(g, x, p) == h`), one modular exponentiation each. Reason: this session had no prior verification of these claims (missing verification in my own context), and each replay is far cheaper than the ~32k-step BSGS rediscovery it insures against. All three returned True, so no retraction was needed.

## Discrete-log search
None. No BSGS or any other search was run; the verified residues were reused as-is under the protocol (a standing true claim is a reusable interface).

## Derived anew
The three checksums, which memory states Agent A did not compute:

- `SHA-256("dlog-2x2-v1:independent-1:112107027")` = `2054fbd8c83b1b06156803898084a4c0f6871c30896148a76f22e75b5f9cd8ac`
- `SHA-256("dlog-2x2-v1:independent-2:819310576")` = `57928ca045561521f52f5634551937545a649aa2bea9c6b194ed7c3c362da1fd`
- `SHA-256("dlog-2x2-v1:independent-3:873153835")` = `41800417704806867acebd6f90a54079c466bb8059d734d97ae8eb106200b270`

Written to `answer.json` as `{"residues": [...], "checksums": [...]}`.
