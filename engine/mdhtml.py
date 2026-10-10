"""Markdown -> HTML converter (stdlib only), shared by the web app and the
static lessons-HTML build script.

Supports the subset used across lessons, briefings and worksheets: headings,
bold/italic/code, lists, tables, blockquotes, rules, bare links, PLUS two
presentation extensions used by the deep lessons:

  * Fenced code blocks render as a titled "terminal card". An info string after
    the opening fence becomes the card title:  ```Terminal — DNS series
  * Callout blocks:
        ::: key | Key concept
        body markdown...
        :::
    types: key, warning, ghana, case, note, outcome.
"""
from __future__ import annotations

import html
import re

CALLOUTS = {
    "key":     ("🔑", "Key concept", "key"),
    "warning": ("⚠",  "Warning", "warning"),
    "ghana":   ("🇬🇭", "Ghana in focus", "ghana"),
    "case":    ("📁", "Case study", "case"),
    "note":    ("ℹ",  "Note", "note"),
    "outcome": ("🎯", "Learning outcome", "outcome"),
    "quote":   ("❝",  "", "quote"),
}


def _inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\">])(https?://[^\s<)]+)",
                  r'<a href="\1" target="_blank" rel="noopener">\1</a>', text)
    return text


def _join_list_continuations(lines: list[str]) -> list[str]:
    out: list[str] = []
    in_code = False
    for raw in lines:
        if raw.strip().startswith("```"):
            in_code = not in_code
            out.append(raw)
            continue
        if (not in_code and re.match(r"^\s+\S", raw)
                and not re.match(r"^\s*([-*]|\d+\.)\s", raw) and out
                and re.match(r"^([-*]|\d+\.)\s", out[-1].lstrip())):
            out[-1] = out[-1].rstrip() + " " + raw.strip()
            continue
        out.append(raw)
    return out


def _table_html(rows: list[str]) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(set(c) <= set("-: ") for c in r)]
    if not cells:
        return ""
    head, *body = cells
    out = ["<div class='tablewrap'><table><thead><tr>"]
    out += [f"<th>{_inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def _code_card(info: str, code: str) -> str:
    title = info.strip() or "Terminal"
    return (f"<div class='term'><div class='term-bar'><span class='dots'>"
            f"<i></i><i></i><i></i></span><span class='term-title'>{html.escape(title)}</span></div>"
            f"<pre><code>{code}</code></pre></div>")


def _figure_html(title: str, raw_lines: list[str]) -> str:
    """A diagram figure. Body is an ASCII diagram, optionally followed by a line
    '~~~svg~~~' and inline SVG; the web reader prefers the SVG, falling back to
    the ASCII rendered in a monospace block."""
    marker = [ln.strip() for ln in raw_lines]
    if "~~~svg~~~" in marker:
        idx = marker.index("~~~svg~~~")
        svg = "\n".join(raw_lines[idx + 1:]).strip()
        body = f"<div class='fig-svg'>{svg}</div>"   # SVG passed through raw
    else:
        body = "<pre class='fig-ascii'>" + html.escape("\n".join(raw_lines), quote=False) + "</pre>"
    cap = f"<figcaption>{html.escape(title)}</figcaption>" if title else ""
    return f"<figure class='fig'>{body}{cap}</figure>"


def md_to_html(md: str) -> str:
    lines = _join_list_continuations(md.splitlines())
    out: list[str] = []
    i = 0
    para: list[str] = []
    list_mode = None

    def flush_para():
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list():
        nonlocal list_mode
        if list_mode:
            out.append(f"</{list_mode}>")
            list_mode = None

    while i < len(lines):
        s = lines[i].strip()

        # ----- callout block -----
        if s.startswith(":::"):
            flush_para(); close_list()
            spec = s[3:].strip()
            m = re.match(r"(\w+)\s*(?:\|\s*(.*))?$", spec)
            kind = (m.group(1).lower() if m else "note")
            override = (m.group(2).strip() if m and m.group(2) else "")
            icon, default_title, cls = CALLOUTS.get(kind, CALLOUTS["note"])
            title = override or default_title
            i += 1
            buf = []
            while i < len(lines) and lines[i].strip() != ":::":
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing :::
            inner = md_to_html("\n".join(buf))
            head = (f"<div class='callout-h'><span class='ci'>{icon}</span>{html.escape(title)}</div>"
                    if title else "")
            out.append(f"<div class='callout callout-{cls}'>{head}<div class='callout-b'>{inner}</div></div>")
            continue

        # ----- fenced code / terminal card / diagram figure -----
        if s.startswith("```"):
            flush_para(); close_list()
            info = s[3:].strip()
            raw = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                raw.append(lines[i])
                i += 1
            i += 1
            if info.split(" ", 1)[0] == "figure":
                out.append(_figure_html(info[len("figure"):].strip(), raw))
            else:
                out.append(_code_card(info, "\n".join(html.escape(x, quote=False) for x in raw)))
            continue

        # ----- tables -----
        if s.startswith("|") and "|" in s[1:]:
            flush_para(); close_list()
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(_table_html(block))
            continue

        if not s:
            flush_para(); close_list()
        elif s.startswith("# "):
            flush_para(); close_list(); out.append("<h1>" + _inline(s[2:]) + "</h1>")
        elif s.startswith("## "):
            flush_para(); close_list(); out.append("<h2>" + _inline(s[3:]) + "</h2>")
        elif s.startswith("### "):
            flush_para(); close_list(); out.append("<h3>" + _inline(s[4:]) + "</h3>")
        elif s.startswith("#### "):
            flush_para(); close_list(); out.append("<h4>" + _inline(s[5:]) + "</h4>")
        elif s in ("---", "***", "___"):
            flush_para(); close_list(); out.append("<hr>")
        elif s.startswith(">"):
            flush_para(); close_list()
            out.append("<blockquote>" + _inline(s.lstrip("> ").rstrip()) + "</blockquote>")
        elif re.match(r"^[-*] ", s):
            flush_para()
            if list_mode != "ul":
                close_list(); out.append("<ul>"); list_mode = "ul"
            out.append("<li>" + _inline(s[2:]) + "</li>")
        elif re.match(r"^\d+\. ", s):
            flush_para()
            if list_mode != "ol":
                close_list(); out.append("<ol>"); list_mode = "ol"
            out.append("<li>" + _inline(s.split(". ", 1)[1]) + "</li>")
        else:
            if list_mode:
                close_list()
            para.append(s)
        i += 1
    flush_para(); close_list()
    return "\n".join(out)
