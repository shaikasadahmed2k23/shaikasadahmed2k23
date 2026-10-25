#!/usr/bin/env python3
"""Render every animated SVG used by the profile README.

    python scripts/render.py            # static assets + live.svg (needs GITHUB_TOKEN for real data)
    python scripts/render.py --mock     # use generated sample data for live.svg (local preview)

Everything is driven by data/profile.json, so updating the profile means
editing that file, not the SVG code. Standard library only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import random
import sys
import urllib.error
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DATA = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))

# ── palette (GitHub dark, so the art sits naturally on the profile page) ──
BG = "#0d1117"
PANEL = "#161b22"
LINE = "#30363d"
TEXT = "#e6edf3"
DIM = "#8b949e"
FAINT = "#484f58"
GREEN = "#3fb950"
BLUE = "#58a6ff"
AMBER = "#d29922"
PURPLE = "#bc8cff"
CORAL = "#f78166"
HEAT = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def x(s: object) -> str:
    """XML-escape any value for text content and attributes."""
    return escape(str(s), {'"': "&quot;"})


def svg_open(w: int, h: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{x(title)}">'
        f"<title>{x(title)}</title>"
    )


def frame(w: int, h: int) -> str:
    return (
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" '
        f'fill="{BG}" stroke="{LINE}"/>'
    )


def typed(text: str, tx: float, ty: float, begin: float, uid: str, *,
          size: int = 14, fill: str = TEXT, cps: float = 38, weight: int = 400) -> tuple[str, float]:
    """Monospace text revealed one character at a time. Returns (svg, end_time)."""
    char_w = size * 0.602
    n = max(len(text), 1)
    dur = n / cps
    widths = ";".join(f"{i * char_w:.1f}" for i in range(n + 1))
    svg = (
        f'<clipPath id="c{uid}"><rect x="{tx}" y="{ty - size}" width="0" height="{size * 1.5}">'
        f'<animate attributeName="width" values="{widths}" calcMode="discrete" '
        f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
        f'<text x="{tx}" y="{ty}" clip-path="url(#c{uid})" font-family="{MONO}" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" xml:space="preserve">{x(text)}</text>'
    )
    return svg, begin + dur


def appear(inner: str, begin: float, *, rise: int = 6) -> str:
    """Fade + slide an element group in at `begin` seconds."""
    return (
        f'<g opacity="0" transform="translate(0 {rise})">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 {rise}" to="0 0" '
        f'begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>{inner}</g>'
    )


def cursor(cx: float, cy: float, begin: float, size: int = 14) -> str:
    return (
        f'<rect x="{cx}" y="{cy - size + 2}" width="{size * 0.6:.1f}" height="{size + 2}" fill="{GREEN}" opacity="0">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.05s" '
        f'begin="{begin:.2f}s" repeatCount="indefinite"/></rect>'
    )


# ══════════════════════════════════════════════════════════════════════
# 1. HERO — name on the left, a terminal booting the agent crew on the right
# ══════════════════════════════════════════════════════════════════════
def render_hero() -> str:
    W, H = 1000, 360
    out = [svg_open(W, H, f"{DATA['name']} — {DATA['role']}"), frame(W, H)]

    # soft grid texture on the left half
    out.append(
        '<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<path d="M24 0H0V24" fill="none" stroke="{PANEL}" stroke-width="1"/></pattern>'
        f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{BG}"/></linearGradient></defs>'
        f'<rect x="1" y="1" width="470" height="{H - 2}" rx="12" fill="url(#g)"/>'
        f'<rect x="300" y="1" width="172" height="{H - 2}" fill="url(#fade)"/>'
    )

    words = DATA["name"].split()
    line1, line2 = " ".join(words[:2]), " ".join(words[2:])
    left = (
        f'<text x="44" y="70" font-family="{MONO}" font-size="13" fill="{DIM}">~/{x(DATA["username"])}</text>'
        f'<text x="42" y="136" font-family="{SANS}" font-size="54" font-weight="700" fill="{TEXT}" letter-spacing="-1.5">{x(line1)}</text>'
        f'<text x="42" y="196" font-family="{SANS}" font-size="54" font-weight="700" fill="{TEXT}" letter-spacing="-1.5">{x(line2)}</text>'
        f'<rect x="44" y="216" width="56" height="3" rx="1.5" fill="{GREEN}"/>'
        f'<text x="44" y="250" font-family="{SANS}" font-size="19" font-weight="600" fill="{GREEN}">{x(DATA["role"])}</text>'
        f'<text x="44" y="276" font-family="{SANS}" font-size="15" fill="{DIM}">{x(DATA["tagline"])}</text>'
        # status pill
        f'<rect x="44" y="296" width="{len(DATA["now"]) * 7.4 + 44:.0f}" height="28" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
        f'<circle cx="62" cy="310" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>'
        f'<circle cx="62" cy="310" r="4" fill="none" stroke="{GREEN}"><animate attributeName="r" values="4;10" dur="1.8s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".8;0" dur="1.8s" repeatCount="indefinite"/></circle>'
        f'<text x="76" y="315" font-family="{SANS}" font-size="13" fill="{TEXT}">{x(DATA["now"])}</text>'
    )
    out.append(appear(left, 0.1, rise=10))

    # terminal window
    tx, ty, tw, th = 492, 28, 480, 304
    out.append(
        f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
        f'<path d="M{tx} {ty + 34}H{tx + tw}" stroke="{LINE}"/>'
        + "".join(f'<circle cx="{tx + 20 + i * 18}" cy="{ty + 17}" r="5.5" fill="{c}"/>'
                  for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]))
        + f'<text x="{tx + tw / 2}" y="{ty + 22}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{DIM}">asad@kurnool — zsh</text>'
    )

    px, y, t = tx + 22, ty + 66, 0.6
    lh = 23
    prompt = f'<text x="{px}" y="{{y}}" font-family="{MONO}" font-size="14" fill="{GREEN}">❯</text>'

    out.append(appear(prompt.format(y=y), t, rise=0))
    s, t = typed("crew up --all", px + 18, y, t + 0.15, "h0")
    out.append(s)
    y += lh + 4
    t += 0.25

    for i, (agent, tools) in enumerate(DATA["agents"]):
        line = (
            f'<text x="{px}" y="{y}" font-family="{MONO}" font-size="13" fill="{FAINT}">↳</text>'
            f'<text x="{px + 18}" y="{y}" font-family="{MONO}" font-size="13" fill="{BLUE}">{x(agent)}</text>'
            f'<text x="{px + 104}" y="{y}" font-family="{MONO}" font-size="12" fill="{DIM}">{x(tools)}</text>'
        )
        # status flips from "booting" to "ready"
        status = (
            f'<text x="{tx + tw - 22}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{AMBER}">'
            f'···<set attributeName="opacity" to="0" begin="{t + 0.55:.2f}s" fill="freeze"/></text>'
            f'<text x="{tx + tw - 22}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{GREEN}" opacity="0">'
            f'ready<set attributeName="opacity" to="1" begin="{t + 0.55:.2f}s" fill="freeze"/></text>'
        )
        out.append(appear(line + status, t, rise=4))
        y += lh
        t += 0.32

    t += 0.45
    done = (
        f'<text x="{px}" y="{y + 6}" font-family="{MONO}" font-size="13" fill="{GREEN}">✓</text>'
        f'<text x="{px + 18}" y="{y + 6}" font-family="{MONO}" font-size="13" fill="{TEXT}">'
        f'{len(DATA["agents"])}/{len(DATA["agents"])} agents online — shipping to production</text>'
    )
    out.append(appear(done, t, rise=4))
    y += lh + 16
    t += 0.5
    out.append(appear(prompt.format(y=y), t, rise=0))
    out.append(cursor(px + 18, y, t))

    out.append("</svg>")
    return "".join(out)


# ══════════════════════════════════════════════════════════════════════
# 2. CAREER TRACE — experience as spans, wins as events (LangSmith-style)
# ══════════════════════════════════════════════════════════════════════
def months(ym: str) -> int:
    if ym == "now":
        today = dt.date.today()
        return today.year * 12 + today.month - 1
    y, m = map(int, ym.split("-"))
    return y * 12 + m - 1


def render_trace() -> str:
    tr = DATA["trace"]
    spans, events = tr["spans"], tr["events"]
    W = 1000
    LX, RX = 360, 968                      # timeline area
    top = 92
    row = 38
    ev_top = top + len(spans) * row + 30
    H = ev_top + 40 + len(events) * 20 + 24

    m0, m1 = months(tr["start"]), months(tr["end"])
    # quiet stretches are squeezed so recent work gets the room it deserves
    squeeze = [(months(a), months(b), w) for a, b, w in tr.get("compress", [])]

    def weight(m: int) -> float:
        return next((w for a, b, w in squeeze if a <= m <= b), 1.0)

    cum = [0.0]
    for m in range(m0, m1 + 1):
        cum.append(cum[-1] + weight(m))
    unit = (RX - LX) / cum[-1]

    def px(ym: str) -> float:
        k = min(max(months(ym) - m0, 0), m1 - m0 + 1)
        return LX + cum[k] * unit

    def month_w(ym: str) -> float:
        return weight(months(ym)) * unit

    out = [svg_open(W, H, "Career trace"), frame(W, H)]
    total_months = sum(max(months(s["to"]) - months(s["from"]) + 1, 1) for s in spans)
    out.append(
        f'<text x="32" y="44" font-family="{MONO}" font-size="15" fill="{TEXT}" font-weight="600">career.trace</text>'
        f'<text x="152" y="44" font-family="{MONO}" font-size="13" fill="{DIM}">'
        f'{len(spans)} spans · {len(events)} events · {total_months} span-months · status '
        f'<tspan fill="{GREEN}">running</tspan></text>'
        f'<path d="M1 62H{W - 1}" stroke="{LINE}"/>'
    )

    # year ticks
    for year in range(int(tr["start"][:4]), int(tr["end"][:4]) + 1):
        ym = f"{year}-01"
        if months(tr["start"]) <= months(ym) <= months(tr["end"]):
            gx = px(ym)
            out.append(
                f'<path d="M{gx:.1f} {top - 14}V{ev_top - 6}" stroke="{LINE}" stroke-dasharray="2 4"/>'
                f'<text x="{gx + 4:.1f}" y="{top - 16}" font-family="{MONO}" font-size="11" fill="{DIM}">{year}</text>'
            )

    # zig-zag break marks where the axis is squeezed
    for a, b, _ in squeeze:
        bx = (LX + cum[a - m0] * unit + LX + cum[b - m0 + 1] * unit) / 2
        out.append(
            f'<rect x="{bx - 9:.1f}" y="{ev_top - 8}" width="18" height="16" fill="{BG}"/>'
            f'<path d="M{bx - 8:.1f} {ev_top}l4 -6 4 12 4 -12 4 6" fill="none" stroke="{DIM}" stroke-width="1.3"/>'
            f'<text x="{bx:.1f}" y="{ev_top + 20}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{FAINT}">compressed</text>'
        )

    # "now" marker
    nx = px("now")
    out.append(
        f'<path d="M{nx:.1f} {top - 14}V{ev_top - 6}" stroke="{GREEN}" stroke-opacity=".5"/>'
        f'<text x="{nx:.1f}" y="{top - 16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GREEN}">now</text>'
    )

    colors = {"work": BLUE, "learn": PURPLE}
    for i, s in enumerate(spans):
        y = top + i * row
        x0, x1 = px(s["from"]), px(s["to"]) + (month_w(s["to"]) if s["to"] != "now" else 0)
        if s["to"] == "now":
            x1 = nx
        bw = max(x1 - x0, 8)
        c = colors.get(s["kind"], BLUE)
        b = 0.3 + i * 0.22
        live = s["to"] == "now"
        dur_m = max(months(s["to"]) - months(s["from"]) + 1, 1)
        label = (
            f'<text x="32" y="{y + 16}" font-family="{SANS}" font-size="14" font-weight="600" fill="{TEXT}">{x(s["name"])}</text>'
            f'<text x="32" y="{y + 31}" font-family="{SANS}" font-size="12" fill="{DIM}">{x(s["org"])}</text>'
        )
        out.append(appear(label, b, rise=4))
        out.append(
            f'<rect x="{x0:.1f}" y="{y + 8}" width="0" height="16" rx="4" fill="{c}" fill-opacity=".22" stroke="{c}" stroke-opacity=".9">'
            f'<animate attributeName="width" from="0" to="{bw:.1f}" begin="{b:.2f}s" dur="0.7s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>'
        )
        tag = f"{dur_m} mo" + (" · live" if live else "")
        tag_x = x0 + bw + 8
        anchor = "start"
        if tag_x + 70 > W - 10:
            tag_x, anchor = x0 - 8, "end"
        out.append(appear(
            f'<text x="{tag_x:.1f}" y="{y + 21}" text-anchor="{anchor}" font-family="{MONO}" font-size="11" fill="{c if live else DIM}">{x(tag)}</text>',
            b + 0.6, rise=0))
        if live:
            out.append(
                f'<circle cx="{x0 + bw:.1f}" cy="{y + 16}" r="3" fill="{GREEN}" opacity="0">'
                f'<set attributeName="opacity" to="1" begin="{b + 0.7:.2f}s" fill="freeze"/>'
                f'<animate attributeName="r" values="3;6;3" dur="1.6s" begin="{b + 0.7:.2f}s" repeatCount="indefinite"/></circle>'
            )

    # events: diamonds on an axis + staircase labels so close dates never collide
    out.append(
        f'<path d="M{LX} {ev_top}H{RX}" stroke="{LINE}"/>'
        f'<text x="32" y="{ev_top + 5}" font-family="{SANS}" font-size="14" font-weight="600" fill="{TEXT}">Wins</text>'
        f'<text x="32" y="{ev_top + 21}" font-family="{SANS}" font-size="12" fill="{DIM}">ranked results</text>'
    )
    base_t = 0.3 + len(spans) * 0.22 + 0.4
    for i, e in enumerate(events):
        ex = px(e["at"]) + month_w(e["at"]) / 2
        ly = ev_top + 30 + i * 20
        right_side = ex < (LX + RX) / 2
        lx = ex + 10 if right_side else ex - 10
        anchor = "start" if right_side else "end"
        t = base_t + i * 0.18
        g = (
            f'<path d="M{ex:.1f} {ev_top}V{ly - 4}" stroke="{AMBER}" stroke-opacity=".5"/>'
            f'<path d="M{ex:.1f} {ev_top - 6}l6 6-6 6-6-6z" fill="{AMBER}"/>'
            f'<text x="{lx:.1f}" y="{ly}" text-anchor="{anchor}" font-family="{MONO}" font-size="12" fill="{TEXT}">'
            f'<tspan fill="{AMBER}">◆ </tspan>{x(e["label"])}</text>'
        )
        out.append(appear(g, t, rise=3))

    out.append("</svg>")
    return "".join(out)


# ══════════════════════════════════════════════════════════════════════
# 3. PROJECT CARDS — one SVG per project so each card can be a link
# ══════════════════════════════════════════════════════════════════════
def wrap(text: str, limit: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > limit and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


def render_card(p: dict, idx: int) -> str:
    W, H = 480, 236
    a = p["accent"]
    out = [svg_open(W, H, p["title"]), frame(W, H)]
    out.append(
        f'<defs><linearGradient id="sweep" x1="0" x2="1">'
        f'<stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}"/>'
        f'<stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="top"><rect x="1" y="1" width="{W - 2}" height="3" rx="1.5"/></clipPath></defs>'
        f'<rect x="1" y="1" width="{W - 2}" height="3" fill="{a}" fill-opacity=".25" clip-path="url(#top)"/>'
        f'<rect x="-160" y="1" width="160" height="3" fill="url(#sweep)" clip-path="url(#top)">'
        f'<animate attributeName="x" from="-160" to="{W}" dur="3.2s" begin="{idx * 0.45:.2f}s" repeatCount="indefinite"/></rect>'
    )
    out.append(
        f'<text x="26" y="40" font-family="{MONO}" font-size="11" font-weight="600" fill="{a}" letter-spacing="1.2">{x(p["badge"])}</text>'
        f'<text x="{W - 26}" y="40" text-anchor="end" font-family="{SANS}" font-size="16" fill="{DIM}">↗</text>'
        f'<text x="26" y="72" font-family="{SANS}" font-size="22" font-weight="700" fill="{TEXT}" letter-spacing="-.3">{x(p["title"])}</text>'
    )
    for j, ln in enumerate(wrap(p["line"], 58)[:2]):
        out.append(f'<text x="26" y="{98 + j * 19}" font-family="{SANS}" font-size="13.5" fill="{DIM}">{x(ln)}</text>')

    colw = (W - 52) / 3
    for j, (val, lab) in enumerate(p["metrics"]):
        mx = 26 + j * colw
        g = (
            f'<text x="{mx:.1f}" y="168" font-family="{SANS}" font-size="26" font-weight="700" fill="{TEXT}">{x(val)}</text>'
            f'<text x="{mx:.1f}" y="187" font-family="{MONO}" font-size="11" fill="{DIM}">{x(lab)}</text>'
        )
        out.append(appear(g, 0.25 + idx * 0.12 + j * 0.15, rise=8))
        if j:
            out.append(f'<path d="M{mx - 12:.1f} 146V190" stroke="{LINE}"/>')

    out.append(
        f'<path d="M1 204H{W - 1}" stroke="{LINE}"/>'
        f'<circle cx="30" cy="220" r="3.5" fill="{a}"/>'
        f'<text x="42" y="224" font-family="{MONO}" font-size="11.5" fill="{DIM}">{x(p["stack"])}</text>'
        "</svg>"
    )
    return "".join(out)


# ══════════════════════════════════════════════════════════════════════
# 4. LIVE — real activity + contribution heatmap, refreshed by GitHub Actions
# ══════════════════════════════════════════════════════════════════════
GQL = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { name stargazerCount primaryLanguage { name color } }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}"""


def gh(url: str, token: str, body: dict | None = None):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "User-Agent": "profile-renderer"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def fetch_live(user: str, token: str) -> dict:
    res = gh("https://api.github.com/graphql", token, {"query": GQL, "variables": {"login": user}})
    if "errors" in res:
        raise RuntimeError(res["errors"])
    u = res["data"]["user"]
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]

    langs: dict[str, list] = {}
    for repo in u["repositories"]["nodes"]:
        lang = repo["primaryLanguage"]
        if lang:
            entry = langs.setdefault(lang["name"], [0, lang["color"] or DIM])
            entry[0] += 1

    events = gh(f"https://api.github.com/users/{user}/events/public?per_page=60", token)
    return {
        "days": [(d["date"], d["contributionCount"]) for d in days],
        "total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "prs": cc["totalPullRequestContributions"],
        "repos": u["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        "langs": sorted(langs.items(), key=lambda kv: -kv[1][0]),
        "feed": parse_events(events),
    }


def parse_events(events: list) -> list[tuple[str, str, str, str]]:
    """-> [(iso_time, verb, repo, detail)] newest first, one line per meaningful event."""
    feed = []
    for ev in events:
        repo = ev["repo"]["name"].split("/", 1)[-1]
        p, kind = ev.get("payload", {}), ev["type"]
        if kind == "PushEvent":
            commits = p.get("commits") or []
            msg = commits[-1]["message"].splitlines()[0] if commits else "pushed changes"
            feed.append((ev["created_at"], "push", repo, msg))
        elif kind == "PullRequestEvent" and p.get("action") in ("opened", "closed"):
            verb = "merged" if p.get("pull_request", {}).get("merged") else p["action"]
            feed.append((ev["created_at"], "pr", repo, f'{verb}: {p["pull_request"]["title"]}'))
        elif kind == "CreateEvent" and p.get("ref_type") == "repository":
            feed.append((ev["created_at"], "new", repo, "created repository"))
        elif kind == "ReleaseEvent":
            feed.append((ev["created_at"], "release", repo, p.get("release", {}).get("tag_name", "")))
        elif kind == "IssuesEvent" and p.get("action") == "opened":
            feed.append((ev["created_at"], "issue", repo, p["issue"]["title"]))
    # collapse consecutive pushes to the same repo
    out, last = [], None
    for item in feed:
        if last and item[1] == "push" and last[1] == "push" and item[2] == last[2]:
            continue
        out.append(item)
        last = item
    return out[:6]


def mock_live() -> dict:
    rnd = random.Random(7)
    today = dt.date.today()
    start = today - dt.timedelta(days=364 + (today.weekday() + 1) % 7)
    days = []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        busy = 0.35 + 0.55 * (i / 364)
        days.append((d.isoformat(), rnd.choice([0, 0, 1, 2, 3, 5, 8, 12]) if rnd.random() < busy else 0))
    now = dt.datetime.now(dt.timezone.utc)
    ago = lambda h: (now - dt.timedelta(hours=h)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "days": days, "total": sum(c for _, c in days), "commits": 1184, "prs": 37,
        "repos": 64, "stars": 41,
        "langs": [("Python", [27, "#3572A5"]), ("TypeScript", [12, "#3178c6"]),
                  ("JavaScript", [10, "#f1e05a"]), ("Jupyter Notebook", [7, "#DA5B0B"]),
                  ("Java", [5, "#b07219"]), ("HTML", [3, "#e34c26"])],
        "feed": [
            (ago(2), "push", "shaikasadahmed2k23", "feat: live agent-log profile"),
            (ago(9), "push", "ration-seva-", "cloudinary: signed upload widget"),
            (ago(27), "pr", "MergeGuard", "merged: trust profile badges"),
            (ago(50), "push", "amazon-ml-challenge-2026", "docs: methodology write-up"),
            (ago(80), "new", "self-improving-research-agent_Submission", "created repository"),
            (ago(130), "push", "agentrouter", "perf: redis semantic cache"),
        ],
    }


def ago_str(iso: str) -> str:
    then = dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    s = (dt.datetime.now(dt.timezone.utc) - then).total_seconds()
    if s < 3600:
        return f"{max(int(s // 60), 1)}m"
    if s < 86400:
        return f"{int(s // 3600)}h"
    return f"{int(s // 86400)}d"


def streaks(days: list[tuple[str, int]]) -> tuple[int, int]:
    counts = [c for _, c in days]
    best = cur = 0
    for c in counts:
        cur = cur + 1 if c else 0
        best = max(best, cur)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:      # today not over yet
        i -= 1
    current = 0
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    return current, best


def clip(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


def render_live(d: dict) -> str:
    W, H = 1000, 470
    out = [svg_open(W, H, "Live GitHub activity"), frame(W, H)]
    now = dt.datetime.now(dt.timezone.utc)

    # header bar
    out.append(
        f'<circle cx="32" cy="34" r="4.5" fill="{GREEN}"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="46" y="39" font-family="{MONO}" font-size="14" fill="{TEXT}" font-weight="600">live</text>'
        f'<text x="88" y="39" font-family="{MONO}" font-size="13" fill="{DIM}">tail -f ~/github/activity.log</text>'
        f'<text x="{W - 28}" y="39" text-anchor="end" font-family="{MONO}" font-size="12" fill="{FAINT}">'
        f'rendered {now:%Y-%m-%d %H:%M} UTC by GitHub Actions</text>'
        f'<path d="M1 58H{W - 1}" stroke="{LINE}"/>'
    )

    # stat tiles
    cur, best = streaks(d["days"])
    tiles = [
        (f'{d["total"]:,}', "contributions · 1y", GREEN),
        (f'{d["commits"]:,}', "commits · 1y", BLUE),
        (f'{d["prs"]:,}', "pull requests · 1y", PURPLE),
        (f'{cur}d', f"current streak · best {best}d", AMBER),
        (f'{d["repos"]}', f'repos · {d["stars"]}★', CORAL),
    ]
    tw = (W - 56 - 4 * 12) / 5
    for i, (v, lab, c) in enumerate(tiles):
        tx = 28 + i * (tw + 12)
        g = (
            f'<rect x="{tx:.1f}" y="76" width="{tw:.1f}" height="70" rx="8" fill="{PANEL}" stroke="{LINE}"/>'
            f'<rect x="{tx:.1f}" y="76" width="3" height="70" rx="1.5" fill="{c}"/>'
            f'<text x="{tx + 18:.1f}" y="112" font-family="{SANS}" font-size="24" font-weight="700" fill="{TEXT}">{x(v)}</text>'
            f'<text x="{tx + 18:.1f}" y="132" font-family="{MONO}" font-size="11" fill="{DIM}">{x(lab)}</text>'
        )
        out.append(appear(g, 0.1 + i * 0.1, rise=6))

    # heatmap — cells light up week by week, then a scan line sweeps across forever
    days = d["days"][-371:]
    nonzero = sorted(c for _, c in days if c)
    def level(c: int) -> int:
        if not c or not nonzero:
            return 0
        q = [nonzero[int(len(nonzero) * f)] for f in (0.25, 0.5, 0.75)]
        return 1 + sum(c > t for t in q)

    hx, hy, cs, gap = 28, 184, 11, 3
    first = dt.date.fromisoformat(days[0][0])
    offset = (first.weekday() + 1) % 7         # GitHub weeks start on Sunday
    weeks = (len(days) + offset + 6) // 7
    out.append(f'<text x="{hx}" y="{hy - 12}" font-family="{MONO}" font-size="12" fill="{DIM}">contributions — last 12 months</text>')
    cells = []
    for i, (date, c) in enumerate(days):
        k = i + offset
        wk, wd = divmod(k, 7)
        cx, cy = hx + wk * (cs + gap), hy + wd * (cs + gap)
        lv = level(c)
        b = 0.5 + wk * 0.018
        fill = HEAT[lv]
        cells.append(
            f'<rect x="{cx}" y="{cy}" width="{cs}" height="{cs}" rx="2.5" fill="{HEAT[0]}">'
            + (f'<set attributeName="fill" to="{fill}" begin="{b:.2f}s" fill="freeze"/>' if lv else "")
            + f'<title>{x(date)}: {c}</title></rect>'
        )
    out.append(f'<g>{"".join(cells)}</g>')
    grid_w = weeks * (cs + gap)
    out.append(
        f'<defs><linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{GREEN}" stop-opacity=".35"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="grid"><rect x="{hx}" y="{hy}" width="{grid_w}" height="{7 * (cs + gap)}"/></clipPath></defs>'
        f'<rect x="{hx - 60}" y="{hy}" width="60" height="{7 * (cs + gap)}" fill="url(#scan)" clip-path="url(#grid)">'
        f'<animate attributeName="x" from="{hx - 60}" to="{hx + grid_w}" dur="4.5s" begin="2s" repeatCount="indefinite"/></rect>'
    )

    # language bar (right of heatmap)
    lx = hx + grid_w + 26
    lw = W - 28 - lx
    total = sum(v[0] for _, v in d["langs"]) or 1
    out.append(f'<text x="{lx}" y="{hy - 12}" font-family="{MONO}" font-size="12" fill="{DIM}">languages · by repo</text>')
    cx = lx
    for i, (name, (n, color)) in enumerate(d["langs"][:6]):
        seg = lw * n / total
        out.append(
            f'<rect x="{cx:.1f}" y="{hy}" width="0" height="10" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{max(seg - 2, 1):.1f}" begin="{0.6 + i * 0.12:.2f}s" dur=".5s" fill="freeze"/></rect>'
        )
        cx += seg
        ly = hy + 32 + i * 15
        out.append(appear(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4" fill="{color}"/>'
            f'<text x="{lx + 16}" y="{ly}" font-family="{SANS}" font-size="12" fill="{TEXT}">{x(name)}</text>'
            f'<text x="{lx + lw}" y="{ly}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{DIM}">{n * 100 / total:.0f}%</text>',
            0.8 + i * 0.1, rise=3))

    # activity feed
    fy = hy + 7 * (cs + gap) + 40
    out.append(f'<path d="M1 {fy - 18}H{W - 1}" stroke="{LINE}"/>')
    verb_color = {"push": GREEN, "pr": PURPLE, "new": BLUE, "release": AMBER, "issue": CORAL}
    t = 1.6
    for i, (iso, verb, repo, detail) in enumerate(d["feed"]):
        y = fy + i * 24
        line = (
            f'<text x="28" y="{y}" font-family="{MONO}" font-size="12.5" fill="{FAINT}">{x(ago_str(iso).rjust(4))} ago</text>'
            f'<text x="120" y="{y}" font-family="{MONO}" font-size="12.5" fill="{verb_color.get(verb, DIM)}">{x(verb.ljust(7))}</text>'
            f'<text x="196" y="{y}" font-family="{MONO}" font-size="12.5" fill="{BLUE}">{x(clip(repo, 30))}</text>'
            f'<text x="452" y="{y}" font-family="{MONO}" font-size="12.5" fill="{TEXT}">{x(clip(detail, 66))}</text>'
        )
        out.append(appear(line, t, rise=4))
        t += 0.2
    out.append(cursor(28, fy + len(d["feed"]) * 24, t, size=12))
    out.append("</svg>")
    return "".join(out)


# ══════════════════════════════════════════════════════════════════════
def main() -> int:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "hero.svg").write_text(render_hero(), encoding="utf-8")
    (ASSETS / "trace.svg").write_text(render_trace(), encoding="utf-8")
    for i, p in enumerate(DATA["projects"]):
        (ASSETS / f"card-{p['slug']}.svg").write_text(render_card(p, i % 2), encoding="utf-8")

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if "--mock" in sys.argv:
        live = mock_live()
    elif token:
        try:
            live = fetch_live(DATA["username"], token)
        except (urllib.error.URLError, RuntimeError, KeyError) as err:
            print(f"live fetch failed, keeping previous live.svg: {err}", file=sys.stderr)
            return 0
    else:
        print("no GITHUB_TOKEN; skipping live.svg (use --mock for a preview)", file=sys.stderr)
        return 0
    (ASSETS / "live.svg").write_text(render_live(live), encoding="utf-8")
    print("rendered:", ", ".join(sorted(p.name for p in ASSETS.glob("*.svg"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
