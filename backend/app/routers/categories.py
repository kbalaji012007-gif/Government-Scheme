from typing import List
from fastapi import APIRouter
from app.schemas.category import CategoryItem
from app.repositories.scheme_repository import SchemeRepository

router = APIRouter(prefix="/categories", tags=["Categories"])
scheme_repo = SchemeRepository()

BASE_CATEGORIES = [
    {
        "id": "farmers",
        "name_en": "Farmers",
        "name_kn": "ರೈತರು",
        "description_en": "Agricultural subsidies, crop insurance, equipment loans, and soil health welfare.",
        "description_kn": "ಕೃಷಿ ಸಹಾಯಧನ, ಬೆಳೆ ವಿಮೆ, ಯಂತ್ರೋಪಕರಣ ಸಾಲ ಮತ್ತು ಭೂಮಿ ಸಂರಕ್ಷಣೆ ಯೋಜನೆಗಳು.",
        "icon": "Tractor",
    },
    {
        "id": "students",
        "name_en": "Students",
        "name_kn": "ವಿದ್ಯಾರ್ಥಿಗಳು",
        "description_en": "Pre-matric & post-matric scholarships, fee concessions, and hostel admissions.",
        "description_kn": "ಪೂರ್ವ ಮೆಟ್ರಿಕ್ ಮತ್ತು ಮೆಟ್ರಿಕ್ ನಂತರದ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ಹಾಗೂ ವಸತಿ ನಿಲಯ ಸೌಲಭ್ಯಗಳು.",
        "icon": "GraduationCap",
    },
    {
        "id": "women",
        "name_en": "Women",
        "name_kn": "ಮಹಿಳೆಯರು",
        "description_en": "Financial assistance, self-help group revolving funds, and maternal nutrition benefits.",
        "description_kn": "ಗೃಹ ಲಕ್ಷ್ಮಿ, ಸ್ತ್ರೀ ಶಕ್ತಿ ಸಂಘಗಳ ನೆರವು, ಮಾತೃಪೂರ್ಣ ಮತ್ತು ಮಹಿಳಾ ಸಬಲೀಕರಣ ಯೋಜನೆಗಳು.",
        "icon": "HeartHandshake",
    },
    {
        "id": "senior_citizens",
        "name_en": "Senior Citizens",
        "name_kn": "ಹಿರಿಯ ನಾಗರಿಕರು",
        "description_en": "Monthly social security pensions, healthcare assistance, and day-care support.",
        "description_kn": "ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ, ಮಾಸಾಶನ ಪಿಂಚಣಿ, ಉಚಿತ ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸೆ ಮತ್ತು ಹಿರಿಯರ ಆರೈಕೆ.",
        "icon": "Users",
    },
    {
        "id": "rural_families",
        "name_en": "Rural Families",
        "name_kn": "ಗ್ರಾಮೀಣ ಕುಟುಂಬಗಳು",
        "description_en": "Free food grains, subsidized electricity, housing grants, and MGNREGA work.",
        "description_kn": "ಅನ್ನ ಭಾಗ್ಯ, ಗೃಹ ಜ್ಯೋತಿ ಉಚಿತ ವಿದ್ಯುತ್, ವಸತಿ ಯೋಜನೆಗಳು ಮತ್ತು ಉದ್ಯೋಗ ಖಾತರಿ.",
        "icon": "Home",
    },
    {
        "id": "other_beneficiaries",
        "name_en": "Other Beneficiaries",
        "name_kn": "ಇತರ ಫಲಾನುಭವಿಗಳು",
        "description_en": "Artisans, weavers, gig workers, and persons with disabilities welfare schemes.",
        "description_kn": "ಕುಶಲಕರ್ಮಿಗಳು, ನೇಕಾರರು, ಗಿಗ್ ಕಾರ್ಮಿಕರು ಮತ್ತು ವಿಕಲಚೇತನರ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು.",
        "icon": "Briefcase",
    },
]


@router.get("", response_model=List[CategoryItem])
async def list_categories():
    counts = scheme_repo.count_by_category()
    result: List[CategoryItem] = []
    for cat in BASE_CATEGORIES:
        cid = cat["id"]
        c_count = counts.get(cid, 0)
        # also map other_beneficiaries to general or its count
        if cid == "other_beneficiaries":
            c_count = counts.get("general", 0) + counts.get("other_beneficiaries", 0)
        result.append(
            CategoryItem(
                id=cid,
                name_en=cat["name_en"],
                name_kn=cat["name_kn"],
                description_en=cat["description_en"],
                description_kn=cat["description_kn"],
                icon=cat["icon"],
                scheme_count=c_count,
            )
        )
    return result
