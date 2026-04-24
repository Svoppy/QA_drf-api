# Paper Draft Plan
## Literature-Grounded Draft Blueprint

This file is the working plan for the final course paper.

The goal is not to write the article yet.
The goal is to fix:

- the research direction
- the paper structure
- the literature backbone
- the logic of argumentation
- the mapping from assignment outputs to paper sections

---

## 1. Working Research Direction

The paper should not look like a project report about one Django repository.
It should look like a literature-grounded QA study that uses the implemented
e-commerce API project as an empirical case.

### Core direction

- focus on QA for API-centric, transaction-heavy systems
- justify a risk-informed, multi-level automated testing strategy
- support the strategy through recent literature
- evaluate the strategy through measured outcomes from the project

### What the paper should naturally argue

- critical API systems require targeted QA rather than uniform testing
- layered automation is needed because different risks appear at different levels
- CI/CD is not only an engineering convenience, but part of continuous quality verification
- metrics are needed to justify QA value, but not all metrics are equally informative

### What the paper should avoid

- looking like a walkthrough of one repository
- claiming that one exact tool stack is universally best
- looking like the methodology was invented after the implementation
- overclaiming novelty

---

## 2. Final Section Structure

The final paper should follow this exact structure.

### 1. Abstract

- write last
- only after all other sections are complete
- should summarize:
  - problem
  - objective
  - method
  - key results
  - key implication

### 2. Introduction

- define the QA problem in API-centric systems
- explain why transaction-heavy systems need reliable QA
- introduce the need for prioritization, automation, CI/CD, and metrics
- state research objective
- include keywords
- include 3 research questions

### 3. Lit Review

- review recent literature that supports:
  - API testing
  - automated black-box testing
  - prioritization
  - CI/CD testing
  - metrics and test stability
- end with a synthesis that leads logically into the chosen method

### 4. Method

- describe the research design
- define the case context
- explain the QA strategy under study
- explain data sources
- define evaluation dimensions
- explain validity and limitations

### 5. Results

- present measured findings
- show metrics, tables, graphs, and visualizations
- connect results to research questions
- include primary outcomes only, not long interpretation

### 6. Discussion

- explain meaning of the results
- answer the research questions directly
- discuss cause and effect
- discuss limitations
- discuss threats to validity
- state what can and cannot be concluded

### 7. References

- only real sources used in the text
- recent literature only
- no padding with weak or unused papers

---

## 3. Proposed Research Questions

These research questions are aligned with the current literature set and the
implemented QA work.

| ID | Research Question |
|---|---|
| RQ1 | How well does a risk-informed multi-level automated testing strategy align with recent literature on quality assurance for API-centric systems? |
| RQ2 | Which metrics most meaningfully justify such a strategy in CI/CD environments: coverage, defect detection, execution time, or test stability? |
| RQ3 | To what extent do the empirical outcomes of the e-commerce API case support the expected benefits described in recent software testing literature? |

### How these RQs should function

- `RQ1` connects the paper to literature and methodology
- `RQ2` connects the paper to metrics and evaluation logic
- `RQ3` connects the paper to empirical results and discussion

---

## 4. Core Literature Corpus

Only the strongest papers should structure the draft.

### Core papers

| ID | File | Main role in paper |
|---|---|---|
| L1 | `applsci-12-04369.pdf` | API testing foundations and challenges |
| L2 | `3460319.3469082.pdf` | Automated black-box testing of REST APIs |
| L3 | `STVR22.pdf` | Nominal and error scenario testing for REST APIs |
| L4 | `2410.12547v2.pdf` | REST API testing in DevOps / evolving systems |
| L5 | `2103.05451v3.pdf` | Continuous integration and software quality |
| L6 | `Parry-2022-A-survey-of-flaky-tests.pdf` | Flaky tests and test trustworthiness |
| L7 | `2106.13891v2.pdf` | Test selection and prioritization logic |

### Reserve papers

| ID | File | Use only if needed |
|---|---|---|
| R1 | `2207.01047v1.pdf` | Additional evidence on flaky test causes |
| R2 | `7285-Empirical_Analysis_of_Widely_Used_Website_Automated_Testing_Tools.pdf` | Tool comparison background |
| R3 | `3655022.pdf` | Defect prediction guidance background |

### Papers intentionally excluded from the main backbone

- `issue2-p16-21.pdf`
- `4365.pdf`
- `Jyoti,+Islam+and+Kudapa_ijbei24v4i40134.pdf`

Reason:

- weaker fit to the argument
- more generic than needed
- lower value as core academic support

---

## 5. Literature Review Matrix

This matrix should be used when writing the actual literature review.

| Paper | Theme | What it supports | Best section usage |
|---|---|---|---|
| L1 `RESTful API Testing Methodologies` | API testing | REST APIs are critical and require structured testing | Introduction, Lit Review |
| L2 `RESTest` | automated REST testing | automated black-box testing is viable and useful for REST APIs | Lit Review, Method |
| L3 `Automated Black-Box Testing of Nominal and Error Scenarios in RESTful APIs` | error and robustness testing | nominal plus error scenarios are essential for API quality | Lit Review, Method |
| L4 `REST API Testing in DevOps` | testing in evolving systems | API automation fits continuous DevOps contexts | Lit Review, Method, Discussion |
| L5 `The Effects of Continuous Integration on Software Development` | CI/CD | CI strengthens continuous quality verification and testing discipline | Introduction, Lit Review, Method |
| L6 `A Survey of Flaky Tests` | test reliability | flaky tests threaten trust in automated suites | Lit Review, Method, Discussion |
| L7 `Test Case Selection and Prioritization Using Machine Learning` | prioritization | selective and prioritized testing is justified under CI constraints | Lit Review, Method |

---

## 6. Section-by-Section Blueprint

This is the actual writing blueprint for the draft.

## 6.1 Introduction

### Paragraph plan

#### Paragraph 1

- define the context of modern API-centric systems
- explain why e-commerce-like backends are operationally sensitive
- mention critical flows such as orders, cart, pricing, validation, and access control

Sources:

- L1
- L4

#### Paragraph 2

- explain why ad hoc or purely manual testing is insufficient
- introduce the need for systematic automated verification
- bring in the need for continuous quality control in CI/CD

Sources:

- L1
- L5

#### Paragraph 3

- state the central problem:
  - not all modules are equally risky
  - not all tests provide equal value
  - not all metrics justify QA effectiveness equally well

Sources:

- L5
- L7

#### Paragraph 4

- state the purpose of the paper
- describe the study as a literature-grounded empirical case
- state the three research questions

No heavy citation needed here beyond light support.

### Keywords

Working keyword set:

- software quality assurance
- API testing
- risk-informed testing
- test automation
- continuous integration
- quality gates
- flaky tests
- e-commerce systems

---

## 6.2 Lit Review

The literature review should be thematic, not author-by-author.

### Subsection A. API testing as a QA problem

What to cover:

- why REST APIs are critical integration surfaces
- why black-box testing is practical and often necessary
- why both nominal and error scenarios matter

Sources:

- L1
- L2
- L3

### Subsection B. Multi-level automated testing

What to cover:

- different layers detect different defect types
- unit, integration, and end-to-end testing play different roles
- layered strategy is structurally stronger than single-level coverage

Sources:

- L1
- L3
- L4

### Subsection C. Prioritization and selective testing

What to cover:

- CI creates time and cost pressure
- not all tests can be equally emphasized first
- prioritization logic supports focusing on critical or high-risk areas

Sources:

- L7

### Subsection D. CI/CD and continuous verification

What to cover:

- CI improves testing discipline
- automated pipelines enable repeatability and visibility
- quality verification becomes part of delivery, not a separate afterthought

Sources:

- L5
- L4

### Subsection E. Metrics and trustworthiness of automation

What to cover:

- coverage is useful but incomplete
- defect detection gives stronger practical value
- execution time matters because CI is time-sensitive
- flaky tests reduce trust in test outcomes

Sources:

- L6
- R1 if needed

### Closing synthesis of Lit Review

The last paragraph of the literature review should naturally conclude:

- literature supports API-focused testing
- literature supports layered automation
- literature supports selective prioritization under CI constraints
- literature supports the use of metrics and reliability considerations
- therefore it is reasonable to study a risk-informed multi-level QA strategy in an empirical case

---

## 6.3 Method

The method section should sound like research design, not implementation notes.

### Subsection A. Research design

Recommended wording direction:

- empirical case study
- literature-grounded evaluation
- mixed-method assessment

### Subsection B. Case context

Describe the case as:

- an API-centric e-commerce backend
- transaction-heavy
- containing multiple high-impact modules
- suitable for layered automated testing

### Subsection C. QA strategy under study

Describe the strategy in principle-first form:

- prioritization of critical modules
- unit testing for logic and validation
- integration testing for service interactions and endpoint behavior
- E2E testing for realistic and access-sensitive flows
- CI/CD execution for repeatability
- quality gates for operationalized quality control

### Subsection D. Data sources

| Source Type | Actual project source |
|---|---|
| planned QA basis | Assignment 1 risk assessment and strategy |
| automation implementation | Assignment 2 automation outputs |
| empirical updates | Midterm additions and reassessment |
| pipeline evidence | GitHub Actions runs, gate outcomes, screenshots |
| metrics | coverage, defects, runtime, flaky observations |
| literature basis | core corpus L1-L7 |

### Subsection E. Evaluation dimensions

This subsection must be explicit.

| Dimension | Type | Why it matters |
|---|---|---|
| Coverage of high-risk modules | Quantitative | indicates breadth of verification on critical areas |
| Defect detection by module/risk | Quantitative | indicates practical bug-finding value |
| Execution time | Quantitative | indicates CI feasibility and operational cost |
| Test stability / flaky rate | Quantitative | indicates trustworthiness of the suite |
| Structural adequacy of test layers | Qualitative | indicates whether risk types are matched to suitable test levels |
| CI/CD reproducibility | Qualitative | indicates whether the process is repeatable and verifiable |
| Literature alignment | Qualitative | indicates whether the strategy is academically defensible |

### Subsection F. Validity and limitations

This subsection should already acknowledge:

- single-case design
- no direct experimental control group
- context-specific metrics
- limited observation window for stability
- coverage does not equal absence of defects

---

## 6.4 Results

Results should present measured outcomes first and interpretation second.

### Subsection A. Strategy implementation summary

Present:

- total number of tests
- distribution by level
- high-risk modules covered
- CI/CD presence
- quality gate status

### Subsection B. Metrics

Present:

- coverage
- defect counts
- execution times
- flaky rate
- pipeline outcomes

### Subsection C. Risk and defect alignment

Present:

- expected risk vs observed issues
- high-risk modules vs actual findings
- where the strategy confirmed or challenged prior assumptions

### Subsection D. Structural results

Present:

- what unit tests covered
- what integration tests uncovered
- what E2E tests uniquely revealed

### Required table

| Test Layer | Primary role | Main modules covered | Main defect or risk type addressed |
|---|---|---|---|

### Required synthesis table

| Literature-Supported Principle | Implemented in Case | Observed Outcome |
|---|---|---|

This table is important because it connects literature and project evidence.

---

## 6.5 Discussion

Discussion must answer the research questions directly and interpret cause and effect.

### Subsection A. Answer to RQ1

Main goal:

- explain how strongly the strategy aligns with the literature

Expected line:

- alignment is strong at the level of principles
- alignment is moderate at the level of exact tool realization

### Subsection B. Answer to RQ2

Main goal:

- rank the practical value of the chosen metrics

Likely argument:

- coverage is useful but insufficient alone
- defect detection is the strongest practical indicator
- execution time matters because of CI constraints
- flaky rate matters because trust in automation matters

### Subsection C. Answer to RQ3

Main goal:

- compare literature expectations and empirical outcomes

Likely argument:

- empirical case largely supports expected benefits
- but also reveals gaps and context-specific limitations

### Subsection D. Implications

What this means for QA:

- literature-supported strategy can be implemented in real API systems
- prioritization and layering are more defensible than broad undifferentiated testing

### Subsection E. Limitations

Must include:

- single system type
- one empirical case
- no full head-to-head comparison with another strategy
- project-specific architecture may influence outcomes

### Subsection F. Threats to validity

Recommended structure:

| Threat Type | Description |
|---|---|
| Construct validity | metrics such as coverage do not fully represent overall QA effectiveness |
| Internal validity | some observed outcomes may be influenced by project-specific implementation details |
| External validity | findings may not generalize to all domains beyond API-centric transactional systems |

### Subsection G. Conclusion-like close inside Discussion

If no separate conclusion section is allowed, the discussion should end with:

- overall judgment of the strategy
- what remains incomplete
- what future work should address

---

## 7. Visualisation Plan

The teacher explicitly asked for data visualisation.

### Required visuals

| Visual | Purpose |
|---|---|
| coverage by high-risk module graph | compare verification depth |
| defect count by module/risk level graph | show where problems were actually found |
| execution time before/after graph | show efficiency trade-offs |
| pipeline visual or screenshot | prove CI/CD integration |
| architecture diagram of QA strategy | show flow from risk -> tests -> pipeline -> metrics |

### Required tables

| Table | Purpose |
|---|---|
| literature matrix | academic grounding |
| research questions and evaluation dimensions | methodological clarity |
| metrics summary | quantitative results |
| defects vs risk level | risk validation |
| quality gates | operational thresholds |
| literature principle vs implementation vs outcome | bridge between theory and practice |

---

## 8. Assignment-to-Paper Mapping

This is how the existing course work feeds the paper naturally.

| Existing artifact | Paper section |
|---|---|
| `docs/1_risk_assessment.md` | Introduction, Method |
| `docs/2_test_strategy.md` | Method |
| `docs/5_automation_strategy.md` | Method |
| `docs/6_quality_gate_report.md` | Method, Results |
| `docs/7_metrics_report.md` | Results |
| `docs/8_midterm_plan.md` | Method, Results |
| `docs/9_midterm_analysis_tables.md` | Results, Discussion |
| `docs/REPORT_Midterm_Kazikhanov.docx` | Results evidence and visuals |

---

## 9. Narrative Rules For Writing

These rules should control the style of the final draft.

### Rule 1

Do not justify the approach by tool names first.
Justify it by literature-backed QA principles first.

### Rule 2

Do not say:

- "we used this because it was convenient"

Prefer:

- "this implementation operationalized literature-supported QA principles in the case context"

### Rule 3

Do not overclaim:

- avoid saying the study proves universal superiority
- present it as a defensible case-supported strategy

### Rule 4

Keep project specifics in the role of empirical evidence, not the whole paper.

### Rule 5

Always connect:

- research question -> metric or analysis dimension -> result -> interpretation

---

## 10. Writing Order

This should be the actual execution order.

1. finalize the literature matrix
2. finalize the 3 research questions
3. write `Introduction`
4. write `Lit Review`
5. write `Method`
6. assemble tables and visuals for `Results`
7. write `Results`
8. write `Discussion`
9. write `Abstract`
10. clean references and final formatting

---

## 11. Immediate Next Step

The next practical step should be:

- build the final literature matrix from the 7 core papers
- extract the exact role of each paper in the draft
- then start writing the `Introduction`
