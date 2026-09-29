import re


def analyze_opportunity(job: dict) -> dict:
    warnings: list[str] = []
    description = str(job.get("description", ""))
    company = str(job.get("company", "")).strip()
    salary = str(job.get("salary", "")).strip()
    url = str(job.get("application_url", "")).strip()
    experience = str(job.get("experience_required", "")).lower()
    text = " ".join(str(job.get(k, "")) for k in ["title", "description", "salary"]).lower()

    if len(description.split()) < 35:
        warnings.append("Job description is unusually short")
    if not company:
        warnings.append("Company information is missing")
    if not salary:
        warnings.append("Salary information is not provided")
    if not url:
        warnings.append("Application URL is missing")
    if re.search(r"pay\s+(a\s+)?fee|deposit|registration\s+fee|send\s+money", text):
        warnings.append("Posting appears to request a payment or deposit")
    if re.search(r"apply\s+within\s+\d+\s*(hours?|days?)|urgent|immediately", text):
        warnings.append("Urgency language is present")
    if re.search(r"[3-9]\+?\s*years?|[1-9]\d+\s*years?", experience):
        warnings.append("Experience requirement may be unusually high for an internship")
    if re.search(r"\$?\d{4,6}\s*(per\s*(week|day)|/\s*(week|day))", salary.lower()):
        warnings.append("Compensation may be unusually high for an internship")
    if len(description.split()) < 60:
        warnings.append("Responsibilities may be insufficiently detailed")

    score = max(0, 100 - 12 * len(warnings))
    return {"quality_score": score, "warnings": warnings, "signals": {"warning_count": len(warnings)}}
