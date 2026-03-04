"""Load and format built-in prompt skills for documentation agents."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

SKILLS_DIR = Path(__file__).resolve().parent / "skills"
DEFAULT_SKILLS = ["mermaid-validator"]


def normalize_skill_names(skill_names: Optional[List[str]]) -> List[str]:
    """Normalize skill names and remove duplicates while preserving order."""
    if skill_names is None:
        candidate = DEFAULT_SKILLS
    else:
        candidate = skill_names

    normalized: List[str] = []
    seen = set()
    for raw_name in candidate:
        name = (raw_name or "").strip().lower()
        if not name or name in seen:
            continue
        seen.add(name)
        normalized.append(name)
    return normalized


def load_skill_content(skill_name: str) -> Optional[str]:
    """Load skill markdown content by name."""
    path = SKILLS_DIR / f"{skill_name}.md"
    if not path.exists():
        logger.warning(f"Skill not found: {skill_name} ({path})")
        return None
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        logger.warning(f"Failed to load skill {skill_name}: {exc}")
        return None


def render_skills_prompt(skill_names: Optional[List[str]]) -> str:
    """Render selected skills into a prompt block."""
    names = normalize_skill_names(skill_names)
    if not names:
        return ""

    blocks: List[str] = []
    for name in names:
        content = load_skill_content(name)
        if content:
            blocks.append(f"<SKILL name=\"{name}\">\n{content}\n</SKILL>")

    if not blocks:
        return ""

    return "<SKILLS>\n" + "\n\n".join(blocks) + "\n</SKILLS>"
