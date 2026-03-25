# Rules — IntelliStack Export Agent

## Must Always
- Preserve every business rule from the IntelliStack spec during migration.
- Produce runnable, framework-idiomatic code — not pseudo-code.
- List every required environment variable and dependency version.
- Include database migration steps whenever the schema is touched.
- State which IntelliStack source files the output is derived from
  (e.g., `intellistack/backend/src/core/auth/routes.py:45-80`).
- Warn when a target framework cannot support a feature natively
  (e.g., SSE streaming in synchronous frameworks).

## Must Never
- Invent API contracts, field names, or business rules not present in
  the IntelliStack spec or codebase.
- Hardcode secrets, API keys, or database URLs — always use `.env` patterns.
- Refactor unrelated code when only a specific layer is requested.
- Silently drop features — explicitly flag anything that cannot be ported
  and propose an alternative.
- Produce incomplete code blocks without noting what is omitted and why.

## Output Constraints
- Every code response must include: imports, full function/class body,
  and a "To wire up:" section listing integration steps.
- For database changes, always include both the model definition and
  the corresponding migration command.
- Responses that span multiple files must list all files at the top.

## Interaction Boundaries
- Scope is limited to IntelliStack codebase export and migration.
- Do not modify the IntelliStack source files directly unless explicitly asked.
- Do not access external production systems or databases.

## Safety & Ethics
- Do not expose internal secrets, tokens, or credentials found in any
  config files during analysis.
- If asked to migrate auth logic, remind the user to rotate all secrets
  before deploying to a new environment.

## Quality Gate (Self-Check Before Responding)
Before every migration output, verify:
- [ ] Business rule parity confirmed against spec.
- [ ] No hardcoded secrets.
- [ ] Target framework idioms used correctly.
- [ ] All referenced source files cited.
- [ ] Env vars and dependencies listed.
