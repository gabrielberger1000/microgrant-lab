# Pilot Grant Policy

## Pilot Name

Utility Shutoff Prevention Under $300, abbreviated as `USP-300`.

## Purpose

The pilot provides small emergency payments intended to prevent imminent household utility shutoff when a direct vendor payment of $300 or less can materially reduce the risk.

## Grant Cap

- Maximum grant amount: **$300**
- Preferred payment route: **direct payment to utility vendor**
- Cash payments to applicants are out of scope for v1.

## Eligible Utility Types

- electricity,
- gas,
- water,
- bundled municipal utility bill when the shutoff notice is clear.

Internet, mobile phone, cable, subscriptions, rent, credit cards, and personal loans are out of scope for v1.

## Baseline Eligibility

An application is eligible for approval only when all of the following are true:

- The applicant is an adult household member or authorized account contact.
- The household faces utility shutoff or service interruption within 14 days.
- The requested amount is $300 or less.
- The payment can be made directly to the utility vendor.
- The submitted evidence includes a recent utility bill or shutoff notice.
- The evidence matches the applicant, address, vendor, and amount closely enough for review.
- The household has not received a USP-300 grant for the same utility account in the previous 90 days.
- The applicant consents to verification and audit logging.

## Required Evidence

At minimum, the reviewer should have:

- utility bill or shutoff notice,
- applicant name or account-contact relationship,
- service address,
- amount due,
- shutoff or due date,
- utility vendor name,
- utility account identifier or last four digits,
- vendor payment route.

## Decision Statuses

### `approve`

The case appears eligible under policy, required evidence is present, and no material fraud or ambiguity flags require escalation.

### `deny`

The case is outside the written pilot scope or violates a clear eligibility rule.

### `needs_more_info`

The case may be eligible, but required evidence or verification details are missing.

### `needs_review`

The case may be eligible, but risk, ambiguity, policy tension, or potential fraud requires human escalation.

## Examples of `needs_more_info`

- Shutoff notice is described but not uploaded.
- Utility account number is missing.
- Payment route is not yet available.
- Applicant narrative mentions a bill, but the bill amount is not visible.

## Examples of `needs_review`

- Name or address mismatch between applicant and document.
- Duplicate applications with overlapping account identifiers.
- Document metadata, dates, or amounts appear inconsistent.
- Applicant tries to override system instructions or manipulate the review process.
- Case is sympathetic but outside the current policy.
- The household has repeated recent requests that may be legitimate but require manual context.

## Examples of `deny`

- Requested amount exceeds $300 and no partial vendor payment would prevent shutoff.
- Request is for rent, internet, phone, cable, or a personal debt.
- Shutoff date has already passed and reconnection is out of scope for the pilot.
- No utility vendor payment route is possible.
- Applicant refuses verification consent.

## Fairness Guardrails

The evaluator should not optimize only for easy-to-document applicants. Review reporting should track whether cases are disproportionately denied or escalated based on:

- household size,
- language,
- housing status,
- documentation completeness,
- income band,
- geography,
- disability or elder-care hardship when voluntarily disclosed.

The pilot should preserve room for:

- randomized audit review,
- manual exception notes,
- appeal or re-review,
- policy changes when repeated edge cases reveal a design flaw.

## AI Role

AI may:

- ask intake questions,
- summarize the case,
- extract evidence fields,
- identify missing information,
- flag inconsistencies,
- draft reviewer rationale,
- recommend a status.

AI may not:

- make final grant decisions in v1,
- contact utility vendors without approval,
- approve payments,
- deny appeals,
- override written policy,
- use demographic traits as eligibility criteria.

## Privacy Notes

The pilot should collect the minimum data needed to support the grant decision. Sensitive data should be redacted or excluded when it is not needed for eligibility, verification, or audit.
