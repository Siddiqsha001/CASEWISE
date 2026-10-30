"""Demo Q&A pairs and mock responses for testing without API calls."""

# Predefined questions and their mock answers based on the 6 sample documents
DEMO_QA_PAIRS = {
    "What were the staffing requirements in the contract?": {
        "answer": "The Master Services Agreement specified that only senior developers with specific certifications would work on the Project. [source:demo-msa-001] However, during a November 15, 2024 project review meeting, Quantum's CTO Marcus Chen admitted that Quantum had assigned junior developers to the Project without TechVision's knowledge or consent, in direct violation of these staffing requirements. [source:demo-complaint-001]",
        "citations": [
            {"documentName": "02-master-services-agreement.txt", "excerpt": "All development work shall be performed by senior developers with minimum 5 years experience and relevant certifications"},
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "Marcus Chen admitted that Quantum had assigned junior developers to the Project without TechVision's knowledge or consent"}
        ]
    },

    "How much did TechVision pay Quantum?": {
        "answer": "The total contract value was $2,850,000, payable in milestone-based installments over an eighteen-month development period. [source:demo-complaint-002] TechVision made timely payments for completed milestones totaling $1,425,000 through December 31, 2024, representing 50% of the total contract value. [source:demo-complaint-003]",
        "citations": [
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "The total contract value was $2,850,000"},
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "TechVision performed all obligations including making timely payments totaling $1,425,000"}
        ]
    },

    "What defects were found in Phase 2 deliverables?": {
        "answer": "Phase 2 deliverables, which were delayed until October 28, 2024, contained numerous critical defects including system crashes, data corruption issues, and failure to meet the specified performance benchmarks outlined in the technical specifications. [source:demo-complaint-004] The expert witness report documented that the code quality was substantially below industry standards, with inadequate error handling and poor architectural decisions. [source:demo-expert-001]",
        "citations": [
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "Phase 2 deliverables contained critical defects including system crashes, data corruption issues, and performance failures"},
            {"documentName": "04-expert-witness-report-technical.txt", "excerpt": "Code quality substantially below industry standards with inadequate error handling"}
        ]
    },

    "What is the total amount of damages claimed?": {
        "answer": "According to the financial damages analysis, TechVision claims total damages of $10.3 million. [source:demo-financial-001] This includes wasted contract payments of $1,425,000, additional costs to hire replacement developers of $3.2 million, lost profits from delayed product launch of $4.8 million, and business opportunity costs of $875,000. [source:demo-financial-002]",
        "citations": [
            {"documentName": "05-financial-damages-analysis.txt", "excerpt": "Total claimed damages: $10.3 million"},
            {"documentName": "05-financial-damages-analysis.txt", "excerpt": "Itemized: $1.425M wasted payments, $3.2M replacement costs, $4.8M lost profits, $875K opportunity costs"}
        ]
    },

    "When did Quantum abandon the project?": {
        "answer": "Based on email evidence, Quantum effectively abandoned the project in January 2025. [source:demo-email-001] The last substantive communication from Quantum was on January 8, 2025, when they stopped responding to TechVision's requests for project updates. [source:demo-email-002] TechVision formally terminated the contract on January 31, 2025. [source:demo-complaint-005]",
        "citations": [
            {"documentName": "03-email-evidence-collection.txt", "excerpt": "Last communication from Quantum: January 8, 2025"},
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "TechVision terminated the contract on January 31, 2025"}
        ]
    },

    "What is QuantumConnect and how is it relevant?": {
        "answer": "QuantumConnect is a competing CRM product that Quantum allegedly developed using TechVision's confidential information and trade secrets. [source:demo-complaint-006] During his deposition, Marcus Chen admitted that Quantum began developing QuantumConnect in November 2024, while still under contract with TechVision, using similar architectural approaches and features. [source:demo-deposition-001] This forms the basis of TechVision's trade secret misappropriation claim.",
        "citations": [
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "Quantum developed QuantumConnect using TechVision's confidential information"},
            {"documentName": "06-witness-deposition-transcript.txt", "excerpt": "Chen admitted Quantum began QuantumConnect development in November 2024 while under contract"}
        ]
    },

    "What are the main causes of action?": {
        "answer": "TechVision asserts three main causes of action: (1) Breach of Contract for failing to deliver conforming work and using unqualified personnel, (2) Breach of Fiduciary Duty for misappropriating confidential information, and (3) Fraud for misrepresenting their capabilities and staffing. [source:demo-complaint-007] Each cause of action is supported by documentary evidence, expert testimony, and witness admissions. [source:demo-expert-002]",
        "citations": [
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "Three causes of action: Breach of Contract, Breach of Fiduciary Duty, and Fraud"},
            {"documentName": "04-expert-witness-report-technical.txt", "excerpt": "Multiple breaches documented including personnel violations and substandard deliverables"}
        ]
    },

    "What evidence supports the breach of contract claim?": {
        "answer": "Multiple sources of evidence support the breach: (1) The MSA contract terms requiring senior developers [source:demo-msa-002], (2) Marcus Chen's admission in deposition that junior developers were used [source:demo-deposition-002], (3) Email communications showing quality problems and delays [source:demo-email-003], (4) Expert witness report documenting substandard code quality [source:demo-expert-003], and (5) Financial analysis showing resulting damages. [source:demo-financial-003]",
        "citations": [
            {"documentName": "02-master-services-agreement.txt", "excerpt": "Contract requires senior developers with specific qualifications"},
            {"documentName": "06-witness-deposition-transcript.txt", "excerpt": "Chen admitted using junior developers"},
            {"documentName": "03-email-evidence-collection.txt", "excerpt": "Multiple emails document quality issues and project delays"}
        ]
    },

    "What were the project timelines and phases?": {
        "answer": "The Project was structured in four phases over 18 months: Phase 1 (completion by June 30, 2024), Phase 2 (September 30, 2024), Phase 3 (December 31, 2024), and Phase 4 (March 31, 2025), with final testing and deployment by September 30, 2025. [source:demo-complaint-008] Phase 1 was delivered on time with minor issues, but Phase 2 was delayed by nearly a month and contained critical defects. [source:demo-complaint-009]",
        "citations": [
            {"documentName": "01-complaint-breach-of-contract.txt", "excerpt": "Four development phases over 18 months from April 2024 to September 2025"},
            {"documentName": "02-master-services-agreement.txt", "excerpt": "Milestone-based delivery schedule with specific completion dates"}
        ]
    },

    "What technical issues did the expert identify?": {
        "answer": "The technical expert report identified multiple serious issues: inadequate error handling, poor architectural decisions, failure to follow industry best practices, insufficient code documentation, lack of proper testing frameworks, and security vulnerabilities in the authentication modules. [source:demo-expert-004] The expert concluded that the code quality was substantially below professional standards and would require significant rework. [source:demo-expert-005]",
        "citations": [
            {"documentName": "04-expert-witness-report-technical.txt", "excerpt": "Multiple violations: inadequate error handling, poor architecture, security vulnerabilities"},
            {"documentName": "04-expert-witness-report-technical.txt", "excerpt": "Code quality substantially below professional standards requiring significant rework"}
        ]
    }
}

def get_predefined_questions():
    """Return list of predefined questions for demo mode."""
    return list(DEMO_QA_PAIRS.keys())

def get_demo_answer(question: str):
    """Get demo answer for a predefined question."""
    # Exact match
    if question in DEMO_QA_PAIRS:
        return DEMO_QA_PAIRS[question]

    # Fuzzy match - find closest question
    question_lower = question.lower().strip()
    for q, answer in DEMO_QA_PAIRS.items():
        if question_lower in q.lower() or q.lower() in question_lower:
            return answer

    # Default fallback
    return {
        "answer": "I could not find sufficient information in the uploaded case documents. Please try one of the suggested questions or upload relevant documents.",
        "citations": []
    }

# Suggested questions to show in UI
SUGGESTED_QUESTIONS = [
    "What were the staffing requirements in the contract?",
    "How much did TechVision pay Quantum?",
    "What defects were found in Phase 2 deliverables?",
    "What is the total amount of damages claimed?",
    "When did Quantum abandon the project?",
    "What is QuantumConnect and how is it relevant?",
    "What are the main causes of action?",
    "What evidence supports the breach of contract claim?",
    "What were the project timelines and phases?",
    "What technical issues did the expert identify?"
]
