from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class DocumentRequirement(BaseModel):
    id: str
    name_en: str
    name_kn: str
    description_en: Optional[str] = None
    description_kn: Optional[str] = None
    mandatory: bool = True


class QuestionOption(BaseModel):
    value: str
    label_en: str
    label_kn: str


class EligibilityQuestion(BaseModel):
    id: str
    question_en: str
    question_kn: str
    question_type: str  # boolean, number, select
    options: Optional[List[QuestionOption]] = None
    help_text_en: Optional[str] = None
    help_text_kn: Optional[str] = None
    mandatory: bool = True


class SchemeSummary(BaseModel):
    id: str
    name_en: str
    name_kn: str
    short_description_en: str
    short_description_kn: str
    category: str
    beneficiary_summary_en: str
    beneficiary_summary_kn: str
    beneficiary_types: List[str]
    tags: List[str] = []
    is_development_sample: bool = True


class SchemeDetail(SchemeSummary):
    full_description_en: str
    full_description_kn: str
    benefits_en: List[str]
    benefits_kn: List[str]
    eligibility_conditions_en: List[str]
    eligibility_conditions_kn: List[str]
    required_documents: List[DocumentRequirement]
    application_process_en: List[str]
    application_process_kn: List[str]
    official_portal_url: Optional[str] = None
    last_verified_date: Optional[str] = None
    disclaimer_en: str
    disclaimer_kn: str


class SchemeListResponse(BaseModel):
    items: List[SchemeSummary]
    total: int
    page: int
    page_size: int
    total_pages: int
