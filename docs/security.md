# Security and authorization

## Identity and role

Supabase Auth issues the user session. `profiles.role` is server-managed and never accepted from a client request as an authority claim. Case access comes from `case_members`, not a case ID in a URL or a vector payload. Invitation and membership changes are privileged operations with audit entries.

## Access matrix

| Resource | Assigned lawyer | Assigned client | Other user |
| --- | --- | --- | --- |
| Case metadata | Read/update according to role | Read client-safe fields | No access |
| Documents | Read/manage | Read only `CLIENT_SHARED` | No access |
| Claims, evidence, timeline | Read/review | Read only `CLIENT_SHARED` | No access |
| Internal AI analyses, counterarguments, hearing preparation | Read/manage | No access unless explicitly shared | No access |
| Lawyer notes | Read/manage | No access unless explicitly shared | No access |
| Client tasks and notifications | Read if case member | Read own or shared records | No access |
| Payments | Read/manage | Read only explicitly shared status | No access |

An assigned lawyer is a `case_members` row with `member_role = LAWYER`; an assigned client is a row with `member_role = CLIENT`. The client row must match the verified `clients.portal_user_id` for the case's client, unless a later multi-client design explicitly permits more. Keep client-safe case data in a view or dedicated response serializer so private columns cannot slip into API responses.

## RLS policy rules

- Enable and test RLS for **every** case-related table, `profiles`, `clients`, and Storage objects. Default deny; define explicit `SELECT`, `INSERT`, `UPDATE`, and `DELETE` rules where needed.
- For lawyer access, require `auth.uid()` to have an active lawyer membership on the same `case_id`. For client access, require client membership and `visibility = CLIENT_SHARED` on records with private content.
- `USING` and `WITH CHECK` must both constrain case ID, membership, and role. Guard against a user changing `visibility`, `case_id`, `created_by`, or role to escalate access.
- Policies for join tables must verify both linked records belong to the same authorized case.
- Notifications are addressed to `auth.uid()`; activity logs are readable only by assigned lawyers and writable through trusted server code.
- Do not expose the Supabase service-role key to browser code. Trusted workers using it must manually check the originating principal and case access.

## Storage and retrieval

Use a private Supabase Storage bucket. A server-generated path such as `cases/{case_id}/{document_id}/{safe_name}` is metadata, not proof of access. Storage read policies should join document records and case membership; clients also need shared visibility. Prefer short-lived signed URLs generated after authorization. Validate MIME type by content, extension, and file size before accepting PDF/DOCX/TXT. Reject executable or malformed content and record processing errors without leaking internals.

Every Qdrant query requires an exact-match `caseId` filter for a case the principal is authorized to read. The retrieval service must check returned `caseId`, document ID, document visibility, and page provenance against PostgreSQL before using chunks or producing citations. Never offer an unrestricted cross-case search endpoint. Qdrant is not an access control system.

## Internal services and MCP

Next.js, FastAPI, and MCP need a verified end-user principal and a protected service-to-service channel. FastAPI and MCP recheck access rather than trusting a forwarded role or case ID. Do not put long-lived service credentials in model prompts. MCP tool calls receive only the minimum data needed; write tools require explicit user confirmation and audit events. Log access decisions and failures without full document contents.

## Required security tests before release

- Unassigned user cannot enumerate cases, documents, storage objects, or Qdrant matches.
- Client cannot see private notes, counterarguments, private analyses, or unshared documents, including via citations or MCP.
- Case A member cannot retrieve Case B chunks even by supplying Case B IDs or malicious filters.
- Users cannot add themselves to `case_members` or change `visibility`/roles through direct Supabase calls.
- Invalid uploads, forged service requests, and expired sessions fail safely.
