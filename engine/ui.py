"""Terminal output helpers: colour, boxes, tables. Honours NO_COLOR / non-TTY."""
from __future__ import annotations

import os
import sys

_USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def _c(code: str) -> str:
    return code if _USE_COLOR else ""


RESET = _c("\033[0m")
BOLD = _c("\033[1m")
DIM = _c("\033[2m")
RED = _c("\033[31m")
GREEN = _c("\033[32m")
YELLOW = _c("\033[33m")
BLUE = _c("\033[34m")
MAGENTA = _c("\033[35m")
CYAN = _c("\033[36m")
GREY = _c("\033[90m")

# KAIPTC brand accent (purple, matches the courseware)
KALI = _c("\033[38;5;135m")


def banner(line: str) -> None:
    bar = "═" * (len(_strip(line)) + 2)
    print(f"{KALI}{BOLD}╔{bar}╗{RESET}")
    print(f"{KALI}{BOLD}║ {line} ║{RESET}")
    print(f"{KALI}{BOLD}╚{bar}╝{RESET}")


def header(text: str) -> None:
    print(f"\n{BOLD}{KALI}▶ {text}{RESET}")


def ok(text: str) -> None:
    print(f"  {GREEN}✔{RESET} {text}")


def fail(text: str) -> None:
    print(f"  {RED}✘{RESET} {text}")


def warn(text: str) -> None:
    print(f"  {YELLOW}!{RESET} {text}")


def info(text: str) -> None:
    print(f"  {CYAN}•{RESET} {text}")


def dim(text: str) -> None:
    print(f"{GREY}{text}{RESET}")


def error(text: str) -> None:
    print(f"{RED}{BOLD}error:{RESET} {text}", file=sys.stderr)


def cmd(text: str) -> str:
    """Render a shell command the student should type."""
    return f"{GREEN}$ {text}{RESET}"


def _strip(text: str) -> str:
    """Length without ANSI codes, for alignment."""
    out, i = [], 0
    while i < len(text):
        if text[i] == "\033":
            while i < len(text) and text[i] != "m":
                i += 1
            i += 1
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def table(rows: list[list[str]], headers: list[str]) -> None:
    """Print an aligned table. Cells may contain ANSI colour."""
    cols = len(headers)
    widths = [len(_strip(h)) for h in headers]
    for r in rows:
        for i in range(cols):
            widths[i] = max(widths[i], len(_strip(r[i])) if i < len(r) else 0)

    def line(cells: list[str], bold: bool = False) -> str:
        out = []
        for i in range(cols):
            cell = cells[i] if i < len(cells) else ""
            pad = widths[i] - len(_strip(cell))
            out.append((BOLD + cell + RESET if bold else cell) + " " * pad)
        return "  ".join(out)

    print("  " + line(headers, bold=True))
    print("  " + GREY + "  ".join("─" * w for w in widths) + RESET)
    for r in rows:
        print("  " + line(r))
