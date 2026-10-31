# CaseWise MCP (Model Context Protocol) Integration

## Overview

This directory contains an **MCP server implementation** for CaseWise that exposes legal case management functionality to AI assistants like Claude. This is a **reference implementation** and is not actively used in the current application.

## What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol created by Anthropic that allows AI assistants to:
- Call functions/tools in your application
- Read resources from your system
- Use pre-defined prompts for common workflows

Think of it as **"USB for AI"** - a universal way to connect AI assistants to external systems.

---

## Architecture

```
┌──────────────┐
│    Claude    │  (AI Assistant)
│   Desktop    │
└──────┬───────┘
       │ MCP Protocol
       │ (stdin/stdout)
       ↓
┌──────────────┐
│ mcp_server.py│  (This file)
│              │
│ - Tools      │  (Actions Claude can perform)
│ - Resources  │  (Data Claude can read)
│ - Prompts    │  (Workflow templates)
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  CaseWise    │
│  Database    │  (PostgreSQL + Qdrant)
└──────────────┘
```

---

## Available Tools

### Case Management
- **`list_cases`** - List cases with filtering (status, user)
- **`get_case_details`** - Get complete case information
- **`create_case`** - Create a new case
- **`search_cases_by_keyword`** - Search across cases

### Case Content
- **`add_case_note`** - Add notes to a case
- **`add_timeline_event`** - Add timeline events
- **`add_claim`** - Add legal claims
- **`add_evidence`** - Add evidence items
- **`schedule_hearing`** - Schedule court hearings
- **`add_task`** - Add tasks/action items

### AI-Powered
- **`ask_case_question`** - RAG-based Q&A on case documents
- **`get_upcoming_hearings`** - Get upcoming hearings

---

## Available Resources

Resources provide read-only access to case data:

- **`case://{case_id}/timeline`** - Chronological events
- **`case://{case_id}/claims`** - All legal claims
- **`case://{case_id}/evidence`** - Evidence list
- **`case://{case_id}/documents`** - Document list

---

## Available Prompts

Pre-defined workflows for common legal tasks:

1. **`case-intake`** - Client intake interview guide
2. **`hearing-prep`** - Hearing preparation checklist
3. **`document-review`** - Document analysis workflow
4. **`case-summary`** - Executive case summary generator

---

## How to Activate (Future Use)

### Step 1: Install MCP SDK

```bash
pip install mcp
```

### Step 2: Uncomment MCP Code

In `mcp_server.py`, uncomment:
- Import statements at the top
- `@server.tool()` decorators
- `@server.resource()` decorators
- `@server.prompt()` decorators
- Server initialization in `main()`

### Step 3: Configure Claude Desktop

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on Mac):

```json
{
  "mcpServers": {
    "casewise": {
      "command": "python",
      "args": ["/path/to/Casewise/services/ai/app/mcp_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://casewise:casewise@localhost:5433/casewise",
        "QDRANT_URL": "http://localhost:6334",
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Step 4: Restart Claude Desktop

The CaseWise tools will appear in Claude's tool palette.

---

## Example Usage

Once activated, you can chat with Claude like this:

### Example 1: Create a New Case
```
You: Create a new case for client John Doe (id: abc-123) 
     regarding a contract dispute with XYZ Corp. 
     This is a civil case filed in Superior Court.

Claude: I'll create that case for you.
[Calls create_case tool]
✓ Created case "Contract Dispute - XYZ Corp" 
  Case ID: def-456
  Status: ACTIVE
```

### Example 2: Ask About Documents
```
You: What are the payment terms mentioned in case def-456's documents?

Claude: Let me search the case documents.
[Calls ask_case_question tool]

Based on the contract documents:
- Payment: $50,000 due within 30 days
- Late fees: 5% per month
- Method: Wire transfer

Source: contract.pdf, page 3
```

### Example 3: Prepare for Hearing
```
You: Help me prepare for the hearing in case def-456 next week.

Claude: I'll use the hearing prep workflow.
[Uses hearing-prep prompt]
[Calls get_case_details, get_claims, get_evidence]

Here's your hearing preparation checklist:

**Key Points to Emphasize:**
1. Clear breach of contract on January 15th
2. Documented payment delays (evidence #5)
3. Good faith attempts to resolve (emails, evidence #8)

**Evidence to Bring:**
- Original signed contract
- Payment records
- Email correspondence
...
```

### Example 4: Get Upcoming Schedule
```
You: What hearings do I have coming up?

Claude: [Calls get_upcoming_hearings]

You have 3 hearings in the next 30 days:

1. **Tomorrow, Nov 1, 2026 at 9:00 AM**
   - Smith v. Jones
   - Superior Court, Room 403
   - Motion to Dismiss hearing

2. **Nov 8, 2026 at 2:00 PM**
   - XYZ Corp Contract Dispute
   - Case Management Conference
...
```

---

## Why MCP vs REST API?

| Aspect | REST API (Current) | MCP (This Implementation) |
|--------|-------------------|---------------------------|
| **Integration** | Frontend calls backend | AI calls backend |
| **User** | Web browser | AI assistant |
| **Protocol** | HTTP/JSON | stdio/JSON-RPC |
| **Discovery** | Manual (docs) | Automatic (schema) |
| **Workflows** | Hardcoded in UI | Natural language |

### MCP Benefits:
✅ **Natural Language**: "Schedule a hearing next Tuesday at 2pm"  
✅ **Context Aware**: AI remembers conversation context  
✅ **Multi-Step**: AI can chain tools together  
✅ **Discovery**: AI knows what tools are available  
✅ **Flexible**: No need to build UI for every action  

---

## Code Structure

```python
# mcp_server.py

# 1. DATABASE CONNECTION SETUP
# - PostgreSQL connection pool
# - Qdrant vector database client
# - Gemini API for RAG

# 2. TOOLS (Actions)
@server.tool()
async def add_case_note(case_id: str, note: str):
    # Insert into database
    # Return confirmation

# 3. RESOURCES (Read-only data)
@server.resource("case://{case_id}/timeline")
async def get_timeline(case_id: str):
    # Query database
    # Return JSON

# 4. PROMPTS (Workflow templates)
@server.prompt("hearing-prep")
def hearing_prep_prompt(case_id: str):
    # Return instructions for AI
    # Guide multi-step workflow
```

---

## Security Considerations

When activating MCP in production:

1. **Authentication**: Add user authentication to tools
2. **Authorization**: Check user permissions before DB operations
3. **Rate Limiting**: Prevent abuse of AI tools
4. **Audit Logging**: Log all MCP tool calls
5. **Input Validation**: Validate all parameters
6. **Sandboxing**: Run MCP server in isolated environment

Example authentication:
```python
@server.tool()
async def add_case_note(
    case_id: str,
    note: str,
    user_token: str  # Add authentication
):
    # Verify token
    user = await verify_jwt_token(user_token)
    
    # Check permissions
    if not await user_can_access_case(user.id, case_id):
        raise PermissionError("Access denied")
    
    # Proceed with operation
    ...
```

---

## Comparison: Current Implementation vs MCP

### Current: Web UI Flow
```
User clicks "Add Note" button
  ↓
Form appears
  ↓
User types note
  ↓
User clicks "Save"
  ↓
POST /api/cases/{id}/case_notes
  ↓
Database insert
  ↓
UI refreshes
```

### With MCP: AI Assistant Flow
```
User: "Add a note to the Smith case: 
       Received payment confirmation today"
  ↓
Claude calls add_case_note(
  case_id="abc-123",
  note="Received payment confirmation today"
)
  ↓
Database insert
  ↓
Claude: "✓ Note added to Smith v. Jones case"
```

**Fewer steps, more natural interaction!**

---

## Integration with Existing FastAPI

The MCP server can run **alongside** the existing FastAPI server:

```yaml
# docker-compose.yml (future addition)

services:
  ai:
    # Existing FastAPI server (port 8001)
    
  mcp:
    build: ./services/ai
    command: python -m mcp_server
    environment:
      - DATABASE_URL=postgresql://...
      - QDRANT_URL=http://qdrant:6333
    # Communicates via stdin/stdout, no port needed
```

Both can share the same database connections and business logic.

---

## Testing MCP Tools

You can test individual tools without Claude:

```python
# test_mcp.py
import asyncio
from mcp_server import list_cases, add_case_note, init_connections

async def test():
    await init_connections()
    
    # Test listing cases
    cases = await list_cases(limit=5)
    print(cases)
    
    # Test adding note
    result = await add_case_note(
        case_id="abc-123",
        note="Test note from MCP"
    )
    print(result)

asyncio.run(test())
```

---

## Future Enhancements

1. **Streaming Responses**: Stream long document analyses
2. **File Uploads**: Allow document uploads via MCP
3. **Webhooks**: Notify MCP clients of case updates
4. **Multi-Model**: Support different AI models (GPT, Claude, Llama)
5. **Caching**: Cache frequent queries for performance
6. **GraphQL**: Add GraphQL resource endpoints

---

## Related Documentation

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Anthropic MCP SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/mcp)

---

## Questions?

This MCP implementation demonstrates how AI assistants could interact with CaseWise in the future. It's not currently active but provides a complete reference for when you're ready to enable AI-powered automation in your legal workflow!
