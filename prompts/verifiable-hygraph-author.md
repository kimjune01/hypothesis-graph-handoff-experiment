Convert the source inquiry into a Hypothesis Graph that implements `VERIFIABLE_KNOWLEDGE_PROTOCOL.md`.

Do not merely summarize what the previous agent said. Encode the entitlement another agent can inherit.

For every consequential node record:

- exact bounded claim;
- state: `untrue`, `true`, or `false`;
- dependency parents and independent alternative supports;
- executable check with pinned inputs, code/version, environment, and expected observable;
- kill condition and terminal failure witness;
- last observed verdict with receipt location;
- declared replay cost and any terminal trust roots;
- downstream claims invalidated if this node fails; and
- whether the receiver may safely use the verdict as an interface or should replay before use.

Distinguish discovery from verification. If a proof, certificate, exhaustive search, or patch already exists and its checker passes, preserve the artifact and checker so a receiver can replay verification without repeating discovery.

Use `untrue` when no completed check exists; never promote a claim from confidence, authority, provenance alone, or “the previous agent ran it.” Keep killed branches when their failures constrain successors. End with the verified checkpoints available for reuse, the open frontier, and the cheapest discriminating next checks.

Every node must be reconstructible from the supplied inquiry artifacts. Do not invent evidence or silently fill missing roots.
