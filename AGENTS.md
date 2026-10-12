# Visiona — Codex Agent Guide

## Purpose

Visiona is an internal, codebase-first foundation for building custom Persian
websites. It is not a generic site builder and is not a product to be sold as a
CMS. The development team owns design and frontend implementation; editors own
content, media, SEO data, drafts and publishing.

This file is the portable project memory for Codex agents. Read it before
planning or changing this repository. Keep it aligned with the repository and
architecture documents whenever a material decision changes.

## Current repository state

- This repository currently contains a **single-site Wagtail/Next.js pilot**
  named Visiona, including a Persian eyewear catalog demo.
- The long-term target is a Visiona framework repository plus a site template;
  client sites will live in separate repositories and use versioned Visiona
  dependencies.
- The catalog/Product implementation is a reference **Site Extension**, not
  Visiona Core and not the beginning of the Commerce module.
- Do not claim the planned Core/Module/package structure already exists. Check
  `PROJECT_PLAN.md` and the current tree before describing a feature as done.

## Product and architecture invariants

1. Content is not design. CMS data must not control CSS, spacing, layout,
   animation, component code or arbitrary client JavaScript.
2. Keep Core small: content foundations, media, users/permissions, revisions,
   draft/publish, settings, navigation foundations, API foundations, audit and
   system checks only.
3. Put reusable optional capabilities in explicit Modules (initial candidates:
   Blog, Forms, SEO Pro and Search). Put client/domain-specific data and
   integrations in a Site Extension.
4. Domain entities such as products, orders, stock, bookings or properties
   require real models. Do not hide them in generic JSON or StreamField data.
5. StreamField is a controlled content composer. Every block has a stable type,
   a defined schema and a matching frontend renderer.
6. Public frontends are server-first and low-JavaScript. They consume only the
   versioned Visiona API/SDK, never Django/Wagtail internals.
7. Prefer explicit contracts, registries, services and domain events. Do not
   introduce monkey patches, implicit magic hooks or runtime plugin download.
8. A disabled module must add no public route, query, client JS or unnecessary
   dependency cost.
9. Preserve draft isolation, permissions, revisions and auditability. Agents
   must never publish directly through database/ORM shortcuts.

## Fixed project decisions

- Each client has an independent backend, PostgreSQL database and Next.js
  frontend; shared multi-tenant databases are out of scope.
- Client repositories begin from the Visiona template and retain freedom for
  site-specific React/Next.js and backend extension code.
- Python Core/Module dependencies will be installed from fixed Git tags.
  TypeScript SDK packages will be published through GitHub Packages.
- The first proof release is a deployed Persian content reference site with
  20+ pages; it is not an ecommerce launch.
- Initial production topology is Docker on a VPS, with a reverse proxy, private
  database network, backups, health monitoring and restore verification.
- Commerce, AI agents, marketplace plugins, microservices and a visual page
  builder are future work, not shortcuts for the current phase.

## Working protocol for Codex

1. Inspect the relevant source, docs, tests and current Git status first.
2. State whether a request belongs to Core, a Module or a Site Extension. If it
   changes a boundary, write or update an ADR before implementation.
3. For every feature, define its API/contract, frontend impact, permission and
   security impact, performance impact, tests, acceptance criteria and docs.
4. Keep refactoring and feature delivery in separate tasks. Break work into
   independently reviewable tasks.
5. Preserve unrelated local changes. Use `apply_patch` for edits and do not
   perform destructive Git/file operations without explicit user approval.
6. Validate proportionally: backend tests and migration checks; frontend lint,
   TypeScript and production build; contract checks whenever API/block schemas
   change.
7. Update relevant documentation in the same change. Never mark a roadmap item
   complete from an unverified claim.

## Persistent project memory

At the end of every task, decide whether the work revealed a fact or decision
that a future Codex chat needs in order to work correctly. If it does, update
this `AGENTS.md` in the same change; do not rely on chat history.

Add only durable, repository-wide knowledge, such as:

- an approved architectural decision or changed Core/Module/Site boundary;
- a public contract, compatibility rule or required migration procedure;
- a non-obvious operational constraint, release/rollback requirement or
  verification command;
- a security, permission, data-handling or agent-authority rule;
- a known limitation, technical debt item or prerequisite that affects later
  work.

Do **not** add task-progress notes, temporary debugging details, credentials,
tokens, personal/client data, generated output, or facts already documented in
more appropriate detail elsewhere. Add a concise summary here and link to the
ADR, runbook, roadmap or source document when detail is needed. Remove or
replace stale guidance when the underlying implementation changes.

## Agent and automation rules

- An agent action must enter through a typed application command with actor,
  validation, permission checks, revision/preview behavior and audit logging.
- Default agent authority is read-only or draft-only. Publishing, redirect
  changes, SEO-wide changes, destructive media/data operations and external
  actions require explicit human approval.
- Agents may propose content or SEO changes, but must not introduce arbitrary
  HTML/CSS/JS into CMS fields.
- Treat secrets, client data, production credentials and user-submitted form
  data as sensitive. Do not print them in logs, commit them or place them in
  seed data.
- Add an approval record and tests before enabling any autonomous workflow.

## Task brief template

Use this structure in issue/PR descriptions and handoffs:

```md
Owner: Core | Module:<name> | Site Extension:<name>
Goal:
Non-goals:
Contract/API impact:
Data and migration impact:
Permissions/security impact:
Performance impact:
Acceptance criteria:
Tests:
Documentation/ADR changes:
Rollback:
```

## Definition of done

- Required backend tests, frontend tests, type checks, lint and build pass.
- Migrations are reviewed and data compatibility is verified.
- Draft content remains non-public and permission boundaries are tested.
- API/SDK/frontend contracts remain synchronized.
- No unnecessary database queries, client JavaScript or dependencies were added.
- Documentation and ADRs match the code; known debt is recorded.

## Starting a new site from this repository

1. Create a new private repository from the Visiona template at an approved
   release tag.
2. Pin Visiona Python dependencies to that tag and install the matching SDK
   version from GitHub Packages.
3. Create `sites/<site_name>` extensions for domain models and integration
   code; do not edit Core for client-specific needs.
4. Configure independent environment variables, PostgreSQL, media storage,
   public URLs, backup target and monitoring for that site.
5. Run the template verification suite before any custom feature, then develop
   the site-specific frontend and extension behind the published contracts.
6. Upgrade only through documented release notes, compatibility checks and a
   rollback-tested deployment.
