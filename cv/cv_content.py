"""Single source of truth for the CV content.

Edit this file to change the CV, then run `python3 cv/build_cv.py` to regenerate
both the .docx and the .pdf. Keeping one source avoids the two files drifting apart.
"""

NAME = "HIGOR LUIZ ARAÚJO DE MESQUITA"

# Mixed-case form for the page footer and PDF metadata, where all caps reads as shouting.
DISPLAY_NAME = "Higor Luiz Araújo de Mesquita"

HEADLINE = "QA Engineer  |  SDET  |  AI-Assisted Test Automation  |  Playwright · TypeScript · Cursor · MCP"

CONTACT_LINE_1 = "João Pessoa, PB, Brazil (Remote, UTC-3)  ·  higormesquita@gmail.com  ·  +55 83 99397-1661"

# (display text, url) — rendered as clickable links side by side.
CONTACT_LINKS = [
    ("linkedin.com/in/higor-mesquita", "https://linkedin.com/in/higor-mesquita"),
]

SUMMARY = (
    "QA Engineer and SDET with 5+ years designing test automation for AI-powered healthcare, "
    "digital payments, banking, and e-commerce platforms. Specialist in Playwright with TypeScript, "
    "combining two complementary strengths: validating AI and GenAI features for correctness and "
    "consistency, and applying AI-augmented quality engineering with Cursor and Playwright MCP to "
    "accelerate test design, authoring, and failure triage. Built automated test suites from the "
    "ground up, totaling 2,000+ test cases, automated 20+ end-to-end services, and cut regression "
    "execution time by 40%. "
    "Works across web, API, mobile, and database layers, contributing to CI/CD pipelines and keeping "
    "suites stable through disciplined locator strategy and Page Object Model architecture."
)

SKILLS = [
    (
        "Test Automation",
        "Playwright (TypeScript), Cypress (JavaScript), Robot Framework (Python), Selenium, Appium, "
        "Page Object Model, BDD and Gherkin (Cucumber)",
    ),
    (
        "AI Product Testing",
        "Validation of AI and GenAI features for correctness, safety, and consistency; detection of "
        "hallucinations, inconsistent outputs, and edge cases; schema and business-rule assertions "
        "over non-deterministic output",
    ),
    (
        "AI-Augmented QA",
        "Cursor (test authoring, refactoring, and CI failure triage), Cursor Rules, Playwright MCP, "
        "prompt engineering, AI-assisted test generation from requirements, user stories, and "
        "acceptance criteria",
    ),
    (
        "Testing Types",
        "End-to-end, API, regression, integration, mobile, cross-browser, accessibility (WCAG), "
        "visual regression, exploratory, performance and load (k6, JMeter)",
    ),
    (
        "CI/CD and Infrastructure",
        "GitHub Actions, Jenkins, Git, Docker, Linux, AWS (basic), test sharding and parallelization",
    ),
    (
        "Databases and APIs",
        "SQL, PostgreSQL, DBeaver, REST APIs, Postman",
    ),
    (
        "Reporting and Debugging",
        "Allure, Playwright trace viewer and video artifacts, flaky test analysis, defect reporting",
    ),
    (
        "Process and Collaboration",
        "Jira, ClickUp, Scrum, Kanban, shift-left testing, risk-based testing, test strategy",
    ),
]

EXPERIENCE = [
    {
        "company": "MEDOME",
        "title": "QA Engineer",
        "dates": "Feb 2025 – Present",
        "context": "Remote (US company)  ·  AI-powered clinical decision support for healthcare providers",
        "bullets": [
            "Built the automation suite from zero to 900+ Playwright and TypeScript test cases covering "
            "critical clinical journeys and edge cases.",
            "Test AI-assisted clinical features, validating non-deterministic model outputs through "
            "schema and business-rule assertions.",
            "Re-architected the legacy suite into Page Object Model with a locator strategy based on "
            "roles and test IDs, reducing flaky failures and CI re-runs.",
            "Use Cursor and Playwright MCP for test scaffolding, refactoring, and CI failure triage, "
            "shortening test authoring and debugging cycles.",
            "Contribute to CI/CD pipelines in GitHub Actions, using Allure reports to analyze failures "
            "and improve test reliability.",
            "Fix existing Vitest unit and integration tests when feature work or refactors break them.",
            "Validate complex API integrations and backend authentication flows.",
            "Manage tasks and bugs in Jira and ClickUp, keeping QA work traceable from requirement to "
            "test case to defect.",
        ],
    },
    {
        "company": "HST CARD TECHNOLOGY",
        "title": "QA Engineer",
        "dates": "Apr 2022 – Feb 2025",
        "context": "Remote (Campinas, SP, Brazil)  ·  Digital wallets and card tokenization for the banking sector",
        "bullets": [
            "Automated 20+ end-to-end services covering 1,200+ test scenarios in Python with Robot Framework.",
            "Cut web regression execution time by 40% by re-engineering the Cypress suite through locator "
            "strategy, selective execution, and parallelization.",
            "Validated ETL and payment data integrity with complex SQL queries in DBeaver across "
            "transaction and settlement workflows.",
            "Delivered quality and security testing for digital wallet products sold to 5+ banks across "
            "API, web, and mobile platforms.",
            "Partnered with squads on test strategy for tokenization and wallet flows, embedding QA from "
            "refinement onward.",
        ],
    },
    {
        "company": "DOCK",
        "title": "QA Engineer",
        "dates": "Aug 2021 – Apr 2022",
        "context": "Remote (Barueri, SP, Brazil)  ·  Core banking: card authorization, ledger, and reconciliation",
        "bullets": [
            "Defined the test strategy for a banking reconciliation system and a document management product.",
            "Tested web, mobile, and API layers of a multi-asset ledger serving 300+ clients.",
            "Identified critical pre-release defects in card authorization and reconciliation flows, "
            "protecting financial data integrity.",
        ],
    },
    {
        "company": "UNIPÊ SOFTWARE FACTORY",
        "title": "QA Lead",
        "dates": "Feb 2021 – Jul 2021",
        "context": "João Pessoa, PB, Brazil  ·  Web system for cost control in healthcare programs",
        "bullets": [
            "Led the QA team through test planning and the execution of manual and automated tests.",
            "Built the automation layer with Java, Selenium, and Maven.",
            "Reviewed requirements documentation to close test coverage gaps before delivery.",
        ],
    },
]

EDUCATION = [
    {
        "degree": "Technologist Degree in Systems Analysis and Development",
        "school": "Centro Universitário de João Pessoa (UNIPÊ)",
        "dates": "2021 – 2023",
    },
]

LANGUAGES = "Portuguese (Native)  ·  English (C1 Advanced, daily working proficiency with US teams)"
