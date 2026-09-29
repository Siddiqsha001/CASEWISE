# MCP architecture

The MCP server is a separate interface for the CaseWise AI assistant. It exposes structured capabilities backed by the same CaseWise services used by application APIs. It must not duplicate SQL, retrieval, or analysis rules inside tool handlers.

```text
CaseWise assistant → MCP client → authenticated MCP server
                                     → CaseWise service functions
                                     → Supabase / Qdrant / FastAPI
```

## Initial read-only tools

| Tool | Purpose | Access |
| --- | --- | --- |
| `get_case` | Client-safe or lawyer-complete case summary | Case member; role-aware projection |
| `list_case_documents` | Authorized document metadata | Case member; visibility filtered |
| `search_case_documents` | Case-scoped semantic excerpts and source IDs | Case member; exact case filter and source recheck |
| `get_case_timeline` | Sourced timeline events | Case member; visibility filtered |
| `list_case_evidence` | Reviewed and suggested evidence | Case member; visibility filtered |
| `get_upcoming_hearings` | Authorized hearing list | Case member; visibility filtered |

Other prompt-listed tools—claim evidence, evidence gaps, conflicts, contradictions, counterarguments, hearing briefs—should be added when the underlying service and records exist. The tool list is deliberately focused; avoid demo-only tools.

## Tool contract

Every tool receives the authenticated principal from transport context, validates role and case membership in the service layer, and returns bounded structured data with source IDs. A model-supplied `caseId` is only a requested scope, never an authorization claim. Search must pass an exact case filter to Qdrant and validate each result against PostgreSQL. Tool errors should reveal no private case existence to unauthorized users.

## Actions and confirmation

Keep read tools separate from future write/action tools (`create_case`, `update_case`, reminders, tasks, payment tracking). The assistant first presents the proposed action and asks the user to confirm its concrete details. Only after confirmation may the server execute it under the user's permissions and record an audit event. MCP itself should not autonomously file legal documents or decide strategy.
