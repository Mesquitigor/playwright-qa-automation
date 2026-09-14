"""Single source of truth for the CV content.

Edit this file to change the CV, then run `python3 cv/build_cv.py` to regenerate
both the .docx and the .pdf. Keeping one source avoids the two files drifting apart.
"""

NAME = "HIGOR LUIZ ARAÚJO DE MESQUITA"

# Mixed-case form for the page footer and PDF metadata, where all caps reads as shouting.
DISPLAY_NAME = "Higor Luiz Araújo de Mesquita"

HEADLINE = "Senior QA Engineer  |  SDET  |  AI-Assisted Test Automation  |  Playwright · TypeScript · Cursor · MCP"

CONTACT_LINE_1 = "João Pessoa, PB, Brazil (Remote, UTC-3)  ·  higormesquita@gmail.com  ·  +55 83 99397-1661"

# (display text, url) — rendered as clickable links side by side.
CONTACT_LINKS = [
    ("linkedin.com/in/higor-mesquita", "https://linkedin.com/in/higor-mesquita"),
    ("github.com/Mesquitigor", "https://github.com/Mesquitigor"),
]

SUMMARY = (
    "Senior QA Engineer and SDET with 5+ years designing test automation for AI-powered healthcare, "
    "digital payments, banking, and e-commerce platforms. Specialist in Playwright with TypeScript, "
    "combining two complementary strengths: validating AI and GenAI features for correctness and "
    "consistency, and applying AI-augmented quality engineering with Cursor and Playwright MCP to "
    "accelerate test design, authoring, and failure triage. Built automated test suites from the "
    "ground up, totaling 1,600+ tests, automated 20+ end-to-end services, and cut regression "
    "execution time by 40%. "
    "Acts as QA Tech Lead, setting automation standards, owning CI/CD quality gates, and mentoring "
    "engineers to deliver automation independently."
)

SKILLS = [
    (
        "Test Automation",
        "Playwright (TypeScript), Cypress (JavaScript), Robot Framework (Python), Selenium, Appium, "
        "Vitest, Page Object Model, fixtures, BDD and Gherkin (Cucumber)",
    ),
    (
        "AI Product Testing",
        "Validation of AI and GenAI features for correctness, safety, and consistency; detection of "
        "hallucinations, inconsistent outputs, and edge cases; schema and business-rule assertions over "
        "non-deterministic output; prompt and model regression; golden datasets",
    ),
    (
        "AI-Augmented QA",
        "Cursor (test authoring, refactoring, and CI failure triage), Cursor Rules, Playwright MCP, "
        "prompt engineering, AI-assisted test generation from requirements, user stories, and "
        "acceptance criteria",
    ),
    (
        "Testing Types",
        "End-to-end, API, regression, integration, performance and load, mobile, cross-browser, "
        "accessibility (WCAG), visual regression, exploratory",
    ),
    (
        "CI/CD and Infrastructure",
        "GitHub Actions, Jenkins, Docker, Linux, test sharding and parallelization, Allure, trace and "
        "video artifact analysis",
    ),
    (
        "Data and Tools",
        "SQL, PostgreSQL, DBeaver, REST APIs, Postman, k6, JMeter, Git, Jira, ClickUp, AWS (basic)",
    ),
    (
        "Practices",
        "Scrum, Kanban, shift-left testing, risk-based testing, test strategy, quality governance, "
        "technical mentoring",
    ),
]

EXPERIENCE = [
    {
        "company": "SOAP HEALTH",
        "title": "Senior QA Engineer & QA Tech Lead",
        "dates": "Feb 2025 – Present",
        "context": "Remote (US company)  ·  AI-powered clinical decision support for healthcare providers",
        "bullets": [
            "Built the automation practice from zero to 400+ Playwright and TypeScript tests covering "
            "critical clinical journeys, edge cases, and backend authentication flows.",
            "Own the quality of AI-assisted clinical features, validating non-deterministic model outputs "
            "through schema and business-rule assertions, plus regression checks on prompt and model changes.",
            "Lead the QA team as technical mentor, running training on Playwright fundamentals, Git "
            "workflows, code quality, dependency management, and CI/CD, taking members from zero "
            "automation experience to independent test delivery.",
            "Re-architected the legacy suite into Page Object Model with fixtures and a locator strategy "
            "based on roles and test IDs, reducing flaky failures and CI re-runs.",
            "Introduced AI-augmented workflows with Cursor and Playwright MCP for test scaffolding, "
            "refactoring, and CI failure triage, shortening test authoring and debugging cycles.",
            "Own CI quality gates in GitHub Actions with parallelized runs and Allure reporting, turning "
            "failure analysis into a repeatable, artifact-driven process.",
            "Write unit and integration tests in Vitest alongside developers to shift quality left and "
            "catch defects before end-to-end execution.",
            "Run a traceable QA process in Jira and ClickUp, from requirement to test case to defect.",
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
