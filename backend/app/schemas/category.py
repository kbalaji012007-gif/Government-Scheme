from pydantic import BaseModel
from typing import Optional


class CategoryItem(BaseModel):
    id: str
    name_en: str
    name_kn: str
    description_en: str
    description_kn: str
    icon: str
    scheme_count: Optional[int] = 0
