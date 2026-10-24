from typing import Optional, List
from fastapi import APIRouter, Query, Path
from app.schemas.scheme import SchemeListResponse, SchemeDetail, DocumentRequirement
from app.schemas.eligibility import SchemeEligibilityConfigResponse, CheckEligibilityRequest, CheckEligibilityResponse
from app.services.scheme_service import SchemeService
from app.services.eligibility_service import EligibilityService

router = APIRouter(prefix="/schemes", tags=["Schemes"])
scheme_service = SchemeService()
eligibility_service = EligibilityService()


@router.get("", response_model=SchemeListResponse)
async def list_schemes(
    category: Optional[str] = Query(None, description="Filter by category slug"),
    beneficiary_type: Optional[str] = Query(None, description="Filter by beneficiary type"),
    query: Optional[str] = Query(None, description="Search keyword in scheme names or tags"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
):
    return scheme_service.list_schemes(
        category=category,
        beneficiary_type=beneficiary_type,
        query=query,
        page=page,
        page_size=page_size,
    )


@router.get("/{scheme_id}", response_model=SchemeDetail)
async def get_scheme_details(
    scheme_id: str = Path(..., description="Unique scheme identifier or slug")
):
    return scheme_service.get_scheme_by_id(scheme_id)


@router.get("/{scheme_id}/documents", response_model=List[DocumentRequirement])
async def get_scheme_documents(
    scheme_id: str = Path(..., description="Unique scheme identifier or slug")
):
    return scheme_service.get_scheme_documents(scheme_id)


@router.get("/{scheme_id}/eligibility", response_model=SchemeEligibilityConfigResponse)
async def get_scheme_eligibility_questions(
    scheme_id: str = Path(..., description="Unique scheme identifier or slug")
):
    return eligibility_service.get_eligibility_questions(scheme_id)


@router.post("/{scheme_id}/check-eligibility", response_model=CheckEligibilityResponse)
async def check_scheme_eligibility(
    payload: CheckEligibilityRequest,
    scheme_id: str = Path(..., description="Unique scheme identifier or slug"),
):
    return eligibility_service.evaluate_eligibility(scheme_id, payload.answers)
