# Master Article Draft

## Abstract

Abstract will be written last, after the full paper is stabilized and the final results-discussion wording is fixed.

---

# Introduction

Modern software systems increasingly rely on REST APIs as the main channel through which services exchange data, trigger business actions, and expose critical functionality to users and external systems. In that sense, an API-centric backend is not just a technical layer hidden behind the interface. It is often the place where failures become financially visible, operationally expensive, and difficult to ignore. This is especially true for transaction-heavy platforms such as e-commerce systems, where order creation, cart behavior, pricing logic, tax calculation, validation rules, and access control are tightly connected to business continuity. A failure in one of these flows is rarely isolated. It can affect payment processing, user trust, order correctness, or administrative control over the platform. Recent work on REST API testing reflects this concern and shows that API testing has moved well beyond being a secondary quality activity; it is now treated as a central QA problem in its own right (Ehsan et al., 2022).

At the same time, the practical difficulty is not only that APIs are important. The harder issue is that they are rarely simple to verify in a uniform way. Some faults are rooted in business logic and validation, some appear at the interaction level between components, and others surface only when realistic user behavior or restricted flows are exercised end to end. This creates a fairly common QA tension: a single testing level may look sufficient on paper, but in practice it leaves blind spots. Black-box testing research for REST systems has repeatedly shown that nominal scenarios alone are not enough and that error-oriented and robustness-oriented verification must be part of the testing picture as well (Martin-Lopez et al., 2021; Corradini et al., 2022). In other words, the question is not whether automated testing should be used, but how it should be structured so that different classes of risk are actually visible.

Another pressure comes from the delivery process itself. In modern development settings, tests are no longer run only as occasional verification steps before release. They are expected to operate continuously inside CI/CD workflows, where fast feedback, reproducibility, and operational trust matter almost as much as raw defect detection. The literature on continuous integration suggests that CI affects not only build automation, but also testing discipline, visibility of quality issues, and the ability of teams to maintain continuous verification over time (Soares et al., 2021). That makes QA strategy a design problem rather than a collection of isolated checks. A suite may have many tests and still be weak if it is poorly prioritized, too slow to support feedback cycles, or unstable enough to undermine confidence in its own results.

This becomes even more relevant when test effort is constrained by time, pipeline cost, or frequent code changes. In such settings, it is not realistic to assume that all testing has equal value or should be emphasized equally. Prioritization enters the picture for a reason. Recent literature on test selection and prioritization in CI contexts shows that early feedback, selective focus, and informed ordering of tests are not marginal concerns; they are part of how testing remains useful under practical delivery constraints (Pan et al., 2021). The exact implementation of prioritization may vary, but the broader implication is clear: when systems contain flows with very different business impact, QA strategy has to reflect that asymmetry instead of pretending every path carries the same risk.

There is also a second layer of evaluation that matters for an academic and engineering discussion of QA strategy: metrics. Coverage is widely used, but by itself it does not explain whether the most critical defects are being found, whether the suite is stable, or whether the test process is operationally sustainable in CI. Defect yield, execution time, and stability indicators such as flaky behavior often reveal practical qualities that raw coverage cannot fully capture. The software testing literature has been particularly explicit about the damage caused by flaky tests, which weaken trust in automation, distort pipeline feedback, and limit the credibility of empirical conclusions drawn from automated suites (Parry et al., 2022). Because of that, a meaningful QA evaluation needs to treat automated testing not only as a question of breadth, but also as a question of trustworthiness and usefulness.

Against this background, the present study examines a risk-informed, multi-level automated testing strategy for an API-centric e-commerce backend, implemented through unit, integration, and end-to-end tests executed in a CI/CD-oriented workflow. The point of the study is not to argue that one specific toolchain is universally best, nor to present one project as a universal proof of software quality. The narrower and more defensible aim is to investigate whether such a strategy is consistent with recent literature on API-oriented quality assurance, whether the selected evaluation metrics genuinely justify the strategy, and whether the empirical outcomes of the implemented case support the kinds of benefits that the literature tends to associate with structured automated testing.

The case used in this paper is an e-commerce API backend whose higher-risk areas include order and checkout flows, cart behavior, pricing and tax logic, validation rules, and access-sensitive administrative functionality. These areas are useful for study because they represent a mix of business-critical operations, interaction-heavy behavior, and fault types that cannot be captured equally well at a single testing layer. That makes the case suitable for examining a layered QA structure in a way that is practical enough to be measurable and still broad enough to support discussion about quality assurance strategy rather than isolated debugging outcomes.

From that starting point, the paper is guided by the following research questions:

| ID | Research Question |
|---|---|
| RQ1 | How well does a risk-informed multi-level automated testing strategy align with recent literature on quality assurance for API-centric systems? |
| RQ2 | Which metrics most meaningfully justify such a strategy in CI/CD environments: coverage, defect detection, execution time, or test stability? |
| RQ3 | To what extent do the empirical outcomes of the e-commerce API case support the expected benefits described in recent software testing literature? |

These questions are meant to keep the paper balanced between theory and implementation. RQ1 anchors the work in the literature, RQ2 keeps the evaluation from collapsing into a single metric such as coverage, and RQ3 ties the article back to the empirical case without reducing the whole paper to project documentation. The broader goal is to show that a QA approach based on prioritization, layered automation, CI/CD execution, and measured evaluation can be defended as a coherent strategy for API-centric systems, while also making clear where its evidential limits remain.

Keywords: software quality assurance, API testing, automated testing, risk-informed testing, continuous integration, quality gates, flaky tests, e-commerce systems


---

# Literature Review

Recent literature gives fairly strong support to the idea that quality assurance for API-centric systems should be approached as a structured activity rather than as a scattered collection of endpoint checks. The available studies do not point to one magical framework or one universally superior stack. They are less tidy than that. Still, once the papers are read side by side, a few themes keep resurfacing: APIs are operationally central, black-box automation is practical and legitimate, negative scenarios matter, CI changes what "useful testing" looks like, and automated suites have to be trusted, not merely counted. This section follows those themes instead of walking through the papers one by one.

## 1. API Testing as a Primary QA Concern

One of the clearest messages in the literature is that REST APIs should not be treated as a secondary verification target. Ehsan et al. (2022) frame RESTful API testing as a field with its own rationale, challenges, and methodological direction. That framing matters because it moves the discussion away from the older assumption that backend behavior can be covered indirectly and that explicit API verification is just a convenience layer. In API-centric systems, the service interface is often where validation rules, integration faults, error propagation, and business-sensitive behavior become visible in a way that directly affects dependability.

That same concern appears in a more operational form in the work of Martin-Lopez et al. (2021), who present RESTest as an automated black-box testing approach for RESTful APIs. The present paper does not need to adopt RESTest itself for the source to be relevant. Its value lies elsewhere: it helps justify the broader claim that automated black-box verification is not merely acceptable for APIs, but often one of the most practical ways to test them. For a backend where the service surface is the main point of interaction, that claim is hard to ignore.

Corradini et al. (2022) sharpen the picture by focusing not only on nominal behavior, but also on error scenarios. That distinction is more than methodological housekeeping. A system can behave well under valid requests and still become brittle under malformed input, unexpected flow order, inconsistent state, or partial failures. Once that is acknowledged, API testing stops being a question of "does the endpoint return the expected response?" and becomes a question of how the interface behaves when real-world conditions are less cooperative. For transaction-heavy systems, that shift in emphasis is especially important, because error-path quality often matters just as much as happy-path correctness.

Taken together, these papers support three ideas that are central to the present study. First, APIs are an independent QA object rather than a hidden by-product of the architecture. Second, black-box automation is a reasonable and research-supported way to verify them. Third, robustness cannot be reduced to valid outputs on valid inputs. This cluster of ideas provides the conceptual ground for giving serious attention to malformed requests, validation boundaries, and access-sensitive behavior later in the paper.

## 2. Why Layered Testing Makes More Sense Than Single-Level Coverage

The literature does not usually hand over a neat prescription such as "always use unit, integration, and end-to-end tests in this exact ratio." That kind of formula would be too rigid for real systems anyway. Even so, the selected papers strongly suggest that different verification levels expose different kinds of failure. The API testing literature makes clear that service interfaces need explicit functional and robustness verification (Ehsan et al., 2022; Corradini et al., 2022), while DevOps-oriented research shows that evolving systems benefit from regression-oriented automated checks across continuous change cycles (Sartaj et al., 2024). Read together, these studies do not force a single blueprint, but they make a diversified testing structure look far more reasonable than a flat one.

At a smaller scale, logic and validation faults are often cheaper and clearer to isolate in focused tests. Once the view widens, request handling, boundary conditions, and service interaction start to matter more. At the broadest level, realistic flows such as restricted access, navigation-sensitive behavior, and end-to-end consistency become much harder to ignore. These are not interchangeable observation points. They reveal different failure shapes. That is why a single testing layer can look sufficient in the abstract and still leave very practical blind spots in the actual system.

The paper needs to stay measured here. It should not claim that the selected sources prove one exact three-layer architecture. That would be too blunt. A more careful claim is that the literature repeatedly supports diversified verification because different defects become visible under different forms of observation. For the empirical case in this study, that is enough. It justifies combining unit, integration, and end-to-end testing in a backend where logic faults, request-level failures, and access-control defects do not naturally surface at the same level.

## 3. Prioritization and the Logic of Unequal Test Value

A second major theme in the literature is prioritization. This matters because CI environments create pressure by design: frequent execution, limited time, finite compute, and a constant need for timely feedback. Pan et al. (2021), in their systematic review of machine-learning-based test case selection and prioritization, examine methods intended to improve regression testing by selecting or ordering tests so that useful feedback arrives earlier. Their focus is narrower than the present study because it centers on ML-based techniques. Even so, the larger lesson carries over quite well. Testing becomes more realistic, and frankly more defensible, once it admits that not all tests carry the same value at the same moment.

This does not mean the present paper should borrow claims it cannot support. The implemented case does not use machine-learning-based prioritization. What the literature offers instead is methodological permission to treat prioritization as a legitimate testing concern. Under CI constraints, selective emphasis is not a sign of weakness. In many cases it is what prevents the test process from becoming broad, expensive, and strategically vague. That logic supports a risk-informed focus on modules such as checkout, cart behavior, pricing, validation, and access control, because defects in these areas are more likely to have visible operational consequences.

This theme is especially useful because it prevents the paper from slipping into a shallow equation of more tests with better QA. The literature on prioritization reminds us that test quantity and test value are not the same thing. A smaller but better-aimed suite may produce stronger quality feedback than a larger but weakly targeted one. In the context of this study, that distinction matters a great deal. The case is not best understood as an attempt to automate everything evenly. It makes more sense to describe it as an effort to align testing depth with business and technical risk.

## 4. CI/CD as Part of QA Strategy Rather Than Just Execution Infrastructure

The literature on continuous integration helps move the paper past a thin description such as "the tests were run in a pipeline." Soares et al. (2021), through a systematic literature review, show that CI influences software development in ways that reach well beyond build automation. Their findings touch testing discipline, process visibility, feedback cycles, collaboration, and quality-related development practices. For the present study, that matters because CI can be positioned not merely as infrastructure, but as part of the quality strategy itself.

Once testing is moved into CI/CD, a different set of questions starts to matter. How quickly can the suite run? How stable is it from run to run? Which failures should block delivery? Which thresholds are strict enough to be useful without becoming performative? These are not side concerns. They shape what quality enforcement looks like in practice. Sartaj et al. (2024), from the API and DevOps side, reinforce this view by examining automated API testing in an evolving application context. Their work supports the broader point that API verification in changing systems needs repeatable, tool-supported checking rather than occasional manual reassurance.

This strand of literature supports the present paper in two connected ways. First, it justifies treating CI/CD as part of the methodology rather than as a postscript about tooling. Second, it creates a natural bridge to quality gates and metrics. Once test execution becomes continuous, runtime, reproducibility, and failure transparency stop being operational trivia and become part of what "good QA" means. In that sense, pipeline design is not separate from test quality. It shapes what quality assurance can realistically enforce and what kind of evidence it can produce.

## 5. Metrics, Stability, and the Problem of Trust in Automation

If the literature on APIs and CI explains why automated testing matters, the literature on flaky tests explains why automated testing must also be trusted. Parry et al. (2022) make a strong case that flaky tests are not just an irritation or a maintenance nuisance. They threaten the validity of any testing process that assumes failures reflect the state of the system under test rather than instability in the test suite itself. For the present paper, that point is especially valuable. It gives research weight to something that project reports often handle too casually: the test suite is also an object of quality assessment.

That matters because a suite can look respectable on paper while still being operationally unreliable. A suite with acceptable coverage but unstable behavior can produce noisy CI feedback. A suite that occasionally finds defects but fails unpredictably weakens confidence in both the results and the process around them. The survey by Parry et al. (2022) therefore supports the inclusion of stability-oriented measures, such as repeated-run consistency and flaky rate, alongside more familiar indicators such as coverage and execution time.

This cluster of literature also helps keep coverage in proportion. Coverage remains useful, especially when discussing high-risk modules and visible gaps in verification. But once flakiness, defect yield, and CI practicality enter the picture, coverage becomes much harder to treat as sufficient on its own. A more credible evaluative stance is to look at several dimensions together: coverage, defect detection, execution time, and stability. Taken together, they say more about the practical value of automated testing than any single number can manage alone.

## 6. Synthesis: What the Literature Actually Supports

The selected corpus does not dictate one exact framework combination, one fixed architecture, or one universal set of gate thresholds. It would be a mistake to pretend otherwise. What it does provide is a fairly coherent direction. API-centric systems deserve explicit and systematic testing. Automated black-box methods are valid for REST interfaces. Negative and error scenarios belong inside the core testing picture rather than at the margins. CI/CD turns testing from periodic checking into continuous quality control. Prioritization becomes reasonable once time, cost, and feedback speed matter. And, finally, an automated suite should be judged not only by its breadth, but also by its reliability and operational usefulness.

This synthesis leads naturally into the methodological choice of the present study. A risk-informed, multi-level automated QA strategy for an e-commerce API backend can be defended as literature-aligned without claiming that the literature prescribes its exact implementation in every detail. That balance is important. The method should be presented as a practical realization of literature-supported principles in a concrete case, and the empirical results should then be used to examine how well those principles hold up when applied to a real, transaction-heavy API system.


---

# Method

In this paper, the term `Method` is used as the title of the section, while the contents of the section cover the methodological design of the study. This choice fits the structure of a technical article more naturally. In practical terms, the section explains what kind of study is being conducted, what case is being examined, what data are used, how the evaluation is organized, and what limitations affect the interpretation of the findings.

## 1. Research Design

This study uses a literature-grounded empirical case study design. The aim is not to propose a new testing framework or to experimentally prove that one universal QA strategy outperforms all alternatives. The narrower purpose is to examine whether a risk-informed, multi-level automated testing strategy for an API-centric e-commerce backend is defensible in light of recent literature, and whether its empirical outcomes support the benefits that the literature tends to associate with structured QA in continuous delivery settings (Ehsan et al., 2022; Soares et al., 2021; Sartaj et al., 2024).

The study therefore combines two layers of analysis. The first layer is conceptual and literature-oriented. It identifies the main principles supported by recent work on REST API testing, continuous integration, prioritization, and test reliability. The second layer is empirical. It evaluates how those principles were operationalized in the implemented case and what measurable results followed from that implementation. Because of this dual structure, the study is best described as a mixed evaluation rather than as a purely quantitative experiment or a purely qualitative reflection.

## 2. Case Context

The empirical case is an API-centric backend for an e-commerce platform. The system contains business-sensitive and transaction-heavy areas where failure consequences are not trivial. These include order and checkout functionality, cart-related behavior, pricing and tax logic, validation rules, and administrative access control. Such modules are suitable for study because they involve different classes of risk at the same time. Some faults are logic-oriented, some are caused by invalid or malformed input, some emerge at the service interaction level, and some only become visible through realistic end-to-end flows.

This makes the case useful for examining a layered testing strategy. A single level of testing would only partially reflect the quality profile of the system. Validation and field constraints can often be isolated in smaller tests, while endpoint behavior and malformed requests are more visible at the integration level. Access-sensitive or flow-sensitive failures, by contrast, may only appear when the system is exercised in an end-to-end setting. For that reason, the case is suitable not merely as a software project, but as a compact empirical context in which QA strategy can be observed through several complementary forms of verification.

## 3. QA Strategy Under Study

The strategy examined in this paper is built around four connected ideas: prioritization, layered automation, CI/CD execution, and metric-based evaluation. These ideas do not appear in isolation in the literature. They emerge across work on API robustness, selective test emphasis, continuous verification, and trust in automation (Ehsan et al., 2022; Pan et al., 2021; Soares et al., 2021; Parry et al., 2022).

First, testing was organized using a risk-informed logic rather than a uniform coverage logic. Higher-risk modules were given earlier and deeper attention because their failure impact was expected to be greater in both business and operational terms. This does not mean that lower-risk functionality was ignored. It means that testing effort was intentionally distributed unequally, in line with the assumption that different parts of the system do not contribute equally to quality risk.

Second, the automation strategy was multi-level. Unit tests were used for smaller and more isolated checks related to logic and validation behavior. Integration tests were used to verify API interaction, request handling, and resilience against malformed or unexpected inputs. End-to-end tests were used for user-flow-sensitive or access-sensitive behavior, especially in areas where the interaction between authentication state and application navigation had to be verified more realistically. The point of this layering was not formal symmetry. It was functional differentiation: each layer was used where it was most likely to reveal meaningful defects.

Third, the strategy was executed in a CI/CD-oriented workflow. Automated tests were not treated as occasional local checks only. They were integrated into a GitHub Actions pipeline so that repeatability, gate enforcement, and result traceability could be observed as part of the quality process itself. This matters because the study is not only concerned with whether defects can be found, but also with whether the resulting QA process is operationally sustainable and verifiable.

Fourth, the strategy was evaluated through metrics rather than described only narratively. Coverage, defects found, execution time, and stability observations were all treated as evidence dimensions. This was done because no single indicator is sufficient on its own. A suite may cover many lines and still miss critical defects. A suite may find defects and still be too unstable for trustworthy CI feedback. A suite may be stable and still be too slow to be practical in delivery settings. The study therefore treats evaluation as multi-dimensional by design, which is consistent with the broader literature on CI-oriented testing and flaky-test-aware evaluation (Soares et al., 2021; Parry et al., 2022).

## 4. Data Sources

The paper uses several connected sources of evidence. The first group consists of planning and baseline artifacts from earlier course assignments. These provide the original risk assessment, initial strategy, environment setup, and baseline metrics. They are important because they establish what was expected before automation was expanded and before additional empirical findings were observed.

The second group consists of implementation and execution artifacts from the automation stages. These include the automated tests themselves, the CI/CD pipeline configuration, quality gate definitions, test execution evidence, and the resulting reports. These materials are used not as isolated documentation, but as traceable evidence of how the strategy was operationalized.

The third group consists of midterm-stage analytical outputs. These include updated risk observations, added tests, defect findings, coverage gaps, repeated-run stability checks, and comparative metrics collected after the strategy had matured beyond its earlier assignment form. This group is especially important for the results and discussion sections, because it shows not only what was planned, but also what changed after empirical testing exposed new information.

The fourth group is the selected literature corpus. The literature is not treated as decorative background. It functions as the conceptual frame through which the empirical case is interpreted. In that sense, the paper moves in both directions: literature helps justify the strategy, and the empirical case helps test how well that strategy holds in practice.

## 5. Evaluation Dimensions

The study combines quantitative and qualitative evaluation dimensions. The quantitative part focuses on numerical indicators that make the strategy measurable. The qualitative part focuses on whether the testing structure and quality process are coherent, traceable, and aligned with what the literature would lead us to expect.

### 5.1 Quantitative Evaluation

The quantitative evaluation uses four main metric groups.

The first is coverage of high-risk modules. This is used to indicate how much of the critical area of the system is directly exercised by automated tests. Coverage is useful here because it helps identify visible test gaps and uneven verification depth. At the same time, the study does not assume that coverage alone equals QA effectiveness.

The second is defect detection. This dimension tracks the number and distribution of issues observed in relation to the modules under study and, where relevant, their prior risk expectations. This is especially important because one of the central claims behind a risk-informed strategy is that higher-risk areas should justify stronger testing attention and, in many cases, yield more practically relevant findings.

The third is execution time. Runtime matters because a strategy that appears sound in isolation can still become weak in practice if it slows down continuous verification too much. Since the study explicitly includes CI/CD as part of QA design, execution time is not treated as a secondary operational detail. It is part of the evaluation.

The fourth is test stability, including repeated-run observations and flaky behavior where applicable. This dimension is included because unstable suites distort the meaning of test outcomes. If a test fails unpredictably, the value of that test as evidence becomes weaker. For that reason, stability is treated as a necessary part of QA evaluation rather than an optional appendix.

### 5.2 Qualitative Evaluation

The qualitative part of the evaluation focuses on structural adequacy and quality reasoning.

One dimension is layered test structure adequacy. This asks whether the different testing levels are meaningfully mapped to different risk types. The question is not whether the suite contains several layers in name only, but whether each layer is used in a way that makes sense for the defects or behaviors under observation.

Another dimension is CI/CD reproducibility. Here the concern is whether the strategy can be rerun, checked, and interpreted as part of a repeatable quality process rather than as a one-time manual demonstration. The use of pipeline evidence, quality gates, and repeatable execution contributes to this assessment.

The final qualitative dimension is literature alignment. This evaluates whether the chosen QA strategy reflects the major themes emerging from the reviewed literature, such as API robustness, selective emphasis under delivery constraints, continuous verification, and test trustworthiness. This dimension matters because the paper aims to be more than a technical summary. It aims to show that the case strategy can be defended in research terms.

## 6. Mapping Research Questions to Evaluation

The three research questions are linked directly to the evaluation design.

RQ1 is addressed primarily through literature alignment and structural adequacy. It asks whether the strategy under study is broadly consistent with recent work on QA for API-centric systems. For that reason, the main evidence here comes from the relationship between the literature themes and the design choices visible in the case.

RQ2 is addressed primarily through the metric set. Coverage, defect detection, execution time, and test stability are compared not only as measurements, but as different kinds of justification. This allows the paper to move beyond a narrow assumption that one number, such as coverage, can stand in for quality as a whole.

RQ3 is addressed through the empirical outcomes of the case. Here the study compares what the literature would lead us to expect from a structured QA approach with what was actually observed in the implemented e-commerce API setting. This includes both confirmation and mismatch. If the results validate some expected benefits while also revealing unresolved gaps, both findings remain relevant.

## 7. Validity and Limitations

Several limitations shape the interpretation of the study.

First, this is a single-case study. The findings are grounded in one API-centric e-commerce backend and should not be generalized too aggressively to all system types. The value of the study lies more in methodological defensibility and evidence-based interpretation than in universal empirical generalization.

Second, the study does not use a controlled head-to-head comparison against an alternative QA strategy. For example, it does not compare the implemented approach against a no-prioritization condition, an AI-driven test generation strategy, or a separate manually executed baseline under identical conditions. Because of that, the paper can argue that the strategy is literature-aligned and empirically supported, but not that it has been experimentally proven superior to every reasonable alternative.

Third, some of the chosen metrics have known construct limitations. Coverage can reveal test reach, but it cannot prove the absence of important defects. Defect counts can indicate practical value, but they are sensitive to both the design of the suite and the architecture of the system. Execution time depends partly on environment and tooling, not only on test quality. Stability findings, especially in smaller suites, depend on observation windows and repeated-run scope.

Fourth, although the literature corpus is recent and relevant, it supports the principles of the strategy more directly than it supports the exact tool configuration used in the project. This is acceptable for the purpose of the paper, but it should be stated clearly. The paper is ultimately defending a QA approach, not claiming that one exact stack is the inevitable conclusion of the literature.

## 8. Summary of the Method

In summary, the paper studies a risk-informed, multi-level automated QA strategy for an API-centric e-commerce backend through a literature-grounded empirical case design. The strategy is examined through both numerical and structural evidence. Quantitative indicators make the case measurable, while qualitative dimensions make it interpretable in terms of design quality, reproducibility, and academic defensibility. This combined method is intended to support a results section that is data-driven without becoming mechanically metric-only, and a discussion section that is analytical without drifting into unsupported generalization.


---

# Results

This section presents the primary results of the study. The goal here is to stay close to what was actually observed. The section therefore concentrates on the implemented QA structure, the measured outcomes, the relation between expected risk and actual findings, and the degree to which the case reflects the testing principles highlighted in the literature. Fuller interpretation is deliberately held for the discussion.

## 1. Implemented QA Strategy Summary

By the end of the current iteration, the empirical case had moved beyond the Assignment 2 baseline and into a broader, more deliberate QA arrangement. The final setup combined risk-informed prioritization, three levels of automated testing, CI/CD execution, and metric-based evaluation. In practical terms, the suite covered unit, integration, and end-to-end scenarios, with heavier attention given to higher-risk areas such as order handling, payment-related logic, validation, tax calculation, cart behavior, and access-sensitive dashboard flows.

One visible change between the earlier assignment stage and the current state was not simply the number of tests. It was the shape of verification. New tests were added where empirical evidence suggested either higher business sensitivity or lower detectability. That point matters because it shows the strategy did not stay frozen after planning. It was adjusted in response to findings, visible coverage gaps, and defects uncovered during execution.

Table 1 summarizes the growth of the automated suite.

| Test Level | Assignment 2 Baseline | Current Midterm State | Change |
|---|---:|---:|---:|
| Unit | 22 | 26 | +4 |
| Integration | 28 | 30 | +2 |
| E2E | 5 | 7 | +2 |
| Total | 55 | 63 | +8 |

The additional tests were not spread randomly. Four were added at the unit level, two at the integration level, and two at the end-to-end level. That distribution reflects the fact that some of the newly targeted risks were best isolated in smaller logic-oriented checks, while others only became meaningful when request handling or access behavior was exercised in a more realistic setting.

## 2. Metric Outcomes

The quantitative results show a noticeably stronger QA picture than the earlier baseline. The most visible overall change was the increase in measurable `store_app` coverage from 41.00% to 74.41%. That is a meaningful gain, but the number becomes much more useful once it is broken down by high-risk module rather than treated as one clean headline.

Table 2 presents the current coverage profile of the high-risk modules.

| Module | Measured Coverage % | Threshold | Status |
|---|---:|---:|---|
| M1 - Order and Checkout | 72.00 | 70 | Pass |
| M2 - Stripe Payment Integration | 66.67 | 70 | Below threshold |
| M6 - Data Validation | 81.08 | 70 | Pass |
| M8 - Tax Calculation | 94.74 | 70 | Pass |
| M3 - Cart Management | 54.17 | 70 | Below threshold |

This distribution says more than the total coverage figure on its own. The current strategy achieved strong measurable reach in validation and tax-related logic, acceptable but still incomplete reach in order handling, and visibly weaker reach in payment integration and cart behavior. Put differently, the coverage gains were real, but they were not evenly spread across all critical areas.

The broader metric summary is shown in Table 3.

| Metric | Before Midterm | Current State | Change |
|---|---:|---:|---:|
| Total automated tests | 55 | 63 | +8 |
| Total coverage (`store_app`) | 41.00% | 74.41% | +33.41 pp |
| Unit runtime | 2.18s | 1.77s | -0.41s |
| Integration runtime | 1.11s | 1.15s | +0.04s |
| E2E runtime | 5.82s | 9.17s | +3.35s |
| Total local runtime | 9.11s | 12.09s | +2.98s |

The runtime pattern is also worth noting. Unit execution became slightly faster, integration time remained almost unchanged, and the main runtime increase appeared in the end-to-end layer. That does not weaken the suite by itself. What it does is make the cost of deeper behavioral coverage more visible, which is exactly the kind of trade-off that becomes relevant once testing is treated as part of CI/CD practice rather than as an isolated local activity.

For the article version, these results should be accompanied by the following visuals:

- Figure 1: coverage by high-risk module
- Figure 2: before/after comparison of total tests and total coverage
- Figure 3: runtime comparison by test layer

Existing supporting visuals already available in the project materials can be reused:

- [graph_coverage.png](C:\Users\nurym\Documents\AQA mid term\QA_drf-api\docs\graph_coverage.png)
- [graph_defects.png](C:\Users\nurym\Documents\AQA mid term\QA_drf-api\docs\graph_defects.png)
- [graph_runtime.png](C:\Users\nurym\Documents\AQA mid term\QA_drf-api\docs\graph_runtime.png)

## 3. Risk and Defect Alignment

One of the key assumptions behind a risk-informed strategy is that the most business-sensitive or failure-prone areas should justify deeper testing attention and, quite often, produce the most meaningful findings. The empirical case broadly supports that expectation, though not in a perfectly even way.

Table 4 shows the distribution of defects across modules.

| Module | Risk Level | Defects Found | Current Count |
|---|---|---|---:|
| M1 - Order and Checkout | Critical | D-004, MT-DEF-01 | 2 |
| M2 - Stripe Payment Integration | Critical | No live defect reproduced | 0 |
| M6 - Data Validation | Critical | D-005 | 1 |
| M8 - Tax Calculation | High | D-002, D-003, MT-DEF-01 | 3 |
| M3 - Cart Management | High | D-001 | 1 |
| M7 - Authentication / Admin Setup | Medium | D-006 | 1 |

The highest number of confirmed issues appeared in tax-related and order-related areas, which is consistent with the expectation that transaction-sensitive logic deserves heavier scrutiny. Validation also produced a meaningful defect, while cart behavior revealed an ambiguity that remained open. Payment integration is the least tidy case in the table. It stayed high-impact, yet its defect evidence remained weaker than expected because the current suite covers failure-oriented branches more clearly than real payment success behavior.

The updated risk reassessment further shows that empirical testing changed the risk picture itself instead of merely confirming the original plan. Tax calculation moved upward in importance after two serious crash modes were confirmed. Validation risk was moderated once detectability improved. Payment risk, by contrast, remained effectively unchanged because its impact stayed high while measurable confidence remained incomplete.

Table 5 summarizes the updated risk positions.

| Module | Original Risk Score | Updated Risk Score | Main Reason for Reassessment |
|---|---:|---:|---|
| M1 - Order and Checkout | 20 | 18 | Negative-path detectability improved, though duplicate-order concern remains open |
| M2 - Stripe Payment Integration | 15 | 15 | Impact remains high and measurable coverage is still below threshold |
| M6 - Data Validation | 16 | 14 | Validation paths became more visible after new unit coverage |
| M8 - Tax Calculation | 12 | 16 | Real high-impact crash modes were confirmed empirically |
| M3 - Cart Management | 12 | 13 | No crash under repeated requests, but detectability remains weak |

This part of the results is especially relevant to RQ3 because it shows that the case did not simply confirm earlier assumptions. It revised them. Some modules became less uncertain after testing was expanded, while others turned out to be more problematic than the initial planning had suggested.

## 4. Stability, Runtime, and CI/CD Outcomes

Stability observations were positive within the repeated-run sample. The monitored integration and end-to-end cases did not display flaky behavior across the observed reruns, and the measured flaky rate in the sample was 0.00%.

Table 6 summarizes the stability observations.

| Metric | Value |
|---|---:|
| Repeated integration runs observed | 5 |
| Repeated E2E runs observed | 5 |
| Flaky tests observed | 0 |
| Flaky rate in repeated sample | 0.00% |

This does not prove that the suite is universally stable under all environments or future changes. It would be too strong to claim that. What it does show is that, within the current observation window, the added tests did not introduce visible instability. That matters because the value of a CI-oriented suite depends not only on the presence of tests, but also on whether those tests can be trusted from run to run, which is exactly the concern raised in the flaky-test literature (Parry et al., 2022).

The quality gate outcomes were also broadly positive at the current stage.

Table 7 presents the latest gate evaluation.

| Gate | Threshold | Current Result | Evaluation |
|---|---:|---:|---|
| Test pass rate | 100% | 63/63 passed locally | Appropriate |
| Total coverage | 70% | 74.41% | Appropriate |
| High-risk module coverage | 70% | M2 = 66.67%, M3 = 54.17% | Strict but informative |
| Critical failures allowed | 0 | 0 open blocking failures after fixes | Appropriate |

The interesting point here is that not all gates behaved in the same way. The overall coverage threshold was satisfied, but the module-level thresholds kept unresolved weak spots visible in payment and cart-related functionality. In that sense, the gate structure did not merely report success. It also preserved visibility into what remained under-tested, which is precisely what one would want from CI-based quality control rather than a pass-friendly facade (Soares et al., 2021).

Pipeline evidence from the current workflow run further supports the operational side of the strategy. The updated test suite completed successfully in the CI environment, and the workflow artifacts provide traceable confirmation that the expanded test structure is not only locally executable but also reproducible in pipeline form. For the article version, this should be presented as a compact screenshot-based figure rather than a long operational narrative.

## 5. Literature-Alignment Results

Beyond the raw numbers, the results also show how the implemented case matches the core ideas emphasized in the literature reviewed earlier. The point here is not to claim that the case reproduces every research finding in neat miniature. It is simply to show where the case behaves in ways the literature would lead us to expect.

Table 8 summarizes that alignment.

| Literature-Supported Principle | Implemented in the Case | Observed Outcome |
|---|---|---|
| API-centric systems require robustness-oriented testing | Yes | Invalid-input and failure-path testing revealed meaningful defects and controlled-error behavior |
| Layered testing is more useful than a single-level suite | Yes | Different defect types became visible at unit, integration, and E2E levels |
| Prioritization is necessary under practical delivery constraints | Yes | High-risk modules received deeper attention and produced most of the meaningful findings |
| CI/CD strengthens repeatability and traceability of QA | Yes | The suite was executed through pipeline-based verification and quality gates |
| Stability matters for trust in automated testing | Yes | Repeated-run sample showed no observed flakiness after the current fixes |

These outcomes line up well with the main directions identified in the reviewed studies. The emphasis on robustness-oriented API behavior reflects the concerns raised by Ehsan et al. (2022) and Corradini et al. (2022). The value of layered verification is consistent with the distinction between different observation levels implied across the API and DevOps literature (Martin-Lopez et al., 2021; Sartaj et al., 2024). The role of CI/CD in traceability and repeatability sits comfortably beside the process-oriented view described by Soares et al. (2021), while the stability observations speak directly to the concerns about trust in automation raised by Parry et al. (2022).

Taken together, these results speak most directly to RQ1. They show that the case is not only operationally complete enough to run. It is also structurally consistent with the main testing principles identified in the literature: API sensitivity, layered verification, selective emphasis, CI-based execution, and attention to trustworthiness.

## 6. Primary Result Pattern Across the Research Questions

To keep the article logic visible, the primary findings can be mapped back to the research questions at a high level.

| Research Question | Primary Result Signal |
|---|---|
| RQ1 | The implemented QA structure is broadly consistent with the literature on API-centric testing, CI-based verification, prioritization, and stability-aware automation |
| RQ2 | Coverage was useful but not sufficient on its own; defect distribution, module-level gaps, runtime, and stability gave a stronger justification of the strategy |
| RQ3 | The empirical case largely supported the expected benefits of structured automation, but it also exposed unresolved gaps in payment and cart-related areas |

At the results level, then, the study shows a mixed but coherent picture. The strategy improved measurable coverage, expanded the suite in a targeted way, found and fixed meaningful defects, and remained stable enough to support repeatable execution. At the same time, the results did not erase all uncertainty. Some critical modules still remain less visible than others, which is exactly why the next section needs to move beyond headline numbers.


---

# Discussion

The results show a QA strategy that became stronger, more visible, and more defensible over time, but not one that suddenly turned into a complete proof of software quality. That distinction matters. The case does not suggest that layered automation, CI/CD execution, and metric-driven evaluation automatically guarantee a reliable system. What it does suggest is something more measured and, arguably, more useful: when these elements are combined under a risk-informed structure, they produce a QA process that is easier to justify, easier to trace, and harder to mistake for shallow box-ticking.

This section interprets the findings through the three research questions. From there, it moves into practical implications, limitations, and threats to validity. The aim is to stay close to the evidence while still saying something meaningful about what the case adds to a wider QA discussion.

## 1. Discussion of RQ1

RQ1 asked how well a risk-informed multi-level automated testing strategy aligns with recent literature on quality assurance for API-centric systems. The short answer is that the alignment is strong in principle, though less absolute when it comes to exact implementation details.

The reviewed literature keeps returning to a familiar cluster of ideas: APIs need explicit robustness-oriented verification (Ehsan et al., 2022; Corradini et al., 2022), a single testing level leaves practical blind spots (Martin-Lopez et al., 2021; Sartaj et al., 2024), CI changes what makes a test process useful in practice (Soares et al., 2021), and automated suites are only as valuable as the extent to which they can be trusted (Parry et al., 2022). The empirical case fits that general picture rather well. The testing structure was layered rather than flat, attention moved toward higher-risk areas instead of being spread evenly, and CI/CD execution was treated as part of the QA design rather than as a deployment-side convenience.

What makes this alignment more convincing is that the case did not simply borrow the language of the literature and leave it at that. The same distinctions that appear in the papers also became visible in the project evidence. Unit tests were the most effective place to isolate narrow validation and failure-branch logic. Integration tests carried more weight in malformed requests, resilience checks, and endpoint-level behavior. End-to-end tests became necessary where access-sensitive and navigation-dependent faults had to be exercised in a more realistic setting. That separation was not cosmetic. It reflected real differences in defect visibility.

Still, the case also reminds us that literature alignment is not the same thing as methodological perfection. Some of the reviewed studies investigate automated API testing in forms that are broader, more generator-oriented, or more experimentally controlled than what was implemented here (Martin-Lopez et al., 2021; Corradini et al., 2022). The present study is narrower and more practice-driven. It is more accurate to describe it as a grounded implementation of literature-supported principles than as a replication of any one published method.

So, in response to RQ1, the case supports the view that a risk-informed, multi-level strategy is not only defensible for API-centric systems, but also structurally consistent with the broader direction of recent testing research. The important qualifier is that this consistency applies more clearly to the logic of the approach than to the exact stack or exact project arrangement.

## 2. Discussion of RQ2

RQ2 asked which metrics most meaningfully justify such a strategy in CI/CD environments: coverage, defect detection, execution time, or test stability. The results suggest that no single metric can do that job alone, though some clearly carry more explanatory weight than others when taken in isolation.

Coverage was useful, but it was not decisive by itself. The jump from 41.00% to 74.41% is substantial and does show that the suite gained reach across important logic. Even so, the module-level breakdown tells a more candid story than the aggregate number. Payment integration and cart management remained below the 70% threshold despite the stronger overall figure. That immediately exposes one weakness of leaning too heavily on total coverage: it can make the suite look more complete than it actually is in the areas where confidence matters most.

Defect detection turned out to be more practically revealing. Meaningful defects and risk-relevant failures were found in tax, order, validation, and access-control areas, which gives the strategy stronger support than coverage alone could offer. Defect evidence is not flawless, because the number of observed issues depends on both test design and system behavior, but it speaks more directly to the practical yield of testing than reach alone. In the present case, it also helped confirm that several high-risk modules did in fact justify deeper attention, which is exactly what a risk-informed strategy is supposed to accomplish.

Execution time mattered in a quieter but still non-trivial way. The suite remained operationally usable, yet the runtime increase in the end-to-end layer made the cost of deeper behavioral coverage visible. That is not a contradiction. It is the trade-off one would expect in a CI-oriented testing strategy. A suite that becomes better at exposing access-sensitive or realistic workflow defects will usually pay for that depth with longer E2E execution. The point is not to eliminate that cost altogether. It is to keep it visible, proportionate, and worth the feedback it buys.

Test stability may have been the least dramatic metric on paper, but it is arguably the one that protects the meaning of the others. A flaky suite can distort defect interpretation, delay pipeline feedback, and undermine confidence in the automation process itself. The repeated-run sample in this case did not reveal flaky behavior after the relevant fixes, which strengthens the credibility of the results. That does not mean the suite is permanently stable. It does mean that, within the observed window, the strategy produced execution stable enough to keep its other metrics interpretable. That point matters a great deal once Parry et al. (2022) are taken seriously: unstable tests do not just inconvenience teams, they weaken the evidential value of the whole setup.

Taken together, the findings point to a balanced answer to RQ2. Coverage is necessary, but it is not the strongest metric on its own. Defect detection gives the clearest practical signal, especially when mapped back to risk. Stability determines whether those signals can be trusted. Execution time determines whether the strategy remains viable inside CI/CD. So the most meaningful justification of the approach does not come from one standout number. It comes from the interaction among these four dimensions.

## 3. Discussion of RQ3

RQ3 asked to what extent the empirical outcomes of the e-commerce API case support the benefits that the literature tends to associate with structured automated testing. The answer is largely positive, though not in a neat or uniformly flattering way.

Several expected benefits did appear rather clearly. First, layered automation improved defect visibility across different classes of behavior, which fits the logic implied by the API-testing and DevOps literature (Ehsan et al., 2022; Sartaj et al., 2024). Not all faults surfaced at the same level, and the fact that different layers uncovered different defect types supports the idea that mixed verification is more suitable than a single-level approach for API-centric systems. Second, CI/CD integration and quality gates gave the process repeatability and traceability instead of leaving it as a local or one-off demonstration, which is very much in line with the process-oriented effects described by Soares et al. (2021). Third, the risk-informed logic helped direct effort toward modules where the operational and business consequences of failure were more serious.

At the same time, the case also makes it clear that a strategy can be structurally sound and still remain incomplete in places that matter. Payment integration is the clearest example. It retained high business impact, yet its measurable visibility remained weaker than some other critical modules because the implemented tests covered failure branches more clearly than full live success behavior. Cart management showed a different version of the same problem: it was not the most dramatic failure area, but it stayed under-covered and retained an unresolved ambiguity. These are not side notes. They matter precisely because they prevent the paper from sounding cleaner than the evidence allows.

In that sense, the case supports the literature in a realistic rather than idealized way. The expected benefits did appear: better detectability, broader structured verification, more transparent measurement, and a more reproducible QA process. But the case also shows that literature-supported strategy does not erase the need for critique. Some critical paths became much more visible. Others remained only partially exercised. The empirical picture improved, but it did not become uniformly complete, and that is part of the result rather than a footnote to it.

## 4. Why the Strategy Is Defensible

One point is worth stating plainly. The defensibility of the implemented approach does not rest on the claim that the exact stack used in the project is universally optimal. That would be too strong and not especially credible. The stronger claim is narrower: the project implemented a QA strategy whose underlying principles are well aligned with recent literature, and the empirical case produced outcomes that broadly support those principles.

That distinction matters because it changes how the paper should be read. The contribution is not "this exact toolchain should always be used." The contribution is that the case offers a coherent example of how risk prioritization, layered automation, CI execution, quality gates, and multi-dimensional metrics can be combined into a defensible QA workflow for a transaction-heavy API system. That is a methodological contribution more than a tooling argument.

It is also why the paper remains valid even without a head-to-head experimental comparison. Its value is interpretive and design-oriented. It shows how a practical QA implementation can be discussed in research terms without pretending that one project settles every broader question about testing strategy.

## 5. Practical Implications

The findings suggest several implications for QA work in API-centric systems.

First, critical modules should not be treated as equal by default. The results support the view that testing effort gains more value when it is distributed in a risk-aware way rather than spread evenly for appearance's sake.

Second, layered automation is worth preserving even when it makes the overall test architecture less simple. In this case, the layers did not duplicate each other mechanically. They exposed different kinds of problems and, together, produced a fuller quality picture than any one of them could have delivered alone.

Third, quality gates are most useful when they do more than signal pass or fail. The module-level coverage gate did exactly that. It allowed the suite to improve overall while still keeping weak spots in payment and cart-related behavior visible.

Fourth, stability deserves active attention even when the suite currently looks healthy. A clean repeated-run sample is encouraging, but trust in automation can erode quickly if flakiness begins to appear and teams notice only after CI feedback has already become noisy.

## 6. Limitations

Several limitations shape how far the findings can be taken.

The first is scope. This is a single-case study built around one API-centric e-commerce backend. It offers grounded evidence, but it does not justify broad generalization to every software domain or testing environment.

The second is the absence of a controlled comparison group. The study did not compare the implemented strategy against a deliberately flatter approach, against a no-prioritization baseline, or against an alternative AI-assisted workflow under identical conditions. Because of that, the paper can show that the chosen strategy is defensible and supported, but not that it is experimentally superior to every plausible alternative.

The third limitation concerns metric interpretation. Coverage is informative, but not sufficient. Defect counts are practically useful, but they are shaped by where tests were aimed and by how the system behaves internally. Runtime is partly environment-dependent. Stability findings depend on the observation scope and rerun window. None of this makes the metrics invalid, but it does narrow what they can honestly claim.

The fourth limitation is that the literature supports the principles behind the strategy more directly than it supports any single exact tool choice. The paper can justify the shape of the QA approach more confidently than it can justify every implementation detail as uniquely best.

## 7. Threats to Validity

Because the paper is meant to read as a technical article rather than a project memo, the main threats to validity should be stated explicitly.

### 7.1 Construct Validity

There is a risk that the chosen metrics do not fully capture what QA effectiveness means in practice. Coverage, defect counts, execution time, and stability are all relevant, but they remain proxies rather than complete measures of software quality.

### 7.2 Internal Validity

Some findings may be influenced by the specific architecture of the system and by the way the suite evolved over time. The relationship between prior risk assumptions and observed defects is therefore plausible and evidence-based, but not experimentally isolated from all project-specific factors.

### 7.3 External Validity

The findings are more likely to transfer to other API-centric, transaction-heavy systems than to software in general. Systems with very different architectures, delivery pressures, or quality constraints may require a different testing balance and a different metric emphasis.

### 7.4 Reliability of Observation

The repeated-run sample was sufficient to observe the absence of flakiness in the monitored cases, but it was still limited. A longer observation window or a more varied execution environment could reveal stability issues that were not visible in the current sample.

## 8. Closing Interpretation

Overall, the case points to a grounded conclusion rather than a grand one. A risk-informed, multi-level automated testing strategy executed through CI/CD and assessed through several complementary metrics can provide a strong and research-defensible QA structure for an API-centric transactional system. In this study, the strategy did not produce uniform certainty across all critical modules, and it did not remove the need for further work in payment and cart-related areas. Even so, it moved the QA process away from broad but shallow verification and toward a more selective, more traceable, and more credible form of quality assurance.

That conclusion is intentionally modest. The case does not claim to settle the question of the best possible QA design. What it does offer is a realistic, measurable example of how literature-supported testing principles can be translated into structured practice and then examined through both metrics and analysis.


---

# References

Corradini, D., Zampieri, A., Pasqua, M., Viglianisi, E., Dallago, M., & Ceccato, M. (2022). Automated black-box testing of nominal and error scenarios in RESTful APIs. *Software Testing, Verification and Reliability, 32*(2), e1808. [https://doi.org/10.1002/stvr.1808](https://doi.org/10.1002/stvr.1808)

Ehsan, A., Abuhaliqa, M. A., Catal, C., & Mishra, D. (2022). RESTful API testing methodologies: Rationale, challenges, and solution directions. *Applied Sciences, 12*(9), 4369. [https://doi.org/10.3390/app12094369](https://doi.org/10.3390/app12094369)

Martin-Lopez, A., Segura, S., & Ruiz-Cortes, A. (2021). RESTest: Automated black-box testing of RESTful web APIs. In *Proceedings of the 30th ACM SIGSOFT International Symposium on Software Testing and Analysis* (pp. 541-545). [https://doi.org/10.1145/3460319.3469082](https://doi.org/10.1145/3460319.3469082)

Parry, O., Kapfhammer, G. M., Hilton, M., & McMinn, P. (2022). A survey of flaky tests. *ACM Transactions on Software Engineering and Methodology, 31*(1), Article 17. [https://doi.org/10.1145/3476105](https://doi.org/10.1145/3476105)

Pan et al. (2021). *Test case selection and prioritization using machine learning: A systematic literature review*. arXiv preprint arXiv:2106.13891.

Sartaj, H., Ali, S., & Gjoby, J. (2024). *REST API testing in DevOps: A study on an evolving healthcare IoT application*. arXiv preprint arXiv:2410.12547.

Soares, E., Sizilio, G., Santos, J., da Costa, D. A., & Kulesza, U. (2021). *The effects of continuous integration on software development: A systematic literature review*. arXiv preprint arXiv:2103.05451.

## Notes for Final Cleanup

- The entry for `Pan et al. (2021)` should be replaced with the full author list if that metadata is extracted later from the source PDF or a trusted index.
- If the final submission requires one strict citation style such as APA 7 or IEEE, the formatting of all entries should be normalized at the end rather than adjusted piecemeal during drafting.


---

