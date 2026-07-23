#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "satyam-1906"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_DIR = Path("data")
OUT_FILE = OUT_DIR / "contributions.json"


def parse_contributions(resp_text: str) -> list[dict]:
    soup = BeautifulSoup(resp_text, "html.parser")
    items = []

    for cell in soup.select("td[data-date]"):
        date = cell.get("data-date")
        level = int(cell.get("data-level", 0))
        tooltip = cell.find_next_sibling("tool-tip")
        label = tooltip.get_text(" ", strip=True) if tooltip else ""
        count_match = re.search(r"(\d+)", label)
        count = int(count_match.group(1)) if count_match else 0

        items.append({
            "date": date,
            "level": level,
            "count": count,
        })

    return items


def derive_stats(days: list[dict]) -> dict:
    sorted_days = sorted(days, key=lambda item: item["date"])
    if not sorted_days:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": {"date": None, "count": 0},
            "monthly_totals": {},
        }

    current_streak = 0
    longest_streak = 0
    streak = 0

    for item in reversed(sorted_days):
        if item["count"] > 0:
            current_streak += 1
        else:
            break

    for item in sorted_days:
        if item["count"] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0

    best_day = max(sorted_days, key=lambda item: (item["count"], item["level"]))
    monthly_totals = Counter()
    for item in sorted_days:
        month = item["date"][:7]
        monthly_totals[month] += item["count"]

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": best_day["date"], "count": best_day["count"]},
        "monthly_totals": dict(sorted(monthly_totals.items())),
    }


def main() -> int:
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    days = parse_contributions(resp.text)
    stats = derive_stats(days)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "days": days,
        "stats": stats,
    }

    OUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Contribution data written to {OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
