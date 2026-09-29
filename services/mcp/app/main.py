"""Read-only MCP adapter. Launch per user with CASEWISE_USER_TOKEN in its environment."""
import os
import httpx
from mcp.server.fastmcp import FastMCP

server = FastMCP("CaseWise")
BASE = os.getenv("AI_SERVICE_URL", "http://localhost:8000")


def call(path: str):
    token = os.getenv("CASEWISE_USER_TOKEN")
    if not token:
        raise ValueError("CASEWISE_USER_TOKEN is required for MCP access")
    response = httpx.get(f"{BASE}/api{path}", headers={"Authorization": f"Bearer {token}"}, timeout=30)
    response.raise_for_status()
    return response.json()


def post(path: str, payload: dict):
    token = os.getenv("CASEWISE_USER_TOKEN")
    if not token:
        raise ValueError("CASEWISE_USER_TOKEN is required for MCP access")
    response = httpx.post(f"{BASE}/api{path}", headers={"Authorization": f"Bearer {token}"}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


@server.tool()
def list_cases() -> list[dict]:
    """List cases available to the authenticated CaseWise user."""
    return call("/cases")


@server.tool()
def get_case(case_id: str) -> dict:
    """Get an authorized case and its client-safe or lawyer view."""
    return call(f"/cases/{case_id}")


@server.tool()
def list_case_documents(case_id: str) -> list[dict]:
    """List visible documents and their real processing states for one case."""
    return call(f"/cases/{case_id}/documents")


@server.tool()
def search_case_documents(case_id: str, question: str) -> list[dict]:
    """Search only authorized documents in one case; return source excerpts."""
    return post(f"/cases/{case_id}/search", {"question": question})


@server.tool()
def get_case_timeline(case_id: str) -> list[dict]:
    """List source-aware timeline events for an authorized case."""
    return call(f"/cases/{case_id}/timeline_events")


@server.tool()
def list_case_evidence(case_id: str) -> list[dict]:
    """List evidence records visible to the authenticated user."""
    return call(f"/cases/{case_id}/evidence")


@server.tool()
def get_upcoming_hearings(case_id: str) -> list[dict]:
    """List hearings visible in a case."""
    return call(f"/cases/{case_id}/hearings")


if __name__ == "__main__":
    server.run(transport="stdio")
