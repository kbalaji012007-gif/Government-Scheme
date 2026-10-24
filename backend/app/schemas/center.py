from typing import List, Optional
from pydantic import BaseModel


class CenterSummary(BaseModel):
    id: str
    name_en: str
    name_kn: str
    center_type: str  # Grama One, Bangalore One, Karnataka One, Bapuji Seva Kendra
    district: str
    taluk: str
    address_en: str
    address_kn: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    operating_hours_en: Optional[str] = None
    operating_hours_kn: Optional[str] = None
    is_development_sample: bool = True


class CenterDetail(CenterSummary):
    directions_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    services_offered_en: List[str] = []
    services_offered_kn: List[str] = []


class CenterListResponse(BaseModel):
    items: List[CenterSummary]
    total: int
    page: int
    page_size: int
    total_pages: int
    districts: List[str]
    taluks: List[str]
    center_types: List[str]
