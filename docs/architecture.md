# Architecture

## Repository inspection

The repository was empty at the start of phase 1. A local development stack has since been added. The design below remains the target architecture; current implementation and remaining gaps are tracked in [project context](../CASEWISE_PROJECT_CONTEXT.md).

## Planned system

```text
Lawyer / client browser
        │ Supabase session
        ▼
Next.js UI + application API routes
        ├── Supabase Auth / PostgreSQL (RLS) / private Storage
        └── authenticated internal call ──► FastAPI CaseWise services
                                            ├── document extraction
                                            ├── local embeddings ↔ Qdrant
                                            └── LLMProvider → Gemini (Ollama optional)

AI assistant ──► MCP client ──► authenticated MCP server
                                   └── same CaseWise services and access checks
```

PostgreSQL is authoritative for identity, case membership, structured records, processing state, and visibility. Qdrant is a derived search index and must never grant access by itself. FastAPI owns document and AI workflows. Next.js owns user-facing APIs and UI. MCP adapts authenticated service capabilities into tools without duplicating business logic.

## Boundaries

1. **Browser to Next.js:** Supabase session; validate inputs and user access on the server for every route.
2. **Next.js to FastAPI:** authenticated internal request carrying verified user identity and case ID; FastAPI rechecks case access against PostgreSQL. Never trust a browser-supplied role.
3. **FastAPI to Qdrant:** require a case ID obtained from an authorized request; exact-match case filter on every read. Revalidate returned payloads and source records.
4. **MCP to services:** each invocation has a verified end-user principal and scoped case access. Write tools, when introduced, require explicit user confirmation and audit logging.

## Folder structure to grow into

```text
apps/web/
  app/(auth)/                 sign-in and sign-up
  app/(lawyer)/               lawyer dashboard and register-case flow
  app/(client)/               client dashboard
  app/api/                    normal application APIs
  components/                 shared and feature-specific UI
  lib/auth/                   Supabase session helpers
  lib/services/               server-side case services and AI client
  lib/validation/             request schemas
services/ai/
  app/api/                    FastAPI routers
  app/auth/                   principal and case authorization
  app/services/               ingestion, retrieval, analysis
  app/providers/              LLM and embedding interfaces/adapters
  app/models/                 request and response schemas
  tests/                      security and pipeline tests
services/mcp/
  app/                        MCP server and thin tool adapters
  tests/                      authorization tests
supabase/migrations/          schema and RLS migrations
infra/qdrant/                 local configuration and collection setup
docs/                         architecture and API contracts
```

These nested folders are a design, not a claim that their code exists. Add them as their corresponding phase begins.

## Initial vertical slice

Authenticate a lawyer, register a case with an authorized client association, upload one private document, extract and index it, then answer one case-specific question with a verified citation. Expose structured timeline, claims, and evidence only after that path is reliable.
