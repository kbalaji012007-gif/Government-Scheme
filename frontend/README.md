# RuralConnect Karnataka - React Frontend

The responsive, bilingual client interface for **RuralConnect Karnataka**, built with React 18, TypeScript, Vite, and Tailwind CSS 4.

---

## Tech Stack

- **Framework:** React 18 & TypeScript
- **Bundler:** Vite 6
- **Styling:** Tailwind CSS 4 (configured with `@tailwindcss/vite` and `@import "tailwindcss";`)
- **Icons:** Lucide React
- **Routing:** React Router v6
- **Testing:** Vitest and React Testing Library

---

## Directory Structure

```text
frontend/
├── public/                  # Static assets and favicon
├── src/
│   ├── assets/              # Logos and media
│   ├── components/
│   │   ├── common/          # Badges, loading skeletons, error & empty states
│   │   ├── layout/          # Responsive Header & Footer
│   │   └── schemes/         # Reusable SchemeCard components
│   ├── contexts/
│   │   ├── LanguageContext  # Bilingual translations (English / ಕನ್ನಡ)
│   │   └── AuthContext      # Citizen login/session management
│   ├── hooks/               # Custom React hooks
│   ├── pages/
│   │   ├── HomePage         # Hero, search, categories, featured, how-it-works
│   │   ├── SchemesPage      # Search, filter pills, pagination
│   │   ├── SchemeDetailPage # Full scheme guidelines, documents, steps
│   │   ├── EligibilityCheckerPage # Multi-step question wizard
│   │   ├── CentersPage      # Grama One & Karnataka One locator
│   │   ├── LoginPage        # Sign in
│   │   ├── RegisterPage     # Registration
│   │   └── NotFoundPage     # 404 handler
│   ├── services/
│   │   └── api.ts           # Centralized typed API client
│   ├── test/                # Automated Vitest test suite
│   ├── types/               # TypeScript interfaces matching backend models
│   ├── App.tsx              # Application route definition
│   ├── main.tsx             # Entry point
│   ├── index.css            # Tailwind CSS 4 setup
│   └── vite-env.d.ts        # Vite environment types
├── .env.example             # Example frontend environment variables
├── package.json             # Pinned frontend dependencies
├── tsconfig.json            # Strict TypeScript configuration
├── vite.config.ts           # Tailwind CSS 4 Vite plugin configuration
└── README.md
```

---

## Setup & Running (Windows PowerShell)

```powershell
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the Vite development server
npm run dev
```

The frontend will start at: `http://127.0.0.1:5173`

---

## Running Frontend Tests & Production Build

```powershell
# Run Vitest test suite
npm test

# Build production bundle
npm run build
```
