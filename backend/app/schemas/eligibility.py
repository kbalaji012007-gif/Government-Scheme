from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from app.schemas.scheme import DocumentRequirement, EligibilityQuestion


class SchemeEligibilityConfigResponse(BaseModel):
    scheme_id: str
    scheme_name_en: str
    scheme_name_kn: str
    questions: List[EligibilityQuestion]


class CheckEligibilityRequest(BaseModel):
    answers: Dict[str, Any]


class MissingRequirement(BaseModel):
    field: str
    message_en: str
    message_kn: str


class CheckEligibilityResponse(BaseModel):
    scheme_id: str
    scheme_name_en: str
    scheme_name_kn: str
    status: str  # eligible, not_eligible, more_info_required
    status_title_en: str
    status_title_kn: str
    summary_en: str
    summary_kn: str
    reasons_en: List[str]
    reasons_kn: List[str]
    missing_requirements: List[MissingRequirement] = []
    document_checklist: List[DocumentRequirement] = []
    next_steps_en: List[str]
    next_steps_kn: List[str]
    preliminary_notice_en: str
    preliminary_notice_kn: str
