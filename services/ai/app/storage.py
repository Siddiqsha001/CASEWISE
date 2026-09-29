"""Private document storage. Uses hosted Supabase Storage when configured."""
import os
import ssl
from pathlib import Path
from urllib.parse import quote

import certifi
import httpx

BASE = os.getenv("SUPABASE_URL", "").rstrip("/")
SECRET = os.getenv("SUPABASE_SECRET_KEY", "")
BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "case-documents")
LOCAL_DIR = Path(os.getenv("DOCUMENT_DIR", "/data/documents"))


def _headers():
    return {"apikey": SECRET, "Authorization": f"Bearer {SECRET}"}


def _ensure_bucket(client: httpx.Client):
    response = client.get(f"{BASE}/storage/v1/bucket/{BUCKET}", headers=_headers())
    if response.status_code == 404:
        response = client.post(f"{BASE}/storage/v1/bucket", headers=_headers(), json={"id": BUCKET, "name": BUCKET, "public": False})
        if response.status_code not in (200, 201, 409):
            response.raise_for_status()
    else:
        response.raise_for_status()
        if response.json().get("public"):
            raise RuntimeError("Case document bucket must be private")


def put_document(case_id: str, document_id: str, data: bytes, mime_type: str) -> str:
    if BASE and SECRET:
        object_path = f"{case_id}/{document_id}"
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        with httpx.Client(timeout=45, verify=ssl_context) as client:
            _ensure_bucket(client)
            response = client.post(
                f"{BASE}/storage/v1/object/{BUCKET}/{quote(object_path)}",
                headers={**_headers(), "content-type": mime_type, "x-upsert": "false"},
                content=data,
            )
            response.raise_for_status()
        return f"supabase://{BUCKET}/{object_path}"
    path = LOCAL_DIR / case_id / document_id
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return str(path)


def read_document(storage_path: str) -> bytes:
    if storage_path.startswith("supabase://"):
        if not BASE or not SECRET:
            raise RuntimeError("Supabase Storage credentials are missing")
        object_path = storage_path.removeprefix("supabase://")
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        with httpx.Client(timeout=45, verify=ssl_context) as client:
            response = client.get(f"{BASE}/storage/v1/object/{quote(object_path, safe='/')}", headers=_headers())
            response.raise_for_status()
            return response.content
    return Path(storage_path).read_bytes()
