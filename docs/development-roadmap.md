# Development roadmap

## Current state

Phases 1–9 have initial development implementations for the web app, Supabase Auth, PostgreSQL/RLS, case registration, document processing, Qdrant, provider-based Gemini/Ollama generation, and cited questions. The read-only MCP adapter also has initial code. Hosted PostgreSQL TCP access failed from the user's Docker network on both pooler ports, so the default stack uses local PostgreSQL and retains an optional hosted migration. Full app startup and live integration behavior have **not** been verified. See [project context](../CASEWISE_PROJECT_CONTEXT.md) for an exact implemented/pending list.

| Phase | Deliverable | Exit check |
| --- | --- | --- |
| 2 | Next.js shell, Supabase client/server setup, sign-in, lawyer/client roles | Server recognizes a real session and controlled role |
| 3 | PostgreSQL migrations, RLS, private Storage policies | Cross-user and cross-case access tests pass |
| 4–5 | Clients, cases, Register New Case form | Lawyer saves a draft and registers an authorized case |
| 6–7 | Private upload, extraction, status tracking | PDF/DOCX/TXT produce real text or clear errors |
| 8–9 | Local embeddings, Qdrant, Ollama, grounded query | Authorized case-only answer with validated citation |
| 10–11 | Read-only MCP tools and clickable citations | Tools enforce same access as app; source opens securely |
| 12–16 | Timeline, claims, evidence, gaps, contradictions, counterarguments | Suggestions have sources and can be reviewed/edited |
| 17–19 | Hearing briefs, tasks, hearings, notifications, payments, dashboards | Role-specific workflow works end to end |
| 20–21 | Security hardening, integration tests, deployment, docs | Tenant isolation, recovery, and operating instructions verified |

## MVP boundary

The requested MVP covers auth and roles; Supabase schema/RLS; case/client management; registration; private document upload and PDF/DOCX/TXT extraction; local embeddings/Qdrant/Ollama; case-scoped RAG with citations and Ask CaseWise; sourced timeline, claims, evidence, gaps, basic contradictions; a read-only core MCP server; and lawyer/client dashboards. Build this as several verified milestones, not one merge.

## Later features

Advanced counterargument analysis, hearing brief export, OCR, rich reminders, organization-level permissions, broader MCP actions, alternative LLM providers, and deeper readiness indicators can follow the stable MVP. Payment processing and autonomous legal actions remain out of scope unless explicitly requested.

## Packages to evaluate when implementing

| Area | Likely packages | Why / decision point |
| --- | --- | --- |
| Web | `next`, `react`, `react-dom`, `@supabase/supabase-js`, `@supabase/ssr` | App and authenticated Supabase clients; choose compatible current versions |
| Web validation/UI | `zod`; a form library if needed | Shared input validation; use native form handling where sufficient |
| Python API | `fastapi`, `uvicorn`, `pydantic`, `supabase` | Internal service and typed contracts |
| Documents | `pymupdf`, `python-docx` | PDF/DOCX extraction; Python standard library for TXT |
| Search | `sentence-transformers`, `qdrant-client` | Local embeddings and case-filtered vector search |
| Local LLM | `httpx` or Ollama Python client | Configurable Ollama HTTP integration |
| MCP | Official Python MCP SDK | Separate tool server; confirm auth transport support |
| Tests | `pytest`, `httpx`; web testing package as needed | Authorization and pipeline integration checks |

Do not install all packages at once. Inspect the code and select dependencies for each phase. LangChain is optional; LangGraph needs a concrete multi-step use case.

## Technical risks

- **Cross-case or client-private data leakage:** RLS, server-side membership checks, exact Qdrant case filtering, and source revalidation are mandatory release gates.
- **Unsupported AI claims:** weak retrieval, stale index points, and invented citations must fail closed or return insufficient information.
- **Document quality:** scanned PDFs need OCR; DOCX/TXT may have no page number. Show that limitation honestly.
- **Job reliability:** upload, extraction, indexing, and analysis need idempotency, retries, status, and cleanup after partial failures.
- **Local resource use:** embedding models, Ollama, and Qdrant may exceed small developer machines; benchmark a realistic document set.
- **Schema evolution:** role visibility and same-case foreign-key invariants must be designed before adding many dependent tables.
- **Legal domain review:** terminology and generated summaries should be reviewed by qualified professionals before production use.
