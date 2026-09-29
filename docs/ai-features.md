# Product and AI feature plan

AI-generated information should be reviewed and verified by a qualified legal professional. The platform must not predict outcomes, assign win probabilities, give guaranteed legal advice, or autonomously make legal decisions.

## Register New Case

Build a desktop-first, responsive multi-section page for lawyers:

1. **Case information:** title, type, number, court, status, filing date, priority.
2. **Client details:** select an existing client or create an individual/organization with name, phone, email, address. Show which mode is active and avoid duplicate client creation.
3. **Opposing party:** name, kind, contact, address, opposing counsel.
4. **Case details:** main issue and description.
5. **Important dates:** filing date, next hearing, document deadline, payment due date, extra dated events.
6. **Initial documents:** drag-and-drop PDF/DOCX/TXT, file validation, per-file upload/processing/processed/failed states.

Actions are **Save as Draft** and **Register Case & Analyze**. The latter creates the case, uploads files, starts real processing jobs, and displays each actual step: case created, documents uploaded, text extracted, chunks embedded/indexed, timeline and claims suggested, evidence mapped, gaps and contradictions checked, analysis completed. Failed steps stay visible with retry where safe. The dashboard opens when the required pipeline reaches a reliable state; partial results are labeled.

## Case views

The lawyer dashboard emphasizes active cases, upcoming hearings, pending tasks, payment dues, possible evidence gaps, potential contradictions, and recent activity. The client dashboard shows only their case status, next hearing, requested documents, assigned tasks, shared payment status, and notifications. Case details use tabs for Overview, Timeline, Documents, Evidence, Claims, AI Analysis, Hearings, Tasks, Payments, and Notes; client navigation omits inaccessible content.

## Ask CaseWise

Render a concise answer, relevant evidence, clickable citations, potential issues, and suggested review areas. Answers come only from authorized case documents. If retrieval is weak or unavailable, show the explicit insufficient-information response. Citations point to the authorized document and page when page information exists.

## Structured intelligence

- **Timeline:** event date, description, document/page source, uncertainty; show conflicting dates as potential inconsistencies for lawyer verification.
- **Claims and evidence:** editable claim/evidence records, source linkage, and mapping status. Separate extracted suggestions from lawyer-reviewed records.
- **Possible evidence gaps:** identify claims whose uploaded support appears incomplete; do not imply a legal outcome.
- **Potential contradictions:** show both cited sources and request verification without deciding which is true.
- **Potential counterarguments:** explicitly separate fact, inference, and potential argument, with sources.
- **Hearing preparation:** editable brief with date, court, issues, facts, evidence, gaps, contradictions, potential counterarguments, and documents to review.
- **Case preparation readiness:** coverage indicators for documents, claims/evidence, timeline consistency, counterargument review, and hearing preparation. Explain that these measure preparation coverage, not outcome likelihood.

## Other workflows

Hearings have date/time, court, purpose, status, notes, and configurable reminders (7, 3, 1 day, or custom). Tasks can be assigned to lawyers or clients and tracked as pending, in progress, or complete. Payments track total, paid, remaining, due date, and status only. Notifications cover hearings, payment due dates, document requests, tasks, processing completion, gaps, and inconsistencies.

## Fictional demo fixture

Use **ABC Traders vs XYZ Enterprises**, C.S. 245/2026, Commercial Court, Coimbatore, only as labeled fictional fixture data. The prompt lists Agreement, Invoice, Delivery Receipt, Payment Request, Legal Notice, and Communication documents, but provides no actual contents. Do not invent their text, events, citations, or extracted evidence. Add real synthetic fixture files deliberately when test cases are written.
