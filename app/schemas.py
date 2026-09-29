from pydantic import BaseModel, Field

class ResumeTextRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    top_k: int = Field(default=10, gt=0, le=50)

class SkillGapRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    job_id: str = Field(min_length=1)

class OpportunityRequest(BaseModel):
    job_id: str = Field(min_length=1)
