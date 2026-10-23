import logging
import sys
import os

# Ensure backend root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.dirname(current_dir)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from app.db.firebase import db_manager, get_db
from app.core.security import hash_password

logger = logging.getLogger("ruralconnect.seed")

SAMPLE_SCHEMES = [
    {
        "id": "raitha-siri",
        "name_en": "Raitha Siri Millet Assistance Scheme",
        "name_kn": "ರೈತ ಸಿರಿ ಸಿರಿಧಾನ್ಯ ಪ್ರೋತ್ಸಾಹ ಯೋಜನೆ",
        "category": "farmers",
        "short_description_en": "Direct financial incentive of ₹10,000 per hectare for farmers cultivating millets in Karnataka.",
        "short_description_kn": "ಕರ್ನಾಟಕದಲ್ಲಿ ಸಿರಿಧಾನ್ಯ ಬೆಳೆಯುವ ರೈತರಿಗೆ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ನೇರ ಆರ್ಥಿಕ ಪ್ರೋತ್ಸಾಹ ಧನ.",
        "full_description_en": (
            "The Raitha Siri scheme was launched by the Department of Agriculture, Government of Karnataka, "
            "to encourage sustainable dryland agriculture through the cultivation of nutritious millets such as Ragi, "
            "Foxtail millet (Navane), Little millet (Saame), and Kodo millet (Haarka). Financial assistance is credited "
            "directly to the farmer's Aadhaar-seeded bank account via DBT."
        ),
        "full_description_kn": (
            "ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಕೃಷಿ ಇಲಾಖೆಯು ಸಿರಿಧಾನ್ಯಗಳಾದ ರಾಗಿ, ನವಣೆ, ಸಾಮೆ, ಹಾರಕ, ಕೊರಲೆ ಮತ್ತು ಬರಗು ಬೆಳೆಯುವ ರೈತರನ್ನು "
            "ಪ್ರೋತ್ಸಾಹಿಸಲು 'ರೈತ ಸಿರಿ' ಯೋಜನೆಯನ್ನು ಜಾರಿಗೆ ತಂದಿದೆ. ಅರ್ಹ ರೈತರಿಗೆ ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ಸಹಾಯಧನವನ್ನು ಡಿಬಿಟಿ (DBT) ಮೂಲಕ "
            "ನೇರವಾಗಿ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಜಮೆ ಮಾಡಲಾಗುತ್ತದೆ."
        ),
        "beneficiary_summary_en": "Small, marginal, and dryland farmers cultivating eligible millet crops.",
        "beneficiary_summary_kn": "ಸಿರಿಧಾನ್ಯ ಬೆಳೆಯುವ ಸಣ್ಣ, ಅತಿ ಸಣ್ಣ ಮತ್ತು ಒಣಭೂಮಿ ರೈತರು.",
        "beneficiary_types": ["farmers"],
        "tags": ["Agriculture", "Millets", "DBT", "Dryland Farming", "Karnataka"],
        "benefits_en": [
            "Financial grant of ₹10,000 per hectare (up to a maximum of 2 hectares per farmer).",
            "Direct Benefit Transfer (DBT) deposited directly into Aadhaar-linked savings account.",
            "Access to free soil health testing and agricultural extension advisory services.",
        ],
        "benefits_kn": [
            "ಪ್ರತಿ ಹೆಕ್ಟೇರ್‌ಗೆ ₹10,000 ಸಹಾಯಧನ (ಒಬ್ಬ ರೈತನಿಗೆ ಗರಿಷ್ಠ 2 ಹೆಕ್ಟೇರ್‌ವರೆಗೆ).",
            "ಆಧಾರ್ ಜೋಡಿಸಲಾದ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ನೇರ ಹಣ ವರ್ಗಾವಣೆ (DBT).",
            "ಉಚಿತ ಮಣ್ಣು ಪರೀಕ್ಷೆ ಮತ್ತು ಕೃಷಿ ಇಲಾಖೆಯ ತಾಂತ್ರಿಕ ಮಾರ್ಗದರ್ಶನ.",
        ],
        "eligibility_conditions_en": [
            "Must be a resident farmer of Karnataka.",
            "Must own or legally cultivate agricultural land with registered RTC / Pahani record in FRUITS portal.",
            "Must have cultivated eligible minor millets during the notified cropping season.",
            "Farmer registration number (FID) generated through Karnataka FRUITS system is mandatory.",
        ],
        "eligibility_conditions_kn": [
            "ಕರ್ನಾಟಕ ರಾಜ್ಯದ ನಿವಾಸಿ ರೈತರಾಗಿರಬೇಕು.",
            "ಫ್ರೂಟ್ಸ್ (FRUITS) ತಂತ್ರಾಂಶದಲ್ಲಿ ನೋಂದಾಯಿತ ಪಹಣಿ / RTC ಜಮೀನು ಹೊಂದಿರಬೇಕು.",
            "ನಿಗದಿತ ಹಂಗಾಮಿನಲ್ಲಿ ಅಧಿಕೃತ ಸಿರಿಧಾನ್ಯಗಳನ್ನು ಬೆಳೆದಿರಬೇಕು.",
            "ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಎಫ್‌ಐಡಿ (FID) ಸಂಖ್ಯೆ ಹೊಂದಿರಬೇಕು.",
        ],
        "required_documents": [
            {
                "id": "aadhaar_card",
                "name_en": "Aadhaar Card",
                "name_kn": "ಆಧಾರ್ ಕಾರ್ಡ್",
                "description_en": "Applicant's official biometric identity card linked with bank account.",
                "description_kn": "ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಲಿಂಕ್ ಆಗಿರುವ ಅರ್ಜಿದಾರರ ಆಧಾರ್ ಕಾರ್ಡ್.",
                "mandatory": True,
            },
            {
                "id": "rtc_pahani",
                "name_en": "RTC / Pahani Land Record",
                "name_kn": "ಜಮೀನಿನ ಆರ್‌ಟಿಸಿ / ಪಹಣಿ ದಾಖಲೆ",
                "description_en": "Current revenue year RTC document verifying agricultural land ownership.",
                "description_kn": "ಕೃಷಿ ಭೂಮಿಯ ಮಾಲೀಕತ್ವವನ್ನು ದೃಢೀಕರಿಸುವ ಪ್ರಸ್ತುತ ಸಾಲಿನ ಪಹಣಿ.",
                "mandatory": True,
            },
            {
                "id": "fruits_fid",
                "name_en": "FRUITS FID Number",
                "name_kn": "ಫ್ರೂಟ್ಸ್ (FID) ನೋಂದಣಿ ಸಂಖ್ಯೆ",
                "description_en": "Farmer Identification number from the Karnataka FRUITS portal.",
                "description_kn": "ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಫ್ರೂಟ್ಸ್ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಲಾದ ರೈತ ಗುರುತಿನ ಸಂಖ್ಯೆ.",
                "mandatory": True,
            },
            {
                "id": "bank_passbook",
                "name_en": "Bank Passbook Copy",
                "name_kn": "ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಪ್ರತಿ",
                "description_en": "Bank passbook photocopy showing IFSC code and active account details.",
                "description_kn": "ಐಎಫ್‌ಎಸ್‌ಸಿ ಕೋಡ್ ಮತ್ತು ಖಾತೆ ಸಂಖ್ಯೆ ಇರುವ ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಮುಖಪುಟದ ಪ್ರತಿ.",
                "mandatory": True,
            },
        ],
        "application_process_en": [
            "Register in the Karnataka FRUITS database through your local Raitha Samparka Kendra (RSK).",
            "Obtain your verified Farmer ID (FID).",
            "Submit the crop survey data or visit your nearest Grama One centre with your RTC and Aadhaar.",
            "The Agriculture Officer inspects the crop area and submits verification.",
            "Incentive is credited straight to your DBT bank account upon approval.",
        ],
        "application_process_kn": [
            "ಸ್ಥಳೀಯ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರಕ್ಕೆ (RSK) ಭೇಟಿ ನೀಡಿ ಫ್ರೂಟ್ಸ್ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ನೋಂದಾಯಿಸಿಕೊಳ್ಳಿ.",
            "ದೃಢೀಕೃತ ರೈತ ಗುರುತಿನ ಸಂಖ್ಯೆ (FID) ಪಡೆದುಕೊಳ್ಳಿ.",
            "ಬೆಳೆ ಸಮೀಕ್ಷೆ ವಿವರಗಳು, ಆರ್‌ಟಿಸಿ ಮತ್ತು ಆಧಾರ್‌ನೊಂದಿಗೆ ಸಮೀಪದ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
            "ಕೃಷಿ ಅಧಿಕಾರಿಯ ಸ್ಥಳ ಪರಿಶೀಲನೆಯ ನಂತರ ಅನುಮೋದನೆ ದೊರೆಯುತ್ತದೆ.",
            "ಅನುಮೋದನೆಯ ನಂತರ ನೇರವಾಗಿ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಸಹಾಯಧನ ಜಮೆಯಾಗುತ್ತದೆ.",
        ],
        "official_portal_url": "https://fruits.karnataka.gov.in",
        "last_verified_date": "2026-03-15",
        "disclaimer_en": "Informational guide only. Sanction of benefits is subject to field verification by Karnataka Agriculture Department.",
        "disclaimer_kn": "ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ಸಹಾಯಧನದ ಮಂಜೂರಾತಿಯು ಕೃಷಿ ಇಲಾಖೆಯ ಸ್ಥಳ ಪರಿಶೀಲನೆಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
        "is_development_sample": True,
        "eligibility_criteria": {
            "must_be_karnataka_resident": True,
            "requires_land_ownership": True,
            "min_age": 18,
            "max_age": 85,
        },
        "eligibility_questions": [
            {
                "id": "is_karnataka_resident",
                "question_en": "Are you a permanent resident of Karnataka?",
                "question_kn": "ನೀವು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Select Yes if your primary residence is in Karnataka.",
                "help_text_kn": "ನಿಮ್ಮ ಕಾಯಂ ವಾಸಸ್ಥಳ ಕರ್ನಾಟಕದಲ್ಲಿದ್ದರೆ 'ಹೌದು' ಆಯ್ಕೆಮಾಡಿ.",
                "mandatory": True,
            },
            {
                "id": "owns_agricultural_land",
                "question_en": "Do you or your family own cultivable agricultural land in Karnataka?",
                "question_kn": "ನಿಮ್ಮ ಅಥವಾ ನಿಮ್ಮ ಕುಟುಂಬದ ಹೆಸರಿನಲ್ಲಿ ಕರ್ನಾಟಕದಲ್ಲಿ ಕೃಷಿ ಜಮೀನು ಇದೆಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Land must have registered RTC / Pahani.",
                "help_text_kn": "ಜಮೀನಿಗೆ ಅಧಿಕೃತ ಪಹಣಿ ದಾಖಲೆ ಇರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "cultivates_millets",
                "question_en": "Do you cultivate minor millets (Ragi, Navane, Saame, etc.)?",
                "question_kn": "ನೀವು ಸಿರಿಧಾನ್ಯಗಳನ್ನು (ರಾಗಿ, ನವಣೆ, ಸಾಮೆ ಇತ್ಯಾದಿ) ಬೆಳೆಯುತ್ತೀರಾ?",
                "question_type": "boolean",
                "help_text_en": "Raitha Siri specifically subsidizes minor millet cultivation.",
                "help_text_kn": "ರೈತ ಸಿರಿ ಯೋಜನೆಯು ಸಿರಿಧಾನ್ಯಗಳ ಬೆಳೆಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ.",
                "mandatory": True,
            },
            {
                "id": "age",
                "question_en": "What is your current age in completed years?",
                "question_kn": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ ವಯಸ್ಸು ಎಷ್ಟು?",
                "question_type": "number",
                "help_text_en": "Must be at least 18 years old.",
                "help_text_kn": "ಕನಿಷ್ಠ 18 ವರ್ಷ ತುಂಬಿರಬೇಕು.",
                "mandatory": True,
            },
        ],
    },
    {
        "id": "gruha-lakshmi",
        "name_en": "Gruha Lakshmi Guarantee Scheme",
        "name_kn": "ಗೃಹ ಲಕ್ಷ್ಮಿ ಖಾತರಿ ಯೋಜನೆ",
        "category": "women",
        "short_description_en": "Monthly financial aid of ₹2,000 to woman head of each family in Karnataka.",
        "short_description_kn": "ಕರ್ನಾಟಕದ ಪ್ರತಿ ಕುಟುಂಬದ ಯಜಮಾನಿ ಮಹಿಳೆಗೆ ತಿಂಗಳಿಗೆ ₹2,000 ಆರ್ಥಿಕ ನೆರವು.",
        "full_description_en": (
            "The Gruha Lakshmi scheme is a flagship social security initiative of the Government of Karnataka, "
            "providing ₹2,000 per month to the woman head of every eligible household across the state. "
            "It aims to improve female financial autonomy, support household food security, and alleviate rural cost-of-living burdens."
        ),
        "full_description_kn": (
            "ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಯು ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಪ್ರಮುಖ ಖಾತರಿ ಯೋಜನೆಗಳಲ್ಲಿ ಒಂದಾಗಿದ್ದು, ರಾಜ್ಯದ ಅರ್ಹ ಕುಟುಂಬದ ಮಹಿಳಾ ಮುಖ್ಯಸ್ಥರಿಗೆ "
            "ಪ್ರತಿ ತಿಂಗಳು ₹2,000 ಆರ್ಥಿಕ ನೆರವು ನೀಡುತ್ತದೆ. ಮಹಿಳೆಯರ ಆರ್ಥಿಕ ಸ್ವಾವಲಂಬನೆ ಹೆಚ್ಚಿಸಲು ಮತ್ತು ಗ್ರಾಮೀಣ ಕುಟುಂಬಗಳ ವೆಚ್ಚ ಸರಿದೂಗಿಸಲು "
            "ಈ ಯೋಜನೆಯನ್ನು ಜಾರಿಗೊಳಿಸಲಾಗಿದೆ."
        ),
        "beneficiary_summary_en": "Women recognized as the head of household in BPL, AAY, or APL ration cards.",
        "beneficiary_summary_kn": "ಬಿಪಿಎಲ್, ಎಎವೈ ಅಥವಾ ಎಪಿಎಲ್ ಕಾರ್ಡ್‌ನಲ್ಲಿ ಕುಟುಂಬದ ಯಜಮಾನಿ ಎಂದು ನಮೂದಾಗಿರುವ ಮಹಿಳೆಯರು.",
        "beneficiary_types": ["women"],
        "tags": ["Women Empowerment", "Direct Cash Transfer", "Social Security", "Guarantee Scheme"],
        "benefits_en": [
            "Monthly recurring DBT grant of ₹2,000 deposited into Aadhaar-linked bank account.",
            "Completely paperless application at Grama One, Karnataka One, or Seva Sindhu centres.",
            "No application fees charged by authorized government service centres.",
        ],
        "benefits_kn": [
            "ಆಧಾರ್ ಜೋಡಿಸಲಾದ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಪ್ರತಿ ತಿಂಗಳು ₹2,000 ನೇರ ನಗದು ವರ್ಗಾವಣೆ (DBT).",
            "ಗ್ರಾಮ ಒನ್, ಕರ್ನಾಟಕ ಒನ್ ಮತ್ತು ಸೇವಾ ಸಿಂಧು ಕೇಂದ್ರಗಳಲ್ಲಿ ಸಂಪೂರ್ಣ ಕಾಗದರಹಿತ ಅರ್ಜಿ ಸಲ್ಲಿಕೆ.",
            "ಸರ್ಕಾರಿ ಕೇಂದ್ರಗಳಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಯಾವುದೇ ಶುಲ್ಕವಿಲ್ಲ.",
        ],
        "eligibility_conditions_en": [
            "Must be a permanent female resident of Karnataka.",
            "Must be registered as the woman head of family on an active BPL, Antyodaya (AAY), or APL card.",
            "Neither the woman head nor her spouse should be income tax payers or GST filers.",
            "Only one female head per household ration card is eligible.",
        ],
        "eligibility_conditions_kn": [
            "ಕರ್ನಾಟಕದ ಕಾಯಂ ಮಹಿಳಾ ನಿವಾಸಿಯಾಗಿರಬೇಕು.",
            "ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿ (BPL/AAY/APL) ಕುಟುಂಬದ ಯಜಮಾನಿ ಎಂದು ನಮೂದಾಗಿರಬೇಕು.",
            "ಅರ್ಜಿದಾರ ಮಹಿಳೆ ಅಥವಾ ಆಕೆಯ ಪತಿ ಆದಾಯ ತೆರಿಗೆ ಅಥವಾ ಜಿಎಸ್‌ಟಿ ಪಾವತಿದಾರರಾಗಿರಬಾರದು.",
            "ಒಂದು ಕುಟುಂಬದ ರೇಷನ್ ಕಾರ್ಡ್‌ನಲ್ಲಿ ಒಬ್ಬ ಮಹಿಳೆಗೆ ಮಾತ್ರ ಈ ಸೌಲಭ್ಯ ಲಭ್ಯ.",
        ],
        "required_documents": [
            {
                "id": "ration_card",
                "name_en": "Ration Card (BPL / AAY / APL)",
                "name_kn": "ಪಡಿತರ ಚೀಟಿ (BPL / AAY / APL)",
                "description_en": "Karnataka Food and Civil Supplies Department issued family card.",
                "description_kn": "ಆಹಾರ ಮತ್ತು ನಾಗರಿಕ ಸರಬರಾಜು ಇಲಾಖೆ ನೀಡಿರುವ ಕುಟುಂಬದ ಪಡಿತರ ಚೀಟಿ.",
                "mandatory": True,
            },
            {
                "id": "woman_aadhaar",
                "name_en": "Woman Head Aadhaar Card",
                "name_kn": "ಮಹಿಳಾ ಯಜಮಾನಿಯ ಆಧಾರ್ ಕಾರ್ಡ್",
                "description_en": "Aadhaar card of the woman applicant matching the name on the ration card.",
                "description_kn": "ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿರುವ ಹೆಸರಿಗೆ ಹೊಂದಿಕೆಯಾಗುವ ಮಹಿಳೆಯ ಆಧಾರ್ ಕಾರ್ಡ್.",
                "mandatory": True,
            },
            {
                "id": "husband_aadhaar",
                "name_en": "Husband's Aadhaar Card (if married)",
                "name_kn": "ಪತಿಯ ಆಧಾರ್ ಕಾರ್ಡ್ (ವಿವಾಹಿತರಾಗಿದ್ದಲ್ಲಿ)",
                "description_en": "Used for verifying family identity and income tax non-payer status.",
                "description_kn": "ಕುಟುಂಬದ ಗುರುತು ಹಾಗೂ ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿದಾರರಲ್ಲ ಎಂದು ಪರಿಶೀಲಿಸಲು.",
                "mandatory": False,
            },
            {
                "id": "aadhaar_linked_bank",
                "name_en": "Aadhaar Seeded Bank Account",
                "name_kn": "ಆಧಾರ್ ಲಿಂಕ್ ಆದ ಬ್ಯಾಂಕ್ ಖಾತೆ",
                "description_en": "Bank account must be NPCI mapped for direct DBT receipt.",
                "description_kn": "ಡಿಬಿಟಿ ಹಣ ಸ್ವೀಕರಿಸಲು ಎನ್‌ಪಿಸಿಐ (NPCI) ಮ್ಯಾಪ್ ಆಗಿರುವ ಬ್ಯಾಂಕ್ ಖಾತೆ.",
                "mandatory": True,
            },
        ],
        "application_process_en": [
            "Verify that your name is marked as Woman Head on the family ration card.",
            "Ensure your bank account is linked to Aadhaar with NPCI mapping enabled.",
            "Visit the nearest Grama One or Karnataka One centre with your Ration Card and Aadhaar.",
            "The operator submits your details on the Seva Sindhu Guarantee portal.",
            "Receive an official SMS confirmation and monthly payment tracking.",
        ],
        "application_process_kn": [
            "ಕುಟುಂಬದ ರೇಷನ್ ಕಾರ್ಡ್‌ನಲ್ಲಿ ನಿಮ್ಮ ಹೆಸರು ಯಜಮಾನಿ ಎಂದು ನಮೂದಾಗಿದೆಯೇ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
            "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಆಧಾರ್ ಹಾಗೂ ಎನ್‌ಪಿಸಿಐ ಮ್ಯಾಪಿಂಗ್ ಆಗಿರುವುದನ್ನು ಪರಿಶೀಲಿಸಿ.",
            "ರೇಷನ್ ಕಾರ್ಡ್ ಮತ್ತು ಆಧಾರ್‌ನೊಂದಿಗೆ ಸಮೀಪದ ಗ್ರಾಮ ಒನ್ ಅಥವಾ ಕರ್ನಾಟಕ ಒನ್ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ.",
            "ಆಪರೇಟರ್ ಸೇವಾ ಸಿಂಧು ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಅರ್ಜಿಯನ್ನು ದಾಖಲಿಸುತ್ತಾರೆ.",
            "ಅರ್ಜಿ ಯಶಸ್ವಿಯಾದ ನಂತರ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಗೆ ಅಧಿಕೃತ ದೃಢೀಕರಣ ಸಂದೇಶ ಬರುತ್ತದೆ.",
        ],
        "official_portal_url": "https://sevasindhu.karnataka.gov.in",
        "last_verified_date": "2026-02-10",
        "disclaimer_en": "Informational guide only. Formal approval rests with the Department of Women and Child Development.",
        "disclaimer_kn": "ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ಅಧಿಕೃತ ಪರಿಶೀಲನೆ ಮಹಿಳಾ ಮತ್ತು ಮಕ್ಕಳ ಅಭಿವೃದ್ಧಿ ಇಲಾಖೆಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
        "is_development_sample": True,
        "eligibility_criteria": {
            "must_be_karnataka_resident": True,
            "allowed_genders": ["female"],
            "requires_bpl_or_antyodaya": False,
        },
        "eligibility_questions": [
            {
                "id": "is_karnataka_resident",
                "question_en": "Are you a permanent resident of Karnataka?",
                "question_kn": "ನೀವು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Must reside permanently in Karnataka.",
                "help_text_kn": "ಕರ್ನಾಟಕದಲ್ಲಿ ಕಾಯಂ ಆಗಿ ವಾಸಿಸುತ್ತಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "gender",
                "question_en": "What is your gender?",
                "question_kn": "ನಿಮ್ಮ ಲಿಂಗ ಯಾವುದು?",
                "question_type": "select",
                "options": [
                    {"value": "female", "label_en": "Female", "label_kn": "ಮಹಿಳೆ"},
                    {"value": "male", "label_en": "Male", "label_kn": "ಪುರುಷ"},
                    {"value": "other", "label_en": "Other", "label_kn": "ಇತರೆ"},
                ],
                "help_text_en": "Gruha Lakshmi is strictly for women heads of households.",
                "help_text_kn": "ಗೃಹ ಲಕ್ಷ್ಮಿ ಯೋಜನೆಯು ಮಹಿಳಾ ಮುಖ್ಯಸ್ಥರಿಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ.",
                "mandatory": True,
            },
            {
                "id": "is_woman_head_on_ration_card",
                "question_en": "Are you named as the head of family on your household ration card?",
                "question_kn": "ಕುಟುಂಬದ ಪಡಿತರ ಚೀಟಿಯಲ್ಲಿ ನಿಮ್ಮ ಹೆಸರು ಯಜಮಾನಿ ಎಂದು ನಮೂದಾಗಿದೆಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Check your physical ration card or Ahara portal.",
                "help_text_kn": "ರೇಷನ್ ಕಾರ್ಡ್‌ನಲ್ಲಿ ಮಹಿಳೆಯ ಹೆಸರು ಯಜಮಾನಿ ಎಂದು ಇರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "is_income_tax_payer",
                "question_en": "Do you or your spouse pay Income Tax or file GST?",
                "question_kn": "ನೀವು ಅಥವಾ ನಿಮ್ಮ ಪತಿ ಆದಾಯ ತೆರಿಗೆ (Income Tax) ಅಥವಾ ಜಿಎಸ್‌ಟಿ ಪಾವತಿಸುತ್ತೀರಾ?",
                "question_type": "boolean",
                "help_text_en": "Income tax or GST payers are disqualified under scheme rules.",
                "help_text_kn": "ಆದಾಯ ತೆರಿಗೆ ಪಾವತಿಸುವ ಕುಟುಂಬಗಳಿಗೆ ಈ ಯೋಜನೆ ಅನ್ವಯಿಸುವುದಿಲ್ಲ.",
                "mandatory": True,
            },
        ],
    },
    {
        "id": "ssp-post-matric",
        "name_en": "SSP Post-Matric Student Scholarship",
        "name_kn": "ರಾಜ್ಯ ವಿದ್ಯಾರ್ಥಿವೇತನ (SSP) ಮೆಟ್ರಿಕ್ ನಂತರದ ಯೋಜನೆ",
        "category": "students",
        "short_description_en": "Tuition fee waiver, maintenance allowance, and hostel reimbursement for college students.",
        "short_description_kn": "ಕಾಲೇಜು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಬೋಧನಾ ಶುಲ್ಕ ವಿನಾಯಿತಿ, ನಿರ್ವಹಣಾ ಭತ್ಯೆ ಮತ್ತು ವಿದ್ಯಾರ್ಥಿವೇತನ.",
        "full_description_en": (
            "The State Scholarship Portal (SSP) is a unified digital platform managed by the Government of Karnataka "
            "to disburse post-matric scholarships across various departments (Social Welfare, Backward Classes Welfare, "
            "Tribal Welfare, Minorities Welfare, and Technical Education). It supports PUC, Diploma, ITI, Undergraduate, "
            "and Postgraduate students from economically weaker sections."
        ),
        "full_description_kn": (
            "ರಾಜ್ಯ ವಿದ್ಯಾರ್ಥಿವೇತನ ಪೋರ್ಟಲ್ (SSP) ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಏಕೀಕೃತ ಡಿಜಿಟಲ್ ಪೋರ್ಟಲ್ ಆಗಿದ್ದು, ಸಮಾಜ ಕಲ್ಯಾಣ, ಹಿಂದುಳಿದ ವರ್ಗಗಳ ಕಲ್ಯಾಣ, "
            "ಅಲ್ಪಸಂಖ್ಯಾತರ ಕಲ್ಯಾಣ ಮತ್ತು ತಾಂತ್ರಿಕ ಶಿಕ್ಷಣ ಇಲಾಖೆಗಳ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳನ್ನು ಒದಗಿಸುತ್ತದೆ. ಪಿಯುಸಿ, ಐಟಿಐ, ಡಿಪ್ಲೊಮಾ, ಪದವಿ ಮತ್ತು ಸ್ನಾತಕೋತ್ತರ "
            "ವ್ಯಾಸಂಗ ಮಾಡುವ ಗ್ರಾಮೀಣ ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಇದು ಸಹಕಾರಿಯಾಗಿದೆ."
        ),
        "beneficiary_summary_en": "Karnataka students pursuing Post-Matric courses (PUC, Degree, Engineering, Medicine, Diploma).",
        "beneficiary_summary_kn": "ಪಿಯುಸಿ, ಪದವಿ, ಇಂಜಿನಿಯರಿಂಗ್, ಡಿಪ್ಲೊಮಾ ವ್ಯಾಸಂಗ ಮಾಡುತ್ತಿರುವ ವಿದ್ಯಾರ್ಥಿಗಳು.",
        "beneficiary_types": ["students"],
        "tags": ["Education", "Scholarship", "SSP", "Higher Education", "Tuition Fee"],
        "benefits_en": [
            "Full or partial reimbursement of college admission and tuition fees.",
            "Monthly maintenance stipend for day scholars and boarders.",
            "Hostel fee concessions for government and department-recognized hostels.",
        ],
        "benefits_kn": [
            "ಕಾಲೇಜು ಪ್ರವೇಶ ಮತ್ತು ಬೋಧನಾ ಶುಲ್ಕದ ಪೂರ್ಣ ಅಥವಾ ಭಾಗಶಃ ಮರುಪಾವತಿ.",
            "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಮಾಸಿಕ ನಿರ್ವಹಣಾ ಭತ್ಯೆ.",
            "ಸರ್ಕಾರಿ ಹಾಗೂ ಇಲಾಖಾ ಮಾನ್ಯತೆ ಪಡೆದ ವಸತಿ ನಿಲಯಗಳ ಶುಲ್ಕ ರಿಯಾಯಿತಿ.",
        ],
        "eligibility_conditions_en": [
            "Must be a domicile of Karnataka.",
            "Must be currently enrolled in a recognized institution with valid SATS / Student ID.",
            "Annual family income must not exceed ₹2,50,000 for SC/ST and OBC categories (as per department norms).",
            "Must have passed previous qualifying examination without malpractice.",
        ],
        "eligibility_conditions_kn": [
            "ಕರ್ನಾಟಕದ ಕಾಯಂ ನಿವಾಸಿಯಾಗಿರಬೇಕು.",
            "ಮಾನ್ಯತೆ ಪಡೆದ ಕಾಲೇಜು ಅಥವಾ ಶಿಕ್ಷಣ ಸಂಸ್ಥೆಯಲ್ಲಿ ಪ್ರಸ್ತುತ ವ್ಯಾಸಂಗ ಮಾಡುತ್ತಿರಬೇಕು.",
            "ಕುಟುಂಬದ ವಾರ್ಷಿಕ ಆದಾಯ ₹2.50 ಲಕ್ಷ ಮೀರಬಾರದು (ಇಲಾಖಾ ನಿಯಮಗಳ ಅನ್ವಯ).",
            "ಹಿಂದಿನ ತರಗತಿಯಲ್ಲಿ ತೇರ್ಗಡೆಯಾಗಿರಬೇಕು.",
        ],
        "required_documents": [
            {
                "id": "income_caste_cert",
                "name_en": "Income and Caste Certificate (RD Number)",
                "name_kn": "ಆದಾಯ ಮತ್ತು ಜಾತಿ ಪ್ರಮಾಣಪತ್ರ (RD ಸಂಖ್ಯೆ)",
                "description_en": "Issued by Nadakacheri with valid RD number verification.",
                "description_kn": "ನಾಡಕಚೇರಿಯಿಂದ ವಿತರಿಸಲಾದ ಮಾನ್ಯ ಆರ್‌ಡಿ (RD) ಸಂಖ್ಯೆ ಹೊಂದಿರುವ ಪ್ರಮಾಣಪತ್ರ.",
                "mandatory": True,
            },
            {
                "id": "student_aadhaar",
                "name_en": "Student Aadhaar Card",
                "name_kn": "ವಿದ್ಯಾರ್ಥಿಯ ಆಧಾರ್ ಕಾರ್ಡ್",
                "description_en": "Biometric Aadhaar card linked with active mobile number.",
                "description_kn": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆಗೆ ಜೋಡಿಸಲಾದ ವಿದ್ಯಾರ್ಥಿಯ ಆಧಾರ್ ಕಾರ್ಡ್.",
                "mandatory": True,
            },
            {
                "id": "fee_receipt",
                "name_en": "College Admission Fee Receipt",
                "name_kn": "ಕಾಲೇಜು ಪ್ರವೇಶ ಶುಲ್ಕ ರಶೀದಿ",
                "description_en": "Official college fee receipt showing fee breakup and admission number.",
                "description_kn": "ಕಾಲೇಜು ಪ್ರವೇಶ ಸಂಖ್ಯೆ ಹೊಂದಿರುವ ಶುಲ್ಕ ಪಾವತಿ ರಶೀದಿ.",
                "mandatory": True,
            },
            {
                "id": "bank_account",
                "name_en": "Aadhaar Seeded Bank Account",
                "name_kn": "ಆಧಾರ್ ಲಿಂಕ್ ಆದ ಬ್ಯಾಂಕ್ ಖಾತೆ",
                "description_en": "Active savings account in student's own name mapped to NPCI.",
                "description_kn": "ವಿದ್ಯಾರ್ಥಿಯ ಹೆಸರಿನಲ್ಲೇ ಇರುವ ಆಧಾರ್ ಲಿಂಕ್ ಆದ ಬ್ಯಾಂಕ್ ಖಾತೆ.",
                "mandatory": True,
            },
        ],
        "application_process_en": [
            "Visit the Karnataka SSP portal or your nearby Grama One centre.",
            "Create an account using student Aadhaar and Nadakacheri RD number.",
            "Enter college admission details and e-Attestation reference.",
            "Submit the e-attested documents online.",
            "Track verification status directly on the SSP student dashboard.",
        ],
        "application_process_kn": [
            "ಕರ್ನಾಟಕ ಎಸ್‌ಎಸ್‌ಪಿ (SSP) ಪೋರ್ಟಲ್ ಅಥವಾ ಸಮೀಪದ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ.",
            "ವಿದ್ಯಾರ್ಥಿಯ ಆಧಾರ್ ಮತ್ತು ಆದಾಯ ಪ್ರಮಾಣಪತ್ರದ RD ಸಂಖ್ಯೆ ಬಳಸಿ ಖಾತೆ ರಚಿಸಿ.",
            "ಕಾಲೇಜು ಪ್ರವೇಶ ಮಾಹಿತಿ ಹಾಗೂ ಇ-ದೃಢೀಕರಣ (e-Attestation) ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
            "ದಾಖಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಆನ್‌ಲೈನ್ ಮೂಲಕ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
            "ಎಸ್‌ಎಸ್‌ಪಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಅರ್ಜಿಯ ಸ್ಥಿತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ.",
        ],
        "official_portal_url": "https://ssp.postmatric.karnataka.gov.in",
        "last_verified_date": "2026-01-20",
        "disclaimer_en": "Informational guide only. Sanction depends on university verification and department quotas.",
        "disclaimer_kn": "ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ಕಾಲೇಜು ಪರಿಶೀಲನೆ ಮತ್ತು ಇಲಾಖಾ ಮಾನದಂಡಗಳ ಆಧಾರದ ಮೇಲೆ ಮಂಜೂರಾತಿ ಇರುತ್ತದೆ.",
        "is_development_sample": True,
        "eligibility_criteria": {
            "must_be_karnataka_resident": True,
            "requires_student_enrollment": True,
            "max_annual_income": 250000.0,
            "min_age": 15,
            "max_age": 35,
        },
        "eligibility_questions": [
            {
                "id": "is_karnataka_resident",
                "question_en": "Are you a permanent resident of Karnataka?",
                "question_kn": "ನೀವು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Student must have studied in Karnataka or hold domicile.",
                "help_text_kn": "ವಿದ್ಯಾರ್ಥಿಯು ಕರ್ನಾಟಕದಲ್ಲಿ ನೆಲೆಸಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "is_enrolled_student",
                "question_en": "Are you currently enrolled in a recognized Post-Matric course (PUC, Diploma, Degree, etc.)?",
                "question_kn": "ನೀವು ಪ್ರಸ್ತುತ ಮಾನ್ಯತೆ ಪಡೆದ ಪಿಯುಸಿ, ಡಿಪ್ಲೊಮಾ, ಐಟಿಐ ಅಥವಾ ಪದವಿ ಕೋರ್ಸ್‌ನಲ್ಲಿ ವ್ಯಾಸಂಗ ಮಾಡುತ್ತಿದ್ದೀರಾ?",
                "question_type": "boolean",
                "help_text_en": "Must have an active college admission.",
                "help_text_kn": "ಪ್ರಸ್ತುತ ವರ್ಷ ಕಾಲೇಜಿನಲ್ಲಿ ದಾಖಲಾಗಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "annual_income",
                "question_en": "What is your total family annual income as per your income certificate (in ₹)?",
                "question_kn": "ನಿಮ್ಮ ಆದಾಯ ಪ್ರಮಾಣಪತ್ರದ ಪ್ರಕಾರ ಕುಟುಂಬದ ಒಟ್ಟು ವಾರ್ಷಿಕ ಆದಾಯ ಎಷ್ಟು (₹)?",
                "question_type": "number",
                "help_text_en": "Enter the amount as shown on your official RD certificate.",
                "help_text_kn": "ನಾಡಕಚೇರಿ ಆದಾಯ ಪ್ರಮಾಣಪತ್ರದಲ್ಲಿರುವ ಮೊತ್ತವನ್ನು ನಮೂದಿಸಿ.",
                "mandatory": True,
            },
            {
                "id": "age",
                "question_en": "What is the applicant's age?",
                "question_kn": "ಅರ್ಜಿದಾರ ವಿದ್ಯಾರ್ಥಿಯ ವಯಸ್ಸು ಎಷ್ಟು?",
                "question_type": "number",
                "help_text_en": "Post-matric age generally between 15 and 35.",
                "help_text_kn": "ಸಾಮಾನ್ಯವಾಗಿ 15 ರಿಂದ 35 ವರ್ಷ ವಯೋಮಿತಿ.",
                "mandatory": True,
            },
        ],
    },
    {
        "id": "sandhya-suraksha",
        "name_en": "Sandhya Suraksha Senior Citizen Pension",
        "name_kn": "ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ ಹಿರಿಯ ನಾಗರಿಕರ ಪಿಂಚಣಿ ಯೋಜನೆ",
        "category": "senior_citizens",
        "short_description_en": "Monthly social security pension of ₹1,200 for vulnerable senior citizens aged 65 and above.",
        "short_description_kn": "65 ವರ್ಷ ಮತ್ತು ಮೇಲ್ಪಟ್ಟ ಅರ್ಹ ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ಪ್ರತಿ ತಿಂಗಳು ₹1,200 ಮಾಸಾಶನ ಪಿಂಚಣಿ.",
        "full_description_en": (
            "The Sandhya Suraksha Yojana is implemented by the Directorate of Social Security and Pensions, "
            "Revenue Department, Government of Karnataka. It assists indigent senior citizens in rural and urban areas "
            "who lack family support or pension coverage, ensuring dignity, nutritional security, and basic medical access."
        ),
        "full_description_kn": (
            "ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ ಯೋಜನೆಯು ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಕಂದಾಯ ಇಲಾಖೆಯ ಸಾಮಾಜಿಕ ಭದ್ರತೆ ಮತ್ತು ಪಿಂಚಣಿಗಳ ನಿರ್ದೇಶನಾಲಯದ ವತಿಯಿಂದ "
            "ಜಾರಿಯಲ್ಲಿದೆ. ಯಾವುದೇ ಆದಾಯದ ಮೂಲವಿಲ್ಲದ 65 ವರ್ಷ ಮತ್ತು ಮೇಲ್ಪಟ್ಟ ಹಿರಿಯ ನಾಗರಿಕರಿಗೆ ಮಾಸಿಕ ₹1,200 ಪಿಂಚಣಿ ನೀಡಿ ಗೌರವಯುತ ಜೀವನಕ್ಕೆ "
            "ನೆರವಾಗುತ್ತದೆ."
        ),
        "beneficiary_summary_en": "Elderly Karnataka residents aged 65 years and older with annual income under ₹20,000.",
        "beneficiary_summary_kn": "65 ವರ್ಷ ತುಂಬಿರುವ ಹಾಗೂ ವಾರ್ಷಿಕ ಆದಾಯ ₹20,000 ಕ್ಕಿಂತ ಕಡಿಮೆ ಇರುವ ಹಿರಿಯ ನಾಗರಿಕರು.",
        "beneficiary_types": ["senior_citizens"],
        "tags": ["Senior Citizens", "Social Security", "Monthly Pension", "Elderly Welfare"],
        "benefits_en": [
            "Monthly lifelong pension of ₹1,200 deposited into savings account or money order.",
            "Subsidized public healthcare benefits at Taluk hospitals and PHCs.",
            "Concession in KSRTC rural bus travel passes for seniors.",
        ],
        "benefits_kn": [
            "ತಿಂಗಳಿಗೆ ₹1,200 ಮಾಸಿಕ ಪಿಂಚಣಿ ನೇರವಾಗಿ ಬ್ಯಾಂಕ್ ಅಥವಾ ಅಂಚೆ ಖಾತೆಗೆ.",
            "ತಾಲೂಕು ಆಸ್ಪತ್ರೆಗಳು ಮತ್ತು ಪ್ರಾಥಮಿಕ ಆರೋಗ್ಯ ಕೇಂದ್ರಗಳಲ್ಲಿ ಉಚಿತ ವೈದ್ಯಕೀಯ ಸೇವೆ.",
            "ಕೆಎಸ್‌ಆರ್‌ಟಿಸಿ ಗ್ರಾಮೀಣ ಬಸ್ ಪ್ರಯಾಣ ಪಾಸ್‌ನಲ್ಲಿ ರಿಯಾಯಿತಿ.",
        ],
        "eligibility_conditions_en": [
            "Must be a permanent resident of Karnataka for at least 3 years.",
            "Must have completed 65 years of age on the date of application.",
            "Total combined annual income of applicant and spouse must not exceed ₹20,000.",
            "Must not be receiving pension from any other government or private source.",
        ],
        "eligibility_conditions_kn": [
            "ಕನಿಷ್ಠ 3 ವರ್ಷಗಳಿಂದ ಕರ್ನಾಟಕದ ಕಾಯಂ ನಿವಾಸಿಯಾಗಿರಬೇಕು.",
            "ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ದಿನಾಂಕಕ್ಕೆ 65 ವರ್ಷ ವಯಸ್ಸು ಪೂರ್ಣಗೊಂಡಿರಬೇಕು.",
            "ಅರ್ಜಿದಾರ ಮತ್ತು ಪತ್ನಿ/ಪತಿಯ ಒಟ್ಟು ವಾರ್ಷಿಕ ಆದಾಯ ₹20,000 ಮೀರಬಾರದು.",
            "ಇತರ ಯಾವುದೇ ಸರ್ಕಾರಿ ಅಥವಾ ಖಾಸಗಿ ಪಿಂಚಣಿ ಪಡೆಯುತ್ತಿರಬಾರದು.",
        ],
        "required_documents": [
            {
                "id": "age_proof",
                "name_en": "Age Proof (Voter ID / Birth Certificate / Aadhaar)",
                "name_kn": "ವಯಸ್ಸಿನ ಪುರಾವೆ (ಮತದಾರರ ಗುರುತಿನ ಚೀಟಿ / ಆಧಾರ್)",
                "description_en": "Official document clearly showing date of birth or age 65+.",
                "description_kn": "65 ವರ್ಷ ಪೂರ್ಣಗೊಂಡಿರುವುದನ್ನು ದೃಢೀಕರಿಸುವ ಅಧಿಕೃತ ದಾಖಲೆ.",
                "mandatory": True,
            },
            {
                "id": "income_cert",
                "name_en": "Income Certificate from Tahsildar / Nadakacheri",
                "name_kn": "ತಹಶೀಲ್ದಾರ್ / ನಾಡಕಚೇರಿ ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ",
                "description_en": "Certifying family income is under ₹20,000 per year.",
                "description_kn": "ವಾರ್ಷಿಕ ಆದಾಯ ₹20,000 ಕ್ಕಿಂತ ಕಡಿಮೆ ಇದೆ ಎಂದು ದೃಢೀಕರಿಸುವ ಪ್ರಮಾಣಪತ್ರ.",
                "mandatory": True,
            },
            {
                "id": "bank_post_account",
                "name_en": "Bank or Post Office Passbook",
                "name_kn": "ಬ್ಯಾಂಕ್ ಅಥವಾ ಅಂಚೆ ಕಚೇರಿ ಪಾಸ್‌ಬುಕ್",
                "description_en": "Active single account in applicant's name.",
                "description_kn": "ಅರ್ಜಿದಾರರ ಹೆಸರಿನಲ್ಲಿರುವ ಬ್ಯಾಂಕ್ ಅಥವಾ ಅಂಚೆ ಖಾತೆಯ ಪಾಸ್‌ಬುಕ್.",
                "mandatory": True,
            },
        ],
        "application_process_en": [
            "Obtain your verified age and income certificates from the local Nadakacheri.",
            "Visit the nearest Grama One centre or Taluk Office (Nemmadi Kendra).",
            "Fill and submit the Sandhya Suraksha application form with required documents.",
            "Revenue Inspector (RI) / Village Administrative Officer conducts field verification.",
            "Sanction order is issued by the Tahsildar and pension begins in 30-45 days.",
        ],
        "application_process_kn": [
            "ನಾಡಕಚೇರಿಯಿಂದ ವಯಸ್ಸು ಮತ್ತು ಆದಾಯ ಪ್ರಮಾಣಪತ್ರವನ್ನು ಪಡೆದುಕೊಳ್ಳಿ.",
            "ಹತ್ತಿರದ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ ಅಥವಾ ತಾಲೂಕು ಕಚೇರಿಗೆ ಭೇಟಿ ನೀಡಿ.",
            "ಅಗತ್ಯ ದಾಖಲೆಗಳೊಂದಿಗೆ ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ.",
            "ಗ್ರಾಮ ಆಡಳಿತಾಧಿಕಾರಿ ಮತ್ತು ಕಂದಾಯ ನಿರೀಕ್ಷಕರು ಸ್ಥಳ ಪರಿಶೀಲನೆ ನಡೆಸುತ್ತಾರೆ.",
            "ತಹಶೀಲ್ದಾರರ ಅನುಮೋದನೆಯ ನಂತರ 30-45 ದಿನಗಳಲ್ಲಿ ಮಾಸಾಶನ ಆರಂಭವಾಗುತ್ತದೆ.",
        ],
        "official_portal_url": "https://nadakacheri.karnataka.gov.in",
        "last_verified_date": "2026-02-18",
        "disclaimer_en": "Informational guide only. Sanction is determined by the Revenue Department / Tahsildar.",
        "disclaimer_kn": "ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ಮಂಜೂರಾತಿ ನಿರ್ಧಾರವು ಕಂದಾಯ ಇಲಾಖೆ ಹಾಗೂ ತಹಶೀಲ್ದಾರರಿಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
        "is_development_sample": True,
        "eligibility_criteria": {
            "must_be_karnataka_resident": True,
            "min_age": 65,
            "max_annual_income": 20000.0,
        },
        "eligibility_questions": [
            {
                "id": "is_karnataka_resident",
                "question_en": "Are you a permanent resident of Karnataka?",
                "question_kn": "ನೀವು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Must have resided in Karnataka for at least 3 years.",
                "help_text_kn": "ಕನಿಷ್ಠ 3 ವರ್ಷಗಳಿಂದ ಕರ್ನಾಟಕದಲ್ಲಿ ವಾಸಿಸುತ್ತಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "age",
                "question_en": "What is the applicant's age in completed years?",
                "question_kn": "ಅರ್ಜಿದಾರರ ವಯಸ್ಸು ಎಷ್ಟು?",
                "question_type": "number",
                "help_text_en": "Applicant must be 65 years or older.",
                "help_text_kn": "ಕನಿಷ್ಠ 65 ವರ್ಷ ತುಂಬಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "annual_income",
                "question_en": "What is your total annual household income (in ₹)?",
                "question_kn": "ನಿಮ್ಮ ಕುಟುಂಬದ ಒಟ್ಟು ವಾರ್ಷಿಕ ಆದಾಯ ಎಷ್ಟು (₹)?",
                "question_type": "number",
                "help_text_en": "Income must not exceed ₹20,000 per year.",
                "help_text_kn": "ವಾರ್ಷಿಕ ಆದಾಯ ₹20,000 ಮೀರಬಾರದು.",
                "mandatory": True,
            },
            {
                "id": "receives_other_pension",
                "question_en": "Do you already receive any other government pension?",
                "question_kn": "ನೀವು ಈಗಾಗಲೇ ಇತರ ಯಾವುದೇ ಸರ್ಕಾರಿ ಪಿಂಚಣಿ ಪಡೆಯುತ್ತಿದ್ದೀರಾ?",
                "question_type": "boolean",
                "help_text_en": "Beneficiaries of other pensions are ineligible.",
                "help_text_kn": "ಬೇರೆ ಪಿಂಚಣಿ ಪಡೆಯುತ್ತಿರುವವರಿಗೆ ಈ ಯೋಜನೆ ಸಿಗುವುದಿಲ್ಲ.",
                "mandatory": True,
            },
        ],
    },
    {
        "id": "anna-bhagya",
        "name_en": "Anna Bhagya Food & Cash Guarantee",
        "name_kn": "ಅನ್ನ ಭಾಗ್ಯ ಆಹಾರ ಭದ್ರತೆ ಮತ್ತು ಡಿಬಿಟಿ ಯೋಜನೆ",
        "category": "rural_families",
        "short_description_en": "Free food grains plus cash DBT in lieu of extra rice for Antyodaya and BPL families.",
        "short_description_kn": "ಅಂತ್ಯೋದಯ ಮತ್ತು ಬಿಪಿಎಲ್ ಕುಟುಂಬಗಳಿಗೆ ಉಚಿತ ಆಹಾರ ಧಾನ್ಯ ಹಾಗೂ ಹೆಚ್ಚುವರಿ ಅಕ್ಕಿಯ ಬದಲಿಗೆ ನೇರ ನಗದು.",
        "full_description_en": (
            "Anna Bhagya is a core food security scheme by the Food, Civil Supplies & Consumer Affairs Department, "
            "Government of Karnataka. It supplies 5 kg free rice per person per month under the National Food Security Act (NFSA), "
            "plus a cash transfer of ₹170 per person per month (₹34 per kg for an additional 5 kg) directly to the head of the family's bank account."
        ),
        "full_description_kn": (
            "ಅನ್ನ ಭಾಗ್ಯ ಯೋಜನೆಯು ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಆಹಾರ, ನಾಗರಿಕ ಸರಬರಾಜು ಮತ್ತು ಗ್ರಾಹಕರ ವ್ಯವಹಾರಗಳ ಇಲಾಖೆಯ ಮಹತ್ವಾಕಾಂಕ್ಷೆಯ ಯೋಜನೆಯಾಗಿದೆ. "
            "ಪ್ರತಿ ವ್ಯಕ್ತಿಗೆ 5 ಕೆಜಿ ಉಚಿತ ಅಕ್ಕಿಯ ಜೊತೆಗೆ ಹೆಚ್ಚುವರಿ 5 ಕೆಜಿ ಅಕ್ಕಿಯ ಬದಲಾಗಿ ಪ್ರತಿ ಕೆಜಿಗೆ ₹34 ರಂತೆ ತಿಂಗಳಿಗೆ ₹170 ನೇರ ನಗದು (DBT) ಅನ್ನು "
            "ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥರ ಖಾತೆಗೆ ಜಮೆ ಮಾಡಲಾಗುತ್ತದೆ."
        ),
        "beneficiary_summary_en": "All members of Antyodaya Anna Yojana (AAY) and Priority Household (BPL / PHH) ration cards in Karnataka.",
        "beneficiary_summary_kn": "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ಅಂತ್ಯೋದಯ (AAY) ಮತ್ತು ಬಿಪಿಎಲ್ (BPL / PHH) ಪಡಿತರ ಚೀಟಿ ಹೊಂದಿರುವ ಕುಟುಂಬಗಳು.",
        "beneficiary_types": ["rural_families"],
        "tags": ["Food Security", "Ration", "DBT", "BPL", "Nutrition"],
        "benefits_en": [
            "5 kg free food grains per beneficiary per month through Fair Price Shops.",
            "Direct cash DBT of ₹170 per person per month transferred into Aadhaar-seeded bank account.",
            "No cost or card renewal charges.",
        ],
        "benefits_kn": [
            "ನ್ಯಾಯಬೆಲೆ ಅಂಗಡಿಗಳ ಮೂಲಕ ಪ್ರತಿ ಫಲಾನುಭವಿಗೆ ತಿಂಗಳಿಗೆ 5 ಕೆಜಿ ಉಚಿತ ಆಹಾರ ಧಾನ್ಯ.",
            "ಆಧಾರ್ ಲಿಂಕ್ ಆದ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಪ್ರತಿ ಸದಸ್ಯರಿಗೆ ತಿಂಗಳಿಗೆ ₹170 ನೇರ ನಗದು (DBT).",
            "ಯಾವುದೇ ನವೀಕರಣ ಶುಲ್ಕವಿಲ್ಲ.",
        ],
        "eligibility_conditions_en": [
            "Must be a resident of Karnataka holding a valid BPL (Priority Household) or Antyodaya (AAY) card.",
            "Head of the family's bank account must be mapped with NPCI and Aadhaar active.",
            "Cardholder must periodically verify biometric e-KYC at the local Fair Price Shop.",
        ],
        "eligibility_conditions_kn": [
            "ಕರ್ನಾಟಕದಲ್ಲಿ ಮಾನ್ಯವಾದ ಬಿಪಿಎಲ್ ಅಥವಾ ಅಂತ್ಯೋದಯ ಪಡಿತರ ಚೀಟಿ ಹೊಂದಿರಬೇಕು.",
            "ಕುಟುಂಬದ ಮುಖ್ಯಸ್ಥರ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಆಧಾರ್ ಮತ್ತು ಎನ್‌ಪಿಸಿಐ ಮ್ಯಾಪಿಂಗ್ ಸಕ್ರಿಯವಾಗಿರಬೇಕು.",
            "ನ್ಯಾಯಬೆಲೆ ಅಂಗಡಿಯಲ್ಲಿ ಕಾಲಕಾಲಕ್ಕೆ ಬಯೋಮೆಟ್ರಿಕ್ ಇ-ಕೆವೈಸಿ (e-KYC) ಪೂರ್ಣಗೊಳಿಸಿರಬೇಕು.",
        ],
        "required_documents": [
            {
                "id": "bpl_ration_card",
                "name_en": "BPL or Antyodaya Ration Card",
                "name_kn": "ಬಿಪಿಎಲ್ ಅಥವಾ ಅಂತ್ಯೋದಯ ಪಡಿತರ ಚೀಟಿ",
                "description_en": "Valid 12-digit Karnataka ration card number.",
                "description_kn": "12 ಅಂಕಿಗಳ ಮಾನ್ಯ ಕರ್ನಾಟಕ ಪಡಿತರ ಚೀಟಿ ಸಂಖ್ಯೆ.",
                "mandatory": True,
            },
            {
                "id": "family_aadhaar",
                "name_en": "Aadhaar Card of all listed members",
                "name_kn": "ಕುಟುಂಬದ ಎಲ್ಲಾ ಸದಸ್ಯರ ಆಧಾರ್ ಕಾರ್ಡ್",
                "description_en": "Used for e-KYC biometric matching in Ahara database.",
                "description_kn": "ಆಹಾರ ತಂತ್ರಾಂಶದಲ್ಲಿ ಇ-ಕೆವೈಸಿ ಬಯೋಮೆಟ್ರಿಕ್ ದೃಢೀಕರಣಕ್ಕಾಗಿ.",
                "mandatory": True,
            },
        ],
        "application_process_en": [
            "Existing valid BPL and AAY cardholders are enrolled automatically.",
            "Verify your DBT linking status at https://ahara.kar.nic.in or at your Grama One centre.",
            "If DBT fails, link your bank account to Aadhaar at your bank branch.",
            "Collect food grains monthly at your allotted fair price shop using biometric authentication.",
        ],
        "application_process_kn": [
            "ಹಾಲಿ ಚಾಲ್ತಿಯಲ್ಲಿರುವ ಬಿಪಿಎಲ್ ಮತ್ತು ಎಎವೈ ಕಾರ್ಡ್‌ದಾರರು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಅರ್ಹರಾಗಿರುತ್ತಾರೆ.",
            "ahara.kar.nic.in ಅಥವಾ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರದಲ್ಲಿ ಡಿಬಿಟಿ ಸ್ಟೇಟಸ್ ಪರಿಶೀಲಿಸಿ.",
            "ಡಿಬಿಟಿ ಹಣ ಬಾರದಿದ್ದಲ್ಲಿ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಭೇಟಿ ನೀಡಿ ಆಧಾರ್ ಸೀಡಿಂಗ್ ಮಾಡಿಸಿ.",
            "ನ್ಯಾಯಬೆಲೆ ಅಂಗಡಿಯಲ್ಲಿ ಹೆಬ್ಬೆಟ್ಟು ಒತ್ತುವ ಮೂಲಕ ಪ್ರತಿ ತಿಂಗಳು ಪಡಿತರ ಪಡೆದುಕೊಳ್ಳಿ.",
        ],
        "official_portal_url": "https://ahara.kar.nic.in",
        "last_verified_date": "2026-03-01",
        "disclaimer_en": "Informational guide only. Rations and cash entitlement are controlled by Food and Civil Supplies Dept.",
        "disclaimer_kn": "ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ಪಡಿತರ ಹಾಗೂ ನಗದು ವಿತರಣೆಯು ಆಹಾರ ಮತ್ತು ನಾಗರಿಕ ಸರಬರಾಜು ಇಲಾಖೆಯ ನಿಯಮಾವಳಿಗಳಿಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
        "is_development_sample": True,
        "eligibility_criteria": {
            "must_be_karnataka_resident": True,
            "requires_bpl_or_antyodaya": True,
        },
        "eligibility_questions": [
            {
                "id": "is_karnataka_resident",
                "question_en": "Are you a permanent resident of Karnataka?",
                "question_kn": "ನೀವು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Must reside permanently in Karnataka.",
                "help_text_kn": "ಕರ್ನಾಟಕದಲ್ಲಿ ವಾಸಿಸುತ್ತಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "has_bpl_or_antyodaya_card",
                "question_en": "Does your family have an active BPL or Antyodaya (AAY) ration card?",
                "question_kn": "ನಿಮ್ಮ ಕುಟುಂಬವು ಚಾಲ್ತಿಯಲ್ಲಿರುವ ಬಿಪಿಎಲ್ (BPL) ಅಥವಾ ಅಂತ್ಯೋದಯ (AAY) ಪಡಿತರ ಚೀಟಿ ಹೊಂದಿದೆಯೇ?",
                "question_type": "boolean",
                "help_text_en": "APL cardholders are not eligible for Anna Bhagya rice/cash DBT.",
                "help_text_kn": "ಎಪಿಎಲ್ ಕಾರ್ಡ್‌ದಾರರಿಗೆ ಈ ಸೌಲಭ್ಯ ಅನ್ವಯಿಸುವುದಿಲ್ಲ.",
                "mandatory": True,
            },
        ],
    },
    {
        "id": "yuva-nidhi",
        "name_en": "Yuva Nidhi Graduate Allowance Scheme",
        "name_kn": "ಯುವ ನಿಧಿ ನಿರುದ್ಯೋಗ ಭತ್ಯೆ ಯೋಜನೆ",
        "category": "students",
        "short_description_en": "Monthly allowance of ₹3,000 for degree holders and ₹1,500 for diploma holders seeking employment.",
        "short_description_kn": "ಉದ್ಯೋಗ ಹುಡುಕುತ್ತಿರುವ ಪದವೀಧರರಿಗೆ ಮಾಸಿಕ ₹3,000 ಹಾಗೂ ಡಿಪ್ಲೊಮಾ ಹೊಂದಿದವರಿಗೆ ₹1,500 ಭತ್ಯೆ.",
        "full_description_en": (
            "Yuva Nidhi is an unemployment allowance scheme by the Department of Skill Development, Entrepreneurship and Livelihood, "
            "Government of Karnataka. It assists educated youth who completed their graduation or diploma and have remained "
            "unemployed after 180 days, providing financial support for up to 2 years while they upskill or seek jobs."
        ),
        "full_description_kn": (
            "ಯುವ ನಿಧಿ ಯೋಜನೆಯು ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಕೌಶಲ್ಯಾಭಿವೃದ್ಧಿ, ಉದ್ಯಮಶೀಲತೆ ಮತ್ತು ಜೀವನೋಪಾಯ ಇಲಾಖೆಯ ಪ್ರಮುಖ ಯೋಜನೆಯಾಗಿದ್ದು, "
            "ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಮುಗಿಸಿ 180 ದಿನಗಳವರೆಗೆ ಉದ್ಯೋಗ ಸಿಗದ ಯುವಜನತೆಗೆ ಗರಿಷ್ಠ 2 ವರ್ಷಗಳವರೆಗೆ ಅಥವಾ ಉದ್ಯೋಗ ದೊರೆಯುವವರೆಗೆ "
            "ಮಾಸಿಕ ಆರ್ಥಿಕ ನೆರವು ನೀಡುತ್ತದೆ."
        ),
        "beneficiary_summary_en": "Unemployed degree and diploma holders graduated from Karnataka universities/colleges.",
        "beneficiary_summary_kn": "ಕರ್ನಾಟಕದ ವಿಶ್ವವಿದ್ಯಾಲಯಗಳಲ್ಲಿ ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪಡೆದು ಉದ್ಯೋಗ ಹುಡುಕುತ್ತಿರುವ ಯುವಕ-ಯುವತಿಯರು.",
        "beneficiary_types": ["students", "other_beneficiaries"],
        "tags": ["Youth", "Employment", "Allowance", "Skill Development", "Graduates"],
        "benefits_en": [
            "₹3,000 per month for degree holders for up to 24 months.",
            "₹1,500 per month for diploma holders for up to 24 months.",
            "Free access to government skill training and placement workshops.",
        ],
        "benefits_kn": [
            "ಪದವೀಧರರಿಗೆ ತಿಂಗಳಿಗೆ ₹3,000 (ಗರಿಷ್ಠ 24 ತಿಂಗಳವರೆಗೆ).",
            "ಡಿಪ್ಲೊಮಾ ಹೊಂದಿದವರಿಗೆ ತಿಂಗಳಿಗೆ ₹1,500 (ಗರಿಷ್ಠ 24 ತಿಂಗಳವರೆಗೆ).",
            "ಉಚಿತ ಕೌಶಲ್ಯ ತರಬೇತಿ ಮತ್ತು ಉದ್ಯೋಗ ಮೇಳಗಳಲ್ಲಿ ಆದ್ಯತೆ.",
        ],
        "eligibility_conditions_en": [
            "Must be a domicile of Karnataka for at least 6 years.",
            "Must have graduated or completed diploma from a Karnataka institution in academic year 2023 onwards.",
            "Must have remained unemployed or self-unemployed for at least 180 days post-graduation.",
            "Must not be enrolled in higher full-time education.",
        ],
        "eligibility_conditions_kn": [
            "ಕನಿಷ್ಠ 6 ವರ್ಷಗಳಿಂದ ಕರ್ನಾಟಕದ ಕಾಯಂ ನಿವಾಸಿಯಾಗಿರಬೇಕು.",
            "2023 ರ ನಂತರ ಕರ್ನಾಟಕದ ಸಂಸ್ಥೆಗಳಿಂದ ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪಾಸಾಗಿರಬೇಕು.",
            "ಪದವಿ ಪಡೆದ 180 ದಿನಗಳವರೆಗೆ ಯಾವುದೇ ಉದ್ಯೋಗ ಸಿಗದಿರಬೇಕು.",
            "ಮುಂದಿನ ಉನ್ನತ ಶಿಕ್ಷಣಕ್ಕೆ ದಾಖಲಾಗಿರಬಾರದು.",
        ],
        "required_documents": [
            {
                "id": "degree_cert",
                "name_en": "Degree or Diploma Marks Card / Certificate",
                "name_kn": "ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಅಂಕಪಟ್ಟಿ / ಪ್ರಮಾಣಪತ್ರ",
                "description_en": "Final year passing certificate with university registration number.",
                "description_kn": "ವಿಶ್ವವಿದ್ಯಾಲಯದ ನೋಂದಣಿ ಸಂಖ್ಯೆ ಹೊಂದಿರುವ ಅಂತಿಮ ವರ್ಷದ ಅಂಕಪಟ್ಟಿ.",
                "mandatory": True,
            },
            {
                "id": "aadhaar_card",
                "name_en": "Aadhaar Card",
                "name_kn": "ಆಧಾರ್ ಕಾರ್ಡ್",
                "description_en": "Applicant's Aadhaar linked to mobile and bank account.",
                "description_kn": "ಮೊಬೈಲ್ ಮತ್ತು ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಲಿಂಕ್ ಆಗಿರುವ ಆಧಾರ್ ಕಾರ್ಡ್.",
                "mandatory": True,
            },
        ],
        "application_process_en": [
            "Register on the Seva Sindhu portal using your Aadhaar and University Registration Number.",
            "Verify your graduation year and unemployment declaration online.",
            "Submit the application through Seva Sindhu or your nearest Grama One centre.",
            "Direct Benefit Transfer begins on the next monthly billing cycle.",
        ],
        "application_process_kn": [
            "ಸೇವಾ ಸಿಂಧು ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಆಧಾರ್ ಮತ್ತು ಪದವಿ ನೋಂದಣಿ ಸಂಖ್ಯೆ ಬಳಸಿ ನೊಂದಣಿ ಮಾಡಿ.",
            "ಉದ್ಯೋಗವಿಲ್ಲ ಎಂಬ ಸ್ವಯಂ ಘೋಷಣೆಯನ್ನು ಆನ್‌ಲೈನ್ ಮೂಲಕ ದೃಢೀಕರಿಸಿ.",
            "ಗ್ರಾಮ ಒನ್ ಅಥವಾ ಕರ್ನಾಟಕ ಒನ್ ಕೇಂದ್ರದ ಮೂಲಕ ಅರ್ಜಿಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
            "ಮುಂದಿನ ಮಾಸಿಕ ಬಿಲ್ಲಿಂಗ್ ಸೈಕಲ್‌ನಲ್ಲಿ ಹಣ ಖಾತೆಗೆ ಜಮೆಯಾಗುತ್ತದೆ.",
        ],
        "official_portal_url": "https://sevasindhugs.karnataka.gov.in",
        "last_verified_date": "2026-03-05",
        "disclaimer_en": "Informational guide only. Candidate must submit monthly self-declaration of unemployment to maintain allowance.",
        "disclaimer_kn": "ಮಾಹಿತಿಗಾಗಿ ಮಾತ್ರ. ಭತ್ಯೆ ಮುಂದುವರಿಯಲು ಪ್ರತಿ ತಿಂಗಳು ನಿರುದ್ಯೋಗ ಸ್ವಯಂ ಘೋಷಣೆ ಸಲ್ಲಿಸಬೇಕು.",
        "is_development_sample": True,
        "eligibility_criteria": {
            "must_be_karnataka_resident": True,
            "min_age": 18,
            "max_age": 35,
        },
        "eligibility_questions": [
            {
                "id": "is_karnataka_resident",
                "question_en": "Are you a permanent resident of Karnataka?",
                "question_kn": "ನೀವು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯೇ?",
                "question_type": "boolean",
                "help_text_en": "Must have studied in or resided in Karnataka.",
                "help_text_kn": "ಕರ್ನಾಟಕದಲ್ಲಿ ನೆಲೆಸಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "age",
                "question_en": "What is your current age in completed years?",
                "question_kn": "ನಿಮ್ಮ ವಯಸ್ಸು ಎಷ್ಟು?",
                "question_type": "number",
                "help_text_en": "Age must be between 18 and 35.",
                "help_text_kn": "ವಯಸ್ಸು 18 ರಿಂದ 35 ರ ಒಳಗೆ ಇರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "has_degree_or_diploma",
                "question_en": "Have you completed a recognized Degree or Diploma?",
                "question_kn": "ನೀವು ಮಾನ್ಯತೆ ಪಡೆದ ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪೂರ್ಣಗೊಳಿಸಿದ್ದೀರಾ?",
                "question_type": "boolean",
                "help_text_en": "Graduation must be completed.",
                "help_text_kn": "ಪದವಿ ಅಥವಾ ಡಿಪ್ಲೊಮಾ ಪಾಸಾಗಿರಬೇಕು.",
                "mandatory": True,
            },
            {
                "id": "is_currently_employed",
                "question_en": "Are you currently employed in any government, private, or contract job?",
                "question_kn": "ನೀವು ಪ್ರಸ್ತುತ ಯಾವುದೇ ಸರ್ಕಾರಿ, ಖಾಸಗಿ ಅಥವಾ ಗುತ್ತಿಗೆ ಉದ್ಯೋಗದಲ್ಲಿದ್ದೀರಾ?",
                "question_type": "boolean",
                "help_text_en": "Must be currently unemployed to qualify.",
                "help_text_kn": "ಯೋಜನೆಯ ಲಾಭ ಪಡೆಯಲು ಪ್ರಸ್ತುತ ಉದ್ಯೋಗವಿಲ್ಲದಿರಬೇಕು.",
                "mandatory": True,
            },
        ],
    },
]

SAMPLE_CENTRES = [
    {
        "id": "grama-one-hebbalu-davangere",
        "name_en": "Grama One Centre - Hebbalu",
        "name_kn": "ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ - ಹೆಬ್ಬಾಳು",
        "center_type": "Grama One",
        "district": "Davanagere",
        "taluk": "Davanagere Rural",
        "address_en": "Grama Panchayat Office Compound, Main Road, Hebbalu Village, Davanagere - 577514",
        "address_kn": "ಗ್ರಾಮ ಪಂಚಾಯತಿ ಕಾರ್ಯಾಲಯದ ಆವರಣ, ಮುಖ್ಯ ರಸ್ತೆ, ಹೆಬ್ಬಾಳು ಗ್ರಾಮ, ದಾವಣಗೆರೆ - 577514",
        "contact_phone": "+91 8192 234567",
        "contact_email": "gramaone.hebbalu@karnataka.gov.in",
        "operating_hours_en": "Monday to Saturday: 9:00 AM - 6:00 PM (Closed on Sundays & Govt Holidays)",
        "operating_hours_kn": "ಸೋಮವಾರದಿಂದ ಶನಿವಾರ: ಬೆಳಗ್ಗೆ 9:00 ರಿಂದ ಸಂಜೆ 6:00 (ಭಾನುವಾರ ಮತ್ತು ಸರ್ಕಾರಿ ರಜೆ ಹೊರತುಪಡಿಸಿ)",
        "directions_url": "https://maps.google.com/?q=14.4644,75.9218",
        "latitude": 14.4644,
        "longitude": 75.9218,
        "services_offered_en": [
            "Revenue Department Certificates (Caste, Income, RTC)",
            "Gruha Lakshmi & Guarantee Scheme Applications",
            "FRUITS Farmer Registration & e-KYC",
            "SSP Scholarship e-Attestation & Filing",
            "Electricity Bill & Water Bill Payments",
        ],
        "services_offered_kn": [
            "ಕಂದಾಯ ಇಲಾಖೆಯ ಜಾತಿ, ಆದಾಯ ಮತ್ತು ಪಹಣಿ ಪ್ರಮಾಣಪತ್ರಗಳು",
            "ಗೃಹ ಲಕ್ಷ್ಮಿ ಹಾಗೂ ಖಾತರಿ ಯೋಜನೆಗಳ ಅರ್ಜಿ ಸಲ್ಲಿಕೆ",
            "ಫ್ರೂಟ್ಸ್ ರೈತರ ನೋಂದಣಿ ಮತ್ತು ಇ-ಕೆವೈಸಿ",
            "ಎಸ್‌ಎಸ್‌ಪಿ ವಿದ್ಯಾರ್ಥಿವೇತನ ಅರ್ಜಿ",
            "ವಿದ್ಯುತ್ ಮತ್ತು ನೀರಿನ ಬಿಲ್ ಪಾವತಿ",
        ],
        "is_development_sample": True,
    },
    {
        "id": "grama-one-byadgi-haveri",
        "name_en": "Grama One Centre - Byadgi Rural",
        "name_kn": "ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ - ಬ್ಯಾಡಗಿ ಗ್ರಾಮೀಣ",
        "center_type": "Grama One",
        "district": "Haveri",
        "taluk": "Byadgi",
        "address_en": "Near APMC Yard, Motebennur Road, Byadgi, Haveri District - 581106",
        "address_kn": "ಎಪಿಎಂಸಿ ಯಾರ್ಡ್ ಹತ್ತಿರ, ಮೋಟೇಬೆನ್ನೂರು ರಸ್ತೆ, ಬ್ಯಾಡಗಿ, ಹಾವೇರಿ ಜಿಲ್ಲೆ - 581106",
        "contact_phone": "+91 8375 228910",
        "contact_email": "gramaone.byadgi@karnataka.gov.in",
        "operating_hours_en": "Monday to Saturday: 9:30 AM - 6:30 PM",
        "operating_hours_kn": "ಸೋಮವಾರದಿಂದ ಶನಿವಾರ: ಬೆಳಗ್ಗೆ 9:30 ರಿಂದ ಸಂಜೆ 6:30",
        "directions_url": "https://maps.google.com/?q=14.6811,75.4855",
        "latitude": 14.6811,
        "longitude": 75.4855,
        "services_offered_en": [
            "Raitha Siri & Agriculture Subsidy Registration",
            "Sandhya Suraksha & Disability Pension Applications",
            "Pahani / RTC Printing & Mutation Status",
            "Ration Card e-KYC & Member Addition",
        ],
        "services_offered_kn": [
            "ರೈತ ಸಿರಿ ಮತ್ತು ಕೃಷಿ ಸಹಾಯಧನ ನೋಂದಣಿ",
            "ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ ಮತ್ತು ಅಂಗವಿಕಲ ಪಿಂಚಣಿ ಅರ್ಜಿ",
            "ಪಹಣಿ ಆರ್‌ಟಿಸಿ ಮುದ್ರಣ ಮತ್ತು ಮ್ಯುಟೇಶನ್ ಮಾಹಿತಿ",
            "ಪಡಿತರ ಚೀಟಿ ಇ-ಕೆವೈಸಿ",
        ],
        "is_development_sample": True,
    },
    {
        "id": "karnataka-one-shimoga-urban",
        "name_en": "Karnataka One Centre - Shimoga Market",
        "name_kn": "ಕರ್ನಾಟಕ ಒನ್ ಕೇಂದ್ರ - ಶಿವಮೊಗ್ಗ ಮಾರುಕಟ್ಟೆ",
        "center_type": "Karnataka One",
        "district": "Shimoga",
        "taluk": "Shimoga Urban",
        "address_en": "City Municipal Corporation Commercial Complex, Nehru Road, Shimoga - 577201",
        "address_kn": "ಮಹಾನಗರ ಪಾಲಿಕೆ ವಾಣಿಜ್ಯ ಸಂಕೀರ್ಣ, ನೆಹರೂ ರಸ್ತೆ, ಶಿವಮೊಗ್ಗ - 577201",
        "contact_phone": "+91 8182 222145",
        "contact_email": "k1.shimoga@karnataka.gov.in",
        "operating_hours_en": "Monday to Saturday: 8:00 AM - 7:00 PM; Sunday: 9:00 AM - 1:00 PM",
        "operating_hours_kn": "ಸೋಮವಾರದಿಂದ ಶನಿವಾರ: ಬೆಳಗ್ಗೆ 8:00 ರಿಂದ ಸಂಜೆ 7:00; ಭಾನುವಾರ: ಬೆಳಗ್ಗೆ 9:00 ರಿಂದ ಮಧ್ಯಾಹ್ನ 1:00",
        "directions_url": "https://maps.google.com/?q=13.9299,75.5681",
        "latitude": 13.9299,
        "longitude": 75.5681,
        "services_offered_en": [
            "Citizen Services Portal (Seva Sindhu)",
            "Aadhaar Update and Biometric Enrolment",
            "Transport Dept Driving License & RC Renewals",
            "Social Security Pension Verification",
        ],
        "services_offered_kn": [
            "ಸೇವಾ ಸಿಂಧು ನಾಗರಿಕ ಸೇವೆಗಳು",
            "ಆಧಾರ್ ತಿದ್ದುಪಡಿ ಹಾಗೂ ಹೊಸ ನೋಂದಣಿ",
            "ಸಾರಿಗೆ ಇಲಾಖೆಯ ಚಾಲನಾ ಪರವಾನಗಿ ನವೀಕರಣ",
            "ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಪಿಂಚಣಿ ಪರಿಶೀಲನೆ",
        ],
        "is_development_sample": True,
    },
    {
        "id": "grama-one-hunasagi-yadgir",
        "name_en": "Grama One Centre - Hunasagi",
        "name_kn": "ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ - ಹುಣಸಗಿ",
        "center_type": "Grama One",
        "district": "Yadgir",
        "taluk": "Hunasagi",
        "address_en": "Opposite Tahsildar Office, Main Bazaar, Hunasagi, Yadgir - 585215",
        "address_kn": "ತಹಶೀಲ್ದಾರ್ ಕಚೇರಿಯ ಎದುರು, ಮುಖ್ಯ ಬಜಾರ್, ಹುಣಸಗಿ, ಯಾದಗಿರಿ - 585215",
        "contact_phone": "+91 8479 240112",
        "contact_email": "gramaone.hunasagi@karnataka.gov.in",
        "operating_hours_en": "Monday to Saturday: 9:00 AM - 5:30 PM",
        "operating_hours_kn": "ಸೋಮವಾರದಿಂದ ಶನಿವಾರ: ಬೆಳಗ್ಗೆ 9:00 ರಿಂದ ಸಂಜೆ 5:30",
        "directions_url": "https://maps.google.com/?q=16.4421,76.5186",
        "latitude": 16.4421,
        "longitude": 76.5186,
        "services_offered_en": [
            "MGNREGA Job Card Application & Status Check",
            "Anna Bhagya Ration Card Services",
            "Sandhya Suraksha Pension Claims",
            "Kalyana Karnataka Special Concession Certificates",
        ],
        "services_offered_kn": [
            "ನರೇಗಾ ಜಾಬ್ ಕಾರ್ಡ್ ಅರ್ಜಿ ಮತ್ತು ಮಾಹಿತಿ",
            "ಅನ್ನ ಭಾಗ್ಯ ಪಡಿತರ ಚೀಟಿ ಸೇವೆಗಳು",
            "ಸಂಧ್ಯಾ ಸುರಕ್ಷಾ ಮಾಸಾಶನ ಅರ್ಜಿ",
            "ಕಲ್ಯಾಣ ಕರ್ನಾಟಕ 371(ಜೆ) ಪ್ರಮಾಣಪತ್ರ ಸೇವೆಗಳು",
        ],
        "is_development_sample": True,
    },
    {
        "id": "grama-one-mandya-rural",
        "name_en": "Grama One Centre - Dudda Hobli",
        "name_kn": "ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರ - ದುದ್ದ ಹೋಬಳಿ",
        "center_type": "Grama One",
        "district": "Mandya",
        "taluk": "Mandya Rural",
        "address_en": "Ryots Bhavan, Near Dudda Bus Stand, Mandya - 571405",
        "address_kn": "ರೈತ ಭವನ, ದುದ್ದ ಬಸ್ ನಿಲ್ದಾಣದ ಹತ್ತಿರ, ಮಂಡ್ಯ - 571405",
        "contact_phone": "+91 8232 245100",
        "contact_email": "gramaone.dudda@karnataka.gov.in",
        "operating_hours_en": "Monday to Saturday: 9:00 AM - 6:00 PM",
        "operating_hours_kn": "ಸೋಮವಾರದಿಂದ ಶನಿವಾರ: ಬೆಳಗ್ಗೆ 9:00 ರಿಂದ ಸಂಜೆ 6:00",
        "directions_url": "https://maps.google.com/?q=12.5218,76.8951",
        "latitude": 12.5218,
        "longitude": 76.8951,
        "services_offered_en": [
            "Sugarcane and Paddy Crop Insurance Registration",
            "FRUITS Land & Soil Health Certificates",
            "Gruha Lakshmi Cash Transfer Verification",
            "Caste & Income Certificate Applications",
        ],
        "services_offered_kn": [
            "ಕಬ್ಬು ಮತ್ತು ಭತ್ತದ ಬೆಳೆ ವಿಮೆ ನೋಂದಣಿ",
            "ಫ್ರೂಟ್ಸ್ ಭೂಮಿ ಮತ್ತು ಮಣ್ಣಿನ ಆರೋಗ್ಯ ದಾಖಲೆಗಳು",
            "ಗೃಹ ಲಕ್ಷ್ಮಿ ಹಣ ವರ್ಗಾವಣೆ ಪರಿಶೀಲನೆ",
            "ಜಾತಿ ಮತ್ತು ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ ಅರ್ಜಿಗಳು",
        ],
        "is_development_sample": True,
    },
    {
        "id": "bapuji-sevakendra-belagavi-gokak",
        "name_en": "Bapuji Seva Kendra - Gokak Rural",
        "name_kn": "ಬಾಪೂಜಿ ಸೇವಾ ಕೇಂದ್ರ - ಗೋಕಾಕ ಗ್ರಾಮೀಣ",
        "center_type": "Bapuji Seva Kendra",
        "district": "Belagavi",
        "taluk": "Gokak",
        "address_en": "Grama Panchayat Office Building, Konnur Cross, Gokak, Belagavi - 591307",
        "address_kn": "ಗ್ರಾಮ ಪಂಚಾಯತಿ ಕಾರ್ಯಾಲಯ, ಕೊಣ್ಣೂರು ಕ್ರಾಸ್, ಗೋಕಾಕ, ಬೆಳಗಾವಿ - 591307",
        "contact_phone": "+91 8332 225678",
        "contact_email": "bapuji.gokak@karnataka.gov.in",
        "operating_hours_en": "Monday to Saturday: 10:00 AM - 5:30 PM",
        "operating_hours_kn": "ಸೋಮವಾರದಿಂದ ಶನಿವಾರ: ಬೆಳಗ್ಗೆ 10:00 ರಿಂದ ಸಂಜೆ 5:30",
        "directions_url": "https://maps.google.com/?q=16.1667,74.8333",
        "latitude": 16.1667,
        "longitude": 74.8333,
        "services_offered_en": [
            "Panchayat Raj Property Tax & Form 9/11 Services",
            "Water Supply & Sanitation Maintenance Requests",
            "Grama Panchayat Welfare Scheme Applications",
        ],
        "services_offered_kn": [
            "ಗ್ರಾಮ ಪಂಚಾಯತಿ ನಮೂನೆ 9/11 ಮತ್ತು ಆಸ್ತಿ ತೆರಿಗೆ ಸೇವೆಗಳು",
            "ಕುಡಿಯುವ ನೀರು ಮತ್ತು ನೈರ್ಮಲ್ಯ ನಿರ್ವಹಣೆ ವಿನಂತಿ",
            "ಗ್ರಾಮ ಪಂಚಾಯತಿ ಮಟ್ಟದ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು",
        ],
        "is_development_sample": True,
    },
]

SAMPLE_USERS = [
    {
        "id": "user_demo_citizen",
        "email": "citizen@ruralconnect.karnataka.gov.in",
        "full_name": "Ramesh Gowda",
        "role": "citizen",
        "preferred_language": "kn",
        "password_plain": "Karnataka@2026",
    }
]


def seed_database(auto_if_empty: bool = False) -> None:
    db = get_db()
    schemes_col = db.collection("schemes")
    centers_col = db.collection("centers")
    users_col = db.collection("users")

    # 1. Seed Schemes
    existing_schemes = list(schemes_col.limit(1).stream())
    if len(existing_schemes) == 0 or not auto_if_empty:
        logger.info("Seeding schemes collection in Firestore...")
        for s in SAMPLE_SCHEMES:
            schemes_col.document(s["id"]).set(s, merge=True)
        logger.info("Successfully seeded %d schemes in Firestore.", len(SAMPLE_SCHEMES))
    else:
        logger.info("Schemes collection already populated. Skipping auto-seed.")

    # 2. Seed Centres
    existing_centers = list(centers_col.limit(1).stream())
    if len(existing_centers) == 0 or not auto_if_empty:
        logger.info("Seeding centers collection in Firestore...")
        for c in SAMPLE_CENTRES:
            centers_col.document(c["id"]).set(c, merge=True)
        logger.info("Successfully seeded %d service centres in Firestore.", len(SAMPLE_CENTRES))
    else:
        logger.info("Centers collection already populated. Skipping auto-seed.")

    # 3. Seed Demo User
    existing_users = list(users_col.limit(1).stream())
    if len(existing_users) == 0 or not auto_if_empty:
        logger.info("Seeding default demo user in Firestore...")
        for u in SAMPLE_USERS:
            doc = {
                "id": u["id"],
                "email": u["email"],
                "full_name": u["full_name"],
                "role": u["role"],
                "preferred_language": u["preferred_language"],
                "hashed_password": hash_password(u["password_plain"]),
            }
            users_col.document(doc["id"]).set(doc, merge=True)
        logger.info("Demo user seeded successfully in Firestore.")


if __name__ == "__main__":
    db_manager.connect()
    seed_database(auto_if_empty=False)
    db_manager.disconnect()
    print("Seed process completed successfully.")
