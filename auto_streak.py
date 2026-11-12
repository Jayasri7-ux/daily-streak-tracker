#!/usr/bin/env python3
"""
Automated Daily GitHub Streak Maintainer (auto_streak.py)
---------------------------------------------------------
Automatically records daily engineering/learning metrics into `activity_log.json`
and `DAILY_LOG.md`, creates between 1 and 3 atomic commits (for natural-looking
green shade variations on the GitHub contribution graph), and pushes to `main`.

Can be run:
1. Automatically in the cloud via GitHub Actions (works even when your PC is off!)
2. Automatically on your PC via Windows Task Scheduler
3. Manually anytime via `python auto_streak.py`
"""

import argparse
import datetime
import json
import os
import random
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
LOG_JSON_FILE = REPO_DIR / "activity_log.json"
LOG_MD_FILE = REPO_DIR / "DAILY_LOG.md"

GIT_USER_NAME = "Jaya Sri"
GIT_USER_EMAIL = "jayasripalli20@gmail.com"

TOPICS = [
    "Reviewed React state optimization patterns and memoization",
    "Practiced REST API payload validation and schema design",
    "Refactored utility helper functions and error boundaries",
    "Studied system design caching strategies and rate limiting",
    "Updated developer tooling configuration and automation scripts",
    "Solved data structures & string manipulation practice problems",
    "Explored Tailwind CSS responsive grid layouts and dark mode tokens",
    "Analyzed JWT authentication flows and OAuth2 token lifecycle",
]


def run_git(args: list[str]) -> str:
    """Run a git command inside the repository directory."""
    result = subprocess.run(
        ["git"] + args,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def ensure_git_identity() -> None:
    """Ensure commits are authored with the exact GitHub-verified email."""
    run_git(["config", "user.name", GIT_USER_NAME])
    run_git(["config", "user.email", GIT_USER_EMAIL])


def load_activity_data() -> dict:
    if LOG_JSON_FILE.exists():
        try:
            return json.loads(LOG_JSON_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "owner": "Jayasri7-ux",
        "total_commits_generated": 0,
        "last_updated": None,
        "entries": [],
    }


def save_activity_data(data: dict) -> None:
    LOG_JSON_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def update_markdown_summary(data: dict) -> None:
    recent_entries = data["entries"][-15:][::-1]
    lines = [
        "# 📈 Daily Engineering & Streak Log",
        "",
        f"- **Account:** [@Jayasri7-ux](https://github.com/Jayasri7-ux)",
        f"- **Total Automated Updates:** `{data['total_commits_generated']}`",
        f"- **Last Synced (UTC):** `{data['last_updated']}`",
        "",
        "## Recent Activity Log",
        "",
        "| Timestamp (UTC) | Session # | Focus Area |",
        "| :--- | :--- | :--- |",
    ]
    for entry in recent_entries:
        lines.append(
            f"| `{entry['timestamp']}` | #{entry['count']} | {entry['topic']} |"
        )
    lines.append("")
    LOG_MD_FILE.write_text("\n".join(lines), encoding="utf-8")


def perform_daily_commits(min_commits: int = 1, max_commits: int = 3, push: bool = True) -> None:
    ensure_git_identity()
    num_commits = random.randint(min_commits, max_commits)
    print(f"[*] Generating {num_commits} daily contribution commit(s)...")

    data = load_activity_data()

    for i in range(1, num_commits + 1):
        now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        topic = random.choice(TOPICS)

        data["total_commits_generated"] += 1
        data["last_updated"] = now_utc
        data["entries"].append(
            {
                "count": data["total_commits_generated"],
                "timestamp": now_utc,
                "topic": topic,
            }
        )
        # Keep JSON file lightweight (last 200 entries)
        data["entries"] = data["entries"][-200:]

        save_activity_data(data)
        update_markdown_summary(data)

        run_git(["add", "activity_log.json", "DAILY_LOG.md"])
        commit_msg = f"chore(streak): daily activity sync #{data['total_commits_generated']} ({ i }/{ num_commits })"
        run_git(["commit", "-m", commit_msg])
        print(f"  [+] Committed: {commit_msg}")

    if push:
        print("[*] Pushing commits to origin/main...")
        run_git(["push", "origin", "main"])
        print("[+] Successfully pushed to GitHub!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Daily GitHub Streak Bot")
    parser.add_argument("--min", type=int, default=1, help="Minimum commits per run")
    parser.add_argument("--max", type=int, default=3, help="Maximum commits per run")
    parser.add_argument("--no-push", action="store_true", help="Commit locally without pushing")
    args = parser.parse_args()

    perform_daily_commits(
        min_commits=max(1, args.min),
        max_commits=max(args.min, args.max),
        push=not args.no_push,
    )
