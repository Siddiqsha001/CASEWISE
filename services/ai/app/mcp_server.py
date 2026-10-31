"""
CaseWise MCP (Model Context Protocol) Server

This MCP server exposes CaseWise legal case management functionality as tools
and resources that AI assistants (like Claude) can use to interact with the system.

NOT ACTIVELY USED - This is a reference implementation for future integration.

To run this MCP server:
    python -m mcp_server

To connect from Claude Desktop, add to config:
    {
      "mcpServers": {
        "casewise": {
          "command": "python",
          "args": ["/path/to/mcp_server.py"]
        }
      }
    }
"""

import asyncio
import json
import os
from typing import Any, Optional, List, Dict
from datetime import datetime, date

# MCP SDK imports (would need to install: pip install mcp)
# from mcp.server import Server
# from mcp.server.stdio import stdio_server
# from mcp.types import Tool, Resource, TextContent, ImageContent, EmbeddedResource

# Database imports (reuse existing DB connection)
import asyncpg
from qdrant_client import QdrantClient
import httpx


# ============================================================================
# DATABASE CONNECTION SETUP
# ============================================================================

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://casewise:casewise@db:5432/casewise")
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

db_pool: Optional[asyncpg.Pool] = None
qdrant_client: Optional[QdrantClient] = None


async def init_connections():
    """Initialize database connections"""
    global db_pool, qdrant_client
    db_pool = await asyncpg.create_pool(DATABASE_URL)
    qdrant_client = QdrantClient(url=QDRANT_URL)


async def cleanup_connections():
    """Cleanup database connections"""
    global db_pool
    if db_pool:
        await db_pool.close()


# ============================================================================
# MCP SERVER DEFINITION
# ============================================================================

# Uncomment when MCP SDK is installed
# server = Server("casewise-legal")


# ============================================================================
# TOOLS - Actions the AI can perform
# ============================================================================

# @server.tool()
async def list_cases(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
) -> str:
    """
    List legal cases with optional filtering.

    Args:
        user_id: Filter by user ID (optional)
        status: Filter by case status: ACTIVE, CLOSED, ARCHIVED (optional)
        limit: Maximum number of cases to return (default: 50)

    Returns:
        JSON string with list of cases
    """
    query = "SELECT id, title, case_number, court, status, filing_date, created_at FROM cases WHERE 1=1"
    params = []

    if user_id:
        params.append(user_id)
        query += f" AND id IN (SELECT case_id FROM members WHERE user_id = ${len(params)})"

    if status:
        params.append(status)
        query += f" AND status = ${len(params)}"

    query += f" ORDER BY created_at DESC LIMIT {limit}"

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, *params)
        cases = [dict(row) for row in rows]

    return json.dumps(cases, default=str, indent=2)


# @server.tool()
async def get_case_details(case_id: str) -> str:
    """
    Get detailed information about a specific case.

    Args:
        case_id: UUID of the case

    Returns:
        JSON string with complete case information including client details
    """
    query = """
        SELECT c.*,
               u.name as client_name,
               u.email as client_email,
               COUNT(DISTINCT d.id) as document_count,
               COUNT(DISTINCT h.id) as hearing_count
        FROM cases c
        LEFT JOIN users u ON c.client_id = u.id
        LEFT JOIN documents d ON d.case_id = c.id
        LEFT JOIN hearings h ON h.case_id = c.id
        WHERE c.id = $1
        GROUP BY c.id, u.id
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id)
        if not row:
            return json.dumps({"error": "Case not found"})

        case_data = dict(row)

    return json.dumps(case_data, default=str, indent=2)


# @server.tool()
async def create_case(
    title: str,
    client_id: str,
    case_type: str,
    description: Optional[str] = None,
    court: Optional[str] = None,
    case_number: Optional[str] = None,
    filing_date: Optional[str] = None,
    priority: str = "MEDIUM"
) -> str:
    """
    Create a new legal case.

    Args:
        title: Title/name of the case
        client_id: UUID of the client
        case_type: Type of case (e.g., Civil, Criminal, Family)
        description: Detailed description
        court: Court name
        case_number: Official case number
        filing_date: Date case was filed (YYYY-MM-DD)
        priority: LOW, MEDIUM, HIGH (default: MEDIUM)

    Returns:
        JSON string with created case details including case_id
    """
    query = """
        INSERT INTO cases (
            title, client_id, case_type, description, court,
            case_number, filing_date, priority, status
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'ACTIVE')
        RETURNING id, title, case_number, status, created_at
    """

    filing_date_obj = date.fromisoformat(filing_date) if filing_date else None

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            query, title, client_id, case_type, description,
            court, case_number, filing_date_obj, priority
        )
        case_data = dict(row)

    return json.dumps(case_data, default=str, indent=2)


# @server.tool()
async def add_case_note(case_id: str, note: str, visibility: str = "LAWYER_ONLY") -> str:
    """
    Add a note to a case.

    Args:
        case_id: UUID of the case
        note: The note content
        visibility: LAWYER_ONLY or CLIENT_SHARED (default: LAWYER_ONLY)

    Returns:
        JSON string with confirmation
    """
    query = """
        INSERT INTO case_notes (case_id, body, visibility)
        VALUES ($1, $2, $3)
        RETURNING id, created_at
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id, note, visibility)

    return json.dumps({
        "success": True,
        "note_id": str(row["id"]),
        "created_at": str(row["created_at"])
    })


# @server.tool()
async def add_timeline_event(
    case_id: str,
    event_date: str,
    description: str,
    visibility: str = "LAWYER_ONLY"
) -> str:
    """
    Add an event to the case timeline.

    Args:
        case_id: UUID of the case
        event_date: Date of the event (YYYY-MM-DD)
        description: Description of what happened
        visibility: LAWYER_ONLY or CLIENT_SHARED

    Returns:
        JSON string with confirmation
    """
    query = """
        INSERT INTO timeline_events (case_id, event_date, description, visibility)
        VALUES ($1, $2, $3, $4)
        RETURNING id, created_at
    """

    event_date_obj = date.fromisoformat(event_date)

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id, event_date_obj, description, visibility)

    return json.dumps({
        "success": True,
        "event_id": str(row["id"]),
        "created_at": str(row["created_at"])
    })


# @server.tool()
async def add_claim(case_id: str, statement: str, visibility: str = "LAWYER_ONLY") -> str:
    """
    Add a legal claim to the case.

    Args:
        case_id: UUID of the case
        statement: The claim statement
        visibility: LAWYER_ONLY or CLIENT_SHARED

    Returns:
        JSON string with confirmation
    """
    query = """
        INSERT INTO claims (case_id, statement, visibility)
        VALUES ($1, $2, $3)
        RETURNING id, created_at
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id, statement, visibility)

    return json.dumps({
        "success": True,
        "claim_id": str(row["id"]),
        "created_at": str(row["created_at"])
    })


# @server.tool()
async def add_evidence(
    case_id: str,
    name: str,
    evidence_type: str,
    description: Optional[str] = None,
    visibility: str = "LAWYER_ONLY"
) -> str:
    """
    Add evidence to the case.

    Args:
        case_id: UUID of the case
        name: Name/title of the evidence
        evidence_type: Type of evidence (e.g., Document, Testimony, Physical)
        description: Detailed description
        visibility: LAWYER_ONLY or CLIENT_SHARED

    Returns:
        JSON string with confirmation
    """
    query = """
        INSERT INTO evidence (case_id, name, type, description, visibility)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, created_at
    """

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id, name, evidence_type, description, visibility)

    return json.dumps({
        "success": True,
        "evidence_id": str(row["id"]),
        "created_at": str(row["created_at"])
    })


# @server.tool()
async def schedule_hearing(
    case_id: str,
    starts_at: str,
    court: str,
    purpose: str,
    visibility: str = "LAWYER_ONLY"
) -> str:
    """
    Schedule a court hearing.

    Args:
        case_id: UUID of the case
        starts_at: Date and time of hearing (YYYY-MM-DD HH:MM:SS)
        court: Court name/location
        purpose: Purpose of the hearing
        visibility: LAWYER_ONLY or CLIENT_SHARED

    Returns:
        JSON string with confirmation
    """
    query = """
        INSERT INTO hearings (case_id, starts_at, court, purpose, visibility)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, created_at
    """

    starts_at_obj = datetime.fromisoformat(starts_at)

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id, starts_at_obj, court, purpose, visibility)

    return json.dumps({
        "success": True,
        "hearing_id": str(row["id"]),
        "starts_at": str(row["created_at"])
    })


# @server.tool()
async def add_task(
    case_id: str,
    title: str,
    due_at: Optional[str] = None,
    visibility: str = "LAWYER_ONLY"
) -> str:
    """
    Add a task to the case.

    Args:
        case_id: UUID of the case
        title: Task title/description
        due_at: Due date/time (YYYY-MM-DD HH:MM:SS) (optional)
        visibility: LAWYER_ONLY or CLIENT_SHARED

    Returns:
        JSON string with confirmation
    """
    query = """
        INSERT INTO tasks (case_id, title, due_at, visibility)
        VALUES ($1, $2, $3, $4)
        RETURNING id, created_at
    """

    due_at_obj = datetime.fromisoformat(due_at) if due_at else None

    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(query, case_id, title, due_at_obj, visibility)

    return json.dumps({
        "success": True,
        "task_id": str(row["id"]),
        "created_at": str(row["created_at"])
    })


# @server.tool()
async def ask_case_question(case_id: str, question: str) -> str:
    """
    Ask a question about case documents using RAG (Retrieval-Augmented Generation).

    This uses vector search to find relevant document chunks and generates
    an answer with citations from the actual case documents.

    Args:
        case_id: UUID of the case
        question: The question to ask about the case documents

    Returns:
        JSON string with answer and source citations
    """
    # Check if collection exists
    collections = qdrant_client.get_collections().collections
    collection_name = f"case_{case_id}"

    if collection_name not in [c.name for c in collections]:
        return json.dumps({
            "error": "No documents have been processed for this case yet"
        })

    # Embed the question
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={GEMINI_API_KEY}",
            json={"content": {"parts": [{"text": question}]}}
        )
        question_embedding = response.json()["embedding"]["values"]

    # Search for relevant chunks
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=question_embedding,
        limit=5
    )

    if not search_results:
        return json.dumps({
            "answer": "I couldn't find relevant information in the case documents to answer this question.",
            "citations": []
        })

    # Build context from retrieved chunks
    context = "\n\n---\n\n".join([result.payload["text"] for result in search_results])

    # Generate answer with Gemini
    prompt = f"""Based ONLY on the following excerpts from case documents, answer the question.
If the information is not in the excerpts, say you don't have enough information.

DOCUMENT EXCERPTS:
{context}

QUESTION: {question}

Provide a clear, concise answer with specific references to the documents."""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    # Format citations
    citations = [
        {
            "documentName": result.payload.get("document_name", "Unknown"),
            "pageNumber": result.payload.get("page_number"),
            "excerpt": result.payload["text"][:200] + "...",
            "documentId": result.payload.get("document_id")
        }
        for result in search_results
    ]

    return json.dumps({
        "answer": answer,
        "citations": citations
    }, indent=2)


# @server.tool()
async def get_upcoming_hearings(user_id: str, days_ahead: int = 30) -> str:
    """
    Get upcoming hearings for a user's cases.

    Args:
        user_id: UUID of the user (lawyer)
        days_ahead: Number of days to look ahead (default: 30)

    Returns:
        JSON string with list of upcoming hearings
    """
    query = """
        SELECT h.*, c.title as case_title, c.case_number
        FROM hearings h
        JOIN cases c ON h.case_id = c.id
        JOIN members m ON c.id = m.case_id
        WHERE m.user_id = $1
        AND h.starts_at >= NOW()
        AND h.starts_at <= NOW() + INTERVAL '1 day' * $2
        ORDER BY h.starts_at ASC
    """

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, user_id, days_ahead)
        hearings = [dict(row) for row in rows]

    return json.dumps(hearings, default=str, indent=2)


# @server.tool()
async def search_cases_by_keyword(keyword: str, user_id: Optional[str] = None) -> str:
    """
    Search cases by keyword in title, description, or case number.

    Args:
        keyword: Keyword to search for
        user_id: Optional user ID to filter by user's cases

    Returns:
        JSON string with matching cases
    """
    query = """
        SELECT id, title, case_number, status, court, filing_date
        FROM cases
        WHERE (
            title ILIKE $1
            OR description ILIKE $1
            OR case_number ILIKE $1
            OR court ILIKE $1
        )
    """
    params = [f"%{keyword}%"]

    if user_id:
        query += " AND id IN (SELECT case_id FROM members WHERE user_id = $2)"
        params.append(user_id)

    query += " ORDER BY created_at DESC LIMIT 50"

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, *params)
        cases = [dict(row) for row in rows]

    return json.dumps(cases, default=str, indent=2)


# ============================================================================
# RESOURCES - Data the AI can read
# ============================================================================

# @server.resource("case://{case_id}/timeline")
async def get_timeline(case_id: str) -> str:
    """Get chronological timeline of events for a case"""
    query = """
        SELECT event_date, description, created_at
        FROM timeline_events
        WHERE case_id = $1
        ORDER BY event_date ASC
    """

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, case_id)
        events = [dict(row) for row in rows]

    return json.dumps(events, default=str, indent=2)


# @server.resource("case://{case_id}/claims")
async def get_claims(case_id: str) -> str:
    """Get all claims for a case"""
    query = """
        SELECT statement, created_at
        FROM claims
        WHERE case_id = $1
        ORDER BY created_at DESC
    """

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, case_id)
        claims = [dict(row) for row in rows]

    return json.dumps(claims, default=str, indent=2)


# @server.resource("case://{case_id}/evidence")
async def get_evidence_list(case_id: str) -> str:
    """Get all evidence for a case"""
    query = """
        SELECT name, type, description, created_at
        FROM evidence
        WHERE case_id = $1
        ORDER BY created_at DESC
    """

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, case_id)
        evidence = [dict(row) for row in rows]

    return json.dumps(evidence, default=str, indent=2)


# @server.resource("case://{case_id}/documents")
async def get_documents(case_id: str) -> str:
    """Get all documents for a case"""
    query = """
        SELECT id, file_name, processing_status, file_size, created_at
        FROM documents
        WHERE case_id = $1
        ORDER BY created_at DESC
    """

    async with db_pool.acquire() as conn:
        rows = await conn.fetch(query, case_id)
        documents = [dict(row) for row in rows]

    return json.dumps(documents, default=str, indent=2)


# ============================================================================
# PROMPTS - Pre-defined workflows for common tasks
# ============================================================================

# @server.prompt("case-intake")
def case_intake_prompt() -> str:
    """
    Prompt for guiding initial case intake interview.
    Returns structured questions to gather case information.
    """
    return """You are assisting with legal case intake. Guide the conversation to gather:

1. Client Information:
   - Full name
   - Contact information
   - Relationship to the case

2. Case Overview:
   - Brief description of the legal issue
   - Type of case (civil, criminal, family, etc.)
   - Parties involved

3. Timeline:
   - When did the issue begin?
   - Key dates and events
   - Any deadlines or statute of limitations concerns

4. Desired Outcome:
   - What does the client hope to achieve?
   - Any immediate actions needed?

5. Documents:
   - What relevant documents does the client have?
   - Are there any contracts, agreements, or court papers?

Ask one question at a time, be empathetic, and ensure you understand each answer before moving on."""


# @server.prompt("hearing-prep")
def hearing_prep_prompt(case_id: str) -> str:
    """
    Prompt for preparing for an upcoming hearing.
    Reviews case materials and generates preparation checklist.
    """
    return f"""You are helping prepare for an upcoming court hearing.

Case ID: {case_id}

Please review:
1. All case claims and legal arguments
2. Available evidence and supporting documents
3. Timeline of relevant events
4. Any contradictions or gaps in the case

Then create a hearing preparation checklist including:
- Key points to emphasize
- Evidence to present
- Potential questions from opposing counsel
- Weaknesses to address
- Documents to bring

Be thorough and strategic in your analysis."""


# @server.prompt("document-review")
def document_review_prompt(case_id: str) -> str:
    """
    Prompt for comprehensive document review.
    Analyzes case documents for key information.
    """
    return f"""You are conducting a document review for case {case_id}.

Please analyze the case documents and identify:

1. Key Facts:
   - Parties involved
   - Important dates
   - Locations
   - Amounts/figures

2. Legal Issues:
   - Claims being made
   - Potential defenses
   - Applicable laws or regulations

3. Evidence:
   - Documentary evidence
   - Testimony references
   - Physical evidence mentioned

4. Action Items:
   - Missing information
   - Follow-up needed
   - Additional documents to request

Provide specific citations from the documents for each finding."""


# @server.prompt("case-summary")
def case_summary_prompt(case_id: str) -> str:
    """
    Prompt for generating executive case summary.
    Creates concise overview of case status.
    """
    return f"""Create a comprehensive but concise executive summary of case {case_id}.

Include:

**Case Overview** (2-3 sentences)
- Type of case and parties involved
- Core legal issue

**Current Status**
- Stage of proceedings
- Recent developments
- Upcoming deadlines/hearings

**Key Claims**
- Main legal arguments
- Supporting evidence

**Next Steps**
- Immediate action items
- Strategic recommendations

Keep it professional and focused on decision-making information."""


# ============================================================================
# MAIN SERVER STARTUP
# ============================================================================

async def main():
    """Main entry point for MCP server"""
    await init_connections()

    # Uncomment when MCP SDK is installed
    # async with stdio_server() as (read_stream, write_stream):
    #     await server.run(
    #         read_stream,
    #         write_stream,
    #         server.create_initialization_options()
    #     )

    print("CaseWise MCP Server - Reference Implementation")
    print("=" * 60)
    print("\nThis is a reference implementation and is not actively running.")
    print("\nTo use this MCP server:")
    print("1. Install MCP SDK: pip install mcp")
    print("2. Uncomment the MCP decorators and server initialization")
    print("3. Add to Claude Desktop config")
    print("\nAvailable Tools:")
    print("  - list_cases: List all cases with filtering")
    print("  - get_case_details: Get complete case information")
    print("  - create_case: Create a new case")
    print("  - add_case_note: Add notes to a case")
    print("  - add_timeline_event: Add timeline events")
    print("  - add_claim: Add legal claims")
    print("  - add_evidence: Add evidence items")
    print("  - schedule_hearing: Schedule court hearings")
    print("  - add_task: Add tasks/action items")
    print("  - ask_case_question: RAG-based Q&A on case documents")
    print("  - get_upcoming_hearings: Get upcoming hearings")
    print("  - search_cases_by_keyword: Search across cases")
    print("\nAvailable Resources:")
    print("  - case://{case_id}/timeline")
    print("  - case://{case_id}/claims")
    print("  - case://{case_id}/evidence")
    print("  - case://{case_id}/documents")
    print("\nAvailable Prompts:")
    print("  - case-intake: Client intake interview guide")
    print("  - hearing-prep: Hearing preparation checklist")
    print("  - document-review: Document analysis workflow")
    print("  - case-summary: Executive case summary generator")

    await cleanup_connections()


if __name__ == "__main__":
    asyncio.run(main())
