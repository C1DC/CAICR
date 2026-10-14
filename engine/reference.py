"""The reference compendium — framework quick-cards, Ghana-law at-a-glance and
the master glossary. Stdlib only; the same Markdown the lessons use, so it
renders in both the terminal (mdrender) and the web app (mdhtml)."""
from __future__ import annotations

from . import paths

# Ordered topics. Each maps to reference/<id>.md.
TOPICS = [
    ("frameworks", "Frameworks Quick-Reference",
     "Kill Chain, ATT&CK, CSF 2.0, OWASP LLM Top 10, Pyramid of Pain & more"),
    ("ghana-law", "Ghana Cyber & Data Law",
     "Act 843 & Act 1038, DPC / CSA / CERT-GH, breach response"),
    ("glossary", "Master Glossary",
     "Every key term from the programme, A–Z"),
    ("forensics-tools", "Forensics Toolbox",
     "DFIR tools by domain (disk, memory, mobile, Windows, macOS, Linux, email, network) — free & paid — plus online analysis services"),
]


def discover() -> list[dict]:
    """The reference topics that actually have a file on disk."""
    out = []
    for tid, title, desc in TOPICS:
        if (paths.REFERENCE_DIR / f"{tid}.md").is_file():
            out.append({"id": tid, "title": title, "desc": desc})
    return out


def load(topic_id: str) -> str | None:
    f = paths.REFERENCE_DIR / f"{topic_id}.md"
    if not f.is_file():
        return None
    return f.read_text(encoding="utf-8")
