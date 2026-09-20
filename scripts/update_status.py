"""
Fetches recent public GitHub activity for GH_USERNAME and rewrites the
block between <!--LIVE-STATUS-START--> and <!--LIVE-STATUS-END--> in
README.md with a short, honest "what I've been doing lately" summary.

Runs daily via .github/workflows/live-status.yml — no manual edits needed.
"""

import os
import re
from datetime import datetime, timezone

import requests

USERNAME = os.environ["GH_USERNAME"]
TOKEN = os.environ.get("GH_TOKEN")
README_PATH = "README.md"

HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}


def fetch_events():
    url = f"https://api.github.com/users/{USERNAME}/events/public"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()


def time_ago(iso_timestamp: str) -> str:
    event_time = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )
    delta = datetime.now(timezone.utc) - event_time
    hours = int(delta.total_seconds() // 3600)
    if hours < 1:
        return "less than an hour ago"
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"


def build_status_block(events):
    push_events = [e for e in events if e.get("type") == "PushEvent"]

    if not push_events:
        return "> No public commits in the last 90 days — probably deep in a private build."

    latest = push_events[0]
    repo_name = latest["repo"]["name"].split("/")[-1]
    commits = latest.get("payload", {}).get("commits", [])
    message = commits[-1]["message"].splitlines()[0] if commits else "updated the repo"
    ago = time_ago(latest["created_at"])

    active_repos = {e["repo"]["name"].split("/")[-1] for e in push_events[:10]}

    lines = [
        f"> Last shipped to **{repo_name}** {ago} — *\"{message}\"*",
        f"> Active this week on: {', '.join(sorted(active_repos)[:5])}",
    ]
    return "\n".join(lines)


def update_readme(block: str):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = re.sub(
        r"(<!--LIVE-STATUS-START-->\n### 🟢 Right now\n\n).*?(\n<!--LIVE-STATUS-END-->)",
        lambda m: m.group(1) + block + m.group(2),
        content,
        flags=re.DOTALL,
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    events = fetch_events()
    block = build_status_block(events)
    update_readme(block)
    print("README.md live-status block updated.")
