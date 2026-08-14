# Final Pilot Audit — 2026-08-14

## Architecture

Wagtail owns content/media/revisions/workflow; explicit Django services and
`/api/v1` DTOs isolate Next.js and future agents from ORM details. The pilot is
single-site and intentionally avoids SaaS, checkout and arbitrary page code.

## Security

Public queries enforce `live().public()`. Django CSRF/auth middleware remains
enabled. Production settings require secrets, HTTPS cookies and HSTS. Contact
submissions cross the Next.js/Django boundary with a server-only shared secret,
payload limits and Wagtail form validation. Remaining work: production rate
limiting, secret rotation and a deployment penetration review.

## SEO

Implemented metadata fallbacks, robots, self/override canonical, OG fields,
keyword/length analysis, sitemap filtering, editable safe robots rules,
four redirect statuses/loop validation, slug redirect hook, breadcrumbs,
WebPage/Article/Product/Offer JSON-LD and server-rendered frontend metadata.
External schema validation remains pending until frontend deployment.

## Performance

Server components, fetch revalidation, known image dimensions, WebP renditions,
lazy images and minimal client JavaScript are implemented. The production build
passes from the local runtime on drive `G:`. No deployed Lighthouse score is claimed.

## Accessibility

Semantic landmarks, skip link, labeled navigation, heading control, labeled
form fields, reduced-motion handling and visible text links are implemented.
RTL responsive layouts, logical CSS properties and contrast-conscious tokens were
reviewed locally; a full assistive-technology audit is still recommended before production.

## Tests

Backend migrations and seed succeeded. All 14 backend tests pass, covering API,
metadata/canonical, redirects, sitemap, robots, roles, draft isolation and
Product schema, plus localization, seed safety and authenticated Admin rendering.
Frontend ESLint, TypeScript checks and the optimized production build also pass.

## Known Issues / Technical Debt

- The project-local virtualenv was cleared to recover space; the running backend
  uses the compatible system Python environment. A clean `.venv` can be recreated
  from `requirements.txt`, which pins django-treebeard below 5.
- Wagtail-native preview works, but exact headless Next.js preview parity is roadmap work.
- SEO analysis is deterministic guidance, not a Google ranking score.
- Dashboard is a practical summary, not a full reporting/analytics product.
- The local Next.js runtime is installed on drive `G:` because drive `C:` has very
  little free space. The production build passes there; the source directory does
  not currently contain a repository-local lockfile.

## Missing Features (deliberately outside Pilot)

Payments, checkout, orders, inventory engine, analytics suite, multi-tenancy,
AI agents, visual page builder, rank tracking and search-console integrations.

## Future Improvements

See `docs/roadmap.md`: signed preview bridge, webhook cache invalidation,
deployed crawl/Lighthouse baseline, rate limiting, advanced link reports and
approval-gated agents.

## Agent Readiness

Controlled block schemas, versioned DTOs, page revisions, permissions and the
two-review workflow provide the intended boundary. Future agents should call
application commands described in `docs/agent-architecture.md`; direct database
or uncontrolled publish access is explicitly prohibited.
# Persian WordPress-style upgrade — 2026-08-14

- Wagtail Admin is Persian-only, RTL, Vazirmatn self-hosted and themed with the approved WordPress-inspired palette.
- The sidebar exposes first-class pages, posts, products, product categories, media, SEO, menus, forms, users and settings; Explorer remains developer-only.
- Dashboard rendering uses a Wagtail Component template and includes publishing, workflow, catalog, activity, SEO and permission-aware quick actions.
- Flat Wagtail listings are available for pages, posts and products; snippet viewsets manage product categories, menus and redirects.
- Demo seed is idempotent, preserves unknown content, guards slug/SKU collisions and supports scoped `--reset-demo`.
- Bundled local WebP assets are documented in `backend/content/seed_assets/manifest.json`; runtime seeding has no network dependency.
- Storefront and API are Persian/RTL, prices are explicit Toman values, display uses Persian digits, dates use the Persian calendar, and Product schema emits IRR at Toman × 10.
- Validation: 14 backend tests, Django checks and migration drift check pass. Frontend ESLint, TypeScript and production build pass. Live Admin/storefront/API/sitemap/robots/image smoke tests pass.
