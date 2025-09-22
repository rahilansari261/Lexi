# Take Home Assessment
**Role:** Senior Backend Engineer

## Introduction

At Lexi, we're building AI-powered associates and paralegals to help lawyers automate routine work so they can focus on what really matters.

For the context of this assignment:
- We will review all submissions
- If you complete and submit a working assessment, we will get back to you either with feedback or with a decision for the next round.

## Context

One of the use cases we're tackling is enabling lawyers to track the status of their cases as they progress through courts in India.

A key source of this data is Consumer Courts, which are accessible online via the Jagriti portal (https://e-jagriti.gov.in/advance-case-search). Jagriti provides advanced search functionality to query case details by various fields (e.g., case number, complainant, respondent, advocate, industry, judge, etc.).

For this assignment, we want to focus specifically on District Consumer Courts (DCDRC), as they present the most complexity.

## Task

**Recording:** [SeniorBackendEngineer.mp4](https://example.com/SeniorBackendEngineer.mp4)

For this assignment, you will focus specifically on District Consumer Courts (DCDRC).

The recording demonstrates the flow we are looking to emulate:
1. A user submits a search query on the Jagriti portal.
2. The portal returns a list of cases.

Your goal for this assessment is to emulate that flow via a single API call.

When given the appropriate inputs (state name, commission name, and search value), your API should return the same list of cases that Jagriti displays.

You should **NOT** return mock data. For every call that is made to your endpoint, you should make all the corresponding requests to the Jagriti portal, format the received responses and then send back those formatted responses to the user.

To achieve this, you will need to:
1. Figure out how Jagriti maps state names and commission names (text inputs) to their internal IDs.
2. Use the correct internal IDs when constructing API requests.
3. Create supporting endpoints that:
   - List all available states with their internal IDs.
   - List all available commissions (for a given state) with their internal IDs.

## Requirements

### 1. Scope
- Focus only on District Consumer Courts (DCDRC).
- Support multiple search types, each exposed as a separate REST endpoint:
  - `/cases/by-case-number`
  - `/cases/by-complainant`
  - `/cases/by-respondent`
  - `/cases/by-complainant-advocate`
  - `/cases/by-respondent-advocate`
  - `/cases/by-industry-type`
  - `/cases/by-judge`
- Additional endpoints:
  - `/states` → Return list of states with their internal IDs.
  - `/commissions/{state_id}` → Return list of commissions for that state with their internal IDs.
- Restrict results to Daily Orders only.
- Use Case Filing Date as the default date filter.

### 2. Inputs
Each case-search endpoint should accept (via JSON body or query params):
- **State** (text, e.g., "KARNATAKA")
- **Commission** (text, e.g., "Bangalore 1st & Rural Additional")
- **Search Value** (string, e.g., "Reddy")

### 3. Outputs
Each case should return the following fields in JSON:
- `case_number`
- `case_stage`
- `filing_date`
- `complainant`
- `complainant_advocate`
- `respondent`
- `respondent_advocate`
- `document_link`

**Example Response:**
```json
[
  {
    "case_number": "123/2025",
    "case_stage": "Hearing",
    "filing_date": "2025-02-01",
    "complainant": "John Doe",
    "complainant_advocate": "Adv. Reddy",
    "respondent": "XYZ Ltd.",
    "respondent_advocate": "Adv. Mehta",
    "document_link": "https://e-jagriti.gov.in/.../case123"
  }
]
```

## Technical Details

### Stack
- **Python**
- **FastAPI**

### Separation of concerns
- **Models:** Define request/response models clearly.
- **Endpoints:** One endpoint per search type.
- **Logic Layer:** Encapsulate scraping/API-calling logic separately from API routes.

### Implementation Details
- Inspect the network requests made by Jagriti (via browser dev tools) and replicate them.
- Map text-based inputs (state, commission) into internal IDs used by Jagriti's backend.
- Provide `/states` and `/commissions/{state_id}` endpoints to surface these mappings.
- Handle Captcha gracefully

## Deliverables

1. **Codebase** hosted on github with clear structure and documentation.
2. **Hosted backend URL** (so we can quickly test the API without local setup).
3. **Instructions** on how to run the project locally.

### Bonus Points
A short recorded video explaining your project and demonstrating the endpoints in action.
You may upload the video as unlisted on YouTube and share the link in your submission.

## Submission Instructions

Email your submission to **hi@lexi.sg**.

The email subject line must exactly match the following format:
```
[Lexi Take-Home] Senior Backend Engineer - $YOUR_FULL_NAME
```

## Evaluation Criteria

- Code quality and readability.
- API design clarity (models, endpoints, separation of concerns).
- Correctness of data extraction.
- Robustness (handling of different states, commissions, and search types).
- Working hosted demo.
