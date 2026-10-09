"""CAIC CyberLab engine — a zero-dependency lab orchestrator for KAIPTC.

Runs on a student's Kali box. Provisions isolated Docker targets per module,
serves the lab briefing, and grades the student's findings. The engine never
runs attack tools itself — the student does that, in their own terminal,
against targets confined to a private Docker subnet.
"""

__version__ = "1.0.0"
