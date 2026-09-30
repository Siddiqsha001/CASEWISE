CASEWISE AI - SAMPLE LEGAL CASE DOCUMENTS
=========================================

This folder contains comprehensive sample documents for testing CaseWise AI features.
All documents are fictional and created for demonstration purposes only.

CASE SUMMARY
------------
Case Name: TechVision Solutions Inc. v. Quantum Digital Services LLC
Case Type: Breach of Contract, Fraud, Trade Secret Misappropriation
Jurisdiction: Superior Court of California, San Francisco County
Case Number: CV-2025-004892

Case Overview:
TechVision hired Quantum to develop an enterprise CRM platform (VisionCRM) for $2.85M.
Quantum breached the contract by using unqualified personnel, delivering defective work,
and abandoning the project. TechVision claims Quantum also misappropriated trade secrets
to develop a competing product.

DOCUMENT LIST
-------------

1. 01-complaint-breach-of-contract.txt (48 pages)
   - Legal complaint filed by TechVision
   - Contains allegations of breach of contract, breach of fiduciary duty, and fraud
   - Details damages exceeding $7 million
   - Perfect for testing AI case analysis and document summarization

2. 02-master-services-agreement.txt (42 pages)
   - The contract at the center of the dispute
   - Contains detailed service specifications, payment terms, and legal provisions
   - Includes personnel qualifications, confidentiality, and IP assignment clauses
   - Useful for contract analysis and clause extraction features

3. 03-email-evidence-collection.txt (12 pages)
   - Collection of 18 email communications between parties
   - Spans from contract negotiation through project termination
   - Shows deteriorating relationship and admissions of breach
   - Great for timeline generation and evidence organization

4. 04-expert-witness-report-technical.txt (38 pages)
   - Technical expert report on software development standards
   - Detailed code quality analysis and professional practice violations
   - Contains specific technical findings and damages assessments
   - Tests AI's ability to extract expert opinions and technical details

5. 05-financial-damages-analysis.txt (45 pages)
   - Economic expert report calculating damages
   - Itemizes losses: $10.3 million total claimed damages
   - Includes lost profits, wasted costs, and business opportunities
   - Perfect for financial analysis and damages calculation features

6. 06-witness-deposition-transcript.txt (12 pages)
   - Deposition transcript of defendant's CTO Marcus Chen
   - Contains admissions and key testimony
   - Shows questioning strategy and witness responses
   - Useful for testimony analysis and key admissions extraction

TOTAL PAGES: ~197 pages of comprehensive legal content

TESTING RECOMMENDATIONS
-----------------------

Document Upload & Processing:
- Upload all documents to test bulk processing capabilities
- Verify text extraction from TXT files
- Test processing status updates for multiple files

AI-Powered Features to Test:

1. Case Summary Generation
   - Should identify parties, claims, and key facts

2. Timeline Creation
   - Should extract chronological events from multiple documents
   - Email dates, contract milestones, project phases

3. Key Issues Identification
   - Contract breach (staffing violations)
   - Defective deliverables
   - Project abandonment
   - Trade secret misappropriation

4. Evidence Organization
   - Contract provisions
   - Email admissions
   - Expert opinions
   - Financial damages

5. Claims Analysis
   - Three causes of action (contract, fiduciary duty, fraud)
   - Damages: $10.3M

6. Document Q&A Examples:
   - "What were the staffing requirements in the contract?"
   - "How much did TechVision pay Quantum?"
   - "What defects were found in Phase 2 deliverables?"
   - "What is the total amount of damages claimed?"
   - "When did Quantum abandon the project?"
   - "What is QuantumConnect and how is it relevant?"

7. Citation Verification
   - AI responses should cite specific documents and page references
   - Test [source:UUID] citation format

8. Cross-Document Analysis
   - Compare contract requirements vs actual performance (emails + expert report)
   - Track financial claims across complaint and damages report
   - Correlate witness testimony with email evidence

REALISTIC COMPLEXITY
--------------------
These documents contain:
- Complex technical concepts (software development, AI/ML)
- Financial analysis (lost profits, damages calculations)
- Legal arguments (breach, fraud, trade secrets)
- Multiple document types (contracts, emails, expert reports, depositions)
- Cross-references between documents
- Chronological narrative spanning 12+ months
- Realistic legal language and formatting

This mirrors actual legal cases and provides comprehensive testing of CaseWise AI's
document analysis, RAG retrieval, and AI-powered insights capabilities.

NEXT STEPS FOR TESTING
-----------------------
1. Create a new case in CaseWise AI
2. Upload all 6 documents
3. Wait for processing to complete (AI indexing via Qdrant)
4. Test "Ask CaseWise" feature with questions
5. Test "AI Analysis" feature for case review
6. Verify citations link back to correct documents
7. Check timeline extraction
8. Evaluate quality of AI-generated summaries and insights

Note: These documents are specifically designed to test semantic search and RAG
capabilities. Questions should retrieve relevant passages and generate accurate,
source-grounded answers.
