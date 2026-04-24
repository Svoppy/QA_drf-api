# Results Draft

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
