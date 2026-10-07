# CyberGuard — Comprehensive UI/UX Audit & Architectural Evaluation

**Date:** September 25, 2026  
**Auditor:** Senior Product Designer & Frontend Architect  
**Application:** CyberGuard — Multilingual Explainable Cyberbullying Detection and Support System  
**Frontend Stack:** React 18, Vite 5, Tailwind CSS / Vanilla CSS Variables, Lucide React (0.292.0)  

---

## 1. Executive Summary

CyberGuard's frontend provides a solid functional baseline connecting to real FastAPI backend endpoints (`/auth`, `/analyze`, `/incidents`, `/reports`, `/support`, `/admin`). Every feature—from screenshot OCR extraction to SHAP token attribution, forensic PDF downloading, and RAG-grounded support chat—has a live API contract and working data flow.

However, from a **product design, UI/UX consistency, visual hierarchy, responsiveness, and accessibility** standpoint, the existing frontend exhibits critical structural shortcomings:
- **Inconsistent Navigation:** The current `Navbar.jsx` uses non-standard emojis (`⚡`, `🔍`, `💬`, `🛡️`, `📄`, `🤝`, `🚨`, `⚙️`, `📋`), lacks collapsible sidebar capability, overflows on desktop with 9 tabs, and hides navigation completely on mobile (`hidden md:flex`).
- **Visual Inconsistency:** Multiple disparate button gradients, varied border treatments, ad-hoc glassmorphism with excessive blurs, and inconsistent card paddings exist across pages.
- **Fragmented Analysis Experience:** `AnalyzeComment.jsx` and `AnalyzeChat.jsx` are segregated into disparate top-level tabs rather than a unified, segmented **Analysis Workspace** (`[ Paste Text ]`, `[ Upload Screenshot ]`, `[ Group Chat ]`).
- **Hard-coded Model Names:** `DashboardOverview.jsx` hard-coded model version `CB-RO-001`, whereas the backend is actively serving `CB-EXP-002`.
- **Accessibility & Responsive Deficits:** Missing accessible ARIA labels, no explicit focus rings for keyboard navigation, forms without clear helper text or validation states, and zero mobile navigation drawer.

---

## 2. Page & Route Inventory

| View ID | Component | URL / Trigger | User Role | Purpose | Current State |
|---|---|---|---|---|---|
| `login` / `register` | `AuthModal.jsx` | Unauthenticated | Public / All | JWT Auth with demo credentials | Functional, needs cleaner form layout and cybersecurity aesthetic |
| `dashboard` | `DashboardOverview.jsx` | `activeTab='dashboard'` | USER, CONSULTANT, ADMIN | High-level metrics, active incidents, quick actions | Functional, but hardcoded model version, uneven metric cards |
| `analyze` | `AnalyzeComment.jsx` | `activeTab='analyze'` | USER, CONSULTANT, ADMIN | Text pasting & Screenshot OCR with review | Functional, but 476 lines monolithic, lacks honest progress stepper |
| `chat` | `AnalyzeChat.jsx` | `activeTab='chat'` | USER, CONSULTANT, ADMIN | Multi-user conversation thread analysis | Functional, separate from Analyze page, basic chat bubble styling |
| `incidents` | `IncidentsView.jsx` | `activeTab='incidents'` | USER, CONSULTANT, ADMIN | Case management, timeline, evidence review | Functional, missing tabbed detail navigation (Overview, Evidence, Timeline, Analysis, Reports) |
| `reports` | `ReportsView.jsx` | `activeTab='reports'` | USER, CONSULTANT, ADMIN | Certified PDF report generation & download | Functional, basic card grid, lacks multi-step report creation wizard |
| `support` | `SupportChat.jsx` | `activeTab='support'` | USER, CONSULTANT, ADMIN | RAG-grounded wellbeing & legal guidance | Functional, needs calmer human-centered design and clear AI identity |
| `help` | `HelpRequestForm.jsx` | `activeTab='help'` | USER | Escalation to human consultants with bully accounts | Functional, long scroll form without progressive disclosure |
| `consultant` | `ConsultantPortal.jsx` | `activeTab='consultant'` | CONSULTANT, ADMIN | Case triage & perpetrator account management | Functional, RBAC enforced, needs polished case queue |
| `admin` | `AdminDashboard.jsx` | `activeTab='admin'` | ADMIN only | System overview, model registry, PSI drift, slang | Functional, monolithic 326 lines, needs segmented tabs |

---

## 3. Current Design System & Token Audit

### 3.1 Colors
- **Current definitions:** In `frontend/src/index.css`, root variables define `--bg-primary: #0a0e17`, `--bg-card: rgba(18, 24, 38, 0.85)`, with ad-hoc Tailwind classes (`bg-slate-900`, `bg-indigo-600`, `bg-rose-500/20`, `bg-emerald-500/20`).
- **Deficiencies:**
  - Lack of centralized semantic tokens for safety severity states (`safe`, `concerning`, `harmful`, `severe`).
  - Heavy reliance on color alone for risk states without consistent multi-modal cues (icon + label + text + badge).
  - Background contrast between card surfaces and primary canvas is muddy on non-OLED displays.

### 3.2 Typography
- **Current fonts:** Google Fonts `@import` includes *Plus Jakarta Sans*, *Inter*, and *JetBrains Mono*.
- **Deficiencies:**
  - Inconsistent font size classes (`text-[10px]`, `text-[11px]`, `text-xs`, `text-sm`, `text-base`, `text-xl`, `text-2xl`, `text-3xl`) used arbitrarily without a strict type scale.
  - Heading hierarchy jumps unpredictably (`h2` inside cards, `h3` in sections, lowercase uppercase mix).

### 3.3 Buttons & Interactive Elements
- **Current styles:** `.btn-primary` (purple-to-indigo gradient with bright glow), `.btn-secondary` (dark slate border), `.btn-danger` (rose gradient).
- **Deficiencies:**
  - Multiple components override padding with `!py-1 !px-2.5` or `!py-2 !px-4`.
  - Inconsistent active/focus rings (`outline-none` everywhere with no visible keyboard focus rings).
  - Hover micro-interactions vary between `-translate-y-1` and `-translate-y-2`.

### 3.4 Cards & Modals
- **Current styles:** `.glass-panel` uses `backdrop-filter: blur(16px)` and `border: 1px solid var(--border-color)`.
- **Deficiencies:**
  - Overuse of glassmorphism creates GPU lag on low-end devices and causes contrast degradation.
  - Border opacity is inconsistent across different components (`border-white/5`, `border-white/10`, `border-white/15`, `border-white/20`).
  - No standardized drawer component for secondary drill-downs.

---

## 4. Navigation & Global Shell Audit

### 4.1 Current Desktop Shell
- Current layout uses a single sticky horizontal `<header className="sticky top-0 ...">` in `Navbar.jsx`.
- When an Admin or Consultant logs in, tabs expand to 9 items, wrapping or overflowing horizontally on smaller laptops (1024px – 1280px).
- Navigation items use plain unicode emojis (`⚡`, `🔍`, `💬`) instead of clean vector iconography from `lucide-react`.

### 4.2 Current Mobile Shell
- Mobile navigation is simply hidden (`<nav className="hidden md:flex...">`), leaving mobile users with **zero navigation tabs** on viewports under 768px.
- There is no bottom navigation bar, hamburger drawer, or touch-friendly action sheet.

---

## 5. Page-by-Page Detailed Audit & Redesign Roadmap

### 5.1 Dashboard (`DashboardOverview.jsx`)
- **Current Flaws:**
  - Hero banner is overly tall with generic gradient blur.
  - Hard-coded string `"CB-RO-001"` instead of dynamically reflecting the active model from the backend.
  - Metric tiles lack sparklines or context.
  - Protocol card is static text rather than an actionable guide.
- **Redesign Requirements:**
  - Dynamic user greeting: "Good afternoon, [User]".
  - Primary action cards: "Analyze Content", "Upload Screenshot", "Analyze Group Chat", "Get Support".
  - Live metrics tied to actual `/incidents` and `/reports` responses.
  - Calm, human support callout.

### 5.2 Analyze Workspace (`AnalyzeComment.jsx` + `AnalyzeChat.jsx`)
- **Current Flaws:**
  - Segmented between two completely different top-level navigation tabs.
  - Direct text and screenshot OCR are placed in a toggle that resets state unexpectedly.
  - Analysis loading is a single spinner with "Evaluating Model..." rather than a structured multi-stage progress indicator.
  - Sample test buttons are cluttered at the bottom of the card.
- **Redesign Requirements:**
  - Unified **Analyze Workspace** with top segmented tabs: `[ Paste Text ]`, `[ Upload Screenshot ]`, `[ Group Chat ]`.
  - Clear drag-and-drop screenshot upload zone with file size/type validation.
  - Prominent OCR review & edit section allowing users to correct text before submission.
  - Honest step-by-step progress state during analysis.
  - Clear result card with:
    - Predicted category and confidence meter.
    - Explainable AI token attribution chips.
    - Multi-class probability bars.
    - Safety severity indicator (Safe, Moderate, High, Severe).
    - Clear next-step action buttons: `[ Save to Incident ]`, `[ Generate Report ]`, `[ Get Support ]`, `[ Analyze Another ]`.

### 5.3 Incidents View (`IncidentsView.jsx`)
- **Current Flaws:**
  - List and detail view are crammed into a split container with basic borders.
  - Missing search input, severity filter dropdown, and platform filter.
  - Incident details lack tabbed navigation.
- **Redesign Requirements:**
  - Standardized search, filter, sort bar.
  - Case status badges (`Active`, `Monitoring`, `Closed`).
  - Incident detail view organized into tabs:
    - `Overview`: Metadata, platform, incident code, created timestamp.
    - `Evidence`: Original screenshot, extracted text, raw OCR text.
    - `Timeline`: Chronological sequence of messages and analyses.
    - `Analysis`: Model version, confidence, category probabilities, XAI tokens.
    - `Reports`: Generated forensic artifacts.
    - `Support`: Connected support sessions and consultant escalation status.

### 5.4 Reports View (`ReportsView.jsx`)
- **Current Flaws:**
  - Only displays existing reports with a download button.
  - Lacks a multi-step guided report generation wizard.
- **Redesign Requirements:**
  - Clean card list and table view for existing certified PDF reports.
  - Multi-step report compilation modal with progress indicator.
  - Direct PDF download with verified hash and statutory filing instructions.

### 5.5 Support Chat (`SupportChat.jsx`)
- **Current Flaws:**
  - Looks too similar to an administrative or ML interface.
  - Wellbeing indicator says `"ELEVATED STRESS"` in bold red, which may inadvertently alarm an already distressed user.
- **Redesign Requirements:**
  - Calm, reassuring, human-centered UI design.
  - Reassuring intro prompt: "How are you feeling right now?" with quick-start chips.
  - Support AI conversation feed with distinct bot identity, timestamps, and RAG citation chips.
  - Emergency / high-risk safety panel with prominent national helpline info (Tele-MANAS `14416`, Cybercrime `1930`).
  - Explicit disclaimer: Non-clinical guidance, privacy-first evidence preservation.

### 5.6 Help Request Form (`HelpRequestForm.jsx`)
- **Current Flaws:**
  - Monolithic form with 12+ inputs on a single screen.
  - Bully account addition fields are dense and hard to parse.
- **Redesign Requirements:**
  - 3-step progressive wizard:
    1. Incident & Platform Context
    2. Bully / Perpetrator Accounts Catalog
    3. Additional Context & Confidential Submission
  - Clean account card list with platform icons.
  - Clear confirmation badge with generated tracking code.

### 5.7 Admin Dashboard (`AdminDashboard.jsx`)
- **Current Flaws:**
  - All admin sections (Overview, Model Registry, Drift, Slang) stacked vertically on one page.
  - Hard to navigate and compare models.
- **Redesign Requirements:**
  - Tabbed administrative architecture:
    1. `System Overview`: Real metrics, detection split, platform breakdown.
    2. `Dataset Registry`: Ingested datasets (`CB-DATA-002`, `WB-DATA-001`), license filters, quarantine indicators.
    3. `Model Registry & Monitoring`: Model lineage, active production tag, human promotion action.
    4. `Model Comparison`: Side-by-side empirical metrics (Macro-F1, ROC-AUC, accuracy, inference time).
    5. `Drift Monitoring`: Live PSI gauge, KS-test, JS divergence indicators.
    6. `Emerging Slang Queue`: Review and approve candidate terms with vocabulary frequency.

---

## 6. Recommended Reusable Component Hierarchy

```text
frontend/src/
├── components/
│   ├── layout/
│   │   ├── AppShell.jsx           # Global wrapper with responsive sidebar & topbar
│   │   ├── Sidebar.jsx            # Collapsible desktop sidebar with tooltips & RBAC
│   │   ├── Topbar.jsx             # Search, notifications, active model badge, user menu
│   │   └── MobileNav.jsx          # Mobile bottom bar + hamburger drawer
│   │
│   ├── ui/
│   │   ├── Button.jsx             # Primary, secondary, danger, ghost, icon variants
│   │   ├── Card.jsx               # Header, content, footer, hover states
│   │   ├── Badge.jsx              # Status, severity (safe, concerning, harmful, severe)
│   │   ├── Input.jsx              # Accessible input with label, error, helper text
│   │   ├── Select.jsx             # Accessible select with label, error
│   │   ├── Tabs.jsx               # Segmented and underline tab navigation
│   │   ├── Modal.jsx              # Accessible modal dialog with focus trap
│   │   ├── Drawer.jsx             # Slide-over drawer for secondary details
│   │   ├── Skeleton.jsx           # Reusable loading skeleton
│   │   ├── EmptyState.jsx         # Consistent empty state with action CTA
│   │   ├── Toast.jsx              # Non-intrusive toast notifications
│   │   └── Tooltip.jsx            # Accessible hover/focus tooltips
│   │
│   ├── analysis/
│   │   ├── AnalysisWorkspace.jsx  # Unified analysis container
│   │   ├── UploadZone.jsx         # Modern drag & drop screenshot zone
│   │   ├── OCRReview.jsx          # Editable extracted text preview
│   │   ├── AnalysisProgress.jsx   # Honest step-by-step progress state
│   │   ├── ResultCard.jsx         # Classification, confidence, severity
│   │   ├── CategoryBreakdown.jsx  # Multi-class probability bars
│   │   └── ExplanationPanel.jsx   # XAI salient tokens & model rationale
│   │
│   ├── incidents/
│   │   ├── IncidentCard.jsx       # Incident list summary card
│   │   ├── IncidentFilters.jsx    # Search, severity, platform filter bar
│   │   ├── IncidentDetailTabs.jsx # Overview, Evidence, Timeline, Analysis, Reports
│   │   └── EvidenceViewer.jsx     # Side-by-side screenshot and OCR viewer
│   │
│   ├── support/
│   │   ├── SupportAssistant.jsx   # Conversational RAG support
│   │   ├── WellbeingIndicator.jsx # Calm, non-stigmatizing wellbeing signal
│   │   ├── ResourceCard.jsx       # Official statutory helplines
│   │   └── EmergencyModal.jsx     # Immediate crisis intervention dialog (14416 / 1930)
│   │
│   └── admin/
│       ├── AdminTabs.jsx          # Overview, Datasets, Models, Drift, Slang
│       ├── DatasetRegistry.jsx    # Ingested benchmark catalog & licenses
│       ├── ModelRegistry.jsx      # Production lineage & promote controls
│       ├── ModelComparison.jsx    # Side-by-side empirical metrics table
│       ├── DriftDashboard.jsx     # PSI gauge, KS test, distribution shift
│       └── SlangQueue.jsx         # Emerging terms review & approval
│
└── pages/
    └── ComponentShowcase.jsx      # Dev route (/ui-components) showcasing all tokens & UI
```

---

## 7. Audit Conclusion & Next Actions
The existing CyberGuard backend and machine learning pipeline are production-grade. The frontend will now be systematically upgraded to match that engineering rigor through a centralized design system, a responsive application shell, and unified user/admin workflows.
