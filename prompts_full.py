"""Comprehensive prompt templates and helpers for the Paralegal Assistant persona.

This module provides system prompts, document-specific templates, checklists,
and procedures aligned with federal and state civil litigation.
"""

SYSTEM_PROMPT = """You are an expert Paralegal AI Assistant with comprehensive knowledge of paralegal duties, legal procedures, document preparation, case management, and client support. You function as a highly skilled paralegal professional supporting attorneys and legal teams with practical, hands-on legal work.

## Core Role & Boundaries
- You provide paralegal support, NOT legal advice or legal opinions
- All work product requires attorney review and approval
- You clarify your role: "I am a paralegal AI assistant working under attorney supervision"
- You cannot represent clients, establish attorney-client relationships, or make legal decisions
- You work within the scope of paralegal duties and applicable professional conduct rules

## Your Competencies
- Legal document preparation (pleadings, motions, discovery, subpoenas, affidavits)
- Court filing procedures (federal and state, e-filing systems)
- Case management and organization
- Legal research and investigation assistance
- Discovery management and coordination
- Trial preparation and logistics
- Client intake and communication
- Deadline tracking and calendar management
- Federal Rules of Civil Procedure, Criminal Procedure, Evidence
- State court procedures and local court rules

## Communication Standards
1. Be practical and efficient
2. Provide specific instructions and checklists
3. Organize information clearly with formatting
4. Remain professional and supportive
5. Always include mandatory disclaimers

## Mandatory Disclaimer for Every Response
Include this in every response: "Disclaimer: I am a paralegal AI assistant. This is not legal advice and requires attorney review. All legal decisions must be made by your supervising attorney."
"""

DOCUMENT_TEMPLATES = {
    "complaint": {
        "title": "Civil Complaint (Federal)",
        "checklist": [
            "Verify court jurisdiction (federal question, diversity, etc.)",
            "Confirm correct court and division",
            "Identify all parties (plaintiffs, defendants, their roles)",
            "Verify jurisdiction and venue requirements",
            "Draft caption with proper formatting",
            "Number and label each count/cause of action",
            "Include factual allegations (short and plain statement)",
            "State legal basis for each count",
            "Include demand for relief (damages, injunction, etc.)",
            "Verify Rule 11 compliance (reasonable inquiry)",
            "Check signature requirements (attorney name, address, phone)",
            "Prepare certificate of service",
            "Calculate filing fee",
            "Prepare cover sheet (if required by local rule)",
        ],
        "formatting": {
            "font": "Times New Roman or Arial, 12pt",
            "margins": "1 inch all sides",
            "line_spacing": "double-spaced",
            "page_limit": "None (unless local rule)",
            "caption_format": "Case number, court, judge (if assigned)",
        },
        "federal_rules": ["FRCP 8(a)", "FRCP 11", "28 U.S.C. § 1332 (diversity)", "28 U.S.C. § 1331 (federal question)"],
    },
    "motion_summary_judgment": {
        "title": "Motion for Summary Judgment",
        "checklist": [
            "Verify deadline (before trial, typically 56 days before trial)",
            "Confirm no material fact disputes exist",
            "Gather supporting evidence (affidavits, discovery responses, documents)",
            "Draft concise statement of undisputed material facts",
            "Include legal argument with case citations",
            "Prepare statement of issues to be decided",
            "Include rule 56 certification of no disputes",
            "Prepare supporting declarations/affidavits",
            "Prepare motion memorandum",
            "Include proof of service",
            "Calculate filing deadline (not less than 21 days before hearing)",
            "Check local rules for page limits and formatting",
        ],
        "formatting": {
            "font": "Times New Roman or Arial, 12pt",
            "margins": "1 inch all sides",
            "line_spacing": "double-spaced",
            "page_limit": "20-25 pages (verify local rule)",
        },
        "federal_rules": ["FRCP 56", "Anderson v. Liberty Lobby, 477 U.S. 242 (1986)"],
    },
    "discovery_request": {
        "title": "Interrogatories, Requests for Production, Requests for Admission",
        "checklist": [
            "Verify discovery scope (relevance, proportionality under Rule 26(b)(1))",
            "Check local court limitations (interrogatory count, etc.)",
            "Draft clear, specific questions (avoid compound questions)",
            "Include definitions and instructions",
            "Numbering: interrogatories, requests for production, requests for admission",
            "Include certificate of service",
            "Verify response deadline (30 days, or as agreed)",
            "Prepare response instructions",
            "Track objections and privilege claims",
            "Ensure proportionality to needs of case",
        ],
        "federal_rules": ["FRCP 26(b)", "FRCP 33 (interrogatories)", "FRCP 34 (production)", "FRCP 36 (admissions)"],
    },
    "affidavit": {
        "title": "Affidavit / Declaration Under Penalty of Perjury",
        "checklist": [
            "Confirm affiant capacity (personal knowledge, etc.)",
            "Draft clear statements (first person)",
            "State only facts, not legal conclusions",
            "Number each paragraph",
            "Include 'I declare under penalty of perjury...' or oath language",
            "Prepare signature block with date and notary (if required)",
            "Include notary seal (if required by jurisdiction)",
            "Proofread for accuracy",
            "Verify Rule 56 requirements if for motion",
        ],
        "federal_rules": ["FRCP 56(c)(4)", "28 U.S.C. § 1746 (unsworn declarations)"],
    },
    "subpoena": {
        "title": "Subpoena / Subpoena Duces Tecum",
        "checklist": [
            "Verify court issuing subpoena (case name, number, court)",
            "Identify correct recipient (individual or entity)",
            "Specify service method (certified mail, personal service, etc.)",
            "Include specific documents or testimony request",
            "State return date and location",
            "Include mileage fee (witnesses only, typically $0.20/mile minimum)",
            "Prepare instructions to recipient",
            "Arrange service (process server, certified mail, etc.)",
            "Verify Rule 45 requirements (subpoena formatting, service, notice)",
            "Include objection deadline",
        ],
        "federal_rules": ["FRCP 45 (subpoena requirements and service)"],
    },
}

FILING_PROCEDURE_CHECKLIST = """
## Court Filing Procedure (Federal / E-Filing)

### Pre-Filing
1. Verify correct court and division
2. Confirm case number and caption
3. Check filing deadline (including holidays/weekends)
4. Verify page limits and formatting requirements
5. Proofread entire document
6. Prepare certificate of service
7. Calculate filing fee
8. Verify filing method (electronic / paper)

### E-Filing (CM/ECF or similar)
1. Register e-filing account (if new filer)
2. Log in with credentials
3. Select case number
4. Select document type
5. Upload document(s) PDF
6. Enter service list / select recipients
7. Review entry summary
8. Submit filing
9. Confirm e-mail receipt from system
10. Print receipt (Notice of Electronic Filing)

### Paper Filing (if e-filing not available)
1. Print documents (required copies per court rule)
2. Prepare cover sheet (if required)
3. Prepare certificate of service (proof of service)
4. Include filing fee check
5. Mail certified to court clerk
6. Retain proof of mailing

### Post-Filing
1. Confirm docket entry on court website (24-48 hours)
2. Verify document appears as filed
3. Update case calendar with response deadline
4. Notify client and supervising attorney
5. File copy in case file
"""

DEADLINE_CALCULATION = """
## Federal Court Deadline Rules (FRCP)

**Computing Time (FRCP 6):**
- Count all days including Saturdays, Sundays, and holidays
- EXCLUDE: day of the act; INCLUDE: last day
- If deadline falls on Saturday, Sunday, or legal holiday → extend to next business day
- **3-day rule**: Add 3 calendar days if service by mail

**Common Deadlines:**
- Response to complaint: 21 days (or as extended)
- Summary judgment motion notice: 21 days before hearing
- Discovery responses: 30 days (or as extended)
- Trial preparation: varies per scheduling order

**Calculation Example:**
- Document served by email on Friday, January 5
- 21-day deadline: Count from Saturday Jan 6 (day 1) through Friday Jan 26 (day 21)
- If Jan 26 is holiday, extend to Monday Jan 29
"""

DISCOVERY_CHECKLIST = """
## Discovery Management Checklist

### Requests to Other Side
- [ ] Draft interrogatories (limit: typically 25 per FRCP, unless modified)
- [ ] Draft requests for production of documents
- [ ] Draft requests for admission (avoid mixing with other discovery)
- [ ] Include definitions and instructions
- [ ] Calculate response deadline (30 days + 3-day mail rule if applicable)
- [ ] Send with certificate of service
- [ ] Track responses in discovery log
- [ ] Monitor for objections and untimely responses
- [ ] Report to supervising attorney if responses inadequate

### Responses to Other Side
- [ ] Review requests immediately upon receipt
- [ ] Create response log and deadline tracking
- [ ] Identify responsive documents/information
- [ ] Draft responses (factually accurate, specify objections)
- [ ] Include privilege log if claiming privilege
- [ ] Obtain attorney review
- [ ] Serve responses before deadline (or seek extension)
- [ ] Maintain certificate of service

### Deposition Coordination
- [ ] Schedule with opposing counsel
- [ ] Prepare notice of deposition
- [ ] Arrange court reporter
- [ ] Prepare deponent (if your client)
- [ ] Organize documents for deposition
- [ ] Request exhibit list from opposing counsel
- [ ] Obtain transcript after deposition
- [ ] Review and index transcript
- [ ] Update case chronology with deposition information

### Privilege Management
- [ ] Create privilege log (document ID, date, parties, subject, privilege claim)
- [ ] Segregate privileged materials
- [ ] Avoid waiving privilege (review before production)
- [ ] Track inadvertent productions
- [ ] Review for attorney-client privilege, work product doctrine
"""

def build_document_prompt(doc_type: str, jurisdiction: str, user_text: str) -> str:
    """Build a combined prompt for document preparation or procedural guidance."""
    parts = [SYSTEM_PROMPT]
    
    # Add document-specific template if available
    if doc_type.lower() in DOCUMENT_TEMPLATES:
        template = DOCUMENT_TEMPLATES[doc_type.lower()]
        parts.append(f"\n## Document Type: {template['title']}\n")
        parts.append("### Preparation Checklist:")
        for item in template["checklist"]:
            parts.append(f"- {item}")
        if "formatting" in template:
            parts.append("\n### Formatting Requirements:")
            for key, value in template["formatting"].items():
                parts.append(f"- {key}: {value}")
        if "federal_rules" in template:
            parts.append("\n### Applicable Rules:")
            for rule in template["federal_rules"]:
                parts.append(f"- {rule}")
    
    # Add jurisdiction-specific info
    parts.append(f"\n## Jurisdiction: {jurisdiction}")
    if jurisdiction.lower() == "federal":
        parts.append("- Use Federal Rules of Civil Procedure (FRCP)")
        parts.append("- Consider local court rules for your district")
        parts.append("- E-filing via CM/ECF (or equivalent)")
    elif "state" in jurisdiction.lower():
        parts.append("- Verify state rules of civil procedure")
        parts.append("- Check local county court rules")
        parts.append("- Verify e-filing availability by court")
    
    # Add user input/question
    parts.append(f"\n## User Request / Question:\n{user_text}")
    
    # Add closing instructions
    parts.append("\n## Instructions:")
    parts.append("1. Address the user's specific question or request")
    parts.append("2. Provide step-by-step guidance where applicable")
    parts.append("3. Reference applicable rules and procedures")
    parts.append("4. Include practical tips and common pitfalls to avoid")
    parts.append("5. Always include the mandatory disclaimer")
    
    return "\n".join(parts)


def build_case_management_prompt(case_info: str) -> str:
    """Build a prompt for case management and organization tasks."""
    parts = [SYSTEM_PROMPT]
    parts.append("\n## Task: Case Management & Organization")
    parts.append(FILING_PROCEDURE_CHECKLIST)
    parts.append(DISCOVERY_CHECKLIST)
    parts.append(f"\n## Case Information Provided:\n{case_info}")
    parts.append("\n## Instructions:")
    parts.append("1. Analyze the case information")
    parts.append("2. Identify key deadlines based on typical litigation timeline")
    parts.append("3. Create an organized action plan")
    parts.append("4. Include discovery, motion practice, and trial preparation phases")
    parts.append("5. Flag items requiring attorney decision")
    parts.append("\nReminder: " + SYSTEM_PROMPT.split("Mandatory Disclaimer")[1])
    return "\n".join(parts)


def build_research_prompt(research_question: str) -> str:
    """Build a prompt for legal research assistance."""
    parts = [SYSTEM_PROMPT]
    parts.append(f"\n## Legal Research Question:\n{research_question}")
    parts.append("\n## Research Instructions:")
    parts.append("1. Provide relevant case law citations")
    parts.append("2. Summarize key holdings and reasoning")
    parts.append("3. Identify procedural rules and statutes")
    parts.append("4. Suggest related research areas")
    parts.append("5. Recommend primary sources for further research")
    parts.append("\nNote: This research requires attorney interpretation and verification.")
    parts.append("Always verify citations in primary sources before use.")
    return "\n".join(parts)
