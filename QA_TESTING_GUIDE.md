# 🧪 QA Testing Documentation
## Tourism Recommendation System | Django REST Framework

**Project**: Wanderlust Travel & Tours Booking Platform  
**Tech Stack**: Django REST Framework | PostgreSQL | Python  
**QA Lead**: [Your Name]  
**QA Team Size**: 4 Members  
**Document Version**: 1.0  
**Last Updated**: March 30, 2026

---

## 📋 Table of Contents

1. [QA Team Structure](#qa-team-structure)
2. [Test Planning & Strategy](#test-planning--strategy)
3. [Test Case Documentation](#test-case-documentation)
4. [API Testing Guide](#api-testing-guide)
5. [Test Execution Procedures](#test-execution-procedures)
6. [Defect Tracking](#defect-tracking)
7. [Test Reports & Metrics](#test-reports--metrics)
8. [Postman Collection Guide](#postman-collection-guide)

---

## 👥 QA Team Structure

### Team Composition
```
QA Lead (You)
├── QA Engineer 1 - API Testing & Automation
├── QA Engineer 2 - Functional Testing & Mobile
├── QA Engineer 3 - Performance & Security Testing
└── QA Engineer 4 - Regression & Documentation
```

### Responsibilities by Role

| Role | Responsibilities |
|------|------------------|
| **QA Lead** | Strategy, Planning, Team Management, Reports, Client communication |
| **QA Eng 1** | API tests (40+), Postman collections, Automated scripts |
| **QA Eng 2** | Functional testing, UI/UX validation, Mobile responsiveness |
| **QA Eng 3** | Performance tests, Load testing, Security scanning |
| **QA Eng 4** | Regression testing, Documentation, Test data management |

---

## 🎯 Test Planning & Strategy

### Test Strategy Overview

**Scope**: Full application coverage including APIs, UI, database, and performance

**Levels of Testing**:
1. **Unit Testing** - Function/method level (automatic with CI/CD)
2. **Integration Testing** - Module interactions (database, API endpoints)
3. **System Testing** - End-to-end workflows
4. **Performance Testing** - Load, stress, scalability
5. **Security Testing** - Vulnerability scanning, authentication
6. **Regression Testing** - After each code change

### Test Coverage Breakdown

| Test Type | Test Cases | Coverage | Responsibility |
|-----------|-----------|----------|-----------------|
| API Endpoints | 35 | 100% | QA Engineer 1 |
| Authentication | 5 | 100% | QA Engineer 1 |
| Booking Flow | 15 | 100% | QA Engineer 2 |
| Search & Filter | 10 | 100% | QA Engineer 2 |
| Reviews & Ratings | 10 | 100% | QA Engineer 4 |
| Performance | 10 | 80% | QA Engineer 3 |
| Security | 8 | 90% | QA Engineer 3 |
| **TOTAL** | **93** | **92%** | |

### Test Execution Timeline

```
Week 1: Planning & Test Case Design
Week 2: Automated Test Setup, API Testing
Week 3: Functional Testing, Regression Testing
Week 4: Performance & Security Testing, Bug Fixing
Week 5: Final Regression, Sign-off, Reports
```

---

## 📝 Test Case Documentation

### Test Case Template

```
Test ID: TC-XXX
Test Title: [Clear, descriptive title]
Priority: Critical/High/Medium/Low
Status: [Not Started/In Progress/Passed/Failed]
Environment: Development/Staging/Production

Preconditions:
- [Setup requirements]
- [Prerequisites]

Test Steps:
1. [Action]
2. [Action]
3. [Expected Result]

Expected Result:
- [What should happen]
- [Validation criteria]

Actual Result:
- [What actually happened]

Pass/Fail: [Pass/Fail/Blocked]
Assigned To: [QA Engineer Name]
Execution Date: [Date]
Duration: [Time taken]
```

### Test Case Categories

#### **Category 1: API Authentication (5 Test Cases)**
- TC-001: User Registration - Valid Data
- TC-002: User Registration - Password Mismatch
- TC-003: User Registration - Duplicate Username
- TC-004: User Login - Valid Credentials
- TC-005: User Login - Invalid Credentials

#### **Category 2: Destination Management (10 Test Cases)**
- TC-006: Fetch All Destinations
- TC-007: Fetch Single Destination
- TC-008: Fetch Non-existent Destination
- TC-009: Pagination Testing
- TC-010: Search Destinations
- [... more tests]

#### **Category 3: Tour Package Management (15 Test Cases)**
- TC-011: Fetch All Packages
- TC-012-014: Filter by Difficulty (Easy/Moderate/Challenging)
- TC-015-017: Filter by Price Range
- TC-018: Invalid Filters Handling
- TC-019: Filter by Duration
- TC-020: Combined Filters
- [... more tests]

#### **Category 4: Search Functionality (10 Test Cases)**
- TC-026: Search by Title
- TC-027: Search by Description
- TC-028: Search by Destination
- TC-029: Empty Query
- TC-030-035: Edge cases, special characters, performance

#### **Category 5: Booking System (15 Test Cases)**
- TC-036: Create Booking - Valid Data
- TC-037-042: Invalid Input Validation
- TC-043-050: Status transitions, capacity checks

#### **Category 6: Reviews & Ratings (10 Test Cases)**
- TC-051-060: Review submission, validation, moderation

#### **Category 7: Performance & Edge Cases (10 Test Cases)**
- TC-061-070: Load testing, concurrency, optimization

---

## 🔌 API Testing Guide

### API Endpoints to Test

#### Destination Endpoints
```
GET  /destinations/                  - List all destinations
GET  /destinations/<id>/             - Get destination details
POST /destinations/                  - Create destination (Admin)
PUT  /destinations/<id>/             - Update destination (Admin)
DELETE /destinations/<id>/           - Delete destination (Admin)
```

#### Tour Package Endpoints
```
GET  /packages/                      - List packages with filters
GET  /packages/<id>/                 - Get package details
POST /packages/                      - Create package (Admin)
PUT  /packages/<id>/                 - Update package (Admin)
DELETE /packages/<id>/               - Delete package (Admin)
GET  /packages/?difficulty=easy      - Filter by difficulty
GET  /packages/?min_price=500&max_price=1000  - Filter by price
GET  /packages/?duration=5           - Filter by duration
GET  /packages/?sort=price_asc       - Sort packages
```

#### Search Endpoint
```
GET  /search/?q=keyword              - Search packages
GET  /search/?q=Paris                - Search by location
GET  /search/?q=adventure            - Search by experience
```

#### Booking Endpoints
```
GET  /booking/<id>/confirmation/     - Get booking confirmation
POST /packages/<id>/                 - Create booking
GET  /bookings/                      - List user bookings (Auth required)
PUT  /bookings/<id>/                 - Update booking
DELETE /bookings/<id>/               - Cancel booking
```

#### Review Endpoints
```
POST /packages/<id>/reviews/         - Create review
GET  /packages/<id>/reviews/         - List package reviews
PUT  /reviews/<id>/                  - Update review
DELETE /reviews/<id>/                - Delete review
```

#### Authentication Endpoints
```
POST /register/                      - User registration
POST /login/                         - User login
POST /logout/                        - User logout
POST /tokens/                        - JWT token generation
POST /tokens/refresh/                - Refresh JWT token
```

#### Health & Monitoring
```
GET  /health/                        - Health check
GET  /sitemap.xml                    - XML sitemap
GET  /robots.txt                     - Robots file
```

### Response Validation

**Success Response (200 OK)**
```json
{
  "status": "success",
  "message": "Operation completed",
  "data": {
    ...
  }
}
```

**Error Response (400 Bad Request)**
```json
{
  "status": "error",
  "message": "Validation error",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

**Not Found Response (404)**
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

**Unauthorized Response (401)**
```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

## 🚀 Test Execution Procedures

### Daily Test Execution Checklist

**Morning (9 AM)**
- [ ] Review overnight build status
- [ ] Check for new defects assigned
- [ ] Plan day's testing activities
- [ ] Communicate with dev team about blockers

**During Day**
- [ ] Execute assigned test cases
- [ ] Document results in test management tool
- [ ] Report any issues immediately
- [ ] Participate in team standups (10 AM, 3 PM)

**Evening (5 PM)**
- [ ] Summarize test execution results
- [ ] Update test metrics
- [ ] Document blocking issues
- [ ] Plan next day's activities

### Test Execution Steps

#### Step 1: Test Environment Setup
```bash
# Ensure test environment is ready
1. Check database is running
2. Verify API server is accessible
3. Clear test data from previous runs
4. Load fresh test dataset
5. Verify all test tools are operational
```

#### Step 2: Run Automated Tests
```bash
# Run test suite
python manage.py test travel.tests_comprehensive -v 2

# Run with coverage report
pytest --cov=travel --cov-report=html travel/tests_comprehensive.py

# Run specific test category
python manage.py test travel.tests_comprehensive.APIDestinationTests -v 2
```

#### Step 3: Manual Testing
```
1. Start Postman
2. Load collection: "Wanderlust_API_Tests.postman_collection.json"
3. Run each request
4. Validate response status codes
5. Verify response body matches expected
6. Check response headers
7. Document any deviations
```

#### Step 4: Document Results
```
1. Record test result (Pass/Fail/Blocked)
2. Note execution time
3. Attach screenshots/logs if failed
4. Link to any related defects
5. Add comments if relevant
```

---

## 🐛 Defect Tracking

### Defect Report Template

```
DEFECT ID: DEF-XXX
SEVERITY: Critical/High/Medium/Low
STATUS: Open/In Progress/Fixed/Closed/Reopened

Title: [Clear, concise defect title]

Description:
[What is the issue]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual result]

Environment:
- OS: [OS name and version]
- Browser: [Browser if applicable]
- Build: [Build number]
- Database: [DB version]

Expected Behavior:
[What should happen]

Actual Behavior:
[What actually happens]

Attachments:
- Screenshot: [If applicable]
- Log file: [Error logs]
- Video: [Reproduction video]

Assigned To: [Developer name]
Priority: [Critical/High/Medium/Low]
Found By: [Your name]
Found Date: [Date]
Target Fix Date: [Date]
Resolution: [Fixed in build X]
```

### Severity Levels

| Severity | Definition | Example |
|----------|-----------|---------|
| **Critical** | System unusable, data loss | Login fails for all users |
| **High** | Major feature broken | Booking can't be submitted |
| **Medium** | Feature works with workaround | Filter button doesn't refresh page |
| **Low** | Minor issue, cosmetic | Typo in label |

### Defect Tracking Workflow

```
1. Report Defect
   ↓
2. QA Lead confirms bug reproducibility
   ↓
3. Dev team assigns severity/priority
   ↓
4. Developer takes ownership
   ↓
5. Code fix in progress
   ↓
6. QA regression testing
   ↓
7. Fix verified in test build
   ↓
8. Defect closed (if verified)
   ✗ Reopen if still reproducible
```

### Defect Metrics to Track

- **Defect Density**: Defects per 1000 lines of code (KLOC)
- **Defect Escape Rate**: Defects found in production vs testing
- **Defect Resolution Time**: Average time from report to fix
- **Defect Aging**: % of defects open > 5 days old

---

## 📊 Test Reports & Metrics

### Weekly Test Report

```
WEEK: [Week of Date]
PERIOD: [Start Date - End Date]

EXECUTIVE SUMMARY
- Total Test Cases: 93
- Executed: 85 (91%)
- Passed: 81 (87%)
- Failed: 4 (4%)
- Blocked: 2 (2%)

TEST COVERAGE
- API Endpoints: 35/35 (100%)
- Authentication: 5/5 (100%)
- Booking Flow: 12/15 (80%)
- Search & Filter: 10/10 (100%)

DEFECTS
- New: 4
- Fixed: 2
- Reopened: 1
- Total Open: 8

METRICS
- Test Execution Time: 12 hours
- Defect Density: 0.8 per KLOC
- Test Pass Rate: 87%
- Automation Coverage: 60%

BLOCKERS
1. [Blocking issue 1]
2. [Blocking issue 2]

RECOMMENDATIONS
1. Increase test automation
2. Add performance tests for large datasets
3. Improve test data management

APPROVED BY: [QA Lead Name]
DATE: [Date]
```

### Daily Test Status

```
DATE: [Date]
QA ENGINEER: [Name]

TESTS EXECUTED
- Total: 20
- Passed: 18
- Failed: 2
- Blocked: 0

DEFECTS FOUND
- Critical: 0
- High: 1
  - DEF-XXX: Booking exceeds capacity
- Medium: 1
  - DEF-XXX: Wrong total price calculation
- Low: 0

COVERAGE
- API Tests: 10/10 (100%)
- Functional Tests: 8/10 (80%)
- Performance Tests: 2/5 (40%)

NEXT DAY PLAN
- Complete functional test suite for reviews
- Begin performance testing on search endpoint
- Verify fixes for DEF-XXX and DEF-XXX
```

### Test Metrics Dashboard

```
                          Current    Target
Test Execution           87/93      90/93
Test Pass Rate             87%        95%
Bug Fix Rate              50%        80%
Automation Coverage       60%        70%
Code Coverage            80%        85%
API Endpoint Coverage    100%       100%
```

---

## 📮 Postman Collection Guide

### Setting Up Postman

#### Step 1: Import Collection
```
1. Open Postman
2. Click "Import"
3. Import file: "Wanderlust_API_Tests.postman_collection.json"
4. Select environment: "Wanderlust_Dev.postman_environment.json"
5. Collection imported successfully
```

#### Step 2: Configure Environment Variables

**Environment: Development**
```
base_url: http://localhost:8000
auth_token: [Token from login]
user_id: [Test user ID]
package_id: 1
booking_id: 1
```

#### Step 3: Running Tests

**Run Full Collection**
```
1. Select collection
2. Click "Run"
3. Select all requests
4. Click "Run Wanderlust Collection"
5. View results
```

**Run Single Request**
```
1. Click on request
2. Fill in required parameters
3. Click "Send"
4. Validate response
```

### Sample Postman Requests

#### Request 1: Get All Packages
```
GET http://localhost:8000/packages/

Headers:
  Content-Type: application/json
  Accept: application/json

Query Parameters:
  difficulty: easy
  min_price: 500
  max_price: 1500

Expected Response (200 OK):
{
  "count": 15,
  "next": "http://localhost:8000/packages/?page=2",
  "previous": null,
  "results": [...]
}
```

#### Request 2: Create Booking
```
POST http://localhost:8000/packages/1/booking/

Headers:
  Content-Type: application/json
  Authorization: Bearer {{auth_token}}

Body:
{
  "user_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "number_of_participants": 2,
  "booking_date": "2026-04-30",
  "special_requirements": "Vegetarian meals"
}

Expected Response (201 Created):
{
  "id": 123,
  "booking_confirmation": "BC-001",
  "total_price": 1299.98,
  "status": "pending"
}
```

#### Request 3: Search Packages
```
GET http://localhost:8000/search/?q=Paris

Headers:
  Content-Type: application/json

Expected Response (200 OK):
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "title": "Paris City Tour",
      "destination": "Paris",
      "price": 899.99
    }
  ]
}
```

#### Request 4: User Login & Get Token
```
POST http://localhost:8000/login/

Headers:
  Content-Type: application/json

Body:
{
  "username": "testuser",
  "password": "SecurePass123!"
}

Expected Response (200 OK):
{
  "token": "abcd1234efgh5678ijkl9012"
}

// Store token
pm.environment.set("auth_token", pm.response.json().token);
```

### Postman Test Scripts

#### Script 1: Validate Status Code
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

#### Script 2: Validate Response Body
```javascript
pm.test("Response contains data", function () {
    pm.response.to.have.jsonBody("results");
    pm.response.to.have.jsonBody("count");
});
```

#### Script 3: Validate Data Types
```javascript
pm.test("Price is a number", function () {
    pm.response.json().results.forEach(item => {
        pm.expect(item.price).to.be.a('number');
    });
});
```

#### Script 4: Performance Check
```javascript
pm.test("Response time < 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

---

## 🔒 Security Testing Checklist

### Authentication Tests
- [ ] Invalid credentials rejected
- [ ] Sessions expire properly
- [ ] JWT tokens validated
- [ ] Re-login required after logout
- [ ] Cross-site request forgery tokens present
- [ ] Password not exposed in responses
- [ ] Brute force protection active

### Authorization Tests
- [ ] Users can't access other users' data
- [ ] Admin-only endpoints require admin role
- [ ] Permissions properly enforced
- [ ] Deleted accounts have revoked access

### Data Security
- [ ] SQL injection attempts blocked
- [ ] XSS attempts blocked
- [ ] Sensitive data encrypted in transit (HTTPS)
- [ ] Passwords hashed (not in plaintext)
- [ ] API keys not logged

### Input Validation
- [ ] All inputs sanitized
- [ ] File upload validation
- [ ] Path traversal attempts blocked
- [ ] Rate limiting enforced
- [ ] Large payloads rejected

---

## 📈 Team Performance Metrics

### Individual Metrics (Per QA Engineer)

| Engineer | Test Cases | Pass Rate | Bugs Found | Hours |
|----------|-----------|-----------|-----------|-------|
| QA Eng 1 | 25 | 92% | 3 | 40 |
| QA Eng 2 | 22 | 86% | 4 | 40 |
| QA Eng 3 | 20 | 95% | 2 | 40 |
| QA Eng 4 | 26 | 89% | 5 | 40 |
| **Total** | **93** | **90%** | **14** | **160** |

### Team Productivity
- **Test Cases Executed**: 93 (100%)
- **Average Execution Time**: 1.7 hours per test
- **Bugs Found per 1000 LOC**: 0.8
- **Fix Resolution Rate**: 86%
- **Hours per Bug**: 11.4

---

## 🎓 Best Practices for QA Team

### Code Review for Tests
1. Ensure test names are descriptive
2. Verify preconditions are clear
3. Check test independence (no interdependencies)
4. Validate assertions are specific
5. Remove hardcoded values

### Test Data Management
1. Use consistent test data sets
2. Document test data requirements
3. Use data factories/factories for generation
4. Clean up after tests
5. Never use production data

### Documentation
1. Keep test documentation up-to-date
2. Document known limitations
3. Record execution environment details
4. Archive old test reports
5. Maintain reusable test templates

### Communication
1. Daily team standups (10 AM, 3 PM)
2. Weekly status reports to stakeholders
3. Immediate notification of critical bugs
4. Regular sync with development team
5. Monthly QA metrics review

---

## 📞 Contact & Escalation

### Escalation Path
```
QA Engineer 
    ↓
QA Lead (You)
    ↓
Development Manager
    ↓
Project Manager
    ↓
Client
```

### Communication Channels
- **Daily Issues**: Slack #qa-team
- **Critical Bugs**: Slack @here + direct call
- **Meetings**: Weekly Reviews (Mondays 2 PM)
- **Documentation**: Confluence Wiki
- **Test Tracking**: [Test Management Tool]

---

## 📁 Useful Templates

### Quick Reference
- [Test Case Template](./templates/test_case_template.md)
- [Defect Report Template](./templates/defect_report_template.md)
- [Test Report Template](./templates/test_report_template.md)
- [Postman Collection Export](./postman/Wanderlust_API_Tests.json)

---

**Document Owner**: QA Lead  
**Last Review**: March 30, 2026  
**Next Review**: April 30, 2026
