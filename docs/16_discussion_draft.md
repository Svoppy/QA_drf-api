# Discussion Draft

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
