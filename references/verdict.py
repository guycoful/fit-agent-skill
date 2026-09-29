#!/usr/bin/env python3
"""Deterministic daily verdict for the fit-agent skill.

Reads profile.json and one day log, computes totals from the meals list,
checks every condition against the profile and prints JSON:
  {"verdict": "success" | "fail" | "incomplete", ...}
The model quotes this output. It never decides the verdict itself.
"""
import argparse
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def num(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--day", required=True)
    args = ap.parse_args()
    profile, day = load(args.profile), load(args.day)

    meals = day.get("meals")
    missing = []
    if not isinstance(meals, list) or not meals:
        missing.append("meals")
    for field in ("water_l", "steps", "sleep_hours"):
        if num(day.get(field)) is None:
            missing.append(field)
    for meal in meals if isinstance(meals, list) else []:
        for field in ("calories", "protein_g"):
            if num(meal.get(field)) is None:
                missing.append("meals[%s].%s" % (meal.get("description", "?"), field))
    if missing:
        print(json.dumps({"verdict": "incomplete", "missing": missing}, ensure_ascii=False))
        return 2

    calories = sum(m["calories"] for m in meals)
    protein = sum(m["protein_g"] for m in meals)
    forbidden_meals = [m.get("description", "?") for m in meals if m.get("forbidden_hit")]

    failed = []

    def check(name, actual, target, kind):
        ok = actual >= target if kind == "min" else actual <= target
        if not ok:
            failed.append({"condition": name, "actual": actual, "target": target,
                           "gap": round(actual - target, 2)})

    check("calories_min", calories, profile["calories_min"], "min")
    check("calories_max", calories, profile["calories_max"], "max")
    check("protein_min_g", protein, profile["protein_min_g"], "min")
    check("water_min_l", day["water_l"], profile["water_min_l"], "min")
    check("steps_min", day["steps"], profile["steps_min"], "min")
    check("sleep_min_hours", day["sleep_hours"], profile["sleep_min_hours"], "min")
    if forbidden_meals:
        failed.append({"condition": "forbidden", "items": forbidden_meals})

    alerts = [m.get("description", "?") for m in meals if m["calories"] > profile.get("meal_alert_calories", 10**9)]

    result = {
        "date": day.get("date"),
        "verdict": "fail" if failed else "success",
        "totals": {"calories": calories, "protein_g": protein},
        "failed": failed,
        "meal_alerts": alerts,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
