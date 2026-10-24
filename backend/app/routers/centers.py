from typing import Optional
from fastapi import APIRouter, Query, Path
from app.schemas.center import CenterListResponse, CenterDetail
from app.services.center_service import CenterService

router = APIRouter(prefix="/centers", tags=["Service Centres"])
center_service = CenterService()


@router.get("", response_model=CenterListResponse)
async def list_centers(
    district: Optional[str] = Query(None, description="Filter by district name"),
    taluk: Optional[str] = Query(None, description="Filter by taluk name"),
    center_type: Optional[str] = Query(None, description="Filter by center type"),
    query: Optional[str] = Query(None, description="Search keyword in center name or address"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
):
    return center_service.list_centers(
        district=district,
        taluk=taluk,
        center_type=center_type,
        query=query,
        page=page,
        page_size=page_size,
    )


@router.get("/{center_id}", response_model=CenterDetail)
async def get_center_details(
    center_id: str = Path(..., description="Unique service center ID")
):
    return center_service.get_center_by_id(center_id)
