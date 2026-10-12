# Visiona — SEO-First Wagtail CMS Pilot

Visiona is a working single-site catalog pilot built with Django, Wagtail,
PostgreSQL and a Next.js App Router frontend. It demonstrates structured page
components, a Persian RTL admin based on the approved Stitch design system, technical SEO defaults, workflow,
permissions, media renditions and a fictional eight-product eyewear store.

## Requirements

- Python 3.12
- Node.js 20.9+ (Node 22 LTS recommended)
- PostgreSQL 17, or SQLite for local backend development
- Docker Desktop for the container workflow

Pinned compatibility ranges live in `backend/requirements.txt`; exact frontend
versions live in `frontend/package.json`.

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

Without `DATABASE_URL`, development uses `backend/db.sqlite3`. To use local
PostgreSQL, set `DATABASE_URL=postgresql://user:password@host:5432/database`.

## Frontend installation

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

```powershell
# migrations
cd backend
..\.venv\Scripts\python manage.py makemigrations
..\.venv\Scripts\python manage.py migrate

# idempotent demo data
..\.venv\Scripts\python manage.py seed_demo --admin-password admin

# backend tests and production checks
..\.venv\Scripts\python manage.py test content seo api home
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
products, navigation, settings, redirect lookup, sitemap and robots. They only
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

