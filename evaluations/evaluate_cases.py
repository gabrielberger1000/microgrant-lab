#!/usr/bin/env python3
"""Evaluate USP-300 synthetic cases with a simple baseline policy."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


ALLOWED_UTILITY_TYPES = {"electric", "gas", "water", "municipal_bundle"}
REQUIRED_NOTICE_TYPES = {"utility_bill", "shutoff_notice"}
GRANT_CAP_USD = 300


def parse_created_date(case: dict[str, Any]) -> date:
    created_at = case.get("created_at", "")
    return datetime.fromisoformat(created_at).date()


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def has_notice(case: dict[str, Any]) -> bool:
    return any(
        item.get("type") in REQUIRED_NOTICE_TYPES and item.get("status") == "provided"
        for item in case.get("evidence", [])
    )


def has_suspicious_evidence(case: dict[str, Any]) -> bool:
    return any(item.get("status") == "suspicious" for item in case.get("evidence", []))


def has_mismatched_evidence(case: dict[str, Any]) -> bool:
    return any(
        item.get("type") in REQUIRED_NOTICE_TYPES
        and item.get("status") == "provided"
        and item.get("matches_applicant") is False
        for item in case.get("evidence", [])
    )


def high_or_medium_flags(case: dict[str, Any]) -> list[str]:
    return [
        flag.get("code", "unknown_flag")
        for flag in case.get("risk_flags", [])
        if flag.get("severity") in {"medium", "high"}
    ]


def instruction_like_text(case: dict[str, Any]) -> bool:
    narrative = case.get("narrative", "").lower()
    triggers = [
        "ignore all previous",
        "ignore previous",
        "override policy",
        "approve this application immediately",
        "system instructions",
    ]
    return any(trigger in narrative for trigger in triggers)


def baseline_decision(case: dict[str, Any]) -> tuple[str, float | None, list[str]]:
    request = case["request"]
    flags: list[str] = []
    created = parse_created_date(case)
    shutoff_date = parse_date(request.get("shutoff_date"))

    if request.get("utility_type") not in ALLOWED_UTILITY_TYPES:
        return "deny", None, ["out_of_scope_utility"]

    if request.get("amount_requested_usd", 0) > GRANT_CAP_USD:
        return "deny", None, ["over_cap"]

    if request.get("payment_route") != "direct_to_vendor":
        if request.get("payment_route") == "unknown" or request.get("account_last4") is None:
            return "needs_more_info", None, ["missing_payment_route_or_account"]
        return "deny", None, ["unsupported_payment_route"]

    if shutoff_date is None:
        return "needs_more_info", None, ["missing_shutoff_date"]

    if shutoff_date < created:
        return "deny", None, ["post_shutoff"]

    if (shutoff_date - created).days > 14:
        flags.append("shutoff_not_imminent")

    if has_suspicious_evidence(case):
        flags.append("suspicious_evidence")

    if has_mismatched_evidence(case):
        flags.append("mismatched_evidence")

    flags.extend(high_or_medium_flags(case))

    if instruction_like_text(case):
        flags.append("prompt_injection")

    if flags:
        return "needs_review", None, sorted(set(flags))

    if not has_notice(case):
        return "needs_more_info", None, ["missing_notice"]

    amount = round(float(request.get("amount_requested_usd", 0)), 2)
    return "approve", amount, []


def load_cases(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array of cases")
    return data


def validate_minimal(case: dict[str, Any]) -> list[str]:
    missing = []
    for field in ["case_id", "created_at", "request", "evidence", "ground_truth"]:
        if field not in case:
            missing.append(field)
    if "expected_decision" not in case.get("ground_truth", {}):
        missing.append("ground_truth.expected_decision")
    return missing


def print_distribution(title: str, counts: Counter[str]) -> None:
    print(title)
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path, help="Path to a JSON case array.")
    args = parser.parse_args()

    cases = load_cases(args.cases)
    expected_counts: Counter[str] = Counter()
    predicted_counts: Counter[str] = Counter()
    confusion: dict[str, Counter[str]] = defaultdict(Counter)
    mismatches = []
    validation_errors = []

    for case in cases:
        case_id = case.get("case_id", "<missing>")
        missing = validate_minimal(case)
        if missing:
            validation_errors.append((case_id, missing))
            continue

        expected = case["ground_truth"]["expected_decision"]
        predicted, amount, flags = baseline_decision(case)
        expected_counts[expected] += 1
        predicted_counts[predicted] += 1
        confusion[expected][predicted] += 1

        if predicted != expected:
            mismatches.append(
                {
                    "case_id": case_id,
                    "expected": expected,
                    "predicted": predicted,
                    "flags": flags,
                    "amount": amount,
                    "reason": case["ground_truth"].get("reason", ""),
                }
            )

    evaluated = sum(expected_counts.values())
    accuracy = 0 if evaluated == 0 else (evaluated - len(mismatches)) / evaluated

    print(f"Dataset: {args.cases}")
    print(f"Cases loaded: {len(cases)}")
    print(f"Cases evaluated: {evaluated}")
    print(f"Validation errors: {len(validation_errors)}")
    print(f"Agreement rate: {accuracy:.1%}")
    print()
    print_distribution("Expected decisions:", expected_counts)
    print()
    print_distribution("Predicted decisions:", predicted_counts)
    print()
    print("Confusion table:")
    for expected in sorted(confusion):
        cells = ", ".join(
            f"{predicted}={count}" for predicted, count in sorted(confusion[expected].items())
        )
        print(f"  {expected}: {cells}")

    if validation_errors:
        print()
        print("Validation errors:")
        for case_id, missing in validation_errors:
            print(f"  {case_id}: missing {', '.join(missing)}")

    if mismatches:
        print()
        print("Mismatches:")
        for mismatch in mismatches:
            print(
                "  {case_id}: expected {expected}, predicted {predicted}, flags={flags}; {reason}".format(
                    **mismatch
                )
            )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
