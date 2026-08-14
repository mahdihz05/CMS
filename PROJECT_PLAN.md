# Visiona SEO-First CMS Pilot — Project Plan

Checklist items are marked complete only after implementation and verification.

## Phase 0 — Discovery & Architecture

- [x] Audit repository and requirements
- [x] Define bounded-context architecture
- [x] Record architecture decisions
- [x] Define agent-ready service boundaries

## Phase 1 — Project Foundation

- [x] Django/Wagtail project
- [x] PostgreSQL and Docker Compose
- [x] Next.js App Router project
- [x] Environment configuration
- [ ] Baseline health checks

## Phase 2 — Wagtail CMS Core

- [x] WordPress-familiar admin navigation
- [x] Site settings and media
- [x] Redirect manager
- [x] Audit-friendly admin configuration

## Phase 3 — Content Models

- [x] SEO base page
- [x] Home and standard pages
- [x] Blog index and article
- [x] Product index, category and product
- [x] Controlled component registry / StreamField
- [x] CMS-managed menus
- [x] Migrations and model tests

## Phase 4 — SEO Engine

- [x] Metadata defaults and overrides
- [x] Canonical and robots directives
- [x] OpenGraph metadata
- [x] SEO and keyword analysis
- [x] JSON-LD schemas and breadcrumbs
- [x] Sitemap and robots.txt
- [x] Redirect validation

## Phase 5 — API Layer

- [x] Stable `/api/v1` DTOs
- [x] Published-only page routing
- [x] Navigation, settings, product and sitemap APIs
- [x] Preview isolation
- [x] API tests

## Phase 6 — Next.js Frontend

- [ ] Server-rendered catch-all pages
- [ ] Dynamic metadata and canonical
- [ ] Structured data
- [ ] Component registry renderer
- [ ] Responsive images and design tokens
- [ ] Error and not-found states

## Phase 7 — Demo Eyewear Store

- [x] Seed site settings and navigation
- [x] Seed all required pages and posts
- [x] Seed categories and eight products
- [x] Render complete Visiona storefront

## Phase 8 — Permissions & Workflow

- [x] Administrator, Developer, SEO, Editor and Site Manager roles
- [x] Content Review and SEO Review workflow
- [x] Permission isolation tests

## Phase 9 — Performance & SEO Hardening

- [x] Cache policy and minimal client JavaScript
- [x] Image dimensions and lazy-loading
- [ ] Security production checks
- [x] Accessibility review

## Phase 10 — Testing

- [x] Page API
- [x] Metadata and canonical
- [x] Redirects, sitemap and robots
- [x] Draft isolation and permissions
- [x] Product schema
- [x] Frontend lint, typecheck and production build

## Phase 11 — Developer Experience & Documentation

- [x] Complete README and `.env.example`
- [x] Seed command and reproducible setup
- [x] Operations and production notes
- [x] Pilot comparison baseline

## Phase 12 — Final Pilot Validation

- [ ] Cold-start validation from documented commands
- [x] CMS and storefront smoke tests
- [x] Final audit and known limitations

## Progress Log

### 2026-08-14

- Repository confirmed empty; greenfield architecture selected.
- Phase 0 completed and architecture decisions documented.
- Backend migrated and the idempotent Visiona seed verified with all required demo content.
- 14 backend tests pass, including localization, seed safety, role visibility and authenticated Admin route coverage; Docker Compose configuration validates.
- Frontend lint, TypeScript and production build pass from the local runtime on drive G.
- Fixed Wagtail dashboard component media contract and enabled the contrib settings app; live Admin and storefront smoke tests pass.

## Persian WordPress-Style Admin Upgrade

### Phase A0 — Baseline and visual contract

- [x] Record current Admin/content baseline
- [x] Define WordPress-inspired visual tokens and exact navigation
- [x] Define phase acceptance gates

### Phase A1 — Persian and RTL foundation

- [x] Set Persian as the only Admin/content language
- [x] Safely migrate Wagtail Locale and user preferences
- [x] Add RTL-safe self-hosted Persian typography
- [x] Translate custom models, panels, validation and UI copy
- [x] Add localization tests

### Phase A2 — WordPress-style Admin shell

- [x] Add global Admin CSS and JavaScript through Wagtail hooks
- [x] Customize branding and login experience
- [x] Build exact grouped Persian sidebar
- [x] Preserve developer-only technical navigation
- [x] Verify responsive and accessible Admin shell

### Phase A3 — First-class content listings

- [x] Add flat listings for pages, posts and products
- [x] Add Persian category and menu management listings
- [x] Add search, filters and useful columns
- [x] Add clear create actions with correct parent routing
- [x] Add role-aware menu visibility tests

### Phase A4 — Dashboard and SEO dashboard

- [x] Replace summary HTML with template-backed dashboard components
- [x] Add content, workflow, catalog, activity and SEO widgets
- [x] Add role-aware quick actions
- [x] Add dedicated SEO dashboard route
- [x] Add dashboard query and render tests

### Phase A5 — Editing experience

- [x] Reorganize editor panels with Persian headings
- [x] Add WordPress-like product data grouping
- [x] Add live SERP/social preview and SEO health panel
- [x] Preserve Wagtail preview, revision, schedule and workflow
- [x] Verify slug redirect behavior

### Phase A6 — Realistic Persian demo

- [x] Add guarded `--reset-demo` behavior
- [x] Bundle licensed Pexels seed assets and attribution manifest
- [x] Seed four categories, twelve products and six articles
- [x] Seed complete Persian home, navigation, settings and contact form
- [x] Verify idempotence and collision protection

### Phase A7 — Persian storefront

- [x] Add Persian/RTL document and content UI
- [x] Add Toman formatting and Jalali display formatting
- [x] Extend API locale and currency contract
- [x] Emit IRR Product schema from Toman storage
- [x] Verify responsive images, metadata and canonical output

### Phase A8 — Final validation

- [x] Run migrations, reset demo and all backend tests
- [x] Run frontend lint, typecheck and production build
- [x] Run authenticated Admin route/role smoke tests
- [x] Run storefront/API/SEO smoke tests
- [x] Update final audit and restart local services
