# Document processing and grounded RAG

## Ingestion

1. Next.js checks lawyer membership and validates PDF, DOCX, or TXT upload. Store the original in a private Supabase bucket and a `documents` row with `UPLOADED` state.
2. A durable worker job moves through `VALIDATING`, `EXTRACTING`, `CHUNKING`, `EMBEDDING`, `INDEXING`, and `READY`, or records `FAILED` with a safe error. Do not show completed steps before they finish.
3. Use PyMuPDF for page-aware PDF text, `python-docx` for DOCX, and a bounded decoder for TXT. DOCX and TXT may have no reliable page number; represent that as `null`, never invent page references. Empty/scanned PDFs report `OCR_REQUIRED`; OCR is a later feature.
4. Chunk per page or logical section with controlled overlap. Persist chunk text and source metadata in PostgreSQL. Embed locally using a configured Sentence Transformers/BGE model.
5. Upsert Qdrant points using the chunk UUID. Required payload: `caseId`, `documentId`, `documentName`, `pageNumber` (nullable), `section` (nullable), `chunkId`. Also store content/version metadata for reindexing.

The database and vector index can diverge. Keep a retryable indexing state, idempotent point IDs, and a reconciliation job. Deleting a document revokes database access immediately and queues vector deletion; retrieval also checks the database so stale points cannot leak.

## Retrieval and answer

```text
verified principal + authorized case ID + question
  → local question embedding
  → Qdrant exact caseId filter
  → score threshold and diversity selection
  → recheck each chunk and document in PostgreSQL
  → context with stable source IDs
  → LLMProvider (Gemini selected; Ollama optional)
  → validate cited source IDs and answer shape
  → cited response or insufficient-information response
```

If there is no sufficient source material, respond: **“I could not find sufficient information in the uploaded case documents.”** Do not fill missing facts from model memory. Distinguish source fact, inference, and potential argument. Source citations should include document name, page when available, and a source route that checks access before opening the document. Prompt injection in documents must be treated as untrusted text; document instructions cannot change the assistant's tool or access rules.

## Provider interfaces

`LLMProvider` supports answer generation and structured output. `GeminiProvider` reads `GEMINI_API_KEY`, `GEMINI_ANSWER_MODEL`, and `GEMINI_ANALYSIS_MODEL` from central configuration; `OllamaProvider` remains an optional local adapter. `EmbeddingProvider` is separate; the local BGE adapter reads `EMBEDDING_MODEL`. Changing embedding models requires a new compatible Qdrant collection or full reindex; vector dimensions are fixed per collection.

LangChain may help with parsing/retrieval but is optional. LangGraph is only justified by a multi-step workflow with meaningful state and recovery. A simple case question should remain a direct service flow.

## Structured analysis

Timeline events, claims, evidence mappings, gaps, contradictions, counterarguments, and hearing briefs should be persisted as suggestions with source chunk IDs, confidence/uncertainty, visibility, and review status. Lawyers can edit and approve them. A generated item without verifiable source IDs must be rejected or explicitly labeled as an unsupported suggestion. No outcome probability is computed.
