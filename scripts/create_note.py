#!/usr/bin/env python3
"""Create a new Daily Review Note from the template."""

from __future__ import annotations

import argparse
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "daily-review-note-template.md"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "untitled"


def review_dates(start: date) -> list[str]:
    offsets = [1, 3, 7, 14, 30]
    return [(start + timedelta(days=o)).isoformat() for o in offsets]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a daily review note")
    parser.add_argument("--topic", required=True, help="Note topic")
    parser.add_argument("--folder", default="01_LangChain", help="Target folder")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    args = parser.parse_args()

    note_date = date.fromisoformat(args.date)
    slug = slugify(args.topic)
    target_dir = ROOT / args.folder
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{args.date}-{slug}.md"

    content = TEMPLATE.read_text(encoding="utf-8")
    content = content.replace('topic: ""', f'topic: "{args.topic}"')
    content = content.replace("date: YYYY-MM-DD", f"date: {args.date}")
    content = content.replace("# Daily Review Note: <Topic>", f"# Daily Review Note: {args.topic}")

    dates = review_dates(note_date)
    content = content.replace(
        "  - YYYY-MM-DD\n  - YYYY-MM-DD\n  - YYYY-MM-DD",
        "\n".join(f"  - {d}" for d in dates),
    )

    if target.exists():
        raise SystemExit(f"File already exists: {target}")

    target.write_text(content, encoding="utf-8")
    print(f"Created: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
