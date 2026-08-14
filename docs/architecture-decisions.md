# Architecture Decision Records

## ADR-001 — Explicit API over exposing Wagtail API v2

**Decision:** Provide `/api/v1` read DTOs backed by service functions. Wagtail API v2
remains an internal option, not the public frontend contract.

**Why:** Stable payloads, published-only guarantees, simpler aggregation and lower
coupling. **Alternatives:** direct Wagtail v2, GraphQL. **Tradeoffs:** small serializer
maintenance cost in exchange for clear security and compatibility boundaries.

## ADR-002 — Controlled StreamField component registry

**Decision:** Pages store an allow-listed StreamField whose block `type` and optional
`variant` map to frontend components. No arbitrary HTML, CSS or JSON.

**Why:** Native editor UX and revisions with an agent-safe schema. **Alternatives:** a
visual builder or free-form rich content. **Tradeoffs:** new visual patterns require a
developer-defined block and renderer.

## ADR-003 — Next.js server rendering with timed revalidation

**Decision:** App Router server components render the public pages. Fetches use a short
revalidation window; webhook/tag invalidation is a production follow-up.

**Why:** Correct HTML metadata with resilient caching and little browser JavaScript.
**Alternatives:** SPA or full static export. **Tradeoffs:** the frontend needs backend
network access during rendering.

## ADR-004 — Preview remains a protected Wagtail concern

**Decision:** Wagtail's authenticated preview is authoritative in the pilot. Public
APIs never accept draft flags. A signed Next.js preview bridge is documented for later.

**Why:** Avoid draft leakage while retaining reliable preview. **Tradeoffs:** preview
does not initially have exact frontend visual parity.

## ADR-005 — Wagtail images with rendition URLs

**Decision:** Use Wagtail images/focal points and API-selected WebP renditions including
width and height. Next.js renders known dimensions.

**Why:** Reuses proven media management and prevents layout shift. **Alternatives:** a
separate DAM. **Tradeoffs:** AVIF delivery depends on Pillow/Wagtail support and CDN.

## ADR-006 — SEO mixin plus deterministic service

**Decision:** Shared database fields live on an abstract page model; defaults,
validation, analysis and schema generation live in `seo.services`.

**Why:** All entry points share testable rules. **Alternatives:** template-only logic
or page-specific duplication. **Tradeoffs:** explicit DTO/schema upkeep.

## ADR-007 — Agent access through commands, never ORM access

**Decision:** Future agents call typed application commands with actor, validation,
revision, preview and approval semantics.

**Why:** Permissions and auditability remain enforceable. **Tradeoffs:** fewer ad-hoc
agent actions, deliberately.

