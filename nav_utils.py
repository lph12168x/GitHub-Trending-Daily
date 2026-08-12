#!/usr/bin/env python3
"""Reusable pager-nav injection for GitHub Trending daily report pages.

Adds a theme-aware navigation bar (上一个 / 主页 / 最新 / 下一个) to every
github-trending-YYYY-MM-DD.html page so readers can quickly jump between
reports. The injection is idempotent: re-running only updates the nav, never
duplicates the CSS or the bar.
"""

import glob
import re

NAV_CSS = """
.pagenav{max-width:960px;margin:22px auto;padding:0 20px;display:flex;gap:10px;flex-wrap:wrap}
.pagenav a,.pagenav span{display:inline-flex;align-items:center;gap:6px;text-decoration:none;
  font-size:.86rem;font-weight:600;padding:8px 14px;border-radius:999px;
  border:1px solid var(--line);background:var(--card);color:var(--muted);transition:.15s}
.pagenav a:hover{color:var(--accent);border-color:var(--accent);transform:translateY(-1px)}
.pagenav .pn-home{color:var(--accent);border-color:var(--accent)}
.pagenav .pn-latest{color:var(--accent-2);border-color:var(--accent-2)}
.pagenav .disabled{opacity:.4;pointer-events:none}
@media(max-width:680px){.pagenav{gap:8px}.pagenav a,.pagenav span{padding:7px 11px;font-size:.8rem}}
"""

NAV_START = "<!--PAGENAV-START-->"
NAV_END = "<!--PAGENAV-END-->"


def _collect_dates():
    dates = []
    for fn in glob.glob("github-trending-*.html"):
        ds = fn.replace("github-trending-", "").replace(".html", "")
        if ds == "index" or "-" not in ds:
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}$", ds):
            dates.append(ds)
    dates.sort()
    return dates


def _item(href, label, cls, disabled):
    if disabled or not href:
        return f'<span class="disabled">{label}</span>'
    return f'<a class="{cls}" href="{href}">{label}</a>'


def _nav_block(cur, dates):
    idx = dates.index(cur)
    prev = dates[idx - 1] if idx > 0 else None
    nxt = dates[idx + 1] if idx < len(dates) - 1 else None
    latest = dates[-1]
    prev_item = _item(
        f"github-trending-{prev}.html" if prev else None, "← 上一个", "pn-prev",
        disabled=prev is None)
    home = '<a class="pn-home" href="index.html">🏠 主页</a>'
    latest_item = _item(
        f"github-trending-{latest}.html", "⚡ 最新", "pn-latest",
        disabled=(cur == latest))
    next_item = _item(
        f"github-trending-{nxt}.html" if nxt else None, "下一个 →", "pn-next",
        disabled=nxt is None)
    return (f"{NAV_START}\n  <nav class=\"pagenav\">{prev_item}{home}{latest_item}{next_item}"
            f"</nav>\n  {NAV_END}")


def inject_nav():
    """Inject (or refresh) the pager nav into every daily report page.

    Adds a theme-aware nav bar (上一个 / 主页 / 最新 / 下一个) immediately
    after the header AND again right before the footer, so readers can switch
    reports directly after finishing without scrolling back to the top.
    The injection is idempotent: re-running only updates the nav, never
    duplicates the CSS or the bars.
    """
    dates = _collect_dates()
    if not dates:
        print("[nav] No daily pages found, skip.")
        return 0
    changed = 0
    for ds in dates:
        fn = f"github-trending-{ds}.html"
        try:
            html = open(fn, encoding="utf-8").read()
        except OSError:
            continue
        # strip any prior injected nav / old backnav to stay idempotent
        html = re.sub(re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\s*",
                      "", html, flags=re.S)
        html = re.sub(r'<div class="backnav">.*?</div>\s*', "", html, flags=re.S)
        block = _nav_block(ds, dates)
        m = re.search(r"</header>", html)
        if m:
            html = html[:m.end()] + "\n" + block + "\n" + html[m.end():]
        else:
            html = html.replace("<body>", "<body>\n" + block, 1)
        # bottom nav: place right before the footer (or before </body> fallback)
        fm = re.search(r'<div class="footer">', html)
        if fm:
            html = html[:fm.start()] + block + "\n" + html[fm.start():]
        else:
            html = html.replace("</body>", block + "\n</body>", 1)
        if ".pagenav{" not in html:
            html = html.replace("</style>", NAV_CSS + "\n  </style>", 1)
        open(fn, "w", encoding="utf-8").write(html)
        changed += 1
    print(f"[nav] Injected top + bottom pager nav into {changed} daily pages.")
    return changed


if __name__ == "__main__":
    inject_nav()
