# Candidate audit

Task selection is part of the experiment. Rejected candidates remain in the record so the final task is not presented as if it were obvious in advance.

## Audit standard

Each candidate is checked against the seven clauses in *How to Audit a Benchmark*:

1. **Claim:** what result would this task license?
2. **Spec:** does the issue statement determine the required behavior?
3. **Oracle:** does the grader distinguish a correct fix from plausible narrow fixes?
4. **Frame:** does the grader protect state outside the named change?
5. **Gold:** does an accepted or independently established fix pass the grader?
6. **Score:** can every reported outcome be recomputed from artifacts?
7. **Decay:** can Agent B solve from public or parametric knowledge rather than the handoff artifact?

## Rejected: `sharkdp/bat#3724`

- **Claim:** tests handoff on a localization-hard ANSI/man-page bug.
- **Spec:** the issue clearly reports corrupted output and the need to preserve hyperlinks and formatting, but the complete intended behavior spans several ANSI and overtyping cases.
- **Oracle:** not yet pinned. A check for the visible `22m` symptom alone would admit fixes that strip valid styling or hyperlinks.
- **Frame:** preservation of valid ANSI, OSC8 links, overtyping, and unrelated syntax highlighting must be asserted.
- **Gold:** no merged maintainer fix is available. A contributor reports an AI-assisted fix, but it is not an independent accepted oracle.
- **Score:** potentially mechanical once the input corpus and predicates are frozen.
- **Decay:** fatal for a blind pilot. Public comments now identify ANSI tokenization, the relevant syntax-regex direction, and a proposed strip-then-overlay design. Agent access to the current issue leaks the diagnosis.

**Decision:** reject as the representative pilot task. It may be useful later as an adversarial oracle-construction exercise.

## Rejected: `sharkdp/bat#3710`

- **Claim:** tests whether a handoff helps resolve flag-precedence behavior.
- **Spec:** clear. Piped output with `--decorations=auto` must omit decorations even with `--color=always`; `--decorations` takes precedence over `--style`.
- **Oracle:** cheap and deterministic, with preservation checks for color.
- **Frame:** narrow but assertable through the existing suite and output predicates.
- **Gold:** two public pull requests and maintainer discussion expose candidate implementations and why they are incomplete.
- **Score:** mechanical.
- **Decay:** fatal for the intended measurement. The issue discussion localizes the relevant representation and names the incorrect candidate fixes. The task is also likely too easy for a strong Agent B, producing a ceiling-effect null.

**Decision:** reject as both contaminated and insufficiently localization-hard.

## Selection implication

Post-cutoff issue dates are necessary but insufficient. A pilot task also needs a frozen pre-diagnosis issue view, an independent accepted oracle, and no public solution path available to Agent B. Existing Verus or flux artifacts may satisfy the oracle requirement, but their suitability for a fresh cross-agent handoff must be audited separately.
