# Literature Matrix
## Core Sources for the Final Paper Draft

This file fixes the literature backbone for the final paper.

It is based only on the strongest papers from the available corpus.
The goal is not to summarize every source in full detail.
The goal is to identify:

- what each source contributes
- where each source should be used
- how each source supports the paper argument
- what each source cannot support

---

## 1. Core Corpus

| ID | File | Title | Year | Main theme |
|---|---|---|---:|---|
| L1 | `applsci-12-04369.pdf` | RESTful API Testing Methodologies: Rationale, Challenges, and Solution Directions | 2022 | REST API testing foundations |
| L2 | `3460319.3469082.pdf` | RESTest: Automated Black-Box Testing of RESTful Web APIs | 2021 | automated black-box REST testing |
| L3 | `STVR22.pdf` | Automated Black-Box Testing of Nominal and Error Scenarios in RESTful APIs | 2022 | nominal and error scenario generation |
| L4 | `2410.12547v2.pdf` | REST API Testing in DevOps: A Study on an Evolving Healthcare IoT Application | 2024 | REST API testing in DevOps and evolving systems |
| L5 | `2103.05451v3.pdf` | The Effects of Continuous Integration on Software Development: a Systematic Literature Review | 2021 | CI and software quality |
| L6 | `Parry-2022-A-survey-of-flaky-tests.pdf` | A Survey of Flaky Tests | 2022 | flaky tests and test reliability |
| L7 | `2106.13891v2.pdf` | Test Case Selection and Prioritization Using Machine Learning: A Systematic Literature Review | 2021 | selection and prioritization under CI constraints |

---

## 2. Full Matrix

| ID | Type of source | Main contribution | Best use in paper | Which RQ it supports | Strength of fit | Main limitation for our paper |
|---|---|---|---|---|---|---|
| L1 | Systematic/review-style API testing paper | Explains why REST APIs require systematic testing and identifies methodological challenges | Introduction, Lit Review | RQ1, RQ3 | Strong | Does not justify our exact stack or exact test layering by itself |
| L2 | Empirical/tool paper | Shows automated black-box testing for REST APIs is feasible and valuable | Lit Review, Method | RQ1 | Strong | Focuses on automated REST generation, not on the full CI/CD strategy |
| L3 | Empirical/method paper | Supports testing both nominal and error scenarios in REST APIs | Lit Review, Method, Results framing | RQ1, RQ3 | Strong | More about test generation for APIs than about broad QA governance |
| L4 | DevOps/API case study | Links REST API testing to evolving systems and continuous delivery contexts | Introduction, Lit Review, Method, Discussion | RQ1, RQ3 | Strong | Different domain from e-commerce, so transfer must be argued carefully |
| L5 | Systematic literature review | Provides academic grounding for CI, continuous verification, and test discipline | Introduction, Lit Review, Method | RQ1, RQ2 | Very strong | About CI broadly, not specifically e-commerce or REST APIs |
| L6 | Survey | Explains flaky tests as a threat to reliability and trust in automated suites | Lit Review, Method, Discussion | RQ2, RQ3 | Very strong | Does not justify all other metrics, only stability-related ones |
| L7 | Systematic literature review | Supports prioritization and selective test execution under time and cost constraints | Lit Review, Method | RQ1, RQ2 | Moderate to strong | Focuses on ML-based prioritization, so our risk-based logic must be framed as aligned, not identical |

---

## 3. Detailed Source Notes

## L1. RESTful API Testing Methodologies: Rationale, Challenges, and Solution Directions

### What it gives us

- strong academic foundation for treating REST APIs as a serious QA target
- supports the idea that API testing is not an optional secondary activity
- supports a structured rather than ad hoc testing approach
- helps justify why invalid inputs, failures, robustness, and integration issues matter

### Where it belongs

- `Introduction`
- `Lit Review`

### What it should support

- why API-centric systems need systematic QA
- why API failures can affect critical business functionality
- why a methodology-driven approach is justified

### What it should not be used to claim

- that our exact toolchain is mandated by literature
- that one paper alone proves our whole strategy

---

## L2. RESTest: Automated Black-Box Testing of RESTful Web APIs

### What it gives us

- practical academic support for automated black-box testing of REST APIs
- supports the idea that API testing can be automated beyond simple hand-written checks
- helps defend automated endpoint-level verification as an academically serious method

### Where it belongs

- `Lit Review`
- `Method`

### What it should support

- use of automation at the API layer
- black-box testing as a realistic strategy for service interfaces
- the value of automated request-based verification

### What it should not be used to claim

- that generated testing and our manually designed suite are the same thing
- that it justifies our E2E or CI/CD choices directly

---

## L3. Automated Black-Box Testing of Nominal and Error Scenarios in RESTful APIs

### What it gives us

- supports the testing of both valid and invalid scenarios
- supports the idea that error-path testing is a first-class QA concern
- helps justify negative testing, malformed input testing, and robustness testing

### Where it belongs

- `Lit Review`
- `Method`
- `Results` framing

### What it should support

- inclusion of error scenarios in the automated suite
- focus on invalid behavior, malformed input, and controlled failures
- idea that nominal-only testing is insufficient

### What it should not be used to claim

- that all our negative tests were automatically generated
- that it directly covers pipeline metrics

---

## L4. REST API Testing in DevOps: A Study on an Evolving Healthcare IoT Application

### What it gives us

- supports API testing in continuous and changing environments
- supports the idea that automation should fit a DevOps context
- gives a concrete case study where REST API testing matters across evolving releases

### Where it belongs

- `Introduction`
- `Lit Review`
- `Method`
- `Discussion`

### What it should support

- alignment between API automation and CI/CD-style workflows
- justification for treating automated testing as part of continuous quality control
- argument that evolving systems need repeatable automated verification

### What it should not be used to claim

- direct domain equivalence between healthcare IoT and e-commerce
- that our exact metrics match theirs one-to-one

---

## L5. The Effects of Continuous Integration on Software Development: a Systematic Literature Review

### What it gives us

- strongest academic basis for CI as part of software quality practice
- supports continuous verification, rapid feedback, and testing discipline
- supports the idea that automation and CI are structurally linked

### Where it belongs

- `Introduction`
- `Lit Review`
- `Method`

### What it should support

- why CI/CD belongs in the QA methodology
- why pipeline execution is not just an implementation detail
- why execution time and repeatability matter

### What it should not be used to claim

- that CI automatically guarantees software quality
- that CI alone explains all observed improvements

---

## L6. A Survey of Flaky Tests

### What it gives us

- strongest source for discussing test trustworthiness
- shows why flaky tests are a QA problem, not just a testing annoyance
- supports inclusion of stability or flaky-rate metrics

### Where it belongs

- `Lit Review`
- `Method`
- `Discussion`

### What it should support

- why suite reliability matters
- why flaky tests reduce confidence in automation and CI
- why stability metrics belong in the methodology

### What it should not be used to claim

- that our suite is flaky unless measured
- that flakiness is the only important indicator of reliability

---

## L7. Test Case Selection and Prioritization Using Machine Learning: A Systematic Literature Review

### What it gives us

- supports the broader idea of selective and prioritized testing
- supports the logic that testing effort should be guided under CI constraints
- helps justify focusing on high-value tests first rather than treating all tests equally

### Where it belongs

- `Lit Review`
- `Method`

### What it should support

- methodological legitimacy of prioritization
- balancing feedback speed and test value
- arguing that not all test effort should be uniformly distributed

### What it should not be used to claim

- that our approach is ML-driven
- that risk-based prioritization and ML-based prioritization are identical

---

## 4. Theme-to-Source Mapping

This table shows which sources support each major theme in the paper.

| Theme | Core sources | Role |
|---|---|---|
| API-centric QA | L1, L2, L3, L4 | foundation for focusing the paper on API systems |
| automated black-box testing | L2, L3 | support for API automation and error-path testing |
| testing in evolving systems | L4, L5 | support for continuous verification and CI integration |
| prioritization | L7 | support for selective focus on critical areas |
| CI/CD | L5, L4 | support for pipeline-based QA execution |
| metrics and test trust | L6, L5 | support for stability and operational evaluation |

---

## 5. Mapping Sources to Sections

## Introduction

Use mainly:

- L1
- L4
- L5

Purpose:

- define the problem space
- justify API-centric QA
- justify continuous quality verification

## Lit Review

Use all core papers:

- L1-L7

Purpose:

- build the conceptual foundation
- show that our chosen QA direction is literature-aligned

## Method

Use mainly:

- L2
- L3
- L4
- L5
- L6
- L7

Purpose:

- justify layered automation
- justify CI/CD integration
- justify prioritization
- justify the chosen metrics and stability concerns

## Results

Use literature lightly:

- L3
- L4
- L5
- L6

Purpose:

- frame the meaning of measured results without fully interpreting them yet

## Discussion

Use mainly:

- L4
- L5
- L6
- L7

Purpose:

- compare expected benefits from literature with the empirical outcomes

---

## 6. Literature-Supported Claims We Can Safely Make

These are the claims we should be able to defend with the selected corpus.

### Safe claim set

- API-centric systems require systematic and robust testing
- automated black-box testing is a valid strategy for REST APIs
- negative and error scenarios are important in API verification
- CI supports continuous quality verification and testing discipline
- selective or prioritized testing is methodologically reasonable under CI constraints
- flaky tests are a meaningful threat to the trustworthiness of automated testing
- metrics such as execution time and stability are defensible evaluation dimensions in CI contexts

### Claims we should avoid or soften

- one exact tool stack is the academically best stack
- our project proves universal superiority of this strategy
- coverage alone is sufficient to demonstrate QA success
- ML-based prioritization literature directly validates our risk scoring approach

---

## 7. How This Matrix Supports The Final Narrative

The final article should be built so that the literature leads naturally into the
implemented strategy.

### Narrative sequence

1. API systems are critical and difficult to test reliably
2. Literature supports systematic API automation, including negative scenarios
3. CI/CD creates the need for repeatable and operationally efficient testing
4. Prioritization is justified because not all testing has equal value under CI constraints
5. Metrics and test trustworthiness are necessary for evaluation
6. Therefore, a risk-informed multi-level automated strategy is a defensible case to study

This sequence should be visible in the final paper.

---

## 8. Next Writing Step

The next step after this matrix should be:

- write the `Introduction`
- using L1, L4, and L5 as the main support
- while keeping the three research questions fixed
