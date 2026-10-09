"""Markdown -> HTML converter (stdlib only), shared by the web app and the
static lessons-HTML build script. Handles the subset used across lessons,
briefings and worksheets: headings, bold/italic/code, fenced code, lists,
tables, blockquotes, horizontal rules, bare links."""
from __future__ import annotations

import html
import re


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
    out = ["<table><thead><tr>"]
    out += [f"<th>{_inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


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
        if s.startswith("```"):
            flush_para(); close_list()
            buf = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(html.escape(lines[i], quote=False))
                i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            i += 1
            continue
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
