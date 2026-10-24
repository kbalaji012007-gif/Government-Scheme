# RuralConnect Karnataka (ರೂರಲ್ ಕನೆಕ್ಟ್ ಕರ್ನಾಟಕ)
### Full-Stack Government Scheme Discovery and Accessibility Platform

> "Discover government schemes, understand eligibility, and find the support you need."

RuralConnect Karnataka is an accessible, bilingual (Kannada & English) discovery platform designed to help rural residents of Karnataka—including farmers, students, women, senior citizens, and rural families—discover government welfare programs, understand qualification conditions, identify required documents, and locate nearby authorized government service centres (such as Grama One, Karnataka One, and Bapuji Seva Kendras).

---

## 1. System Architecture

```mermaid
flowchart TD
    subgraph Client ["Frontend (React 18 + Vite + Tailwind CSS 4)"]
        UI[Responsive Layout & Navigation]
        I18n["Language Context (English / ಕನ್ನಡ)"]
        AuthCtx[Auth Context + LocalStorage JWT]
        APIClient[Centralized Typed API Client]
        
        UI --> HomePage[Homepage with Hero & Working Search]
        UI --> SchemeBrowse[Browse Schemes with Category Filters]
        UI --> SchemeDetail[Scheme Details, Documents & Steps]
        UI --> EligibilityChecker[Multi-Step Question Wizard & Review]
        UI --> ServiceCenters[Service Centre Locator & Maps]
        UI --> AuthPages[Citizen Login & Registration]
        
        HomePage --> APIClient
        SchemeBrowse --> APIClient
        SchemeDetail --> APIClient
        EligibilityChecker --> APIClient
        ServiceCenters --> APIClient
        AuthPages --> APIClient
    end

    subgraph Server ["FastAPI Backend (Python 3.12 + Pydantic v2)"]
        FastAPIServer[FastAPI Application Gateway]
        Security[bcrypt Passwords & HS256 JWT]
        
        RouterHealth["/api/v1/health"]
        RouterCategories["/api/v1/categories"]
        RouterSchemes["/api/v1/schemes"]
        RouterEligibility["/api/v1/schemes/{id}/check-eligibility"]
        RouterCenters["/api/v1/centers"]
        RouterAuth["/api/v1/auth"]
        
        FastAPIServer --> RouterHealth
        FastAPIServer --> RouterCategories
        FastAPIServer --> RouterSchemes
        FastAPIServer --> RouterEligibility
        FastAPIServer --> RouterCenters
        FastAPIServer --> RouterAuth
        
        Services[Scheme, Eligibility & Center Services]
        Repo[MongoDB Repositories]
        
        RouterSchemes --> Services
        RouterEligibility --> Services
        RouterCenters --> Services
        RouterAuth --> Security
        Services --> Repo
    end

    subgraph DataStore ["Database Layer (MongoDB)"]
        DBConn[PyMongo Client & Connection Manager]
        Collections[("schemes", "centers", "users")]
        FallbackMock["Resilient In-Process Mock Fallback"]
        
        Repo --> DBConn
        DBConn -->|Online| Collections
        DBConn -.->|Offline Fallback| FallbackMock
    end

    APIClient -->|REST JSON over HTTP| FastAPIServer
```

---

## 2. Core Features

1. **Bilingual Experience (English & ಕನ್ನಡ)**:
   - Full client-side toggle switching navigation, instructions, badges, empty states, and errors.
   - Scheme records and service centre details provided with rich Kannada and English titles, descriptions, and instructions.
2. **Hero Search & Filtering**:
   - Working search input supporting keyword matching, category tags, and beneficiary types.
   - 4 primary category shortcuts: Farmers, Students, Women, and Other Beneficiaries.
3. **Scheme Discovery & Details**:
   - Comprehensive guidelines, key benefits, and eligibility criteria.
   - Document checklist distinguishing mandatory versus optional documentation.
   - Step-by-step application walkthrough with official links and verification timestamps.
4. **Step-by-Step Eligibility Wizard**:
   - One question at a time workflow with progress tracking.
   - Supports Boolean (Yes/No), Number (Age, Income), and Select inputs.
   - Answer review screen before final evaluation.
   - Backend-driven evaluation returning clear preliminary status (`Likely Eligible`, `Not Eligible`, `More Information Required`), specific unmet reasons, missing requirements, and next steps.
5. **Service Centre Locator**:
   - Directory of Grama One, Karnataka One, Bangalore One, and Bapuji Seva Kendras across Karnataka districts.
   - Filter by district, taluk, and centre type.
   - Real addresses, phone contacts, operating hours, and Google Maps direction links.
6. **Authentication & Security**:
   - Secure registration and login with bcrypt password hashing and signed JWT tokens.
   - CORS restricted to local frontend origin.
7. **Public Advisory & Disclaimers**:
   - Prominently informs citizens that assessments are preliminary guidance and official decisions rest with administering departments.

---

## 3. Technology Stack

### Frontend:
- **React:** 18.3.1
- **TypeScript:** 5.6.3
- **Vite:** 6.4.5
- **Tailwind CSS 4:** Modern setup with `@tailwindcss/vite` and `@import "tailwindcss";` (no legacy PostCSS or v3 directives)
- **Icons:** Lucide React
- **Routing:** React Router v6
- **Testing:** Vitest 2.1.8 & React Testing Library

### Backend:
- **Python:** 3.11+ (verified on Python 3.12.10)
- **FastAPI:** 0.115+
- **Server:** Uvicorn 0.32+
- **Validation:** Pydantic v2 & Pydantic-Settings
- **Database Driver:** PyMongo 4.10+ (with transparent mongomock fallback)
- **Security:** bcrypt 5.0+ and PyJWT 2.15+
- **Testing:** pytest 9.1+, pytest-asyncio, and HTTPX

---

## 4. Folder Structure

```text
ruralconnect-karnataka/
├── frontend/
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── common/         # Badges, LoadingSpinner, Skeleton, ErrorMessage, EmptyState
│   │   │   ├── layout/         # Header (bilingual, responsive drawer), Footer
│   │   │   └── schemes/        # Reusable SchemeCard component
│   │   ├── contexts/           # LanguageContext (EN/KN), AuthContext (JWT session)
│   │   ├── hooks/
│   │   ├── pages/              # Home, Schemes, SchemeDetail, Eligibility, Centers, Login, Register, 404
│   │   ├── services/           # api.ts (Centralized typed API client)
│   │   ├── test/               # Vitest test files
│   │   ├── types/              # TypeScript models matching backend contracts
│   │   ├── utils/
│   │   ├── App.tsx             # Routing configuration
│   │   ├── main.tsx            # React root
│   │   ├── index.css           # Tailwind CSS 4 styles
│   │   └── vite-env.d.ts
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── core/               # config.py (Settings), security.py (bcrypt & JWT)
│   │   ├── db/                 # mongodb.py (Connection manager & indexes)
│   │   ├── models/             # Domain schemas
│   │   ├── repositories/       # Scheme, Center, and User data access
│   │   ├── routers/            # Health, Categories, Schemes, Centers, Auth
│   │   ├── schemas/            # Pydantic v2 schemas
│   │   ├── services/           # Business logic & eligibility evaluator
│   │   ├── utils/              # Pagination helpers
│   │   └── main.py             # FastAPI entrypoint & middleware
│   ├── scripts/
│   │   └── seed_data.py        # Idempotent development seed script
│   ├── tests/                  # Pytest automated test suite
│   ├── .env.example
│   ├── pytest.ini
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
└── README.md
```

---

## 5. Getting Started (Windows PowerShell Commands)

### Step 1: Clone / Enter the Repository
```powershell
cd "C:\Users\NAVEEN ASUNDI\.gemini\antigravity\scratch\ruralconnect-karnataka"
```

### Step 2: Backend Setup & Execution
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run database seed (auto-seeds on startup if empty as well)
python scripts\seed_data.py

# Run the FastAPI server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- API Base URL: `http://127.0.0.1:8000/api/v1`
- Swagger Interactive Documentation: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/v1/health`

### Step 3: Frontend Setup & Execution (in a separate terminal)
```powershell
# Navigate to frontend directory
cd frontend

# Install packages
npm install

# Start Vite development server
npm run dev
```
- Frontend Web App: `http://127.0.0.1:5173`

---

## 6. Running Automated Tests

### Backend Test Suite (Pytest)
```powershell
cd backend
.\.venv\Scripts\pytest.exe -v tests
```
- Total tests: 19 passed (Health check, Scheme listing, Category filter, Text search, Pagination, Scheme details, Documents, Eligibility questions, Qualified assessment, Disqualified assessment, Missing mandatory validation, Service centres directory, District filter, Registration, Duplicate rejection, Login authentication, Invalid password rejection).

### Frontend Test Suite (Vitest)
```powershell
cd frontend
npm test
```
- Component unit & integration tests covering navigation, bilingual language switching, SchemeCard rendering, and homepage controls.

### Production Build Verification
```powershell
cd frontend
npm run build
```
- Compiles TypeScript and packages Tailwind CSS 4 assets with zero errors.

---

## 7. Sample Test Credentials

- **Email:** `citizen@ruralconnect.karnataka.gov.in`
- **Password:** `Karnataka@2026`

---

## 8. Disclaimer

RuralConnect Karnataka is an independent informational discovery platform created to assist rural beneficiaries. This application is not an official government portal. Final approval and verification for all welfare programs are conducted exclusively by designated government departments and authorized authorities.
