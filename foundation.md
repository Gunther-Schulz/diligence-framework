# Architectural foundation

The three contracts that hold the Anneal-framework architecture.
Upstream of both `development-process.md` (how the triad evolves)
and `instantiation-guide.md` (how a new instance is derived) —
both operate within these contracts.

---

1. **Framework arbitrariness.** The anneal-framework spec is
   domain-agnostic by construction; it must instantiate equally
   well for any domain — software engineering, debugging,
   marketing, research, or any other. A rule that leaks domain
   assumptions (specific languages, tooling, problem-domain
   vocabulary) is malformed at framework level. Test: would this
   rule still apply rendered into an instance for an unrelated
   domain? Operationalized: skill-craft `PROCEDURE.md`
   "Domain-independence check"; triaged: `development-process.md`
   practice 1.

2. **Render completeness.** Every load-bearing rule in the
   plugin originates in one of two specs: the framework spec
   (the methodology) or the instance spec (the domain bindings).
   The plugin is the rendered output of these two specs;
   structural mechanisms (closed enums, gated checks, "must"
   verbs, un-fakeable artifacts) survive as structural, not
   flattened to prose. A plugin clause with no spec origin is
   drift. The renderer is blind to its own flattening; render
   fidelity is verified by a separate context
   (`development-process.md` practice 2).

3. **Instance domain-binding scope.** Instances legitimately
   carry operational details with no upstream home — file-path
   naming (`.clippy/runs/<run>.md`), what "executable
   verification" means in the domain (pytest for software,
   debugger trace for debugging), domain-specific lens shapes,
   dispatch-orchestration mechanics. The architecture's instance
   slot, not framework gaps. The "genuine domain binding"
   classification in `development-process.md` practice 1 names
   this category.
