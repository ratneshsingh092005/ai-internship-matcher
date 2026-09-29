from fastapi import FastAPI, File, HTTPException, UploadFile

from .dependencies import get_matching_service
from .schemas import (
    ResumeTextRequest,
    SkillGapRequest,
    OpportunityRequest,
)
from .services.resume_service import (
    analyze_resume,
    extract_pdf_text,
)
from .services.recommendation_service import (
    build_recommendations,
)
from src.embeddings.embedding_service import get_model


app = FastAPI(
    title="AI Internship Matcher",
    version="1.0.0",
)


@app.get("/health")
def health():
    try:
        service = get_matching_service()
        get_model()

        return {
            "status": "healthy",
            "model_loaded": True,
            "index_loaded": service.index.ntotal > 0,
        }

    except Exception as exc:
        return {
            "status": "degraded",
            "model_loaded": False,
            "index_loaded": False,
            "detail": str(exc),
        }


@app.post("/analyze-resume")
async def analyze_resume_endpoint(
    file: UploadFile = File(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume",
        )

    try:
        file_bytes = await file.read()

        text = extract_pdf_text(file_bytes)

        result = analyze_resume(text)

        result.pop("text", None)

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc


@app.post("/match-internships")
def match_internships(
    request: ResumeTextRequest,
):
    try:
        results = get_matching_service().match(
            request.resume_text,
            request.top_k,
        )

        return {
            "results": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to match internships",
        ) from exc


@app.post("/skill-gap")
def skill_gap(
    request: SkillGapRequest,
):
    try:
        return get_matching_service().skill_gap(
            request.resume_text,
            request.job_id,
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@app.post("/opportunity-analysis")
def opportunity_analysis(
    request: OpportunityRequest,
):
    try:
        return get_matching_service().opportunity_analysis(
            request.job_id,
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@app.post("/recommendations")
def recommendations(
    request: ResumeTextRequest,
):
    try:
        results = build_recommendations(
            get_matching_service(),
            request.resume_text,
            request.top_k,
        )

        return {
            "recommendations": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate recommendations",
        ) from exc