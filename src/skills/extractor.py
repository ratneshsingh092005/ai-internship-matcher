import re
from .vocabulary import SKILL_ALIASES


def normalize_skill(skill: str) -> str:
    return SKILL_ALIASES.get(skill.strip().lower(), skill.strip())


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found = set()
    for alias, canonical in SKILL_ALIASES.items():
        pattern = rf"(?<![a-z0-9+#]){re.escape(alias)}(?![a-z0-9+#])"
        if re.search(pattern, text_lower):
            found.add(canonical)
    return sorted(found)


def parse_skill_field(value: str) -> list[str]:
    if not value:
        return []
    return sorted({normalize_skill(x) for x in re.split(r"[,;|]", str(value)) if x.strip()})
