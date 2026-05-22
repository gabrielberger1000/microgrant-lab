# Evaluation Plan

## Goal

Measure whether the USP-300 workflow improves small-grant review quality before any real-money pilot.

The first evaluation target is decision support, not autonomous approval.

## Evaluation Phases

### Phase 1: Synthetic Cases

Use generated cases to test whether the workflow can:

- classify clear approvals, denials, missing-information cases, and manual-review cases,
- detect obvious evidence inconsistencies,
- avoid prompt-injection failures,
- produce structured audit output,
- remain stable as cases vary.

### Phase 2: Volunteer Simulations

Ask knowledgeable volunteers or advisors to create or review fictional cases. Compare system outputs against human policy interpretations and collect disagreement notes.

### Phase 3: Shadow Mode

Partner with an organization that already reviews similar requests. Run the system beside the human process without changing real decisions. Compare recommendations, review time, missing-info detection, and reviewer trust.

### Phase 4: Tiny Live Pilot

Only after earlier phases are credible, run a small manual-review pilot with limited funds, explicit consent, and direct vendor payments.

## Primary Metrics

- **Policy agreement:** percent of cases where system recommendation matches expected policy label.
- **Reviewer time:** estimated minutes saved per case.
- **Missing-info detection:** percent of incomplete cases correctly routed to `needs_more_info`.
- **Escalation precision:** percent of `needs_review` cases that contain a real ambiguity or risk.
- **False-denial risk:** eligible cases incorrectly denied by the system.
- **False-approval risk:** ineligible or fraudulent cases incorrectly recommended for approval.
- **Rationale quality:** reviewer score for whether the rationale is complete and grounded in evidence.
- **Audit completeness:** percent of decisions with policy checks, evidence references, and uncertainty notes.

## Safety Metrics

- Prompt-injection success rate.
- Duplicate-account detection rate.
- Name, address, amount, and date inconsistency detection rate.
- Over-cap request handling.
- Out-of-scope hardship handling.
- Sensitive-data minimization failures.

## Fairness and Legitimacy Checks

Report outcomes by available non-sensitive case attributes:

- language,
- household size,
- housing status,
- income band,
- documentation completeness,
- utility type,
- case type.

The point is not to use these fields as eligibility criteria. The point is to detect when the workflow handles different case groups unevenly.

## Initial Acceptance Gates

Before using real applicant data, the system should meet these minimum bars on synthetic and volunteer cases:

- No known prompt-injection case causes policy override.
- Clear out-of-scope cases are not recommended for approval.
- Clear eligible cases are not denied without a policy-grounded reason.
- Missing required evidence is consistently identified.
- Every recommendation includes a structured rationale.
- Reviewers can override, annotate, and audit the system output.

## Reporting Template

Each evaluation run should produce:

- dataset name and version,
- case count,
- label distribution,
- recommendation distribution,
- agreement rate,
- confusion table,
- notable false positives,
- notable false negatives,
- prompt-injection results,
- policy issues discovered,
- recommended policy or workflow changes.
