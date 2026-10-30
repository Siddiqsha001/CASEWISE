"""Demo AI analysis data for testing without API calls."""

DEMO_ANALYSIS_RESULT = {
    "timeline": [
        {
            "text": "March 15, 2024: TechVision and Quantum entered into Master Services Agreement for VisionCRM development project valued at $2,850,000",
            "quote": "On March 15, 2024, TechVision and Quantum entered into a Master Services Agreement",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 1
        },
        {
            "text": "June 28, 2024: Phase 1 deliverables completed on time with minor defects that were subsequently corrected",
            "quote": "Quantum appeared to be performing adequately, delivering Phase 1 deliverables on June 28, 2024",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        },
        {
            "text": "August 2024: Quantum's performance began to deteriorate significantly with delays and quality issues emerging",
            "quote": "beginning in August 2024, Quantum's performance began to deteriorate significantly",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        },
        {
            "text": "October 28, 2024: Phase 2 deliverables delivered nearly one month late containing numerous critical defects",
            "quote": "Phase 2 deliverables, due September 30, 2024, were delayed until October 28, 2024, and contained numerous critical defects",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        },
        {
            "text": "November 15, 2024: CTO Marcus Chen admitted during project review that junior developers were assigned without consent",
            "quote": "Marcus Chen admitted that Quantum had assigned junior developers to the Project without TechVision's knowledge or consent",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        },
        {
            "text": "January 8, 2025: Last substantive communication from Quantum before abandoning the project",
            "quote": "The last substantive communication from Quantum was on January 8, 2025",
            "documentName": "03-email-evidence-collection.txt",
            "pageNumber": 8
        },
        {
            "text": "January 31, 2025: TechVision formally terminated the Master Services Agreement due to material breaches",
            "quote": "TechVision terminated the contract on January 31, 2025",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 3
        }
    ],

    "claims": [
        {
            "text": "Breach of Contract: Quantum violated staffing requirements by using junior developers instead of required senior certified developers",
            "quote": "only senior developers with specific certifications would work on the Project",
            "documentName": "02-master-services-agreement.txt",
            "pageNumber": 15
        },
        {
            "text": "Breach of Contract: Failed to deliver Phase 2 on time and delivered work containing critical defects including system crashes and data corruption",
            "quote": "Phase 2 deliverables contained numerous critical defects including system crashes, data corruption issues",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        },
        {
            "text": "Breach of Fiduciary Duty: Misappropriated TechVision's confidential information and trade secrets to develop competing product QuantumConnect",
            "quote": "Quantum developed QuantumConnect using TechVision's confidential information",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 4
        },
        {
            "text": "Fraud: Quantum misrepresented their capabilities and staffing qualifications during contract negotiations",
            "quote": "Quantum's representations regarding their development team capabilities were materially false",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 5
        },
        {
            "text": "Total Damages: $10.3 million including wasted payments, replacement costs, lost profits, and opportunity costs",
            "quote": "Total claimed damages: $10.3 million itemized as follows",
            "documentName": "05-financial-damages-analysis.txt",
            "pageNumber": 1
        }
    ],

    "evidence": [
        {
            "text": "Master Services Agreement contains explicit staffing requirements mandating senior developers with specific certifications",
            "quote": "All development work shall be performed by senior developers with minimum 5 years experience",
            "documentName": "02-master-services-agreement.txt",
            "pageNumber": 15
        },
        {
            "text": "Email chain documents project deterioration and Quantum's failure to respond to quality concerns from August through December 2024",
            "quote": "multiple emails from TechVision project manager documenting ongoing defects and lack of response",
            "documentName": "03-email-evidence-collection.txt",
            "pageNumber": 3
        },
        {
            "text": "CTO deposition testimony admitting use of junior developers and development of competing product during contract term",
            "quote": "Chen admitted Quantum began QuantumConnect development in November 2024 while under contract",
            "documentName": "06-witness-deposition-transcript.txt",
            "pageNumber": 7
        },
        {
            "text": "Technical expert report documenting code quality substantially below industry standards with inadequate error handling",
            "quote": "Code quality was substantially below professional standards and would require significant rework",
            "documentName": "04-expert-witness-report-technical.txt",
            "pageNumber": 12
        },
        {
            "text": "Financial analysis calculating $10.3M in total damages with detailed breakdown of all cost categories",
            "quote": "$1.425M wasted payments, $3.2M replacement costs, $4.8M lost profits, $875K opportunity costs",
            "documentName": "05-financial-damages-analysis.txt",
            "pageNumber": 2
        },
        {
            "text": "Payment records showing TechVision made $1,425,000 in timely milestone payments representing 50% of contract value",
            "quote": "TechVision performed all obligations including making timely payments totaling $1,425,000",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        }
    ],

    "possibleEvidenceGaps": [
        {
            "text": "Additional documentation may be needed regarding the specific technical certifications held by Quantum's assigned developers",
            "quote": "While the MSA requires specific certifications, the current evidence does not include verification",
            "documentName": "02-master-services-agreement.txt",
            "pageNumber": 15
        },
        {
            "text": "Complete financial records for all development costs and overhead may strengthen the damages calculation",
            "quote": "Financial analysis based on available invoices and estimates",
            "documentName": "05-financial-damages-analysis.txt",
            "pageNumber": 18
        },
        {
            "text": "Additional witness depositions from TechVision's technical staff could corroborate the expert's findings on code quality",
            "quote": "Expert analysis based on code review; internal team testimony would provide supporting context",
            "documentName": "04-expert-witness-report-technical.txt",
            "pageNumber": 25
        }
    ],

    "potentialContradictions": [
        {
            "text": "Phase 1 was completed successfully, which may complicate claims that Quantum never had adequate capabilities",
            "quote": "Phase 1 deliverables passed TechVision's quality assurance testing with minor defects",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        },
        {
            "text": "Initial acceptance of Phase 1 deliverables could be argued as waiver of strict staffing requirement enforcement",
            "quote": "TechVision accepted Phase 1 without raising concerns about personnel qualifications at that time",
            "documentName": "03-email-evidence-collection.txt",
            "pageNumber": 2
        }
    ],

    "potentialCounterarguments": [
        {
            "text": "Defense may argue that technical difficulties were due to unrealistic specifications rather than developer incompetence",
            "quote": "The technical specifications required advanced AI/ML capabilities that are inherently challenging",
            "documentName": "02-master-services-agreement.txt",
            "pageNumber": 8
        },
        {
            "text": "Quantum may claim that TechVision's delays in providing required access and information contributed to project delays",
            "quote": "Several email requests for system access and API documentation had delayed responses",
            "documentName": "03-email-evidence-collection.txt",
            "pageNumber": 5
        },
        {
            "text": "Defense could argue the lost profits calculation is speculative since VisionCRM had not yet launched in the market",
            "quote": "Lost profit projections are based on market analysis rather than actual revenue performance",
            "documentName": "05-financial-damages-analysis.txt",
            "pageNumber": 14
        },
        {
            "text": "Quantum may dispute trade secret misappropriation by arguing QuantumConnect uses different architecture and publicly available technologies",
            "quote": "Defendant may claim independent development and publicly available frameworks",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 4
        }
    ],

    "hearingPreparation": [
        {
            "text": "Prepare detailed timeline demonstrating pattern of declining performance from August 2024 onward with specific examples",
            "quote": "Multiple documented instances of missed deadlines and quality failures over five-month period",
            "documentName": "03-email-evidence-collection.txt",
            "pageNumber": 3
        },
        {
            "text": "Have technical expert available to explain code quality issues in terms understandable to non-technical judge or jury",
            "quote": "Code quality substantially below industry standards with inadequate error handling and security vulnerabilities",
            "documentName": "04-expert-witness-report-technical.txt",
            "pageNumber": 12
        },
        {
            "text": "Emphasize CTO's admission in deposition regarding junior developers and competing product development during contract term",
            "quote": "Chen admitted using junior developers and developing QuantumConnect while still under contract with TechVision",
            "documentName": "06-witness-deposition-transcript.txt",
            "pageNumber": 7
        },
        {
            "text": "Present clear damages breakdown with supporting documentation for each category to establish concrete monetary harm",
            "quote": "Detailed itemization: $1.425M wasted payments, $3.2M replacement costs, $4.8M lost profits, $875K opportunities",
            "documentName": "05-financial-damages-analysis.txt",
            "pageNumber": 2
        },
        {
            "text": "Anticipate and prepare response to argument that Phase 1 success undermines competency claims",
            "quote": "Phase 1 success followed by consistent Phase 2-3 failures suggests staffing or resource changes",
            "documentName": "01-complaint-breach-of-contract.txt",
            "pageNumber": 2
        }
    ]
}


def get_demo_analysis():
    """Get demo analysis result with proper structure."""
    import uuid
    from datetime import datetime

    # Add documentId and chunkId to each item
    result = {}
    for key, items in DEMO_ANALYSIS_RESULT.items():
        result[key] = []
        for item in items:
            enriched = {
                **item,
                "chunkId": str(uuid.uuid4()),
                "documentId": str(uuid.uuid4())
            }
            result[key].append(enriched)

    result["disclaimer"] = "AI-generated information should be reviewed and verified by a qualified legal professional."

    return {
        "id": str(uuid.uuid4()),
        "createdAt": datetime.utcnow().isoformat() + "Z",
        **result
    }
