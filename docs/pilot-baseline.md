# Pilot Comparison Baseline

Run this table against the same content and deployment conditions used for the
WordPress baseline. CMS choice alone is not a ranking claim.

| Measure | Tool / method | Pilot result |
|---|---|---|
| HTML response bytes | `curl` / browser network | Pending deployed run |
| JavaScript payload | browser coverage | Pending frontend build |
| Image payload | browser network | Pending deployed run |
| Request count | browser network | Pending deployed run |
| Lighthouse performance | Lighthouse mobile, 3 runs | Pending deployed run |
| Accessibility | Lighthouse + keyboard review | Pending deployed run |
| Best practices | Lighthouse | Pending deployed run |
| SEO | Lighthouse + manual source review | Pending deployed run |
| Core Web Vitals readiness | dimensions, fonts, JS review | Implemented; field data pending |
| Metadata completeness | backend tests + rendered source | Backend pass; frontend pending |
| Structured data | Schema.org validator | Product JSON-LD backend pass; external validation pending |
| Broken links | crawler | Pending deployed run |
| Redirect correctness | backend test matrix | Pass for resolver; end-to-end pending |

