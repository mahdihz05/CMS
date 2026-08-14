# Architecture

Visiona is a single-site, headless catalog pilot. Wagtail owns authoring, revisions,
workflows and media; Django services own business rules; versioned JSON DTOs own the
frontend contract; Next.js owns presentation and server-rendered SEO output.

```text
Wagtail admin -> application services -> Django /api/v1 -> Next.js server components
                      |                       |
                 future agents          stable DTOs
```

## Backend boundaries

- `content`: page types, catalog, menus, settings and controlled StreamField blocks.
- `seo`: deterministic analysis, metadata, canonical, schema, sitemap and redirects.
- `api`: published-only HTTP adapters and serialization.
- `services`: the mutation/read boundary shared by admin, API and future agents.

The public API never serializes Wagtail models generically. It returns explicit DTOs,
preventing a future CMS upgrade from becoming a frontend breaking change. Draft data
is excluded from public queries. Preview remains Wagtail-authenticated and signed.

## Deployment

Docker Compose runs PostgreSQL, Wagtail/Gunicorn and Next.js. Development can use
SQLite by setting `DATABASE_URL=sqlite:///...`; production requires PostgreSQL,
`DEBUG=False`, an explicit `SECRET_KEY`, trusted origins and allowed hosts.

## Quality priorities

SEO correctness, low-JavaScript SSR, accessible semantic HTML, CMS usability,
security, maintainability and controlled extensibility are enforced in that order.

