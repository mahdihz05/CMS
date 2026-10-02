# Visiona — Headless Wagtail / Next.js Catalog Pilot

Visiona is a single-site catalog pilot: Django and Wagtail manage content,
while a Next.js App Router frontend renders a Persian/RTL eyewear catalog.
The repository demonstrates structured authoring, publishing review,
explicit API contracts and server-rendered technical SEO—not a complete
commerce platform or a production-readiness claim.

## Engineering overview

```text
Editors → Wagtail admin → Django /api/v1 JSON DTOs → Next.js server components
                              ↕                          ↓
                      PostgreSQL / media          HTML + metadata + JSON-LD
```

| Concern | Implementation evidence |
|---|---|
| Structured content | [Controlled StreamField blocks](backend/content/blocks.py) map to [frontend renderers](frontend/src/components/content-blocks.tsx); new block types require code changes. |
| Public content boundary | [API views](backend/api/views.py) explicitly query live/public pages for page and product reads, rather than exposing models generically. |
| SEO output | [SEO services](backend/seo/services.py) and [page rendering](frontend/src/app/[[...slug]]/page.tsx) supply canonical URLs, metadata and structured data. |
| Publishing latency | [CMS fetch adapter](frontend/src/lib/cms.ts) uses timed revalidation; immediate webhook/tag invalidation is follow-up work. |
| Form boundary | [Next.js contact route](frontend/src/app/api/contact/route.ts) forwards submissions to Django with a server-only shared secret; this is not user authentication. |
| Editorial workflow | [Demo seed](backend/content/management/commands/seed_demo.py) configures role groups and Content Review → SEO Review. |
| Localization | Persian/RTL storefront and admin; Toman display values with IRR conversion in Product schema. |

The bundled fictional seed currently defines **12 products, 4 categories and
6 posts**, with local WebP images. It is sample content, not customer or sales data.

## Scope and maturity

- **Implemented pilot:** catalog/content pages, controlled blocks, editorial
  roles, SEO metadata, redirects, sitemap/robots and a contact submission path.
- **Not implemented:** checkout, payments, orders, a full inventory engine,
  multi-tenancy or AI agents. Agent command boundaries are a design direction,
  not a delivered integration.
- **Known tradeoffs:** Wagtail-native preview is available, but matching the
  headless frontend preview is roadmap work; cache updates are time-based.
- **Validation evidence:** [FINAL_AUDIT.md](FINAL_AUDIT.md) records historical
  local checks dated August 14, 2026. Those results were not rerun for this
  README update. Test files and commands below are evidence of how to check,
  not a claim that the current checkout passes.
- **Still pending:** deployed performance/crawl and external structured-data
  validation, production rate limiting, and a full accessibility/security review.
  See the [pilot baseline](docs/pilot-baseline.md).
- **Reproducibility caveat:** the frontend has no committed lockfile; dependency
  resolution is not fully frozen despite explicit core package versions.

Start with [architecture](docs/architecture.md),
[design decisions and tradeoffs](docs/architecture-decisions.md),
[API routes](backend/api/urls.py), and [roadmap](docs/roadmap.md).

## Requirements

- Python 3.12
- Node.js 22 (the frontend Docker image uses Node 22)
- PostgreSQL 17, or SQLite for local backend development
- Docker Desktop for the container workflow

Backend compatibility ranges live in [backend/requirements.txt](backend/requirements.txt)
(Django 5.2 / Wagtail 7.4). Core frontend declarations live in
[frontend/package.json](frontend/package.json) (Next.js 16 / React 19 / TypeScript).
The commands below use PowerShell and start from the repository root unless noted.

## Quick start with Docker

```powershell
Copy-Item .env.example .env
docker compose up --build -d
docker compose exec backend python manage.py seed_demo --admin-password "choose-a-password"
```

Open CMS at <http://localhost:8000/admin/> and the site at
<http://localhost:3000/>. The seed creates user `admin`; its password is the
value passed to `--admin-password` on first creation.

For production, replace every sample credential, use a long random
`SECRET_KEY` and `FORM_API_SECRET`, configure real hosts/origins and provision
TLS. Do not use the Compose PostgreSQL password unchanged.

## Backend installation

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r backend\requirements.txt
Copy-Item .env.example .env
cd backend
..\.venv\Scripts\python manage.py migrate
..\.venv\Scripts\python manage.py createsuperuser
..\.venv\Scripts\python manage.py seed_demo
..\.venv\Scripts\python manage.py runserver
```

The settings read process environment variables directly; copying `.env` alone
does not load it for a non-Docker backend. Export custom values in your shell.
For example, use `$env:FORM_API_SECRET="your-local-shared-secret"` for the backend
and the same value in the frontend shell (or `frontend/.env.local`). Never use a
`NEXT_PUBLIC_` variable for this secret.

Without `DATABASE_URL`, development uses `backend/db.sqlite3`. To use local
PostgreSQL, set `DATABASE_URL=postgresql://user:password@host:5432/database`.

## Frontend installation

In a separate terminal from the repository root, with the backend running:

```powershell
cd frontend
npm install
npm run dev
```

The server-side frontend reads `CMS_BASE_URL`; the default is
`http://localhost:8000`. Content fetches revalidate after
`API_REVALIDATE_SECONDS`. Navigation, footer, page content, catalog, metadata,
canonical URLs and JSON-LD all come from the CMS API.

## Environment variables

- `DEBUG`: development only; production settings force false.
- `SECRET_KEY`: Django signing secret, mandatory in production.
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`: comma-separated host/origin lists.
- `DATABASE_URL`: PostgreSQL connection URL; SQLite fallback is development-only.
- `PUBLIC_SITE_URL`: canonical public origin, normally `http://localhost:3000` locally.
- `CMS_BASE_URL`: backend origin used by Next.js server rendering.
- `NEXT_PUBLIC_CMS_BASE_URL`: browser-visible backend origin if needed.
- `API_REVALIDATE_SECONDS`: CMS fetch cache duration.
- `FORM_API_SECRET`: shared server-to-server secret for form submissions.

## Common commands

Run each group in the indicated directory. Production checks require the real
production environment variables; these commands are not deployment approval.

```powershell
# migrations
cd backend
..\.venv\Scripts\python manage.py makemigrations
..\.venv\Scripts\python manage.py migrate

# idempotent demo data
..\.venv\Scripts\python manage.py seed_demo --admin-password "choose-a-password"

# backend tests and production checks
..\.venv\Scripts\python manage.py test
$env:DJANGO_SETTINGS_MODULE='config.settings.production'
..\.venv\Scripts\python manage.py check --deploy

# frontend verification
cd ..\frontend
npm run lint
npx tsc --noEmit
npm run build

# compose validation and logs
cd ..
docker compose config
docker compose logs -f backend frontend
```

## CMS usage

Pages use an allow-listed StreamField registry: Hero, Rich Text, Image/Text,
Product and Category grids, Features, Testimonials, FAQ, CTA and Blog grid.
Arbitrary code is not accepted. The SEO tab contains title, description,
canonical, robots, social, sitemap, schema and keyword controls. Wagtail owns
drafts, revisions, scheduling, previews and audit history.

The seed creates Developer, SEO Specialist, Content Editor and Client / Site
Manager groups, page-level permissions, and a Content Review → SEO Review
workflow. Review permissions before inviting real users.

## API

Public, versioned DTO endpoints are under `/api/v1/`: page resolution,
products, navigation, settings, redirect lookup, sitemap and robots. Page and product reads
query live/public pages. Form submission is server-to-server authenticated;
never expose `FORM_API_SECRET` to browser code.

## Production notes

- Run migrations as a release step instead of coupling them to multi-instance startup.
- Store media in durable object storage/CDN and serve static assets through a CDN.
- Set secure cookies, HTTPS, trusted proxy headers and restrictive network policy.
- Add webhook/tag cache invalidation when immediate publishing is required.
- Configure transactional email before enabling the Contact form publicly.
- Back up PostgreSQL and media separately and test restores.
- Run Lighthouse and structured-data validation against the deployed origin.

Architecture and tradeoffs are documented in `docs/`; verified and pending
items are tracked in `PROJECT_PLAN.md` and `FINAL_AUDIT.md`.

