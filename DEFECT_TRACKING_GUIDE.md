# 🐛 Defect Tracking & Bug Management
## Tourism Recommendation System | QA Team Documentation

---

## Defect Tracking System Overview

### Purpose
Centralized system for recording, tracking, and managing all discovered defects throughout the testing lifecycle.

### Defect Lifecycle

```
1. REPORTED
   │
   ├─→ NEW (Awaiting triaging)
   │
   ├─→ CONFIRMED (QA verified reproducible)
   │    │
   │    ├─→ ASSIGNED (Assigned to developer)
   │    │    │
   │    │    ├─→ IN PROGRESS (Developer working on fix)
   │    │    │    │
   │    │    │    └─→ READY FOR TESTING (Fix submitted)
   │    │    │         │
   │    │    │         ├─→ VERIFIED FIXED (QA tested, passes)
   │    │    │         │    │
   │    │    │         │    └─→ CLOSED (Defect resolved)
   │    │    │         │
   │    │    │         └─→ REOPENED (QA found issue still exists)
   │    │    │              │
   │    │    │              └─→ ASSIGNED (Back to developer)
   │    │
   │    └─→ DUPLICATE (Same as existing defect)
   │         │
   │         └─→ CLOSED (Marked as duplicate)
   │
   └─→ DEFERRED (Postponed to future release)
        │
        └─→ CLOSED (Not fixed in current release)
```

---

## Defect Report Template

### Standard Defect Report Format

```
═══════════════════════════════════════════════════════════════════
DEFECT REPORT
═══════════════════════════════════════════════════════════════════

DEFECT ID:        DEF-XXX
TITLE:            [Clear, concise defect title]
CREATED DATE:     [Date]
CREATED BY:       [QA Engineer Name]
PRODUCT:          Wanderlust Tourism API
VERSION:          [Version number]

───────────────────────────────────────────────────────────────────
SEVERITY Level:   [CRITICAL / HIGH / MEDIUM / LOW]
PRIORITY:         [P1 / P2 / P3 / P4]
STATUS:           [NEW / CONFIRMED / ASSIGNED / IN PROGRESS / etc]
ASSIGNED TO:      [Developer Name or Unassigned]
─────────────────────────────────────────────────────────────────

CATEGORY:
  ☐ Functional
  ☐ Performance
  ☐ Security
  ☐ UI/UX
  ☐ Database
  ☐ API
  ☐ Integration
  ☐ Documentation

AFFECTED COMPONENT:
  ☐ Authentication
  ☐ Destinations
  ☐ Tour Packages
  ☐ Search
  ☐ Booking
  ☐ Reviews
  ☐ Database
  ☐ Cache/Redis

───────────────────────────────────────────────────────────────────
ENVIRONMENT DETAILS:
───────────────────────────────────────────────────────────────────

Operating System:     [Windows 10 / macOS / Linux]
Browser:              [Chrome 120 / Firefox / Safari]
Django Version:       [5.2]
Database:             [PostgreSQL 15 / SQLite]
Environment:          [Development / Staging / Production]
Test Data Set:        [Default / Custom]

───────────────────────────────────────────────────────────────────
ISSUE DESCRIPTION:
───────────────────────────────────────────────────────────────────

[Detailed description of what is wrong]

Example:
"When booking a tour package with 0 participants, the system 
should validate and reject the request with an error message. 
Instead, the booking is created successfully with negative 
participant count in the database."

───────────────────────────────────────────────────────────────────
TEST CASE LINK:
───────────────────────────────────────────────────────────────────

Related Test Case:    TC-041
Test Category:        Booking System
Last Test Run:        2026-04-01 10:30:00 UTC

───────────────────────────────────────────────────────────────────
PRECONDITIONS:
───────────────────────────────────────────────────────────────────

1. [Precondition 1]
2. [Precondition 2]
3. [Precondition 3]

Example:
1. User is logged in to the application
2. Tour package "Paris City Tour" exists with max capacity of 20
3. User navigates to booking form

───────────────────────────────────────────────────────────────────
STEPS TO REPRODUCE:
───────────────────────────────────────────────────────────────────

1. Navigate to /packages/1/
2. Click "Book Now" button
3. Enter booking details:
   - Name: John Doe
   - Email: john@example.com
   - Phone: +1234567890
   - Participants: 0
   - Date: 2026-05-15
4. Click "Submit Booking"
5. Observe result

───────────────────────────────────────────────────────────────────
EXPECTED BEHAVIOR:
───────────────────────────────────────────────────────────────────

✓ Form validation occurs before submission
✓ Error message displays: "Number of participants must be at least 1"
✓ Booking is NOT created
✓ Form remains visible for correction
✓ HTTP Status: 400 Bad Request (if API endpoint)

───────────────────────────────────────────────────────────────────
ACTUAL BEHAVIOR:
───────────────────────────────────────────────────────────────────

✗ Form validation is bypassed
✗ Booking created with participant count = 0
✗ Database record shows negative/zero participants
✗ Confirmation page displays
✗ HTTP Status: 201 Created

───────────────────────────────────────────────────────────────────
IMPACT ANALYSIS:
───────────────────────────────────────────────────────────────────

Frequency:        Every time 0 is entered as participants
Scope:            Booking API endpoint
Business Impact:  Invalid bookings in system, revenue calculation affected
Data Integrity:   Database contains invalid participant data
User Impact:      Users might not notice booking is invalid
System Load:      None

───────────────────────────────────────────────────────────────────
ATTACHMENTS:
───────────────────────────────────────────────────────────────────

📷 Screenshot 1:   booking_form_with_zero.png
📹 Screen Video:   bug_reproduction_video.mp4
📊 Error Log:      error_log_2026-04-01.txt
📄 Raw Request:    api_request_payload.json

[Include screenshots, videos, error logs, API requests]

───────────────────────────────────────────────────────────────────
BUG ANALYSIS:
───────────────────────────────────────────────────────────────────

Root Cause:
  The validation check in the booking form is missing or 
  improperly implemented. The `number_of_participants` field 
  validation is not enforcing minimum value of 1.

Code Location:
  travel/forms.py - BookingForm.clean_number_of_participants()
  OR
  travel/views.py - book_package() function

Potential Causes:
  1. Missing min_value constraint on form field
  2. validation() method not called
  3. Validation error not being raised
  4. Client-side validation only (no server-side)

───────────────────────────────────────────────────────────────────
SUGGESTED SOLUTION:
───────────────────────────────────────────────────────────────────

Code Fix (travel/forms.py):
```python
class BookingForm(forms.ModelForm):
    number_of_participants = forms.IntegerField(
        min_value=1,
        error_messages={'min_value': 'At least 1 participant required'}
    )
```

OR (travel/views.py):
```python
if form.cleaned_data['number_of_participants'] < 1:
    messages.error(request, "At least 1 participant required")
    return render(request, 'booking.html', {'form': form})
```

───────────────────────────────────────────────────────────────────
WORKAROUND FOR QA TEAM:
───────────────────────────────────────────────────────────────────

Until this bug is fixed, QA should:
1. Test only with participant count ≥ 1
2. Skip TC-039 (Zero Participants test)
3. Log any discovered instances in production
4. Manually validate test bookings have valid counts

───────────────────────────────────────────────────────────────────
DEPENDENCIES / BLOCKED ITEMS:
───────────────────────────────────────────────────────────────────

⚠️ This defect blocks:
   - TC-041 (Booking Capacity Limits)
   - TC-045 (Total Price Calculation)
   - Release v1.0.0 sign-off

⚠️ Depends on:
   - Database schema understanding
   - Form validation framework knowledge

───────────────────────────────────────────────────────────────────
COMMENTS & DISCUSSION:
───────────────────────────────────────────────────────────────────

[2026-04-01 10:45 AM] QA Engineer 4:
  Confirmed issue is reproducible. Tested on both API and web UI.
  Affects all booking submissions with 0 participants.

[2026-04-01 2:30 PM] Developer Sarah:
  Found the issue. Form validation missing min_value constraint.
  Submitting fix to feature branch.

[2026-04-02 9:15 AM] QA Engineer 4:
  Tested fix in build v1.0.1-RC2. Bug is resolved. Closing defect.

───────────────────────────────────────────────────────────────────
RESOLUTION INFORMATION:
───────────────────────────────────────────────────────────────────

Status:           CLOSED
Resolution Type:  FIXED
Fixed in Build:   v1.0.1-RC2
Fixed By:         Developer Sarah
Fixed Date:       2026-04-02
Verified By:      QA Engineer 4
Verification Date: 2026-04-02

───────────────────────────────────────────────────────────────────
```

---

## Defect Severity Levels

### Critical (P1)
**Impact**: System unusable, data loss, security breach
**Response Time**: IMMEDIATE (within 1 hour)
**Examples**:
- Login fails for all users
- Data corruption in database
- SQL injection vulnerability
- Complete feature unavailable

**Action**: 
- Drop all other testing
- Notify management immediately
- Create fix within 4 hours

---

### High (P2)
**Impact**: Major functionality broken or severely impaired
**Response Time**: URGENT (within 4 hours)
**Examples**:
- Booking can't be submitted
- Search returns wrong results
- Payment processing fails
- Performance < 50% of baseline

**Action**:
- Assign to senior developer
- Target fix within 24 hours
- Block release if not fixed

---

### Medium (P3)
**Impact**: Feature works with workaround, moderate impact
**Response Time**: NORMAL (within 24 hours)
**Examples**:
- Filter button requires refresh
- Typo in error message
- Pagination off by 1 result
- Performance acceptable but slow

**Action**:
- Assign to available developer
- Can be scheduled for next sprint
- Can be deferred to next release

---

### Low (P4)
**Impact**: Cosmetic issue or minor inconvenience
**Response Time**: BACKLOG (no deadline)
**Examples**:
- UI label misspelling
- Unnecessary console warning
- Non-critical log message
- Enhancement suggestion

**Action**:
- Add to backlog
- Can be fixed in future release
- May be closed as "won't fix"

---

## Current Defects List

### Open Defects Summary

| ID | Title | Severity | Status | Assigned | Test |
|---|---|---|---|---|---|
| DEF-001 | Duplicate username allowed in registration | HIGH | ASSIGNED | Dev Sarah | TC-003 |
| DEF-002 | Package recommendations returning null | MEDIUM | IN PROGRESS | Dev John | TC-022 |
| DEF-003 | Booking exceeds capacity limit | CRITICAL | ASSIGNED | Dev Mike | TC-041 |
| DEF-004 | Total price calculation incorrect | CRITICAL | ASSIGNED | Dev Sarah | TC-045 |
| DEF-005 | Concurrent booking limits not enforced | CRITICAL | NEW | Unassigned | TC-050 |
| DEF-006 | Duplicate review submission allowed | HIGH | BLOCKED | Dev John | TC-059 |
| DEF-007 | Pagination performance degraded with 250+ items | HIGH | IN PROGRESS | Dev Mike | TC-062 |
| DEF-008 | Server timeout with 10 concurrent users | CRITICAL | IN PROGRESS | Devops Team | TC-064 |
| DEF-009 | N+1 query performance issue | HIGH | ASSIGNED | Dev Sarah | TC-066 |
| DEF-010 | Timeout error handling incomplete | MEDIUM | NEW | Unassigned | TC-069 |

### Defect Metrics

```
Total Defects Reported:     10
Total Open Defects:         10
Total Closed Defects:       0

By Severity:
  Critical:  5 (50%)
  High:      3 (30%)
  Medium:    2 (20%)
  Low:       0 (0%)

By Status:
  NEW:               2
  ASSIGNED:          4
  IN PROGRESS:       3
  READY FOR TEST:    0
  VERIFIED FIXED:    0
  REOPENED:          0
  CLOSED:            0
  DEFERRED:          1

Average Time to Fix:       [Pending first fixes]
Average Time to Verify:    [Pending first fixes]
Escape Rate:               10 defects per sprint
```

---

## Defect Resolution Process

### Step 1: Report Defect
- QA discovers issue during testing
- QA Engineer documents using this template
- QA Lead reviews report for completeness
- Issue assigned DEF-ID

### Step 2: Triage
- QA Lead confirms issue reproducibility
- Severity and priority assigned
- Acceptance criteria defined
- Issue marked as CONFIRMED

### Step 3: Assignment
- Development manager assigns to developer
- Developer reviews and estimates effort
- Dependencies identified
- Issue moved to IN PROGRESS

### Step 4: Development
- Developer creates fix in feature branch
- Code review conducted
- Fix submitted to staging environment
- Issue moved to READY FOR TESTING

### Step 5: QA Verification
- QA tests fix using original reproduction steps
- All related test cases re-executed
- Regression testing performed
- Issue marked VERIFIED FIXED or REOPENED

### Step 6: Closure
- Fix deployed to production (if applicable)
- Monitoring for regression
- Issue marked CLOSED
- Metrics updated

---

## Defect Reporting Best Practices for QA Team

### DO ✅
- ✅ Use clear, specific titles
- ✅ Include exact reproduction steps
- ✅ Document expected vs actual behavior
- ✅ Attach supporting evidence (screenshots, logs)
- ✅ Include environment details
- ✅ Link related test cases
- ✅ Be objective and professional
- ✅ Suggest root cause if obvious
- ✅ Update status as process progresses
- ✅ Document workarounds for blocking issues

### DON'T ❌
- ❌ Use vague descriptions ("System broken")
- ❌ Report issues without steps to reproduce
- ❌ Use emotional language ("This is terrible")
- ❌ Include suggestions as facts ("It must be X")
- ❌ Report without testing environment info
- ❌ Duplicate existing defect reports
- ❌ Leave defects stale without updates
- ❌ Assign without developer's acknowledgment
- ❌ Close defect without verification
- ❌ Include unrelated issues in one report

---

## Integration with Test Management

### Linking Defects to Test Cases

```
Test Case TC-041 ────→ Failed
   │
   └──→ Creates ──→ Defect DEF-003
                    (Booking exceeds capacity)
                    │
                    ├──→ Status: ASSIGNED
                    ├──→ Severity: CRITICAL
                    └──→ Back to Dev
                          │
                          └──→ After Fix ──→ Re-run TC-041
                                            │
                                            ├──→ Pass ──→ Close DEF-003
                                            │
                                            └──→ Fail ──→ Reopen DEF-003
```

---

## Monthly Defect Analysis Report

### Template
```
DEFECT ANALYSIS REPORT
Month: April 2026
Reporting Period: April 1-30, 2026

METRICS:
- Total Defects Reported: 15
- Critical Defects: 5
- High Priority: 4
- Medium Priority: 4
- Low Priority: 2

TREND ANALYSIS:
- Week 1: 3 defects (Learning phase)
- Week 2: 4 defects (Initial testing)
- Week 3: 5 defects (Functional testing)
- Week 4: 3 defects (Regression testing)

TOP ISSUES:
1. Input Validation (40%) - 6 defects
2. Performance (27%) - 4 defects
3. UI/UX (13%) - 2 defects
4. Database (13%) - 2 defects
5. API (7%) - 1 defect

ROOT CAUSES:
- Missing validation: 6 (40%)
- Query optimization: 4 (27%)
- UI framework issue: 2 (13%)
- Design oversight: 2 (13%)
- API specification: 1 (7%)

RECOMMENDATIONS:
1. Implement server-side validation for all inputs
2. Add query optimization to sprint planning
3. Increase code review focus on input handling
4. Setup performance baseline testing
5. Add API contract testing to CI/CD
```

---

## Appendix: Defect ID Numbering Scheme

```
DEF-XXX

DEF = Defect ID prefix
XXX = Sequential number (001, 002, 003...)

Example: DEF-001, DEF-002, ..., DEF-999

Reset annually:
- 2026: DEF-001 to DEF-999
- 2027: DEF-001 to DEF-999 (restart numbering)
```

---

**Document Version**: 1.0  
**Last Updated**: March 30, 2026  
**Next Review**: April 30, 2026  
**Owner**: QA Lead
