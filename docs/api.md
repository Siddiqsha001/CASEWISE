# API design

This document describes proposed routes; none are implemented yet. JSON contracts should be versioned as they stabilize. All normal application routes authenticate the Supabase session, validate inputs, and perform server-side case authorization.

## Next.js application routes

| Route | Planned operations | Access |
| --- | --- | --- |
| `/api/cases` | List, create draft/register case | Lawyer for create; role-scoped list |
| `/api/cases/[id]` | Read/update case | Assigned member read; lawyer update |
| `/api/cases/[id]/documents` | List/upload documents | Role-visible list; lawyer upload |
| `/api/cases/[id]/documents/[documentId]` | Metadata and signed source URL | Authorized for that document |
| `/api/cases/[id]/claims` | List/review claims | Role-visible list; lawyer edit |
| `/api/cases/[id]/evidence` | List/review evidence | Role-visible list; lawyer edit |
| `/api/cases/[id]/timeline` | Sourced events | Role-visible |
| `/api/cases/[id]/hearings` | List/manage hearings | Role-visible list; lawyer edit |
| `/api/cases/[id]/tasks` | List/manage tasks | Assigned tasks; lawyer management |
| `/api/cases/[id]/payments` | Tracking | Explicitly shared client view; lawyer edit |
| `/api/notifications` | List/read own notifications | Recipient only |
| `/api/cases/[id]/ask` | Grounded question and citations | Authorized document scope |

Use a transaction for case registration and client association. Uploaded files enter a separate retryable pipeline; the response returns real job/document statuses. Validate IDs, pagination, file type/size, and bounded question length. Return `401` for missing session, `403`/`404` without revealing unauthorized case details, `422` for invalid input, and actionable processing errors.

## FastAPI internal routes

| Route | Purpose |
| --- | --- |
| `/ai/process-document` | Start or retry authorized document ingestion |
| `/ai/query-case` | Case-scoped retrieval and grounded answer |
| `/ai/analyze-case` | Orchestrate persisted analysis suggestions |
| `/ai/timeline` | Extract sourced timeline candidates |
| `/ai/claims` | Extract sourced claim candidates |
| `/ai/evidence-gaps` | Find possible gaps from claims and mapped evidence |
| `/ai/contradictions` | Find potential source conflicts |
| `/ai/counterarguments` | Produce sourced potential arguments |
| `/ai/hearing-prep` | Draft an editable preparation brief |

These are internal authenticated endpoints, not public model access. Long jobs should return a job ID and status rather than block a request. Route handlers call service functions that also back MCP tools; embed/index functions can remain internal service calls unless there is a concrete need for HTTP endpoints.

## Response shapes

An answer should contain `answer`, `evidence[]`, `citations[]`, `potentialIssues[]`, `suggestedReview[]`, and `status`. Each citation includes `documentId`, `documentName`, `pageNumber` or null, `chunkId`, and an authorized source route. Processing status includes completed steps and an error code/message when failed. Never return fabricated citations or optimistic completion states.
