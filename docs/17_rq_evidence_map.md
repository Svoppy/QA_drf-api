# Research Question to Evidence Map

This file links each research question to the exact evidence types, metrics, and result patterns used in the draft paper. Its purpose is simple: keep the logic between the questions, the method, and the results explicit.

## 1. RQ-Level Mapping

| Research Question | Main Evidence Type | Primary Metrics / Analytical Inputs | Main Sections That Answer It |
|---|---|---|---|
| RQ1. How well does a risk-informed multi-level automated testing strategy align with recent literature on quality assurance for API-centric systems? | Qualitative and structural | literature themes, test-layer structure, CI/CD integration, literature-alignment table | Introduction, Literature Review, Method, Results 5, Discussion 1 |
| RQ2. Which metrics most meaningfully justify such a strategy in CI/CD environments: coverage, defect detection, execution time, or test stability? | Mixed, metric-centered | total coverage, module-level coverage, defect counts, execution time, flaky rate, quality gates | Method 5, Results 2, Results 4, Discussion 2 |
| RQ3. To what extent do the empirical outcomes of the e-commerce API case support the expected benefits described in recent software testing literature? | Mixed, case-centered | defects by module, updated risk scores, coverage gaps, stability observations, CI/CD evidence, literature-alignment table | Results 3, Results 4, Results 5, Discussion 3 |

## 2. Metric-to-RQ Mapping

| Metric / Evidence Dimension | RQ1 | RQ2 | RQ3 | Why It Matters |
|---|---|---|---|---|
| Total coverage | Partial | Strong | Partial | Useful baseline signal, but too coarse to justify strategy on its own |
| High-risk module coverage | Moderate | Strong | Strong | Shows whether critical areas were actually reached, not just the codebase in aggregate |
| Defect detection by module | Partial | Strong | Strong | Shows practical testing yield and whether risk emphasis was justified |
| Execution time | Partial | Strong | Partial | Shows whether the strategy stays viable inside CI/CD |
| Flaky rate / repeated-run stability | Moderate | Strong | Moderate | Protects trust in the rest of the metrics and in the pipeline signal |
| Layered test structure | Strong | Partial | Moderate | Shows whether different test levels were used for meaningfully different risks |
| CI/CD run evidence and quality gates | Strong | Strong | Moderate | Shows reproducibility, enforcement, and operational discipline |
| Updated risk reassessment | Moderate | Partial | Strong | Shows how empirical evidence changed the original planning assumptions |
| Literature-alignment table | Strong | Partial | Strong | Connects case behavior to claims from the reviewed literature |

## 3. Result Patterns by Research Question

| Research Question | Main Result Pattern |
|---|---|
| RQ1 | The implemented QA structure is broadly aligned with literature on API robustness, layered verification, prioritization under delivery constraints, CI-based verification, and trust-aware automation |
| RQ2 | Coverage was useful but insufficient on its own; defect yield, module-level gaps, runtime, and stability together justified the strategy more convincingly |
| RQ3 | The empirical case supported the expected benefits of structured automation, but it also exposed unresolved weaknesses in payment and cart-related areas |

## 4. Sections to Revisit During Final Merge

| Section | What to verify during final article assembly |
|---|---|
| Introduction | Research questions must appear exactly as used in Method and Discussion |
| Method | Evaluation dimensions must stay aligned with the evidence in Results |
| Results | Tables should remain evidence-first and avoid premature interpretation |
| Discussion | Each RQ answer should explicitly refer back to the evidence already shown |
| Abstract | Must summarize RQ focus, method type, main findings, and limitations only after the full paper is stable |
