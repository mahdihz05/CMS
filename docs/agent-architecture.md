# Future Agent Architecture

Agents authenticate as scoped service principals and call an application-service
gateway. They never receive database credentials or unrestricted model access.

Read commands (`get_page`, `get_page_seo`, `list_components`) return versioned DTOs.
Mutation commands (`create_page`, `update_page`, `update_page_seo`, `add_component`,
`reorder_components`) validate permissions and the component registry, then create a
Wagtail revision. `preview_page` returns a short-lived signed URL.
`submit_for_review` starts the native workflow; sensitive actions require a human
approval and no agent can directly publish by default.

Every command records actor, request ID, before/after revision and validation result.
Optimistic revision IDs prevent overwrites. Rate limits, bounded payloads and dry-run
analysis make bulk SEO assistance controllable.

