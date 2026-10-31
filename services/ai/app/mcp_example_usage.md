# MCP Example Usage Scenarios

This document shows practical examples of how Claude (or another AI assistant) would interact with CaseWise through the MCP server.

---

## Scenario 1: New Case Intake

**Lawyer**: I just met with a new client, Sarah Johnson. She's being sued by her landlord for unpaid rent. Can you create a case for this?

**Claude**: I'll create a case for Sarah Johnson. Let me gather some details first.

[Claude asks follow-up questions using the "case-intake" prompt]

**Claude**: What's Sarah's client ID in your system?

**Lawyer**: It's `550e8400-e29b-41d4-a716-446655440001`

**Claude**: Got it. Creating the case now.

```
[Calls: create_case(
  title="Sarah Johnson v. Landlord - Unpaid Rent Dispute",
  client_id="550e8400-e29b-41d4-a716-446655440001",
  case_type="Civil",
  description="Client is being sued by landlord for allegedly unpaid rent. Claims rent was paid in full.",
  priority="MEDIUM"
)]
```

**Claude**: ✓ Case created successfully!

- **Case ID**: `def-789-ghi-012`
- **Title**: Sarah Johnson v. Landlord - Unpaid Rent Dispute
- **Status**: ACTIVE
- **Created**: 2026-10-31

Would you like me to add the initial timeline events or schedule an intake meeting?

---

## Scenario 2: Document Q&A

**Lawyer**: I need to review the Smith contract case. What are the termination clauses?

**Claude**: Let me search the case documents.

```
[Calls: ask_case_question(
  case_id="abc-123-def-456",
  question="What are the termination clauses in the contract?"
)]
```

**Claude**: Based on the contract documents, there are three termination clauses:

**1. Termination for Convenience (Section 8.1)**
Either party may terminate with 30 days written notice. No penalties apply if notice period is respected.

**2. Termination for Cause (Section 8.2)**
Immediate termination allowed if:
- Material breach not cured within 15 days
- Bankruptcy or insolvency
- Violation of confidentiality provisions

**3. Force Majeure Termination (Section 8.3)**
If force majeure event prevents performance for more than 90 consecutive days, either party may terminate without penalty.

**Sources**:
- `Smith_Contract_Final.pdf`, pages 12-13
- `Amendment_2023.pdf`, page 3 (modified Section 8.2)

Would you like me to add these to the case claims or create a summary document?

---

## Scenario 3: Hearing Preparation

**Lawyer**: I have a hearing tomorrow in the Johnson case. Help me prepare.

**Claude**: I'll help you prepare for tomorrow's hearing. Let me review the case.

```
[Calls: get_case_details("def-789-ghi-012")]
[Calls: get_timeline("def-789-ghi-012")]
[Calls: get_claims("def-789-ghi-012")]
[Calls: get_evidence_list("def-789-ghi-012")]
```

**Claude**: Here's your hearing preparation checklist for **Sarah Johnson v. Landlord**:

### 📋 Hearing Overview
- **Date**: Tomorrow, November 1, 2026
- **Time**: 9:00 AM
- **Court**: Superior Court, Room 305
- **Type**: Motion to Dismiss Hearing

### 🎯 Key Points to Emphasize

1. **Payment Documentation** (Evidence #2)
   - Bank statements showing rent payments
   - 15 consecutive months of on-time payments
   - Highlight payment dated June 5th (the disputed month)

2. **Landlord's Accounting Error**
   - Their records show payment posted to wrong unit
   - Our letter dated June 15th (Evidence #5) notified them
   - No response received for 45 days

3. **Good Faith Efforts**
   - Timeline shows 4 attempts to resolve
   - Certified letters sent (Evidence #7, #8)
   - Client willing to pay late fees if genuinely owed

### 📄 Documents to Bring

✓ Original lease agreement  
✓ Bank statements (June-July 2026)  
✓ Certified mail receipts  
✓ Landlord correspondence (all 8 emails)  
✓ Payment ledger from property management  

### ⚠️ Anticipated Questions

**From Opposing Counsel:**
1. "Why didn't your client respond to the eviction notice?"
   - **Answer**: She did, via certified mail on June 15th (Evidence #7)

2. "Where's proof the June payment was for this unit?"
   - **Answer**: Bank memo field shows "Apt 302 - June Rent"

3. "Why wait until court to resolve this?"
   - **Answer**: Multiple resolution attempts ignored (show timeline)

### 🔍 Weaknesses to Address

- Minor: One payment in March was 2 days late (unrelated)
  - **Mitigation**: That payment included late fee, landlord accepted it

### 📝 Suggested Opening

"Your Honor, this case arises from a simple accounting error. My client has been a model tenant for 15 months, with documented proof of every rent payment including the disputed June payment. The landlord posted the payment to the wrong unit and ignored multiple attempts to correct the mistake."

### ✅ Next Steps After Hearing

If motion granted:
- [ ] Request attorney fees (supported by Section 12 of lease)
- [ ] Get written confirmation no balance owed

If motion denied:
- [ ] File answer to complaint
- [ ] Request discovery on landlord's accounting system
- [ ] Explore settlement (offer 1 month penalty maximum)

---

**Claude**: Would you like me to add any tasks or schedule a follow-up based on the hearing outcome?

---

## Scenario 4: Multi-Case Management

**Lawyer**: What are my upcoming hearings this month?

**Claude**: Let me check your schedule.

```
[Calls: get_upcoming_hearings(
  user_id="your-user-id",
  days_ahead=30
)]
```

**Claude**: You have **5 hearings** in the next 30 days:

### 🚨 This Week

**1. Tomorrow - November 1, 2026 at 9:00 AM**
- **Case**: Sarah Johnson v. Landlord
- **Court**: Superior Court, Room 305
- **Type**: Motion to Dismiss
- **Status**: ⚠️ Needs prep (use hearing-prep?)

**2. November 3, 2026 at 2:00 PM**
- **Case**: Smith Contract Dispute
- **Court**: District Court, Room 12
- **Type**: Case Management Conference
- **Status**: ✓ Ready

### 📅 Next Week

**3. November 8, 2026 at 10:00 AM**
- **Case**: Martinez Personal Injury
- **Court**: Superior Court, Room 201
- **Type**: Settlement Conference
- **Status**: ⏳ Waiting on medical records

**4. November 10, 2026 at 11:30 AM**
- **Case**: Tech Startup v. Former Employee
- **Court**: District Court, Room 8
- **Type**: Preliminary Injunction Hearing
- **Status**: ✓ Ready

### 📆 Later This Month

**5. November 28, 2026 at 9:00 AM**
- **Case**: Estate of Wilson
- **Court**: Probate Court, Room 403
- **Type**: Inventory Hearing
- **Status**: ⚠️ Needs prep

---

**Claude**: Would you like me to:
1. Prepare hearing checklists for any of these?
2. Add reminders/tasks for the ones marked "Needs prep"?
3. Search for missing documents in any case?

---

## Scenario 5: Adding Evidence in Bulk

**Lawyer**: I just scanned 8 documents for the Wilson estate case. Can you add them as evidence?

1. Death certificate
2. Will (original, 2020)
3. Will (amended, 2023)
4. Bank statements - Chase checking
5. Bank statements - Wells Fargo savings
6. Property deed for 123 Main St
7. Vehicle title (2019 Honda)
8. Life insurance policy

**Claude**: I'll add all 8 documents as evidence to the Estate of Wilson case.

```
[Calls: add_evidence(case_id="estate-001", name="Death Certificate", evidence_type="Document", description="Official death certificate")]
[Calls: add_evidence(case_id="estate-001", name="Last Will and Testament (2020)", evidence_type="Document", description="Original will dated March 2020")]
[Calls: add_evidence(case_id="estate-001", name="Amended Will (2023)", evidence_type="Document", description="Amended will dated June 2023, supersedes 2020 version")]
[Calls: add_evidence(case_id="estate-001", name="Chase Bank Statements", evidence_type="Document", description="Checking account ending in 4892")]
[Calls: add_evidence(case_id="estate-001", name="Wells Fargo Bank Statements", evidence_type="Document", description="Savings account ending in 7321")]
[Calls: add_evidence(case_id="estate-001", name="Property Deed - 123 Main St", evidence_type="Document", description="Deed for primary residence")]
[Calls: add_evidence(case_id="estate-001", name="Vehicle Title - 2019 Honda", evidence_type="Document", description="Title for 2019 Honda Accord")]
[Calls: add_evidence(case_id="estate-001", name="Life Insurance Policy", evidence_type="Document", description="MetLife policy #123456")]
```

**Claude**: ✓ Successfully added all 8 evidence items to Estate of Wilson case.

**Summary of assets documented:**
- Real property: 123 Main St
- Vehicle: 2019 Honda Accord
- Financial accounts: 2 bank accounts
- Life insurance: MetLife policy

**Note**: I see you have two wills (2020 and 2023). The 2023 amended version should supersede the original. Would you like me to:
1. Add a note about which will is controlling?
2. Create a task to verify the 2023 will was properly executed?
3. Compare asset distribution between the two versions?

---

## Scenario 6: Cross-Case Research

**Lawyer**: Have I handled any similar landlord-tenant disputes in the past? I want to see how those turned out.

**Claude**: I'll search your case history for similar cases.

```
[Calls: search_cases_by_keyword(keyword="landlord tenant", user_id="your-user-id")]
[Calls: search_cases_by_keyword(keyword="unpaid rent", user_id="your-user-id")]
[Calls: search_cases_by_keyword(keyword="eviction", user_id="your-user-id")]
```

**Claude**: I found **4 similar landlord-tenant cases** you've handled:

### ✅ Won - Chen v. Property Management LLC (2025)
- **Issue**: Wrongful eviction, security deposit dispute
- **Outcome**: Judgment for client, $8,500 + attorney fees
- **Key Factor**: Landlord failed to provide itemized deductions
- **Timeline**: 4 months from filing to judgment

### ✅ Settled - Rodriguez v. Apartments Inc (2024)
- **Issue**: Habitability claims, unpaid rent counterclaim
- **Outcome**: Rent reduction agreement, repairs made
- **Settlement**: $3,200 rent credit
- **Timeline**: 2 months to settlement

### ✅ Won - Mitchell v. Jones (2024)
- **Issue**: Unlawful detainer, payment application dispute
- **Outcome**: Motion to dismiss granted
- **Key Factor**: Bank records proved payment (similar to Johnson case!)
- **Timeline**: Dismissed at first hearing

### ❌ Lost - Taylor v. Riverside Properties (2023)
- **Issue**: Lease breach, early termination
- **Outcome**: Judgment for landlord
- **Key Factor**: Client moved out without proper notice
- **Timeline**: Summary judgment, 6 weeks

---

**Claude**: The **Mitchell v. Jones** case is very similar to your current Johnson case! Both involved:
- Payment accounting errors
- Bank records as proof
- Motion to dismiss strategy
- **Result: Won at first hearing**

Would you like me to:
1. Pull the key arguments from the Mitchell case?
2. Compare the evidence you had then vs. now?
3. Add a case note citing Mitchell as precedent?

---

## Scenario 7: Timeline Building

**Lawyer**: Help me build a timeline for the Johnson case. Here's what happened:
- Jan 1, 2025: Sarah signed lease
- June 5, 2026: Made June rent payment ($1,200)
- June 10: Landlord claimed payment not received
- June 15: Sarah sent certified letter with bank receipt
- July 1: Landlord filed eviction notice
- July 20: Sarah hired me
- Today: Filing motion to dismiss

**Claude**: I'll create a comprehensive timeline for the Johnson case.

```
[Calls: add_timeline_event(case_id="def-789", event_date="2025-01-01", description="Client signed lease agreement for Apt 302")]
[Calls: add_timeline_event(case_id="def-789", event_date="2026-06-05", description="Client made June rent payment ($1,200) via online banking")]
[Calls: add_timeline_event(case_id="def-789", event_date="2026-06-10", description="Landlord contacted client claiming June payment not received")]
[Calls: add_timeline_event(case_id="def-789", event_date="2026-06-15", description="Client sent certified letter to landlord with bank receipt showing payment")]
[Calls: add_timeline_event(case_id="def-789", event_date="2026-07-01", description="Landlord filed eviction notice citing unpaid rent")]
[Calls: add_timeline_event(case_id="def-789", event_date="2026-07-20", description="Client retained counsel (case intake completed)")]
[Calls: add_timeline_event(case_id="def-789", event_date="2026-10-31", description="Filed Motion to Dismiss eviction action")]
```

**Claude**: ✓ Timeline created with 7 key events spanning 22 months.

**Timeline Summary:**
- **Duration**: January 2025 - October 2026
- **Critical Period**: June 5 - July 1 (dispute escalation)
- **Response Time**: 10 days from payment to landlord claim
- **Resolution Attempt**: 5 days (certified letter)
- **Legal Action**: 16 days from eviction to motion filed

**Notable Gaps:**
- No documented response from landlord after June 15 letter
- 50-day gap between cert. letter and eviction notice

**Suggested additions:**
- Any prior rent payments (establish payment history?)
- Date landlord's property manager changed (if relevant?)
- Date of first court hearing assignment

Should I add any of these?

---

## Scenario 8: End-of-Day Summary

**Lawyer**: Summarize what we accomplished today on all my active cases.

**Claude**: Let me review today's activity across all your cases.

```
[Calls: list_cases(user_id="your-user-id", status="ACTIVE")]
[For each case, calls relevant resources and checks for today's updates]
```

**Claude**: Here's your end-of-day summary for **October 31, 2026**:

### 📊 Today's Activity (5 Active Cases)

**🆕 New Cases Created: 1**
- Sarah Johnson v. Landlord (Unpaid Rent Dispute)
  - Status: ACTIVE, intake completed
  - Next: Hearing tomorrow 9:00 AM

**📄 Documents Processed: 8**
- Estate of Wilson: Added 8 evidence items
- Asset inventory now complete

**⚖️ Motions Filed: 1**
- Johnson case: Motion to Dismiss filed
- Prepared hearing checklist

**📅 Hearings Scheduled: 0**
- (But you have 1 hearing tomorrow!)

**📝 Notes Added: 3**
- Smith case: Payment received
- Martinez case: Still waiting on medical records
- Wilson estate: Two wills on file, 2023 controls

### ⏰ Tomorrow's Action Items

**Urgent:**
- [ ] 9:00 AM: Johnson hearing (Room 305)
- [ ] Bring all documents from checklist

**High Priority:**
- [ ] Follow up on Martinez medical records
- [ ] Review Tech Startup case before Friday hearing

**Normal:**
- [ ] Schedule client meeting for Wilson estate
- [ ] Draft discovery requests in Smith case

### 📈 Case Statistics

- **Total Active Cases**: 5
- **Cases Closing This Month**: 2 (projected)
- **Upcoming Hearings (30 days)**: 5
- **Overdue Tasks**: 1 (Martinez follow-up)

---

**Claude**: You had a productive day! The Johnson case intake and motion filing, plus the Wilson estate evidence compilation, were the major accomplishments.

**Recommendation**: Block 30 minutes tomorrow morning before the 9 AM hearing to review the prep checklist one more time.

Good luck tomorrow! 🎯

---

## Summary: MCP Makes Legal Work Conversational

Instead of clicking through forms and tabs, you just **talk to Claude** about your cases:

- "What hearings do I have?"
- "Add a note about..."
- "Search for similar cases"
- "Prepare me for tomorrow's hearing"
- "What did I accomplish today?"

**The MCP server handles the database operations behind the scenes, making legal case management as natural as talking to a paralegal!**
