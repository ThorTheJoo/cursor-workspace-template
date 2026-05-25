# Energy Procurement — LLM Grading Rubric

## Purpose

This rubric guides an LLM grader in scoring agent responses to energy procurement evaluation scenarios. Each scenario contains 3–5 evaluation criteria with pass/fail rubric descriptions. The grader assigns a score to each criterion, and the weighted sum produces the scenario score.

---

## Grading Scale

| Rating | Score | Definition |
|---|---|---|
| **Pass** | 1.0 | Response demonstrates domain expertise. The recommended actions are what an experienced energy procurement manager at a large C&I consumer would do. Correct market structures (ISO/RTO mechanics, capacity markets, LMP pricing), tariff components (energy, demand, capacity, T&D, riders), procurement structures (fixed, index, block-and-index, layered), and financial frameworks (PPA evaluation, hedging instruments, total cost modeling) are applied. The response reflects operational judgment — not just textbook knowledge but awareness of how energy markets price risk, how demand charges compound through ratchets, how basis risk erodes PPA value, and how regulatory changes propagate through the supply chain. |
| **Partial** | 0.5 | Response is directionally correct but incomplete or imprecise. The agent identifies the general category of problem and suggests reasonable actions, but misses critical operational details, applies market benchmarks from the wrong ISO, omits a key tariff component, or provides advice that would work in theory but cause problems in practice (e.g., recommending index pricing in ERCOT without a price cap, or evaluating a VPPA without modeling basis risk). |
| **Fail** | 0.0 | Response is incorrect, dangerously incomplete, or generic. The agent either misidentifies the situation type, applies the wrong framework (e.g., using residential rate optimization logic for a C&I facility), recommends actions that would increase cost or risk exposure, or provides advice so generic it could apply to any cost management context ("negotiate a better rate"). A response that sounds plausible to a general procurement professional but would make an energy procurement manager wince. |

### Grading Decision Guide

When choosing between adjacent ratings, use these tiebreakers:

**Pass vs. Partial:**
- Did the response identify the *single most important action* for this scenario? If yes and the rest is reasonable, lean Pass.
- Would an energy procurement director reading this response need to add significant corrections before acting on it? If yes, Partial.

**Partial vs. Fail:**
- Does the response demonstrate awareness that this is an energy/utility context (not generic vendor management or cost reduction)? If not, Fail.
- Would following the response's advice cause active harm (budget blowout, unhedged exposure, missed capacity tag management, regulatory non-compliance)? If yes, Fail.
- Is the response merely incomplete but pointed in the right direction? Partial.

---

## Domain Expertise vs. Generic Response

The core distinction this rubric enforces is between responses grounded in energy procurement expertise and responses that apply generic cost management or sustainability logic to an energy-shaped problem.

### What Constitutes Domain Expertise

An expert-level response demonstrates knowledge that can only come from managing energy procurement for large C&I consumers. Specifically:

**1. Market Structure and Pricing Knowledge**
- Understands that an electricity bill has distinct components (energy, demand, capacity, T&D, riders) that must be analyzed independently
- Knows that demand charges are based on 15-minute interval peak kW and explains the ratchet mechanism
- References specific ISOs (PJM, ERCOT, CAISO, NYISO, ISO-NE, MISO) and their distinct market structures
- Understands LMP (Locational Marginal Pricing) and its components (energy, congestion, losses)
- Knows the difference between regulated and deregulated markets and how procurement strategy differs
- References capacity markets (PJM RPM, ISO-NE FCA) and how PLC/ICAP tags are set
- Calculates total delivered cost, not just supply rate

**2. Procurement Strategy and Execution**
- Distinguishes between fixed-price, index, block-and-index, and layered procurement structures
- Knows when each structure is appropriate based on risk tolerance, load factor, and market position
- References forward curves as the benchmark for evaluating pricing
- Understands the RFP process for deregulated markets: data requirements, evaluation criteria, supplier credit assessment
- Recognizes that "fixed-price" covers only the supply component — delivery charges, capacity, and riders are pass-through
- Calculates total cost across diesel/gas price scenarios when evaluating proposals

**3. Demand Charge and Load Management**
- Identifies demand charges as the most controllable cost component for C&I facilities
- Knows that peak demand is measured in 15-minute intervals and a single bad interval can cost thousands
- References specific mitigation strategies: staggered startups, load shifting, peak shaving with batteries, demand response programs
- Understands the battery storage value stack: demand charge reduction + capacity tag reduction + TOU arbitrage + DR revenue
- Knows about ratchet clauses and their financial impact
- Calculates ROI on demand-side investments using stacked value, not just demand charge savings

**4. Renewable Energy and Sustainability**
- Distinguishes between physical PPAs, virtual PPAs (VPPAs), RECs (bundled vs. unbundled), utility green tariffs, and on-site generation
- Understands basis risk in VPPAs and can explain why a favorable strike price doesn't guarantee favorable economics
- Knows the difference between GHG Protocol location-based and market-based Scope 2 accounting
- References RE100, SBTi, and CDP in the context of procurement decisions
- Understands curtailment risk and its impact on PPA economics and REC delivery
- Recognizes that unbundled RECs satisfy market-based accounting but face increasing additionality scrutiny

**5. Risk Management and Hedging**
- Understands the fundamental tradeoff between budget certainty and market exposure
- References specific hedging instruments: fixed contracts, blocks, financial swaps, call options, collars
- Knows that layered procurement is the primary hedge for most C&I buyers
- Understands weather risk (HDD/CDD) and its impact on consumption and cost variance
- References regulatory risk: rate cases, capacity market reform, carbon pricing
- Recognizes supplier credit risk and knows how to evaluate and mitigate it

### Common Indicators of Generic Responses

These patterns indicate the response lacks domain-specific expertise. Any single indicator is not disqualifying, but multiple indicators strongly suggest a Fail or low Partial:

**1. Wrong Abstraction Layer**
- Refers to electricity as a commodity that can be "negotiated" without understanding the market structure
- Treats the electricity bill as a single line item rather than decomposing into energy, demand, capacity, T&D, and riders
- Calls energy procurement "vendor management" without referencing tariff structures, ISO markets, or hedging
- Suggests generic "cost reduction strategies" rather than specific interventions (demand charge management, tariff optimization, procurement timing)

**2. Missing Market Mechanics**
- Does not reference ISOs/RTOs or distinguish between regulated and deregulated markets
- Fails to identify demand charges as a distinct, manageable cost component
- Does not mention forward curves as the benchmark for evaluating supply pricing
- Ignores capacity charges and PLC/ICAP tag management
- Recommends "renewable energy" without distinguishing between physical PPAs, VPPAs, RECs, and on-site generation
- Evaluates a PPA on strike price alone without considering basis risk, curtailment, or credit requirements

**3. Incorrect Market Application**
- Treats electricity as a single-price commodity rather than a location-specific, time-varying product
- Applies residential or small commercial energy advice (e.g., "switch to a green energy plan") to a large C&I context
- Does not adjust procurement strategy for the specific ISO or market structure
- Recommends index pricing without discussing tail risk or hedging
- Ignores the distinction between energy supply (competitive) and delivery (regulated)

**4. One-Dimensional Analysis**
- Addresses only energy cost without considering demand charges, capacity charges, or T&D
- Focuses on rate ($/kWh) without calculating total delivered cost including all bill components
- Evaluates sustainability without considering cost implications, or vice versa
- Does not consider the interaction between procurement decisions (e.g., on-site solar affecting DR baseline)
- Ignores regulatory proceedings that affect future cost structure

**5. Missing Risk Awareness**
- Does not mention price risk, basis risk, volume risk, or regulatory risk
- Recommends full index exposure without discussing hedging or price caps
- Evaluates a PPA without stress-testing under adverse market scenarios
- Does not consider supplier credit quality in procurement decisions
- Ignores weather as a driver of consumption and cost variance

---

## Scoring Individual Criteria

For each criterion within a scenario, the grader should:

1. **Read the scenario context and task** to understand what the agent was asked to do.
2. **Read the criterion's pass and fail rubric descriptions** — these are specific to the scenario, not generic.
3. **Evaluate the agent's response** against both the pass and fail descriptions.
4. **Assign a rating:**
   - **Pass (1.0):** The response matches the pass description substantively. Minor wording differences are fine — the grader is evaluating whether the agent demonstrated the same operational judgment, not whether it used identical phrasing.
   - **Partial (0.5):** The response falls between the pass and fail descriptions. It captures some elements of the pass description but misses others, or gets the direction right but the details wrong.
   - **Fail (0.0):** The response matches the fail description, or is worse than the fail description, or does not address the criterion at all.

### Important Scoring Nuances

**Specificity Matters**
A response that says "negotiate a better energy rate" is not the same as a response that says "benchmark against the PJM AEP Dayton Hub 36-month forward curve, model total delivered cost including capacity at the current RPM clearing price, and evaluate block-and-index versus fixed-price structures based on the facility's 0.72 load factor." The first is generic; the second demonstrates domain knowledge. Grade accordingly.

**Market Context Matters**
A response that recommends locking in a fixed-price contract is correct when forwards are in the bottom quartile of the 5-year range and incorrect when forwards are at all-time highs. The grader should evaluate whether the agent's recommendations match the market conditions described in the scenario.

**Total Cost Matters**
A response that evaluates supply pricing without considering demand charges, capacity charges, and delivery charges should receive Partial at best, regardless of how sophisticated the supply analysis is. Energy procurement is total cost management, not just supply rate optimization.

**Interaction Effects Matter**
A technically correct recommendation that ignores interaction effects (e.g., behind-the-meter solar cannibalizing DR value, or a VPPA creating unexpected accounting volatility) should receive Partial rather than Pass. Expert-level responses anticipate secondary effects.

**Omission Is Failure**
If a criterion's pass description includes 4 elements and the response covers 2 well but ignores 2, this is Partial — not Pass. The pass description represents the complete expert response.

**Practicality Test**
Would an experienced energy procurement manager read this response and say "yes, that's exactly what I'd do"? If yes, Pass. Would they say "that's roughly right but they're missing X"? Partial. Would they say "no, that would make things worse"? Fail.

---

## Grading Edge Cases

### When the Response Is Right for the Wrong Reasons

If the agent recommends the correct action but explains it using incorrect reasoning (e.g., recommends buying RECs but cites the wrong GHG Protocol method, or calculates demand charge savings but uses an incorrect demand rate), assign **Partial**. Correct actions with wrong reasoning suggest the agent may not replicate the correct behavior in novel situations.

### When the Response Adds Correct Information Not in the Rubric

If the agent provides additional relevant and correct information beyond what the pass rubric describes, this does not change the scoring — it's still a Pass. Do not penalize for additional correct content, even if it wasn't asked for, unless it contradicts other parts of the response.

### When the Response Contradicts Itself

If the agent states conflicting recommendations (e.g., "lock in a fixed-price contract" in one paragraph and "maintain full index exposure" in another without a clear conditional), assign **Fail** for that criterion unless one recommendation is clearly framed as contingent on a condition.

### When the Response Addresses a Different Aspect of the Problem

If the criterion asks about "demand charge mitigation" and the agent's response focuses entirely on "supply rate negotiation" (a different criterion), assign **Fail** for the demand charge criterion even if the supply analysis is excellent. Each criterion is graded independently.

---

## Aggregate Interpretation

After scoring all criteria for all scenarios, the following aggregate benchmarks indicate capability levels:

| Aggregate Score | Interpretation |
|---|---|
| **≥ 85%** | Expert-level energy procurement capability. The agent can handle the full range of procurement decisions — tariff analysis, RFP evaluation, PPA modeling, demand charge optimization, hedging strategy, and sustainability reporting — with minimal human oversight. Suitable for production use in first-draft analyses, scenario modeling, and communication drafting. |
| **70–84%** | Competent with supervision. The agent handles routine procurement tasks well but needs human review on complex PPA evaluations, multi-ISO portfolio strategy, capacity market positioning, and regulatory interventions. Suitable for first-draft work that an energy manager reviews. |
| **50–69%** | Inconsistent. The agent demonstrates some energy market knowledge but has significant gaps. May produce harmful advice on hard scenarios (e.g., recommending unhedged index exposure in ERCOT, or evaluating a VPPA without basis risk analysis). Requires heavy human supervision. |
| **< 50%** | Insufficient domain expertise. The agent's responses are predominantly generic cost management or sustainability advice without energy market-specific knowledge. Not suitable for any autonomous energy procurement tasks. |

### Difficulty-Adjusted Expectations

The scenario set is designed with a difficulty distribution:
- **Easy (~30%):** An agent with basic energy market knowledge should pass these. Failure on easy scenarios is a strong negative signal.
- **Medium (~40%):** An agent needs genuine operational knowledge to pass these consistently. Partial scores are common and acceptable.
- **Hard (~27%):** These are designed to trip up agents without deep domain expertise. Even competent agents may score Partial on some hard scenarios. Consistent Pass on hard scenarios indicates true expert-level capability.

A capable agent should score ≥90% on easy, ≥70% on medium, and ≥50% on hard scenarios. An agent scoring below 50% on easy scenarios has fundamental gaps that disqualify it from the domain.
