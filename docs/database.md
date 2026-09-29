# Database design

This is the proposed PostgreSQL schema, not an applied migration. Use UUID primary keys, `created_at` / `updated_at` timestamps, foreign keys, bounded status values, and indexes for common case-scoped queries. `auth.users` owns authentication; `profiles.id` references it.

## Core relationships

| Table | Main columns | Notes |
| --- | --- | --- |
| `profiles` | `id`, `role`, `display_name`, `email` | `id → auth.users.id`; role `LAWYER` or `CLIENT`. Email is display data, not the authorization key. |
| `clients` | `id`, `kind`, `name`, `phone`, `email`, `address`, `portal_user_id` | `portal_user_id → profiles.id` nullable until invitation is accepted. Lawyer-created client records can exist without login. |
| `cases` | `id`, `title`, `case_number`, `case_type`, `court`, `status`, `priority`, `filing_date`, `client_id`, `main_issue`, `description`, `created_by` | `client_id → clients.id`; draft or active status. |
| `case_members` | `case_id`, `user_id`, `member_role`, `created_at` | Composite PK. The explicit lawyer/client access grant; link a client login only after verification. |
| `opposing_parties` | `id`, `case_id`, `kind`, `name`, `contact`, `address`, `counsel` | A case may have multiple opposing parties. |
| `documents` | `id`, `case_id`, `file_name`, `mime_type`, `byte_size`, `storage_path`, `processing_status`, `visibility`, `uploaded_by` | Private Storage path is server controlled; status records real pipeline progress/failure. |
| `document_chunks` | `id`, `case_id`, `document_id`, `page_number`, `section`, `text`, `content_hash`, `embedding_state` | PostgreSQL provenance; Qdrant point ID matches this row ID. |
| `claims` | `id`, `case_id`, `statement`, `source_chunk_id`, `status`, `visibility`, `reviewed_by` | AI suggestions are editable and distinguishable from reviewed facts. |
| `evidence` | `id`, `case_id`, `name`, `type`, `description`, `source_document_id`, `source_page`, `status`, `visibility`, `notes` | Source points to a case document. |
| `claim_evidence` | `claim_id`, `evidence_id`, `relationship`, `created_at` | Composite PK; both records must belong to the same case. |
| `timeline_events` | `id`, `case_id`, `event_date`, `description`, `source_chunk_id`, `status`, `visibility` | Store uncertainty/precision if the source gives only a partial date. |
| `contradictions` | `id`, `case_id`, `source_a_chunk_id`, `source_b_chunk_id`, `description`, `review_status`, `visibility` | Potential inconsistency; neither source is declared false. |
| `hearings` | `id`, `case_id`, `starts_at`, `court`, `purpose`, `status`, `notes`, `visibility` | Reminders in a related schedule table or constrained JSON once worker design is set. |
| `tasks` | `id`, `case_id`, `title`, `assignee_id`, `due_at`, `status`, `visibility` | Client assignees see only shared tasks. |
| `payments` | `id`, `case_id`, `total_fee`, `amount_paid`, `due_date`, `status`, `visibility` | Tracking only; no payment credentials or processing. |
| `notifications` | `id`, `recipient_id`, `case_id`, `kind`, `message`, `read_at` | Recipient scoped. |
| `ai_analyses` | `id`, `case_id`, `kind`, `result`, `source_chunk_ids`, `status`, `visibility`, `model` | Generated results and provenance; private by default. |
| `case_notes` | `id`, `case_id`, `author_id`, `body`, `visibility` | Lawyer private by default. |
| `activity_logs` | `id`, `case_id`, `actor_id`, `action`, `entity_type`, `entity_id`, `created_at` | Append-only audit; no sensitive document text in logs. |

## Constraints and indexes

- Enforce `case_members(case_id, user_id)` uniqueness and indexes on `user_id, case_id`.
- Index every case child table on `case_id`; index dates/statuses used by dashboards (`hearings.starts_at`, `tasks.due_at`, `documents.processing_status`).
- Enforce same-case source references for chunk, claim, evidence, and analysis links through composite foreign keys or database triggers; an ordinary foreign key to an ID alone does not prove same-case ownership.
- Use check constraints or carefully migrated enums for roles, visibility, processing status, and task/hearing status.
- Store money in a fixed decimal type with currency; enforce nonnegative amounts. Compute remaining balance from recorded amounts.
- Keep immutable original filenames for display, but use generated IDs in private storage paths.

## RLS strategy

Enable RLS on every user-visible table and private storage bucket. Define narrowly scoped SQL helper functions such as `is_case_lawyer(case_id)` and `is_case_client(case_id)` based on `auth.uid()` and `case_members`; review their `search_path` and privileges. A lawyer sees assigned case records. A client sees their assigned case and only rows explicitly marked `CLIENT_SHARED` (plus their own tasks/notifications where appropriate). `case_members` edits must go through a controlled server operation that checks grant authority; users cannot self-enroll. Inserts and updates require matching `WITH CHECK` policies so records cannot be moved between cases. Service-role use is limited to trusted workers and must perform explicit authorization before accessing user data.

See [security.md](security.md) for policy details and Storage access.
