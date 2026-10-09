"""A small, dependency-free Markdown-to-terminal renderer for lessons.

Handles the subset used in the lessons: headings, bold/italic/code spans,
fenced code blocks, bullet and numbered lists, block quotes, horizontal rules,
and simple pipe tables. Wraps prose to the terminal width for readability.
"""
from __future__ import annotations

import re
import shutil
import textwrap

from . import ui

_WIDTH = min(shutil.get_terminal_size((90, 24)).columns, 94)


def _inline(text: str) -> str:
    """Apply inline styles: **bold**, `code`, *italic*."""
    text = re.sub(r"`([^`]+)`", lambda m: ui.GREEN + m.group(1) + ui.RESET, text)
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: ui.BOLD + m.group(1) + ui.RESET, text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)",
                  lambda m: ui.CYAN + m.group(1) + ui.RESET, text)
    return text


def _wrap(text: str, indent: str = "") -> str:
    out = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        wrapped = textwrap.fill(para, width=_WIDTH - len(indent),
                                initial_indent=indent, subsequent_indent=indent,
                                break_long_words=False, break_on_hyphens=False)
        out.append(wrapped)
    return "\n".join(out)


def _render_table(rows: list[str]) -> None:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(set(c) <= set("-: ") for c in r)]  # drop ---|---
    if not cells:
        return
    ncol = max(len(r) for r in cells)
    # width from the VISIBLE text (markdown markers / ANSI removed)
    widths = [0] * ncol
    for r in cells:
        for i in range(ncol):
            if i < len(r):
                widths[i] = max(widths[i], len(ui._strip(_inline(r[i]))))
    header, *body = cells
    def fmt(r, bold=False):
        parts = []
        for i in range(ncol):
            raw = r[i] if i < len(r) else ""
            shown = (ui.BOLD + raw + ui.RESET) if bold else _inline(raw)
            pad = widths[i] - len(ui._strip(shown))
            parts.append(shown + " " * max(0, pad))
        return "  " + "  ".join(parts)
    print(fmt(header, bold=True))
    print("  " + ui.GREY + "  ".join("─" * w for w in widths) + ui.RESET)
    for r in body:
        print(fmt(r))


def _hang(text: str, marker: str, marker_vis: int, pad: int) -> str:
    """Wrap list-item text with a hanging indent. `marker` may contain ANSI
    colour; `marker_vis` is its visible width so indentation stays correct."""
    body = textwrap.fill(text, width=_WIDTH - pad, break_long_words=False,
                         break_on_hyphens=False).split("\n")
    lead = " " * (pad - 1 - marker_vis)
    out = [f"{lead}{marker} {body[0]}"]
    out += [" " * pad + ln for ln in body[1:]]
    return "\n".join(out)


def _join_list_continuations(lines: list[str]) -> list[str]:
    """Fold hard-wrapped list-item continuation lines back into their item, so
    lessons can be authored with naturally wrapped Markdown. Leaves fenced code
    blocks untouched. Paragraph continuations are handled later by the buffer."""
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


_CALLOUT = {"key": ("🔑", "KEY CONCEPT", ui.GOLD if hasattr(ui, "GOLD") else ui.YELLOW),
            "warning": ("⚠", "WARNING", ui.RED), "ghana": ("🇬🇭", "GHANA IN FOCUS", ui.CYAN),
            "case": ("📁", "CASE STUDY", ui.MAGENTA), "note": ("ℹ", "NOTE", ui.BLUE if hasattr(ui, "BLUE") else ui.CYAN),
            "outcome": ("🎯", "LEARNING OUTCOME", ui.GREEN), "quote": ("❝", "", ui.GREY)}


def render(md: str) -> None:
    import re as _re
    lines = _join_list_continuations(md.splitlines())
    i = 0
    in_code = False
    code_buf: list[str] = []
    code_title = ""
    para: list[str] = []

    def flush():
        if para:
            print(_wrap(_inline(" ".join(para))))
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # callout markers (::: type | Title  ...  :::)
        if not in_code and stripped.startswith(":::"):
            flush()
            spec = stripped[3:].strip()
            if spec:
                m = _re.match(r"(\w+)\s*(?:\|\s*(.*))?$", spec)
                kind = (m.group(1).lower() if m else "note")
                override = (m.group(2).strip() if m and m.group(2) else "")
                icon, label, col = _CALLOUT.get(kind, _CALLOUT["note"])
                title = override or label
                print(f"\n  {col}{ui.BOLD}{icon} {title}{ui.RESET}")
            i += 1
            continue

        # fenced code / terminal card
        if stripped.startswith("```"):
            flush()
            if in_code:
                if code_title:
                    print(f"  {ui.DIM}{code_title}{ui.RESET}")
                print(ui.GREY + "  ┌" + "─" * (_WIDTH - 4) + ui.RESET)
                for c in code_buf:
                    print("  " + ui.GREY + "│ " + ui.GREEN + c + ui.RESET)
                print(ui.GREY + "  └" + "─" * (_WIDTH - 4) + ui.RESET)
                code_buf = []; code_title = ""
            else:
                code_title = stripped[3:].strip()
            in_code = not in_code
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # tables (consecutive lines containing |)
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            flush()
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            _render_table(block)
            continue

        stripped = line.strip()
        if not stripped:
            flush()
            print()
        elif stripped.startswith("# "):
            flush(); print()
            ui.banner(_strip_md(stripped[2:]))
        elif stripped.startswith("## "):
            flush()
            print(f"\n{ui.BOLD}{ui.KALI}▶ {_inline(stripped[3:])}{ui.RESET}")
        elif stripped.startswith("### "):
            flush()
            print(f"\n{ui.BOLD}{ui.CYAN}{_inline(stripped[4:])}{ui.RESET}")
        elif stripped in ("---", "***", "___"):
            flush()
            print(ui.GREY + "  " + "─" * (_WIDTH - 2) + ui.RESET)
        elif stripped.startswith(">"):
            flush()
            print(f"  {ui.YELLOW}│{ui.RESET} {_inline(stripped.lstrip('> ').rstrip())}")
        elif re.match(r"^[-*] ", stripped):
            flush()
            print(_hang(_inline(stripped[2:]), f"{ui.KALI}•{ui.RESET}", 1, 4))
        elif re.match(r"^\d+\. ", stripped):
            flush()
            num = stripped.split(".", 1)[0]
            rest = stripped.split(". ", 1)[1]
            print(_hang(_inline(rest), f"{ui.BOLD}{num}.{ui.RESET}", len(num) + 1, len(num) + 3))
        else:
            para.append(stripped)
        i += 1
    flush()


def _strip_md(text: str) -> str:
    return re.sub(r"[*`]", "", text)
