import numpy as np
SEMANTIC_WEIGHT = 0.65
SKILL_WEIGHT = 0.25
QUALITY_WEIGHT = 0.10


def skill_match_score(resume_skills: list[str], required_skills: list[str]) -> float:
    required = set(required_skills)
    if not required:
        return 100.0
    matched = required.intersection(resume_skills)
    return round(100.0 * len(matched) / len(required), 2)


def final_score(semantic_score: float, skill_score: float, quality_score: float) -> float:
    return round(
        SEMANTIC_WEIGHT * semantic_score
        + SKILL_WEIGHT * skill_score
        + QUALITY_WEIGHT * quality_score,
        2,
    )


def similarity_to_score(similarity: float) -> float:
    return float(np.clip((similarity + 1.0) * 50.0, 0.0, 100.0))
