# Article Rebuild Plan

## 1. New Research Frame

The article must be rebuilt around a different center of gravity.

The current draft still places too much narrative weight on the implemented project itself.
That is not the right academic shape for the final paper.

The project should be treated as:

- an empirical case
- a controlled practical environment
- a reproducible platform for evaluating a QA approach

The project should not be treated as:

- the main subject of the paper
- a globally important product
- a unique software artifact that deserves article-level attention by itself

The real subject of the paper should be:

- the validity of a risk-informed, multi-level automated QA methodology
- for API-centric and transaction-heavy systems
- under CI/CD constraints
- evaluated through measurable QA outcomes

In other words, the paper should answer:

- whether this QA method is academically defensible
- whether it is practically justified for similar systems
- which metrics actually support that justification

The project is only the vehicle through which the method is evaluated.

---

## 2. Core Narrative Shift

### Old narrative to abandon

- we had a project
- we implemented tests for it
- we measured what happened
- we explain why our implementation is good

### New narrative to build

- recent literature supports several principles for QA in API-centric systems
- from those principles, a coherent testing methodology can be derived
- that methodology can be instantiated in a practical case
- the case then serves as an empirical environment for evaluating the methodology
- the article discusses what the case confirms, what it does not confirm, and where the method remains limited

This shift is essential because it changes the paper from a project-centered write-up into a method-centered technical study.

---

## 3. Revised Article Purpose

The final article should aim to do the following:

- synthesize recent literature on QA for API-centric systems
- derive a defensible testing methodology from that literature
- define a reproducible evaluation design
- use the implemented e-commerce API case as an empirical validation environment
- evaluate the method with quantitative and qualitative evidence
- discuss what the evidence does and does not justify

The article should not try to prove that:

- the project itself is special
- the exact toolchain is universally best
- one case proves the superiority of the method in all contexts

The article should try to show that:

- the chosen QA method is literature-aligned
- the method is reproducible
- the method is practically useful in a realistic API-centered case
- the method produces interpretable evidence

---

## 4. Revised Research Questions

The earlier research questions were close, but they still leaned too directly on the project.
They should now be tightened around the methodology.

### Proposed final research questions

| ID | Research Question |
|---|---|
| RQ1 | What principles from recent literature justify a risk-informed, multi-level automated QA methodology for API-centric systems? |
| RQ2 | How can such a methodology be operationalized and evaluated in a reproducible empirical case? |
| RQ3 | To what extent do the observed metrics and defect patterns support the practical validity of the methodology in a transaction-heavy API context? |

### Why these work better

`RQ1`

- belongs mainly to Introduction and Literature Review
- asks for theoretical justification
- is not project-centered

`RQ2`

- belongs mainly to Method
- makes reproducibility central
- shifts focus from implementation details to methodological design

`RQ3`

- belongs mainly to Results and Discussion
- lets the project appear as evidence
- keeps the method, not the repository, at the center

---

## 5. New Role of Each Section

Each section must stay inside its own responsibility.
The new draft must avoid overlap between sections.

### Abstract

Role:

- summarize the entire paper after it is complete

Must include:

- problem
- objective
- method
- main findings
- implication

Must not include:

- excessive case detail
- long background
- unexplained metrics

### Introduction

Role:

- define the problem space
- justify why the topic matters
- position the article
- state research questions

Must focus on:

- QA challenges in API-centric, transaction-heavy systems
- the need for systematic, layered, and measurable QA
- why method validation matters

Must not focus on:

- detailed project description
- test counts
- results
- long literature summaries

### Literature Review

Role:

- synthesize the research base
- derive the methodological need
- create the conceptual foundation for the method

Must focus on:

- API testing as a serious QA concern
- black-box and error-oriented API testing
- layered testing logic
- prioritization under CI/CD constraints
- CI/CD as continuous verification
- flaky tests and trustworthiness
- metrics as evidence, not decoration

Must not focus on:

- what we implemented
- our project timeline
- result commentary

### Method

Role:

- define the research design
- define the methodology
- make the empirical design reproducible

Must focus on:

- research design
- methodological logic
- case selection rationale
- data sources
- operationalization of the method
- evaluation dimensions
- validity and limitations of the method

Must mention the project only as:

- empirical case environment
- system under observation
- platform for applying the methodology

Must not read like:

- a devlog
- setup instructions
- a repository walkthrough

### Results

Role:

- present evidence
- show what the method produced when applied

Must focus on:

- coverage values
- defect findings
- module-level patterns
- runtime
- stability
- quality-gate outcomes
- risk reassessment outcomes

Must not focus on:

- why the results matter in theory
- justification already handled in literature review
- broad interpretation

### Discussion

Role:

- interpret results
- answer research questions
- explain cause and effect
- define what conclusions are justified

Must focus on:

- whether the method is supported by the observed evidence
- which metrics turned out to matter most
- where the method worked well
- where the method stayed incomplete
- limitations
- threats to validity
- practical implications

Must not repeat:

- long raw result tables
- literature survey content
- implementation detail already described in Method

### References

Role:

- provide the exact literature base used by the paper

Must be:

- real
- cited in text
- sorted
- consistent in APA 7

---

## 6. Revised Section Blueprint

## 6.1 Introduction

### Intended flow

Paragraph 1:

- API-centric systems as operationally sensitive software
- transaction-heavy domains as high-consequence environments

Paragraph 2:

- QA challenge is not just "testing exists"
- QA challenge is method selection under uneven risk and continuous delivery

Paragraph 3:

- literature suggests structured, layered, and risk-aware verification
- therefore there is a methodological problem worth studying

Paragraph 4:

- objective of the article:
  - to evaluate a literature-grounded QA methodology
  - using a practical e-commerce API case as empirical environment

Paragraph 5:

- research questions
- keywords

### Project visibility in Introduction

Minimal.
Only mention the case as:

- an API-centric e-commerce backend
- used as empirical context

No detailed module walkthrough here.

---

## 6.2 Literature Review

### Intended flow

Block 1:

- REST/API testing as a distinct QA problem
- supported by:
  - `RESTful API Testing Methodologies`
  - `RESTest`
  - `STVR22`

Block 2:

- Why nominal testing is insufficient
- error-path and robustness testing as first-class concerns
- supported by:
  - `STVR22`
  - `RESTful API Testing Methodologies`

Block 3:

- layered verification as a practical necessity
- different risks become visible at different test levels
- supported indirectly by:
  - `RESTest`
  - `STVR22`
  - `REST API Testing in DevOps`

Block 4:

- prioritization and selective testing under CI pressure
- supported by:
  - `Test Case Selection and Prioritization Using Machine Learning`

Block 5:

- CI/CD as part of the QA method, not just execution infrastructure
- supported by:
  - `The Effects of Continuous Integration on Software Development`
  - `REST API Testing in DevOps`

Block 6:

- flaky tests, stability, and trust in test evidence
- supported by:
  - `A Survey of Flaky Tests`

Block 7:

- synthesis:
  - literature supports a method
  - not one exact toolchain
  - therefore the paper evaluates a methodology rather than a repository

### Project visibility in Lit Review

None, except maybe one short bridge sentence at the end.

---

## 6.3 Method

This section should become the real center of the paper.

### Intended subsections

#### 1. Research design

- literature-grounded empirical case study
- mixed evaluation:
  - quantitative metrics
  - qualitative methodological assessment

#### 2. Methodological proposition under study

- define the method in abstract form:
  - risk-informed prioritization
  - multi-level automation
  - CI/CD execution
  - quality gates
  - metric-based evaluation

This is critical:
the method must be presented before the case.

#### 3. Case selection and context

- explain why the selected system is a suitable empirical platform:
  - API-centric
  - transaction-heavy
  - contains heterogeneous risk classes
  - supports unit, integration, and E2E verification

This is where the project belongs most explicitly.

#### 4. Operationalization

- how the abstract method was implemented in the case
- not tool marketing
- not devlog
- just enough detail for reproducibility

This subsection can include:

- test levels used
- role of each level
- CI/CD integration
- quality gates
- data collection logic

#### 5. Evaluation dimensions

- high-risk coverage
- defect yield
- execution time
- stability
- layered structure adequacy
- CI/CD reproducibility
- literature alignment

#### 6. Validity and limitations of the method

- one case
- no control group
- metric limitations
- domain transfer limitations

### Project visibility in Method

High, but only as:

- empirical platform
- case environment
- methodological instance

Not as the star of the paper.

---

## 6.4 Results

### Intended subsections

#### 1. Method implementation summary

- very concise
- enough to orient the reader

#### 2. Quantitative outcomes

- test growth
- coverage
- runtime
- defect counts
- flaky/stability observations

#### 3. Method effectiveness in high-risk areas

- module-level gaps
- defect concentration
- reassessment of risk

#### 4. Quality gate and CI/CD outcomes

- gate pass/fail status
- what they exposed

#### 5. Summary of findings for each RQ

- brief mapping only

### Project visibility in Results

Moderate.
The section should present observations from the case, but always as evidence about the method.

Each result should answer:

- what this says about the methodology

not:

- what this says about the uniqueness of the project

---

## 6.5 Discussion

### Intended structure

#### RQ1 discussion

- does the method align with literature?
- where is alignment strong?
- where is alignment partial?

#### RQ2 discussion

- how reproducible and methodologically clean is the operationalization?
- what parts of the method are most transferable?

#### RQ3 discussion

- do the metrics and defects support the method?
- which metrics matter most?
- what remains uncertain?

#### Practical implications

- for QA in similar API-centric systems

#### Limitations

- methodological limitations
- metric limitations
- transferability limits

#### Threats to validity

- construct
- internal
- external
- observation reliability

### Project visibility in Discussion

Only as evidence base.
The section should interpret what the case allows us to say about the method.

---

## 7. Revised Use of Literature

The papers in `papers/` should now be used by function, not merely by topic.

| Paper | Best function in new article |
|---|---|
| `RESTful API Testing Methodologies` | justify API testing as serious QA problem |
| `RESTest` | justify automated black-box API verification |
| `STVR22` | justify nominal + error scenario coverage |
| `REST API Testing in DevOps` | justify testing in evolving CI/CD contexts |
| `The Effects of Continuous Integration on Software Development` | justify CI/CD as quality process |
| `A Survey of Flaky Tests` | justify stability and trust as evaluation dimensions |
| `Test Case Selection and Prioritization Using Machine Learning` | justify prioritization as methodologically legitimate |

The literature should not be used to justify:

- Django specifically
- our exact tools as universally best
- exact thresholds unless we can defend them from evidence

---

## 8. What Must Be Removed from the Current Draft

The rebuilt article should remove or reduce:

- language that makes the project sound like the main research object
- repeated references to the repository as if it were itself the contribution
- overly detailed case-specific flow descriptions in early sections
- implementation-oriented phrasing in Literature Review
- result-like claims in Introduction
- discussion-like claims in Results
- any suggestion that one project proves the methodology universally

---

## 9. What Must Be Added or Strengthened

- clearer methodological proposition in Method
- sharper distinction between method and case
- more explicit reproducibility logic
- clearer statement that the case is an empirical validation environment
- stronger RQ-to-section alignment
- stronger chapter discipline:
  - Introduction introduces
  - Lit Review synthesizes
  - Method defines
  - Results shows
  - Discussion interprets

---

## 10. Writing Order for the Rebuild

### Step 1

Freeze the new article frame:

- method-centered
- case-supported
- literature-grounded

### Step 2

Rewrite:

- Introduction
- Literature Review
- Method

before touching Results and Discussion.

### Step 3

Rebuild Results so that every table and graph is framed as evidence about the method.

### Step 4

Rewrite Discussion from the research questions outward, not from the project inward.

### Step 5

Only after all of that:

- finalize References
- write Abstract

---

## 11. Desired Final Shape of the Article

If the rebuild is done correctly, the final paper should read like this:

- the literature points to a promising QA methodology
- the methodology is defined clearly
- the methodology is instantiated in a suitable empirical case
- the case generates evidence
- the evidence is used to assess the methodology
- the final conclusions remain measured, valid, and transferable only where justified

That is the article shape we should now move toward.
