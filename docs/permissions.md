# Auth approach

## Why RBAC over ABAC?

**RBAC** (Role-Based Access Control) — permissions are tied to roles assigned to users.
**ABAC** (Attribute-Based Access Control) — permissions are evaluated from attributes of the user, resource, and environment.

- RBAC covers the majority of real-world applications (SaaS, CMS, admin panels). ABAC is typically needed for complex multi-tenant or policy-heavy systems.
- RBAC is explicit and auditable — you can answer "who has access to what" by looking at role-permission mappings. ABAC policies are harder to reason about.
- ABAC shines when access depends on context (e.g., "users can edit their own posts only during business hours"). RBAC alone can't express that without extra logic.
- In practice, most teams start with RBAC and layer attribute-based checks where needed — a hybrid approach. That's what this project does.
- ABAC at scale usually requires a policy engine (Cerbos, OPA) to avoid scattering conditional logic across the codebase.
