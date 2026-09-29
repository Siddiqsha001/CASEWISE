# CaseWise AI

CaseWise AI is a local development implementation of a legal case workspace with case-scoped document retrieval. AI-generated information should be reviewed and verified by a qualified legal professional.

## Run with one command

Install Docker Desktop, start its engine, then run from this directory:

```bash
docker compose up --build
```

Open **http://localhost:3000**. The default command starts a local PostgreSQL case database with its schema and RLS, then the FastAPI and Next.js services. The ignored `.env` configures hosted Supabase Auth and Storage, hosted Qdrant, and Gemini. The BGE embedding model downloads when the first document is processed. These downloads need internet and can take time.

The hosted PostgreSQL URI remains in `.env` for later use. Both the Session pooler (port 5432) and Transaction pooler (port 6543) failed from the user's Docker network before authentication, so the default app does **not** use hosted Supabase PostgreSQL. Case records stay in the local Docker volume. [The hosted migration](supabase/migrations/20260929_casewise_hosted.sql) is retained but not applied. The Supabase secret key is stored only in `.env` and used server-side for private document Storage.

When PostgreSQL TCP egress is restored, the hosted migration can be run explicitly with `docker compose --profile hosted-db run --rm migrate`. Configure the API to use the hosted database only after that migration succeeds. Passwords in a URI must stay URL-encoded (for example, `@` becomes `%40`). The Python PostgreSQL client disables prepared statements for transaction pooler compatibility.

Create a lawyer account in the app. A lawyer can register a case, reuse or create a client, upload PDF/DOCX/TXT documents, manage case records, and ask a document-grounded question once a document shows `READY`. To give a client access, have them register with the email saved on the client record, then use **Grant client access** in the case overview.

## Services

| Service | Local address | Purpose |
| --- | --- | --- |
| Web | http://localhost:3000 | Next.js UI and API proxy |
| AI/API | http://localhost:8000/docs | FastAPI case services and OpenAPI docs |
| Auth | Supabase project URL | Hosted Supabase Auth |
| Qdrant | Cloud endpoint in `.env` | Case-filtered vector index |
| Gemini | Google API | Grounded answers and case review |
| PostgreSQL | Docker internal (default) | Case data and RLS |

Docker volumes retain case records and the embedding cache. With the supplied Supabase secret key, original documents are kept in a private `case-documents` Supabase Storage bucket and served only through the authorized CaseWise API. `docker compose down` keeps local volumes; cloud data remains in the respective projects.

## Implemented code (runtime verification pending)

- Supabase email/password authentication with lawyer and client profiles.
- PostgreSQL case, client, membership, document, claims, evidence, timeline, hearing, task, payment tracking, note, analysis, and audit tables with RLS policies.
- Lawyer case registration, existing/new client choice, opposing party, private documents, and basic case records.
- Client access through an explicit case grant; client visibility restrictions for case records.
- PDF/DOCX/TXT text extraction, local BGE embeddings, Qdrant indexing with exact case ID payloads and query filters.
- Gemini-backed Ask CaseWise with verified source IDs and clickable document citations. When sources or models are unavailable, the UI shows a real error or insufficient-information response.
- An on-demand AI case review that retains only suggestions containing an exact quote from an authorized source chunk; its sections cover timeline, claims, evidence, possible gaps, potential contradictions, counterarguments, and hearing preparation.
- A read-only MCP adapter in `services/mcp` that reuses the authenticated API. It is intended to launch per user with `CASEWISE_USER_TOKEN` and is not enabled in the default Compose profile.

## Current limits

This is a development build, not production legal software. PDF scanning/OCR, durable job retries, automatic analysis after registration, structured transfer of AI review suggestions into editable case records, reminders, notification delivery/UI, and export still need implementation. The on-demand AI review is experimental and can return empty sections rather than unsupported claims. The Register action processes documents, but it does not claim analysis has finished. Replace development database credentials and configure secure session handling before deployment. Browser sessions currently use local storage with token refresh. Hosted Storage behavior still needs runtime verification.

Docker startup could not be exercised in this workspace because Docker daemon access was denied. `docker compose config` and Python syntax checks passed. See [project context](CASEWISE_PROJECT_CONTEXT.md) and [roadmap](docs/development-roadmap.md) for the remaining work.
