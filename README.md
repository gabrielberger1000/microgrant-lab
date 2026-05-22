# Microgrant Lab

Microgrant Lab is an experimental infrastructure project for AI-assisted emergency microgrant review.

The first pilot is intentionally narrow: **utility shutoff prevention grants capped at $300**. The goal is not to launch an autonomous charity. The goal is to learn whether AI-assisted intake, evidence review, fraud screening, and audit trails can make small-grant decisions faster, cheaper, more consistent, and more transparent.

## Current Scope

- Build a synthetic and adversarial case lab before using real applicant data.
- Keep AI recommendations assistive, with human review as the decision layer.
- Treat policy clarity, auditability, and fraud resistance as first-class product requirements.
- Avoid real-money movement until the workflow can be evaluated in shadow mode.

## Repo Map

```text
docs/
  project-brief.md       # What this project is and is not
  design-doc.md          # v1 system design and architecture
  grant-policy.md        # Utility shutoff pilot policy
  evaluation-plan.md     # How we will measure usefulness and failure modes
schemas/
  case.schema.json       # Structured case format
  decision.schema.json   # Structured review decision format
synthetic_cases/
  generator.py           # Deterministic synthetic case generator
  fixtures/
    utility_shutoff_seed_cases.json
evaluations/
  evaluate_cases.py      # Simple baseline policy evaluator
```

## Quickstart

Run the seed-case evaluator:

```bash
python3 evaluations/evaluate_cases.py synthetic_cases/fixtures/utility_shutoff_seed_cases.json
```

Generate a larger synthetic case file:

```bash
python3 synthetic_cases/generator.py --count 25 --output synthetic_cases/fixtures/generated_cases.json
python3 evaluations/evaluate_cases.py synthetic_cases/fixtures/generated_cases.json
```

## Working Principle

The first useful system is not "AI decides who deserves help."

It is:

> A narrow, auditable review workflow that helps humans make better small-grant decisions under clear policy constraints.
