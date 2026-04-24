# Method Draft

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
