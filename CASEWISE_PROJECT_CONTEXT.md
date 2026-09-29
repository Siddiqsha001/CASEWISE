# CaseWise project context

## Current implementation

The repo has a Docker Compose development stack: local PostgreSQL, Next.js web app, and FastAPI case/AI service. Its ignored `.env` points at hosted Supabase Auth/Storage and Qdrant, and selects Gemini for generation. Hosted Supabase PostgreSQL direct, Session pooler, and Transaction pooler connections were unreachable from the user's Docker network; the default command now uses local PostgreSQL for case records. The guarded hosted migration is an optional Compose profile. Local GoTrue, Qdrant, and Ollama remain optional profiles. The user has built the app images, but application startup and workflows still need verification. The root [README](README.md) describes setup and current limits.

Implemented code covers lawyer/client signup and sign-in; case and client records; case membership and client grants; register case UI; file upload and PDF/DOCX/TXT extraction; local BGE embeddings; Qdrant case-scoped retrieval; Ollama-backed cited answers and on-demand quoted-source case review; basic manual claims, evidence, timeline, hearings, tasks, payment tracking, notes; and a separate read-only MCP adapter with document search. Runtime behavior still needs Docker verification.

## Architecture and decisions

- `apps/web`: Next.js/React/JavaScript UI. Its API route proxies authenticated case requests to FastAPI. Browser authentication calls hosted Supabase Auth directly using the publishable key; Supabase private keys stay server-side.
- `services/ai`: FastAPI owns case services, document extraction, indexing, and grounded AI. It validates GoTrue tokens through `/user`, uses the user's UUID in PostgreSQL transaction claims, and checks case membership before operations.
- `supabase/init/01-schema.sql`: local development schema, applied to a fresh Docker PostgreSQL volume. `supabase/migrations/20260929_casewise_hosted.sql` is the hosted migration; the optional migration service checks for existing tables before applying it transactionally. It has not been applied.
- `services/mcp`: separate per-user stdio MCP server. Tools call the same FastAPI case API using a user access token from its environment; it has no write tools.
- Qdrant stores chunk embeddings with `caseId`, document metadata, and chunk ID. Queries always include exact case ID filtering, then recheck chunks/documents in PostgreSQL.
- Gemini is the selected LLM provider through an abstraction; Ollama remains available as an optional local provider. BGE embeddings remain local. A Gemini API key is required for generated answers and case review.
- Private document bytes use a private Supabase Storage bucket when the hosted URL and secret key are configured; otherwise local development falls back to a Docker volume. Storage requests occur server-side after case authorization. Hosted Storage behavior has not been runtime verified.

## Important pending work

1. Verify local PostgreSQL initialization, API and web startup, and real user workflows. Investigate blocked outbound TCP to Supabase PostgreSQL before any hosted database switch.
2. Add automated integration tests for auth, RLS, cross-case Qdrant access, and client-private data boundaries.
3. Implement durable jobs, retries, deletion/reindex consistency, and Supabase Storage policies.
4. Turn on-demand quoted-source AI review into reliable, editable timeline/claim/evidence records and richer gap, contradiction, counterargument, and hearing preparation workflows. The current review is experimental and can return empty sections.
5. Add reminders, notification delivery, richer case editing, AI result editing, and production session/security hardening.

The architecture documents in `docs/` are the target design. They include planned capabilities that are not yet implemented; use this status file and README to distinguish shipped code from design.
