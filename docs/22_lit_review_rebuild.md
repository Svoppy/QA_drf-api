# Literature Review

The purpose of this review is not to collect loosely related papers on software testing, nor to search for direct approval of one already implemented toolchain. Its role is narrower and more methodological. The review asks what recent literature actually supports when the objective is to build a defensible QA method for API-centric systems that operate under transaction sensitivity, continuous change, and delivery pressure. When read in that way, the literature becomes more useful. It stops looking like a set of isolated findings and starts to function as a basis for methodological design.

## 1. API-Centric Systems as a Distinct QA Problem

One of the clearest points emerging from recent literature is that REST APIs should be treated as a primary verification concern rather than as a secondary artifact of backend implementation. Ehsan et al. (2022) make this point directly by framing RESTful API testing as an area with its own rationale, challenges, and solution directions. What matters here is not just the popularity of APIs, but the role they play as the point where validation rules, service interactions, failure propagation, and client-visible behavior converge. Once that role is acknowledged, QA for API-centric systems can no longer be treated as something that is adequately covered through indirect testing alone.

This point becomes more concrete in the work of Martin-Lopez et al. (2021), who present RESTest as an automated black-box testing approach for REST APIs. The present paper does not need to reproduce their method to benefit from the claim behind it. Their work supports a broader methodological idea: API interfaces are meaningful, legitimate, and practical objects of automated black-box verification. That matters because it shifts attention toward observable service behavior and away from the assumption that valuable QA must always begin from internal white-box access.

Taken together, these sources support a foundational claim for the present study: if APIs are the surface through which critical system behavior is exposed, then QA methodology for such systems must make API verification a central design concern rather than an incidental afterthought.

## 2. Why Robustness and Error Behavior Belong in the Core Method

If API testing is treated seriously, then a second issue follows almost immediately: testing nominal behavior is not enough. Corradini et al. (2022), in their work on automated black-box testing of nominal and error scenarios, make this especially clear. Their contribution is important not because it offers a universal mechanism that every project must copy, but because it sharpens the methodological point that valid-path behavior does not exhaust what quality means for an API.

This matters for any QA method that claims to be useful in transaction-heavy environments. A system may return correct outputs under well-formed requests and still remain fragile when confronted with invalid inputs, inconsistent sequence conditions, or error-triggering combinations of data and state. Once this is acknowledged, negative testing is no longer an optional extension. It becomes part of the method itself. In practice, this means that robustness, malformed input handling, and error-path behavior have to be placed inside the main testing logic rather than treated as a side exercise.

The literature therefore supports a second methodological principle: a QA method for API-centric systems should be built not only around nominal correctness, but also around robustness against invalid or failure-prone interaction patterns.

## 3. From API Verification to Layered Verification

At this point, the literature does not hand over a rigid architecture such as "always use three exact layers in this exact proportion." That kind of prescription would be too blunt for real systems. Yet the reviewed studies do suggest something more useful than a recipe. Different forms of testing illuminate different classes of failure, and a method that collapses them into one level risks losing explanatory power.

The API literature already implies this division. If automated black-box verification is useful for service-level behavior (Martin-Lopez et al., 2021), and if nominal plus error scenarios need explicit attention at the interface level (Corradini et al., 2022), then it becomes difficult to defend a single-level testing strategy as sufficient for all relevant QA concerns. Sartaj et al. (2024), writing from a DevOps and evolving-systems perspective, reinforce this view indirectly. Their work highlights the need for repeatable testing under ongoing change, which makes diversified verification even more plausible because different failure types become relevant at different stages of system evolution.

What the literature supports, then, is not one exact layering formula, but a methodological principle of differentiated observation. Smaller and more isolated defects may be more visible in tightly scoped tests. Interaction-level behavior requires service-oriented checks. Flow-sensitive or access-sensitive issues may only emerge when the system is exercised in a broader and more realistic way. The exact balance can vary across cases, but the principle remains stable: if the risk profile is heterogeneous, the verification method should be heterogeneous as well.

## 4. Prioritization as a Methodological Requirement, Not a Compromise

The next issue is prioritization. This is where testing methodology begins to intersect with delivery pressure more explicitly. Pan et al. (2021), in their systematic review of test case selection and prioritization using machine learning, focus on approaches that improve regression feedback under time and resource constraints. The present study does not adopt machine-learning-based prioritization, so the source has to be used carefully. Still, its value for this paper is substantial. It helps establish that selective emphasis is not a sign of methodological weakness. Under CI-like conditions, it is often part of what makes testing strategically meaningful.

This matters because a risk-informed QA method does not assume that all test effort has equal value. If some parts of a system carry higher operational or business consequence, then a defensible method should acknowledge that asymmetry. Literature on prioritization gives academic support to that logic, even if the operational mechanism differs from one study to another. The lesson that carries over is not "use machine learning," but rather "do not pretend that all tests deserve equal emphasis under continuous delivery constraints."

Once that point is accepted, prioritization becomes easier to position correctly. It is not a shortcut around proper testing. It is a methodological response to unequal risk, limited feedback windows, and the need to keep verification actionable.

## 5. CI/CD Changes the Meaning of a Testing Method

Testing methodology also changes once CI/CD becomes part of the environment in which QA operates. Soares et al. (2021), through a systematic literature review, show that continuous integration affects testing discipline, visibility of quality issues, and development feedback loops more broadly. That matters because it makes CI more than an execution platform. It becomes part of the context in which a QA method must prove itself useful.

Sartaj et al. (2024) reinforce this point from the angle of REST API testing in an evolving DevOps environment. Their work suggests that when systems change continuously, testing has to remain repeatable, tool-supported, and capable of producing interpretable feedback under ongoing revision. This has a methodological consequence that is easy to miss: a QA method cannot be judged only by what it tests. It must also be judged by how well it can sustain quality control under real execution conditions.

That is why CI/CD belongs in the methodological foundation of the present study. It matters for execution time, rerun consistency, gate design, and the overall credibility of automated feedback. A method that only looks convincing outside CI pressure may still fail as an actual QA method in practice.

## 6. Trust, Stability, and the Limits of Coverage-Centered Evaluation

At this stage of the review, one more issue becomes unavoidable: even a well-structured automated suite is not methodologically persuasive if its outputs cannot be trusted. This is where the literature on flaky tests becomes particularly important. Parry et al. (2022) show that flaky tests are not merely a maintenance irritation. They are a threat to the reliability of test evidence itself. If a suite produces inconsistent outcomes, then any argument built on its failures, passes, or quality gates becomes harder to defend.

This insight matters because it changes how metrics should be treated. Coverage remains useful, especially for identifying visible test gaps. But coverage alone says little about whether the most relevant defects are being surfaced, whether the suite behaves consistently, or whether the test process remains practical inside CI/CD. Once stability and trust are brought into the picture, the role of metrics becomes more layered. Coverage may show reach, defect findings may show practical yield, runtime may show operational viability, and stability may determine whether the rest of the evidence can be trusted at all.

The literature therefore supports another methodological principle: evaluation should be multi-dimensional. A QA method should not be judged by a single number, especially not one that can grow while more consequential weaknesses remain hidden.

## 7. Synthesis: What the Literature Allows the Method to Be

Taken together, the reviewed literature does not dictate one exact framework combination or one universally correct implementation path. It would be misleading to claim otherwise. What it does offer is a coherent methodological direction.

It supports the idea that:

- API-centric systems require explicit and systematic verification
- robustness and error behavior belong inside the core QA method
- different risk types justify different forms of observation
- prioritization is legitimate under CI/CD pressure
- CI/CD is part of the methodological environment, not just the execution backdrop
- stability and trust matter enough to shape how evidence is interpreted

This synthesis is important because it gives the present paper its real starting point. The article does not begin from one repository and then search for literature that sounds supportive. It begins from literature-supported methodological principles and then examines how those principles can be operationalized and evaluated in a concrete empirical case. The role of the case, therefore, is not to be the subject of the article, but to serve as a validation environment for the method derived from the literature.
