from .matching_service import MatchingService


def build_recommendations(
    service: MatchingService,
    resume_text: str,
    top_k: int = 10
) -> list[dict]:

    results = service.match(
        resume_text,
        top_k
    )

    for result in results:
        gap = service.skill_gap(
            resume_text,
            result["job_id"]
        )

        quality = service.opportunity_analysis(
            result["job_id"]
        )

        result.update({
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
            "match_percentage": gap["match_percentage"],
            "warnings": quality["warnings"],
            "signals": quality["signals"],
        })

    return results