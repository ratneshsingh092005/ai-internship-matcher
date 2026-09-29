from src.data.loader import load_internships
from src.data.preprocessing import clean_text
from src.skills.extractor import extract_skills, parse_skill_field
from src.embeddings.embedding_service import embed_texts
from src.matching.semantic_matcher import retrieve_matches
from src.matching.ranking import skill_match_score, final_score
from src.quality.analyzer import analyze_opportunity


class MatchingService:
    def __init__(self, dataset_path, index, metadata):
        self.df = load_internships(dataset_path)
        self.index = index
        self.metadata = metadata

    def _job(self, idx: int) -> dict:
        return self.df.iloc[idx].to_dict()

    def match(self, resume_text: str, top_k: int = 10) -> list[dict]:
        resume_text = clean_text(resume_text)
        resume_skills = extract_skills(resume_text)
        _, matches = retrieve_matches(self.index, resume_text, top_k)
        results = []
        for idx, semantic_score, _raw in matches:
            job = self._job(idx)
            job_skills = parse_skill_field(job["skills"])
            skill_score = skill_match_score(resume_skills, job_skills)
            quality = analyze_opportunity(job)
            result = {
                "job_id": job["job_id"], "title": job["title"], "company": job["company"],
                "location": job["location"], "remote": bool(job["remote"]),
                "salary": job["salary"], "employment_type": job["employment_type"],
                "application_url": job["application_url"],
                "semantic_score": round(semantic_score, 2),
                "skill_match_score": skill_score,
                "quality_score": quality["quality_score"],
                "final_score": final_score(semantic_score, skill_score, quality["quality_score"]),
                "warnings": quality["warnings"],
            }
            results.append(result)
        return sorted(results, key=lambda x: x["final_score"], reverse=True)

    def skill_gap(self, resume_text: str, job_id: str) -> dict:
        row = self.df[self.df["job_id"].astype(str) == str(job_id)]
        if row.empty:
            raise KeyError(f"Unknown job_id: {job_id}")
        job = row.iloc[0].to_dict()
        resume_skills = set(extract_skills(resume_text))
        required = set(parse_skill_field(job["skills"]))
        matched = sorted(resume_skills & required)
        missing = sorted(required - resume_skills)
        percentage = round(100 * len(matched) / len(required), 2) if required else 100.0
        return {"job_id": job_id, "matched_skills": matched, "missing_skills": missing, "match_percentage": percentage}

    def opportunity_analysis(self, job_id: str) -> dict:
        row = self.df[self.df["job_id"].astype(str) == str(job_id)]
        if row.empty:
            raise KeyError(f"Unknown job_id: {job_id}")
        return analyze_opportunity(row.iloc[0].to_dict())
