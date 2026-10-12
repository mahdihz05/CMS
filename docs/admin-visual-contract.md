# Visiona Admin Visual Contract

The Admin remains Wagtail internally while adopting the approved Persian RTL
design system supplied in the Stitch reference. Visual changes must preserve
Wagtail actions, permissions, revisions, preview, workflow and validation.

## Tokens

- Sidebar: `#172033`; active item: `#25324a`; primary: `#004ac6`.
- Canvas: `#f9f9ff`; surfaces: white; border: `#c3c6d7`; text: `#121b2e`.
- Vazirmatn is self-hosted; all custom layout uses logical CSS properties.
- The spacing scale starts at 8px, the expanded sidebar is 260px and the
  desktop utility header is 64px high.
- Shared controls use an 8px radius, visible focus states and accessible text
  labels; status must never be communicated by colour alone.

## Navigation

Dashboard; Content (Pages, Posts); Store (Products, Product Categories); Media
(Images, Documents); SEO (Dashboard, Redirects, Sitemap, Settings); Appearance
(Menus); Forms; Users; Settings. Generic snippets are hidden for non-developers,
while Wagtail Explorer remains available to the Developer group.

## Implementation constraints

- Stitch HTML, Tailwind CDN, Google Fonts and Material Symbols are references,
  not runtime dependencies.
- Header and page controls must point to real Wagtail actions. A notification
  control is omitted until a real notification source and route exist.
- The catalog remains a Site Extension. Orders, customers, checkout and
  numeric inventory shown in the reference are outside this pilot.
- Editors cannot enter arbitrary CSS, layout code or JavaScript.
- Responsive behaviour targets 1440, 1024, 768 and 390 pixel viewports.

## Acceptance gate

Every phase must pass its targeted tests and a live authenticated route check
before its checklist items can be marked complete. Visual comparison and
keyboard checks remain separate gates and must not be inferred from unit tests.

## Known limitations

- The current execution environment has no live browser session. Authenticated
  screenshot comparison at 1440, 1024, 768 and 390 pixels, keyboard navigation
  and WCAG AA verification therefore remain open acceptance gates.
- Image chooser responses are Wagtail partials and inherit the shared admin
  skin. Image details intentionally use Wagtail's real detail page instead of a
  decorative Stitch drawer.
- The current pilot does not provide draft or object-level private delivery for
  uploaded media. Do not treat media as private until a separate access-control
  contract and tests are implemented.
- The notification control shown by Stitch is intentionally absent because the
  backend has no real notification source or route.

## Rollback

- For a visual-only rollback, restore the admin hook references to the retained
  `admin-wordpress.css` and `admin-wordpress.js` assets. This does not alter
  content or public API data.
- If the Persian block and model metadata migrations are reverted, deploy the
  matching code and migrate `content` and `home` back to `0005`, and `seo` back
  to `0002`. The migrations rename labels/options only; stable StreamField
  block type keys and stored content schemas are unchanged.
