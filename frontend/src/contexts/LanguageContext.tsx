import React, { createContext, useContext, useState, useEffect } from 'react';

export type Language = 'en' | 'kn';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const translations: Record<Language, Record<string, string>> = {
  en: {
    // Navigation & Brand
    brandName: 'RuralConnect Karnataka',
    brandTagline: 'Discover government schemes, understand eligibility, and find the support you need.',
    navHome: 'Home',
    navSchemes: 'Browse Schemes',
    navEligibility: 'Check Eligibility',
    navCenters: 'Find Service Centres',
    navLogin: 'Login',
    navRegister: 'Register',
    navLogout: 'Logout',
    navProfile: 'My Profile',

    // Hero
    heroHeadline: "Find the Government Schemes You're Eligible For",
    heroSubtitle: 'Explore welfare schemes, understand eligibility, prepare documents, and discover nearby service centres.',
    searchPlaceholder: 'Search schemes (e.g. Raitha Siri, Gruha Lakshmi, scholarship)...',
    btnSearch: 'Search Schemes',
    btnBrowseSchemes: 'Browse All Schemes',
    btnCheckEligibility: 'Check Eligibility',

    // Beneficiary Categories
    categoriesTitle: 'Browse by Beneficiary',
    categoriesSubtitle: 'Select your category to discover tailored state and central welfare programs.',
    catFarmers: 'Farmers',
    catFarmersDesc: 'Agricultural subsidies, crop insurance, equipment loans, and soil health welfare.',
    catStudents: 'Students',
    catStudentsDesc: 'Pre-matric & post-matric scholarships, fee concessions, and hostel admissions.',
    catWomen: 'Women',
    catWomenDesc: 'Financial assistance, self-help group revolving funds, and maternal nutrition benefits.',
    catOther: 'Other Beneficiaries',
    catOtherDesc: 'Senior citizens, rural families, artisans, weavers, and social security programs.',

    // Featured Schemes
    featuredTitle: 'Featured Government Schemes',
    featuredSubtitle: 'Actively sanctioned schemes with verified Karnataka guidelines and DBT support.',
    viewDetails: 'View Details',
    checkEligibilityBtn: 'Check Eligibility',
    noSchemesFound: 'No schemes match your selected search criteria.',
    clearFilters: 'Clear Filters',
    allCategories: 'All Categories',
    allBeneficiaries: 'All Beneficiaries',

    // How It Works
    howItWorksTitle: 'How RuralConnect Helps You',
    howItWorksSubtitle: 'Three simple steps to access citizen welfare programs with confidence.',
    step1Title: '1. Find a Scheme',
    step1Desc: 'Search by beneficiary category, sector, or keyword to find relevant Karnataka welfare initiatives.',
    step2Title: '2. Check Eligibility',
    step2Desc: 'Answer a few simple questions in Kannada or English to see your preliminary eligibility status.',
    step3Title: '3. Prepare & Apply',
    step3Desc: 'Follow the document checklist and locate nearby Grama One or Karnataka One centres for assistance.',

    // Service Centres Promo
    centersPromoTitle: 'Need Assistance? Visit a Government Service Centre',
    centersPromoDesc: 'Get free in-person guidance on document preparation and scheme application at your local Grama One or Karnataka One office.',
    btnFindCentres: 'Find Nearby Centres',

    // Trust & Accessibility
    trustTitle: 'Trust & Transparent Accessibility',
    trustDesc: 'RuralConnect Karnataka empowers citizens with verified public information and simplified questionnaires. Our goal is to bridge the rural digital divide so no eligible family misses government support.',

    // Scheme Details Page
    schemeDetails: 'Scheme Overview',
    keyBenefits: 'Key Scheme Benefits',
    eligibleBeneficiaries: 'Eligible Beneficiaries',
    eligibilityConditions: 'Official Eligibility Conditions',
    requiredDocuments: 'Required Documents Checklist',
    mandatoryDoc: 'Mandatory',
    optionalDoc: 'Optional',
    applicationProcess: 'Step-by-Step Application Process',
    officialPortal: 'Official Application Portal',
    lastVerifiedDate: 'Last Verified Date',
    backToSchemes: 'Back to Schemes',
    officialPortalNotice: 'Apply on Verified Government Portal',

    // Eligibility Checker
    eligibilityTitle: 'Eligibility Self-Check',
    eligibilityIntro: 'Answer the preliminary questions below to check whether you meet the basic conditions for this scheme.',
    questionProgress: 'Question {current} of {total}',
    btnBack: 'Back',
    btnContinue: 'Continue',
    btnReview: 'Review Answers',
    btnSubmitCheck: 'Evaluate Eligibility',
    reviewAnswersTitle: 'Review Your Answers Before Evaluation',
    editAnswer: 'Edit',
    evaluatingText: 'Checking your responses against official criteria...',
    eligibleTitle: 'Preliminary Assessment: Likely Eligible',
    notEligibleTitle: 'Preliminary Assessment: Not Eligible at this Time',
    moreInfoTitle: 'Preliminary Assessment: More Information Required',
    unmetRequirementsTitle: 'Unmet Conditions or Missing Criteria',
    documentChecklistTitle: 'Recommended Document Checklist',
    nextStepsTitle: 'Recommended Next Steps',
    recheckBtn: 'Check Again',
    viewSchemeDetailsBtn: 'Return to Scheme Details',

    // Centres Locator Page
    centersPageTitle: 'Government Service Centre Locator',
    centersPageSubtitle: 'Locate authorized Grama One, Bangalore One, Karnataka One, and Bapuji Seva Kendras across Karnataka districts.',
    searchCentersPlaceholder: 'Search by centre name, taluk, or village...',
    filterDistrict: 'Filter by District',
    filterTaluk: 'Filter by Taluk',
    filterType: 'Centre Type',
    allDistricts: 'All Districts',
    allTaluks: 'All Taluks',
    allTypes: 'All Types',
    operatingHours: 'Operating Hours',
    phone: 'Phone',
    email: 'Email',
    getDirections: 'Get Directions (Google Maps)',
    noCentersFound: 'No service centres found matching your filter selections.',

    // Auth
    loginTitle: 'Citizen Sign In',
    loginSubtitle: 'Sign in to save your discovered schemes and track eligibility checks.',
    registerTitle: 'Create Citizen Account',
    registerSubtitle: 'Register for personalized scheme discovery across Karnataka.',
    emailLabel: 'Email Address',
    passwordLabel: 'Password',
    fullNameLabel: 'Full Name',
    preferredLangLabel: 'Preferred Language',
    signInBtn: 'Sign In',
    signUpBtn: 'Create Account',
    alreadyHaveAccount: 'Already have an account? Sign in',
    dontHaveAccount: "Don't have an account? Register now",

    // Disclaimers & Footer
    disclaimerBadge: 'Public Advisory',
    disclaimerText: 'RuralConnect Karnataka provides preliminary eligibility discovery guidance based on publicly available department rules. It is not an official government portal and does not guarantee government sanction or approval.',
    footerAbout: 'About RuralConnect',
    footerAboutDesc: 'A community-focused discovery initiative helping Karnataka citizens find welfare schemes and nearby service centres.',
    footerQuickLinks: 'Quick Links',
    footerServices: 'Citizen Services',
    footerAccessibility: 'Accessibility & Contrast',
    footerPrivacy: 'Privacy Policy',
    footerDisclaimer: 'Official Disclaimer',
    copyright: 'RuralConnect Karnataka. Informational public discovery initiative.',
  },
  kn: {
    // Navigation & Brand
    brandName: 'ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕ',
    brandTagline: 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ, ಅರ್ಹತೆ ತಿಳಿಯಿರಿ ಮತ್ತು ಅಗತ್ಯ ನೆರವು ಪಡೆಯಿರಿ.',
    navHome: 'ಮುಖಪುಟ',
    navSchemes: 'ಯೋಜನೆಗಳ ಪಟ್ಟಿ',
    navEligibility: 'ಅರ್ಹತೆ ಪರಿಶೀಲನೆ',
    navCenters: 'ಸೇವಾ ಕೇಂದ್ರಗಳು',
    navLogin: 'ಲಾಗಿನ್',
    navRegister: 'ನೋಂದಣಿ',
    navLogout: 'ನಿರ್ಗಮನ',
    navProfile: 'ನನ್ನ ವಿವರ',

    // Hero
    heroHeadline: 'ನೀವು ಅರ್ಹರಾಗಿರುವ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಸುಲಭವಾಗಿ ಕಂಡುಕೊಳ್ಳಿ',
    heroSubtitle: 'ಕಲ್ಯಾಣ ಯೋಜನೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ, ಅರ್ಹತಾ ನಿಯಮಗಳನ್ನು ತಿಳಿಯಿರಿ, ಅಗತ್ಯ ದಾಖಲೆಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಿ ಮತ್ತು ಸಮೀಪದ ಸೇವಾ ಕೇಂದ್ರಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಿ.',
    searchPlaceholder: 'ಯೋಜನೆಗಳ ಹೆಸರು ಹುಡುಕಿ (ಉದಾ: ರೈತ ಸಿರಿ, ಗೃಹ ಲಕ್ಷ್ಮಿ, ವಿದ್ಯಾರ್ಥಿವೇತನ)...',
    btnSearch: 'ಹುಡುಕಿ',
    btnBrowseSchemes: 'ಎಲ್ಲಾ ಯೋಜನೆಗಳು',
    btnCheckEligibility: 'ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ',

    // Beneficiary Categories
    categoriesTitle: 'ಫಲಾನುಭವಿ ವರ್ಗಗಳ ಆಧಾರದ ಮೇಲೆ ಹುಡುಕಿ',
    categoriesSubtitle: 'ನಿಮ್ಮ ವರ್ಗವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು ಅದಕ್ಕೆ ಸೂಕ್ತವಾದ ಸರ್ಕಾರಿ ಕಾರ್ಯಕ್ರಮಗಳನ್ನು ಅನ್ವೇಷಿಸಿ.',
    catFarmers: 'ರೈತರು',
    catFarmersDesc: 'ಕೃಷಿ ಸಹಾಯಧನ, ಬೆಳೆ ವಿಮೆ, ಯಂತ್ರೋಪಕರಣ ಸಾಲ ಮತ್ತು ಭೂಮಿ ಸಂರಕ್ಷಣೆ ಯೋಜನೆಗಳು.',
    catStudents: 'ವಿದ್ಯಾರ್ಥಿಗಳು',
    catStudentsDesc: 'ಪೂರ್ವ ಮೆಟ್ರಿಕ್ ಮತ್ತು ಮೆಟ್ರಿಕ್ ನಂತರದ ವಿದ್ಯಾರ್ಥಿವೇತನಗಳು ಹಾಗೂ ವಸತಿ ನಿಲಯ ಸೌಲಭ್ಯಗಳು.',
    catWomen: 'ಮಹಿಳೆಯರು',
    catWomenDesc: 'ಗೃಹ ಲಕ್ಷ್ಮಿ, ಸ್ತ್ರೀ ಶಕ್ತಿ ಸಂಘಗಳ ನೆರವು, ಮಾತೃಪೂರ್ಣ ಮತ್ತು ಮಹಿಳಾ ಸಬಲೀಕರಣ ಯೋಜನೆಗಳು.',
    catOther: 'ಇತರ ಫಲಾನುಭವಿಗಳು',
    catOtherDesc: 'ಹಿರಿಯ ನಾಗರಿಕರು, ಗ್ರಾಮೀಣ ಕುಟುಂಬಗಳು, ಕುಶಲಕರ್ಮಿಗಳು ಮತ್ತು ಸಾಮಾಜಿಕ ಭದ್ರತಾ ಯೋಜನೆಗಳು.',

    // Featured Schemes
    featuredTitle: 'ಪ್ರಮುಖ ಸರ್ಕಾರಿ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು',
    featuredSubtitle: 'ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಅಧಿಕೃತ ಮಾರ್ಗಸೂಚಿಗಳು ಮತ್ತು ನೇರ ನಗದು (DBT) ಹೊಂದಿರುವ ಯೋಜನೆಗಳು.',
    viewDetails: 'ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ',
    checkEligibilityBtn: 'ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ',
    noSchemesFound: 'ನಿಮ್ಮ ಹುಡುಕಾಟಕ್ಕೆ ಹೊಂದಿಕೆಯಾಗುವ ಯಾವುದೇ ಯೋಜನೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ.',
    clearFilters: 'ಫಿಲ್ಟರ್ ತೆರವುಗೊಳಿಸಿ',
    allCategories: 'ಎಲ್ಲಾ ವರ್ಗಗಳು',
    allBeneficiaries: 'ಎಲ್ಲಾ ಫಲಾನುಭವಿಗಳು',

    // How It Works
    howItWorksTitle: 'ರೂರಲ್ ಕನೆಕ್ಟ್ ಹೇಗೆ ನೆರವಾಗುತ್ತದೆ?',
    howItWorksSubtitle: 'ಸರ್ಕಾರಿ ಸೌಲಭ್ಯಗಳನ್ನು ವಿಶ್ವಾಸದಿಂದ ಪಡೆದುಕೊಳ್ಳಲು ಮೂರು ಸರಳ ಹಂತಗಳು.',
    step1Title: '1. ಯೋಜನೆಯನ್ನು ಹುಡುಕಿ',
    step1Desc: 'ನಿಮ್ಮ ವರ್ಗ, ಅಗತ್ಯತೆ ಅಥವಾ ಕೀವರ್ಡ್ ಬಳಸಿ ನಿಮಗೆ ಸೂಕ್ತವಾದ ಕರ್ನಾಟಕ ಕಲ್ಯಾಣ ಯೋಜನೆಯನ್ನು ಹುಡುಕಿ.',
    step2Title: '2. ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ',
    step2Desc: 'ಕನ್ನಡ ಅಥವಾ ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಕೆಲವೇ ಸರಳ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ ಪ್ರಾಥಮಿಕ ಅರ್ಹತೆಯನ್ನು ತಿಳಿಯಿರಿ.',
    step3Title: '3. ದಾಖಲೆ ಸಿದ್ಧಪಡಿಸಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ',
    step3Desc: 'ದಾಖಲೆಗಳ ಪಟ್ಟಿಯನ್ನು ನೋಡಿ ಹತ್ತಿರದ ಗ್ರಾಮ ಒನ್ ಅಥವಾ ಕರ್ನಾಟಕ ಒನ್ ಕೇಂದ್ರದ ಮೂಲಕ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ.',

    // Service Centres Promo
    centersPromoTitle: 'ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ನೆರವು ಬೇಕೇ? ಸೇವಾ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಿ',
    centersPromoDesc: 'ದಾಖಲೆಗಳ ತಯಾರಿ ಮತ್ತು ಅರ್ಜಿ ಸಲ್ಲಿಕೆಗೆ ನಿಮ್ಮ ಹತ್ತಿರದ ಗ್ರಾಮ ಒನ್ ಅಥವಾ ಕರ್ನಾಟಕ ಒನ್ ಕಚೇರಿಯಲ್ಲಿ ಉಚಿತ ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ.',
    btnFindCentres: 'ಸಮೀಪದ ಕೇಂದ್ರಗಳನ್ನು ಹುಡುಕಿ',

    // Trust & Accessibility
    trustTitle: 'ವಿಶ್ವಾಸಾರ್ಹತೆ ಮತ್ತು ಪಾರದರ್ಶಕತೆ',
    trustDesc: 'ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕವು ಅಧಿಕೃತ ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿಯನ್ನು ಸರಳೀಕರಿಸಿ ಒದಗಿಸುತ್ತದೆ. ಯಾವುದೇ ಅರ್ಹ ಕುಟುಂಬವು ಸರ್ಕಾರಿ ನೆರವಿನಿಂದ ವಂಚಿತವಾಗಬಾರದು ಎಂಬುದು ನಮ್ಮ ಆಶಯ.',

    // Scheme Details Page
    schemeDetails: 'ಯೋಜನೆಯ ವಿವರ',
    keyBenefits: 'ಯೋಜನೆಯಿಂದ ಸಿಗುವ ಪ್ರಮುಖ ಲಾಭಗಳು',
    eligibleBeneficiaries: 'ಅರ್ಹ ಫಲಾನುಭವಿಗಳು',
    eligibilityConditions: 'ಅಧಿಕೃತ ಅರ್ಹತಾ ಷರತ್ತುಗಳು',
    requiredDocuments: 'ಅಗತ್ಯ ದಾಖಲೆಗಳ ಪರಿಶೀಲನಾ ಪಟ್ಟಿ',
    mandatoryDoc: 'ಕಡ್ಡಾಯ',
    optionalDoc: 'ಐಚ್ಛಿಕ',
    applicationProcess: 'ಹಂತ-ಹಂತದ ಅರ್ಜಿ ಸಲ್ಲಿಕೆ ಪ್ರಕ್ರಿಯೆ',
    officialPortal: 'ಅಧಿಕೃತ ಅರ್ಜಿ ಪೋರ್ಟಲ್',
    lastVerifiedDate: 'ಕೊನೆಯ ಪರಿಶೀಲನೆ ದಿನಾಂಕ',
    backToSchemes: 'ಯೋಜನೆಗಳ ಪಟ್ಟಿಗೆ ಹಿಂತಿರುಗಿ',
    officialPortalNotice: 'ಅಧಿಕೃತ ಸರ್ಕಾರಿ ತಾಣದಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ',

    // Eligibility Checker
    eligibilityTitle: 'ಸ್ವಯಂ ಅರ್ಹತಾ ಪರಿಶೀಲನೆ',
    eligibilityIntro: 'ಈ ಯೋಜನೆಗೆ ನೀವು ಪ್ರಾಥಮಿಕ ಅರ್ಹತಾ ಷರತ್ತುಗಳನ್ನು ಪೂರೈಸುತ್ತೀರಾ ಎಂದು ತಿಳಿಯಲು ಕೆಳಗಿನ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ.',
    questionProgress: 'ಪ್ರಶ್ನೆ {current} / {total}',
    btnBack: 'ಹಿಂದೆ',
    btnContinue: 'ಮುಂದುವರಿಯಿರಿ',
    btnReview: 'ಉತ್ತರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ',
    btnSubmitCheck: 'ಅರ್ಹತೆ ಪರೀಕ್ಷಿಸಿ',
    reviewAnswersTitle: 'ಅಂತಿಮ ಮೌಲ್ಯಮಾಪನಕ್ಕೂ ಮುನ್ನ ನಿಮ್ಮ ಉತ್ತರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ',
    editAnswer: 'ತಿದ್ದುಪಡಿ',
    evaluatingText: 'ಅಧಿಕೃತ ನಿಯಮಗಳೊಂದಿಗೆ ನಿಮ್ಮ ಉತ್ತರಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...',
    eligibleTitle: 'ಪ್ರಾಥಮಿಕ ಮೌಲ್ಯಮಾಪನ: ಅರ್ಹತೆಯ ಸಾಧ್ಯತೆಯಿದೆ',
    notEligibleTitle: 'ಪ್ರಾಥಮಿಕ ಮೌಲ್ಯಮಾಪನ: ಪ್ರಸ್ತುತ ಅರ್ಹತೆ ಇರುವುದಿಲ್ಲ',
    moreInfoTitle: 'ಪ್ರಾಥಮಿಕ ಮೌಲ್ಯಮಾಪನ: ಹೆಚ್ಚಿನ ಮಾಹಿತಿ ಅಗತ್ಯವಿದೆ',
    unmetRequirementsTitle: 'ಪೂರೈಸದ ಷರತ್ತುಗಳು ಅಥವಾ ಕೊರತೆಗಳು',
    documentChecklistTitle: 'ಶಿಫಾರಸು ಮಾಡಿದ ದಾಖಲೆಗಳ ಪರಿಶೀಲನಾ ಪಟ್ಟಿ',
    nextStepsTitle: 'ಮುಂದಿನ ಶಿಫಾರಸು ಹಂತಗಳು',
    recheckBtn: 'ಮತ್ತೊಮ್ಮೆ ಪರಿಶೀಲಿಸಿ',
    viewSchemeDetailsBtn: 'ಯೋಜನೆಯ ವಿವರಗಳಿಗೆ ಹಿಂತಿರುಗಿ',

    // Centres Locator Page
    centersPageTitle: 'ಸರ್ಕಾರಿ ಸೇವಾ ಕೇಂದ್ರಗಳ ಪತ್ತೆ',
    centersPageSubtitle: 'ಕರ್ನಾಟಕದ ಜಿಲ್ಲೆಗಳಲ್ಲಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿರುವ ಗ್ರಾಮ ಒನ್, ಬೆಂಗಳೂರು ಒನ್, ಕರ್ನಾಟಕ ಒನ್ ಮತ್ತು ಬಾಪೂಜಿ ಸೇವಾ ಕೇಂದ್ರಗಳನ್ನು ಹುಡುಕಿ.',
    searchCentersPlaceholder: 'ಕೇಂದ್ರದ ಹೆಸರು, ತಾಲೂಕು ಅಥವಾ ಗ್ರಾಮದ ಹೆಸರಿನಿಂದ ಹುಡುಕಿ...',
    filterDistrict: 'ಜಿಲ್ಲೆಯ ಮೂಲಕ ಫಿಲ್ಟರ್',
    filterTaluk: 'ತಾಲೂಕಿನ ಮೂಲಕ ಫಿಲ್ಟರ್',
    filterType: 'ಕೇಂದ್ರದ ವಿಧ',
    allDistricts: 'ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು',
    allTaluks: 'ಎಲ್ಲಾ ತಾಲೂಕುಗಳು',
    allTypes: 'ಎಲ್ಲಾ ವಿಧಗಳು',
    operatingHours: 'ಕಾರ್ಯನಿರ್ವಹಣೆ ಸಮಯ',
    phone: 'ದೂರವಾಣಿ',
    email: 'ಇಮೇಲ್',
    getDirections: 'ದಿಕ್ಕುಗಳನ್ನು ವೀಕ್ಷಿಸಿ (Google Maps)',
    noCentersFound: 'ನೀವು ಆಯ್ಕೆ ಮಾಡಿದ ಫಿಲ್ಟರ್‌ಗೆ ಯಾವುದೇ ಸೇವಾ ಕೇಂದ್ರಗಳು ಕಂಡುಬಂದಿಲ್ಲ.',

    // Auth
    loginTitle: 'ನಾಗರಿಕರ ಲಾಗಿನ್',
    loginSubtitle: 'ನಿಮ್ಮ ಯೋಜನೆಗಳನ್ನು ಉಳಿಸಲು ಮತ್ತು ಅರ್ಹತಾ ಫಲಿತಾಂಶಗಳನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಲು ಲಾಗಿನ್ ಆಗಿ.',
    registerTitle: 'ಹೊಸ ಖಾತೆ ರಚಿಸಿ',
    registerSubtitle: 'ಕರ್ನಾಟಕದಾದ್ಯಂತ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳನ್ನು ಕಂಡುಕೊಳ್ಳಲು ನೋಂದಾಯಿಸಿಕೊಳ್ಳಿ.',
    emailLabel: 'ಇಮೇಲ್ ವಿಳಾಸ',
    passwordLabel: 'ಗುಪ್ತಪದ (Password)',
    fullNameLabel: 'ಪೂರ್ಣ ಹೆಸರು',
    preferredLangLabel: 'ಆದ್ಯತೆಯ ಭಾಷೆ',
    signInBtn: 'ಸೈನ್ ಇನ್',
    signUpBtn: 'ಖಾತೆ ತೆರೆಯಿರಿ',
    alreadyHaveAccount: 'ಈಗಾಗಲೇ ಖಾತೆ ಇದೆಯೇ? ಲಾಗಿನ್ ಆಗಿ',
    dontHaveAccount: 'ಖಾತೆ ಇಲ್ಲವೇ? ಹೊಸದಾಗಿ ನೋಂದಾಯಿಸಿ',

    // Disclaimers & Footer
    disclaimerBadge: 'ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿ ಪ್ರಕಟಣೆ',
    disclaimerText: 'ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕವು ಸಾರ್ವಜನಿಕ ಇಲಾಖಾ ನಿಯಮಗಳ ಆಧಾರದ ಮೇಲೆ ಕೇವಲ ಪ್ರಾಥಮಿಕ ಅರ್ಹತಾ ಮಾರ್ಗದರ್ಶನ ನೀಡುತ್ತದೆ. ಇದು ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಅಲ್ಲ ಮತ್ತು ಸರ್ಕಾರದ ಅಂತಿಮ ಮಂಜೂರಾತಿಯನ್ನು ಖಾತರಿಪಡಿಸುವುದಿಲ್ಲ.',
    footerAbout: 'ರೂರಲ್ ಕನೆಕ್ಟ್ ಬಗ್ಗೆ',
    footerAboutDesc: 'ಗ್ರಾಮೀಣ ಕರ್ನಾಟಕದ ನಿವಾಸಿಗಳಿಗೆ ಸರ್ಕಾರಿ ಕಲ್ಯಾಣ ಯೋಜನೆಗಳು ಮತ್ತು ಸೇವಾ ಕೇಂದ್ರಗಳ ವಿವರ ಒದಗಿಸುವ ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿ ವೇದಿಕೆ.',
    footerQuickLinks: 'ತ್ವರಿತ ಲಿಂಕ್‌ಗಳು',
    footerServices: 'ನಾಗರಿಕ ಸೇವೆಗಳು',
    footerAccessibility: 'ಪ್ರವೇಶಿಸುವಿಕೆ ಮತ್ತು ಸ್ಪಷ್ಟತೆ',
    footerPrivacy: 'ಗೌಪ್ಯತೆ ನೀತಿ',
    footerDisclaimer: 'ಅಧಿಕೃತ ಹಕ್ಕುತ್ಯಾಗ',
    copyright: 'ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕ. ಸಾರ್ವಜನಿಕ ಮಾಹಿತಿ ಜಾಗೃತಿ ವೇದಿಕೆ.',
  },
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    const saved = localStorage.getItem('ruralconnect_language');
    return saved === 'kn' ? 'kn' : 'en';
  });

  const setLanguage = (lang: Language) => {
    setLanguageState(lang);
    localStorage.setItem('ruralconnect_language', lang);
  };

  const t = (key: string): string => {
    return translations[language][key] || translations['en'][key] || key;
  };

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
