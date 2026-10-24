from typing import Dict, Any, List
from fastapi import HTTPException, status
from app.repositories.scheme_repository import SchemeRepository
from app.schemas.scheme import DocumentRequirement, EligibilityQuestion
from app.schemas.eligibility import (
    SchemeEligibilityConfigResponse,
    CheckEligibilityResponse,
    MissingRequirement,
)

scheme_repo = SchemeRepository()


class EligibilityService:
    def get_eligibility_questions(self, scheme_id: str) -> SchemeEligibilityConfigResponse:
        doc = scheme_repo.get_by_id(scheme_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheme with ID '{scheme_id}' was not found",
            )
        questions_raw = doc.get("eligibility_questions", [])
        questions = [EligibilityQuestion(**q) for q in questions_raw]
        return SchemeEligibilityConfigResponse(
            scheme_id=doc["id"],
            scheme_name_en=doc["name_en"],
            scheme_name_kn=doc["name_kn"],
            questions=questions,
        )

    def evaluate_eligibility(self, scheme_id: str, answers: Dict[str, Any]) -> CheckEligibilityResponse:
        doc = scheme_repo.get_by_id(scheme_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Scheme with ID '{scheme_id}' was not found",
            )

        questions = doc.get("eligibility_questions", [])
        rules = doc.get("eligibility_criteria", {})

        reasons_en: List[str] = []
        reasons_kn: List[str] = []
        missing_requirements: List[MissingRequirement] = []

        # 1. Check for missing mandatory questions
        for q in questions:
            qid = q.get("id")
            if q.get("mandatory", True):
                if qid not in answers or answers[qid] is None or answers[qid] == "":
                    return CheckEligibilityResponse(
                        scheme_id=doc["id"],
                        scheme_name_en=doc["name_en"],
                        scheme_name_kn=doc["name_kn"],
                        status="more_info_required",
                        status_title_en="More Information Required",
                        status_title_kn="ಹೆಚ್ಚಿನ ಮಾಹಿತಿ ಅಗತ್ಯವಿದೆ",
                        summary_en="Some mandatory eligibility questions were not answered.",
                        summary_kn="ಕೆಲವು ಕಡ್ಡಾಯ ಅರ್ಹತಾ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಲಾಗಿಲ್ಲ.",
                        reasons_en=["Please provide answers to all required questions to complete preliminary verification."],
                        reasons_kn=["ಪ್ರಾಥಮಿಕ ಪರಿಶೀಲನೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಲು ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಅಗತ್ಯ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ."],
                        missing_requirements=[
                            MissingRequirement(
                                field=qid,
                                message_en=f"Please answer: '{q.get('question_en')}'",
                                message_kn=f"ದಯವಿಟ್ಟು ಉತ್ತರಿಸಿ: '{q.get('question_kn')}'",
                            )
                        ],
                        document_checklist=[],
                        next_steps_en=["Return to the questionnaire and answer all mandatory questions."],
                        next_steps_kn=["ಪ್ರಶ್ನಾವಳಿಗೆ ಹಿಂತಿರುಗಿ ಮತ್ತು ಎಲ್ಲಾ ಕಡ್ಡಾಯ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ."],
                        preliminary_notice_en="This eligibility check is a preliminary discovery guide and does not guarantee government approval.",
                        preliminary_notice_kn="ಈ ಅರ್ಹತಾ ಪರಿಶೀಲನೆಯು ಕೇವಲ ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶಿಯಾಗಿದ್ದು, ಸರ್ಕಾರದ ಅನುಮೋದನೆಯನ್ನು ಖಾತರಿಪಡಿಸುವುದಿಲ್ಲ.",
                    )

        # 2. Evaluate criteria rules against submitted answers
        is_eligible = True

        # Karnataka Resident check
        if rules.get("must_be_karnataka_resident", True):
            is_res = answers.get("is_karnataka_resident")
            if is_res is False or str(is_res).lower() in ("no", "false"):
                is_eligible = False
                reasons_en.append("Applicant must be a permanent resident or domicile of Karnataka state.")
                reasons_kn.append("ಅರ್ಜಿದಾರರು ಕರ್ನಾಟಕ ರಾಜ್ಯದ ಕಾಯಂ ನಿವಾಸಿಯಾಗಿರಬೇಕು.")
                missing_requirements.append(
                    MissingRequirement(
                        field="is_karnataka_resident",
                        message_en="Karnataka domicile requirement not met.",
                        message_kn="ಕರ್ನಾಟಕ ರಾಜ್ಯ ನಿವಾಸದ ಷರತ್ತು ಪೂರೈಸಲಾಗಿಲ್ಲ.",
                    )
                )

        # Gender check
        allowed_genders = rules.get("allowed_genders")
        if allowed_genders and "gender" in answers:
            user_gender = str(answers["gender"]).lower()
            if user_gender not in [g.lower() for g in allowed_genders]:
                is_eligible = False
                reasons_en.append(f"Scheme is designated exclusively for: {', '.join(allowed_genders).title()}.")
                reasons_kn.append(f"ಯೋಜನೆಯು ನಿಗದಿತ ಲಿಂಗದ ಫಲಾನುಭವಿಗಳಿಗೆ ಮಾತ್ರ ಅನ್ವಯಿಸುತ್ತದೆ.")
                missing_requirements.append(
                    MissingRequirement(
                        field="gender",
                        message_en=f"Scheme eligibility is reserved for {', '.join(allowed_genders).title()} applicants.",
                        message_kn="ಯೋಜನೆಯ ಅರ್ಹತೆಯನ್ನು ನಿಗದಿತ ಫಲಾನುಭವಿಗಳಿಗೆ ಮೀಸಲಿಡಲಾಗಿದೆ.",
                    )
                )

        # Age checks
        min_age = rules.get("min_age")
        max_age = rules.get("max_age")
        if "age" in answers and answers["age"] is not None:
            try:
                user_age = int(answers["age"])
                if min_age is not None and user_age < min_age:
                    is_eligible = False
                    reasons_en.append(f"Minimum age requirement is {min_age} years (current age: {user_age}).")
                    reasons_kn.append(f"ಕನಿಷ್ಠ ವಯೋಮಿತಿ {min_age} ವರ್ಷಗಳು (ಪ್ರಸ್ತುತ ವಯಸ್ಸು: {user_age}).")
                    missing_requirements.append(
                        MissingRequirement(
                            field="age",
                            message_en=f"Applicant age ({user_age}) is below minimum requirement of {min_age}.",
                            message_kn=f"ಅರ್ಜಿದಾರರ ವಯಸ್ಸು ({user_age}) ಕನಿಷ್ಠ {min_age} ವರ್ಷಕ್ಕಿಂತ ಕಡಿಮೆಯಿದೆ.",
                        )
                    )
                if max_age is not None and user_age > max_age:
                    is_eligible = False
                    reasons_en.append(f"Maximum age limit is {max_age} years (current age: {user_age}).")
                    reasons_kn.append(f"ಗರಿಷ್ಠ ವಯೋಮಿತಿ {max_age} ವರ್ಷಗಳು (ಪ್ರಸ್ತುತ ವಯಸ್ಸು: {user_age}).")
                    missing_requirements.append(
                        MissingRequirement(
                            field="age",
                            message_en=f"Applicant age ({user_age}) exceeds maximum limit of {max_age}.",
                            message_kn=f"ಅರ್ಜಿದಾರರ ವಯಸ್ಸು ({user_age}) ಗರಿಷ್ಠ {max_age} ವರ್ಷಕ್ಕಿಂತ ಹೆಚ್ಚಾಗಿದೆ.",
                        )
                    )
            except (ValueError, TypeError):
                pass

        # Income check
        max_income = rules.get("max_annual_income")
        if max_income is not None and "annual_income" in answers and answers["annual_income"] is not None:
            try:
                user_income = float(answers["annual_income"])
                if user_income > max_income:
                    is_eligible = False
                    reasons_en.append(f"Annual household income must not exceed ₹{max_income:,.0f} (reported: ₹{user_income:,.0f}).")
                    reasons_kn.append(f"ಕುಟುಂಬದ ವಾರ್ಷಿಕ ಆದಾಯ ₹{max_income:,.0f} ಮೀರಿರಬಾರದು (ದಾಖಲಿಸಿದ ಆದಾಯ: ₹{user_income:,.0f}).")
                    missing_requirements.append(
                        MissingRequirement(
                            field="annual_income",
                            message_en=f"Reported income of ₹{user_income:,.0f} exceeds ceiling of ₹{max_income:,.0f}.",
                            message_kn=f"ದಾಖಲಿಸಿದ ಆದಾಯ ₹{user_income:,.0f} ನಿಗದಿತ ಮಿತಿ ₹{max_income:,.0f} ಕ್ಕಿಂತ ಹೆಚ್ಚಾಗಿದೆ.",
                        )
                    )
            except (ValueError, TypeError):
                pass

        # Land holding check for farmer schemes
        if rules.get("requires_land_ownership"):
            owns_land = answers.get("owns_agricultural_land")
            if owns_land is False or str(owns_land).lower() in ("no", "false"):
                is_eligible = False
                reasons_en.append("Applicant or immediate family must own cultivable agricultural land with RTC / Pahani record.")
                reasons_kn.append("ಅರ್ಜಿದಾರರು ಅಥವಾ ಅವರ ಕುಟುಂಬವು ಪಹಣಿ/RTC ದಾಖಲೆ ಹೊಂದಿರುವ ಕೃಷಿ ಭೂಮಿ ಹೊಂದಿರಬೇಕು.")
                missing_requirements.append(
                    MissingRequirement(
                        field="owns_agricultural_land",
                        message_en="Agricultural land ownership is mandatory for this scheme.",
                        message_kn="ಈ ಯೋಜನೆಗೆ ಕೃಷಿ ಭೂಮಿಯ ಮಾಲೀಕತ್ವ ಕಡ್ಡಾಯವಾಗಿದೆ.",
                    )
                )

        # Student enrolled check
        if rules.get("requires_student_enrollment"):
            is_student = answers.get("is_enrolled_student")
            if is_student is False or str(is_student).lower() in ("no", "false"):
                is_eligible = False
                reasons_en.append("Applicant must be currently enrolled in a recognized school, college, or university.")
                reasons_kn.append("ಅರ್ಜಿದಾರರು ಮಾನ್ಯತೆ ಪಡೆದ ಶಾಲಾ, ಕಾಲೇಜು ಅಥವಾ ವಿಶ್ವವಿದ್ಯಾಲಯದಲ್ಲಿ ಪ್ರಸ್ತುತ ವ್ಯಾಸಂಗ ಮಾಡುತ್ತಿರಬೇಕು.")
                missing_requirements.append(
                    MissingRequirement(
                        field="is_enrolled_student",
                        message_en="Active student enrollment in a recognized institution is mandatory.",
                        message_kn="ಮಾನ್ಯತೆ ಪಡೆದ ಸಂಸ್ಥೆಯಲ್ಲಿ ಸಕ್ರಿಯ ವಿದ್ಯಾರ್ಥಿಯಾಗಿರುವುದು ಕಡ್ಡಾಯವಾಗಿದೆ.",
                    )
                )

        # BPL / Ration Card check if required
        if rules.get("requires_bpl_or_antyodaya"):
            has_ration = answers.get("has_bpl_or_antyodaya_card")
            if has_ration is False or str(has_ration).lower() in ("no", "false"):
                is_eligible = False
                reasons_en.append("Applicant family must possess a valid BPL (Below Poverty Line) or Antyodaya ration card.")
                reasons_kn.append("ಅರ್ಜಿದಾರರ ಕುಟುಂಬವು ಮಾನ್ಯವಾದ ಬಿಪಿಎಲ್ ಅಥವಾ ಅಂತ್ಯೋದಯ ಪಡಿತರ ಚೀಟಿ ಹೊಂದಿರಬೇಕು.")
                missing_requirements.append(
                    MissingRequirement(
                        field="has_bpl_or_antyodaya_card",
                        message_en="Valid BPL or Antyodaya ration card required.",
                        message_kn="ಮಾನ್ಯವಾದ ಬಿಪಿಎಲ್ ಅಥವಾ ಅಂತ್ಯೋದಯ ಪಡಿತರ ಚೀಟಿ ಅಗತ್ಯವಿದೆ.",
                    )
                )

        docs = [DocumentRequirement(**d) for d in doc.get("required_documents", [])]

        if is_eligible:
            return CheckEligibilityResponse(
                scheme_id=doc["id"],
                scheme_name_en=doc["name_en"],
                scheme_name_kn=doc["name_kn"],
                status="eligible",
                status_title_en="Likely Eligible",
                status_title_kn="ಅರ್ಹತೆಯ ಸಾಧ್ಯತೆಯಿದೆ",
                summary_en="Based on your responses, you appear to meet the preliminary eligibility criteria for this scheme.",
                summary_kn="ನಿಮ್ಮ ಪ್ರತಿಕ್ರಿಯೆಗಳ ಆಧಾರದ ಮೇಲೆ, ನೀವು ಈ ಯೋಜನೆಗೆ ಪ್ರಾಥಮಿಕ ಅರ್ಹತಾ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸುತ್ತೀರಿ.",
                reasons_en=[
                    "Your residency, category, and submitted parameters align with the key guidelines of this scheme.",
                    "Review the document checklist below and proceed with your application through the official portal or nearest Grama One centre.",
                ],
                reasons_kn=[
                    "ನಿಮ್ಮ ನಿವಾಸ, ವರ್ಗ ಮತ್ತು ಸಲ್ಲಿಸಿದ ವಿವರಗಳು ಈ ಯೋಜನೆಯ ಮುಖ್ಯ ಮಾರ್ಗಸೂಚಿಗಳಿಗೆ ಅನುಗುಣವಾಗಿವೆ.",
                    "ಕೆಳಗಿನ ದಾಖಲೆಗಳ ಪರಿಶೀಲನಾ ಪಟ್ಟಿಯನ್ನು ಗಮನಿಸಿ, ಅಧಿಕೃತ ತಾಣ ಅಥವಾ ಸಮೀಪದ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರದ ಮೂಲಕ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.",
                ],
                missing_requirements=[],
                document_checklist=docs,
                next_steps_en=[
                    "Gather the original and photocopy sets of all mandatory documents listed below.",
                    "Visit the nearest Grama One or Karnataka One centre or the official government portal.",
                    "Submit your application and keep the acknowledgment / reference slip safe for tracking.",
                ],
                next_steps_kn=[
                    "ಕೆಳಗೆ ಪಟ್ಟಿ ಮಾಡಲಾದ ಎಲ್ಲಾ ಕಡ್ಡಾಯ ದಾಖಲೆಗಳ ಮೂಲ ಮತ್ತು ಜೆರಾಕ್ಸ್ ಪ್ರತಿಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ.",
                    "ಹತ್ತಿರದ ಗ್ರಾಮ ಒನ್ ಅಥವಾ ಕರ್ನಾಟಕ ಒನ್ ಕೇಂದ್ರ ಅಥವಾ ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ಗೆ ಭೇಟಿ ನೀಡಿ.",
                    "ಅರ್ಜಿಯನ್ನು ಸಲ್ಲಿಸಿ ಮತ್ತು ಟ್ರ್ಯಾಕಿಂಗ್‌ಗಾಗಿ ಸ್ವೀಕೃತಿ ರಶೀದಿಯನ್ನು ಸುರಕ್ಷಿತವಾಗಿರಿಸಿಕೊಳ್ಳಿ.",
                ],
                preliminary_notice_en="Preliminary guidance only. Final approval and verification are subject to official government scrutiny.",
                preliminary_notice_kn="ಇದು ಕೇವಲ ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನ. ಅಂತಿಮ ಅನುಮೋದನೆ ಮತ್ತು ಪರಿಶೀಲನೆಯು ಅಧಿಕೃತ ಸರ್ಕಾರಿ ತಪಾಸಣೆಗೆ ಒಳಪಟ್ಟಿರುತ್ತದೆ.",
            )
        else:
            return CheckEligibilityResponse(
                scheme_id=doc["id"],
                scheme_name_en=doc["name_en"],
                scheme_name_kn=doc["name_kn"],
                status="not_eligible",
                status_title_en="Not Eligible at this Time",
                status_title_kn="ಪ್ರಸ್ತುತ ಅರ್ಹತೆ ಇರುವುದಿಲ್ಲ",
                summary_en="Based on the information provided, you do not meet one or more mandatory eligibility requirements.",
                summary_kn="ನೀಡಿದ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ, ನೀವು ಒಂದು ಅಥವಾ ಹೆಚ್ಚಿನ ಕಡ್ಡಾಯ ಅರ್ಹತಾ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸುತ್ತಿಲ್ಲ.",
                reasons_en=reasons_en or ["One or more mandatory requirements were not fulfilled."],
                reasons_kn=reasons_kn or ["ಒಂದು ಅಥವಾ ಹೆಚ್ಚಿನ ಕಡ್ಡಾಯ ಷರತ್ತುಗಳು ಪೂರೈಸಲಾಗಿಲ್ಲ."],
                missing_requirements=missing_requirements,
                document_checklist=docs,
                next_steps_en=[
                    "Review the unmet requirements highlighted above.",
                    "Check other schemes on RuralConnect Karnataka that may better match your profile.",
                    "You may consult your local Grama One operator for clarification on eligibility relaxations.",
                ],
                next_steps_kn=[
                    "ಮೇಲೆ ಉಲ್ಲೇಖಿಸಲಾದ ಪೂರೈಸದ ಷರತ್ತುಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
                    "ನಿಮ್ಮ ವಿವರಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗುವಂತಹ ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕದಲ್ಲಿನ ಇತರ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ.",
                    "ಅರ್ಹತೆಯ ವಿನಾಯಿತಿಗಳ ಸ್ಪಷ್ಟೀಕರಣಕ್ಕಾಗಿ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಗ್ರಾಮ ಒನ್ ಕೇಂದ್ರವನ್ನು ಸಂಪರ್ಕಿಸಬಹುದು.",
                ],
                preliminary_notice_en="Preliminary guidance only. Official decisions are made exclusively by the administering department.",
                preliminary_notice_kn="ಇದು ಕೇವಲ ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನ. ಅಂತಿಮ ನಿರ್ಧಾರಗಳನ್ನು ಆಡಳಿತ ಇಲಾಖೆಯು ಮಾತ್ರ ಕೈಗೊಳ್ಳುತ್ತದೆ.",
            )
