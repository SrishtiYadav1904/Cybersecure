# CyberGuard UI/UX Redesign — Implementation Tracking Matrix

**Date:** September 25, 2026  
**Status Legend:** `NOT_STARTED` | `IN_PROGRESS` | `COMPLETED` | `BLOCKED`  

---

## Task Matrix

| ID | Phase | Component / Area | Description | Status | Verification Notes |
|---|---|---|---|---|---|
| **P1.1** | Phase 1: Audit | `docs/UI_UX_AUDIT.md` | Complete inventory of pages, routes, tokens, flaws, and recommendations | `COMPLETED` | Created & verified |
| **P1.2** | Phase 1: Audit | `docs/UI_IMPLEMENTATION_STATUS.md` | Dynamic task tracking matrix across all phases | `COMPLETED` | Created & actively tracked |
| **P2.1** | Phase 2: Design System | `docs/UI_DESIGN_SYSTEM.md` | Formal specification of semantic color tokens, typography scales, spacing, radius | `IN_PROGRESS` | Drafting design tokens |
| **P2.2** | Phase 2: Design System | `frontend/src/index.css` | Centralized CSS variables, font imports, focus rings, scrollbars, micro-transitions | `NOT_STARTED` | Pending design system doc |
| **P2.3** | Phase 2: Design System | Core UI Components | `Button`, `Card`, `Badge`, `Input`, `Select`, `Tabs`, `Modal`, `Drawer`, `Skeleton`, `EmptyState`, `Toast`, `Tooltip` | `NOT_STARTED` | To be created under `src/components/ui/` |
| **P3.1** | Phase 3: App Shell | `Sidebar.jsx` | Collapsible desktop sidebar with tooltips, active states, RBAC separation | `NOT_STARTED` | Replaces top emoji bar |
| **P3.2** | Phase 3: App Shell | `Topbar.jsx` | Header with breadcrumbs, active model badge (`CB-EXP-002`), emergency hotline, user menu | `NOT_STARTED` | Replaces monolithic navbar |
| **P3.3** | Phase 3: App Shell | `MobileNav.jsx` | Bottom navigation bar + slide-over drawer for mobile viewports | `NOT_STARTED` | Resolves mobile navigation omission |
| **P3.4** | Phase 3: App Shell | `AppShell.jsx` | Responsive layout container wrapping navigation and page content | `NOT_STARTED` | Integrated into `App.jsx` |
| **P4.1** | Phase 4: User Pages | `DashboardOverview.jsx` | Personalized greeting, primary action cards, dynamic metrics from backend, calm support prompt | `NOT_STARTED` | Fixes hardcoded model version |
| **P4.2** | Phase 4: User Pages | `AnalysisWorkspace.jsx` | Segmented tabs (`[ Paste Text ]`, `[ Upload Screenshot ]`, `[ Group Chat ]`), OCR edit, honest progress state | `NOT_STARTED` | Unifies AnalyzeComment and AnalyzeChat |
| **P4.3** | Phase 4: User Pages | Analysis Results View | Category breakdown bars, XAI token chips, safety severity card, next action buttons | `NOT_STARTED` | Enhances explanation readability |
| **P4.4** | Phase 4: User Pages | `IncidentsView.jsx` | Search, filter by severity/platform/status, sort, tabbed detail (Overview, Evidence, Timeline, Analysis, Reports) | `NOT_STARTED` | Case-management overhaul |
| **P4.5** | Phase 4: User Pages | `ReportsView.jsx` | Multi-step report submission wizard, certified PDF artifacts list, instant download | `NOT_STARTED` | Report generator + viewer |
| **P4.6** | Phase 4: User Pages | `SupportChat.jsx` | Calm human-centered layout, quick-start feelings prompt, RAG sources, crisis emergency modal (14416 / 1930) | `NOT_STARTED` | Ethical wellbeing UX |
| **P4.7** | Phase 4: User Pages | `HelpRequestForm.jsx` | 3-step progressive escalation wizard for human consultant referral | `NOT_STARTED` | Progressive disclosure |
| **P4.8** | Phase 4: User Pages | `ConsultantPortal.jsx` | Case triage queue, bully catalog review, dossier status update | `NOT_STARTED` | Consultant RBAC portal |
| **P5.1** | Phase 5: Admin | `AdminDashboard.jsx` | Tabbed architecture: Overview, Dataset Registry, Models, Drift, Slang Queue | `NOT_STARTED` | Monolith decomposition |
| **P5.2** | Phase 5: Admin | Dataset Registry Tab | External datasets (`CB-DATA-002`, `WB-DATA-001`), license filters, quarantine status | `NOT_STARTED` | Real data catalog |
| **P5.3** | Phase 5: Admin | Model Registry & Promote | Active model lineage, empirical comparison (`CB-BASE-001` vs `CB-EXP-002`), promote action | `NOT_STARTED` | Live promotion workflow |
| **P5.4** | Phase 5: Admin | Drift Monitoring Tab | PSI gauges, KS-test, JS divergence, distribution shift alerts | `NOT_STARTED` | Statistical MLOps |
| **P5.5** | Phase 5: Admin | Slang Approval Queue | Pending candidate terms, vocabulary frequency, approve for retraining | `NOT_STARTED` | Slang drift governance |
| **P6.1** | Phase 6: States | Loading & Skeletons | Reusable skeletons for cards, tables, analysis progress | `NOT_STARTED` | Eliminates raw spinners |
| **P6.2** | Phase 6: States | Empty States | Context-rich empty states with helpful primary CTAs across all views | `NOT_STARTED` | No blank screens |
| **P6.3** | Phase 6: States | Error & Toast States | User-friendly error banners and non-intrusive action toasts | `NOT_STARTED` | Standardized notifications |
| **P7.1** | Phase 7: Responsiveness | Responsive QA | Breakpoint testing: 390px, 430px, 768px, 1024px, 1280px, 1440px | `NOT_STARTED` | Mobile-first validation |
| **P7.2** | Phase 7: Accessibility | A11y Audit | Keyboard focus outlines, ARIA roles, color contrast, `prefers-reduced-motion` | `NOT_STARTED` | WCAG 2.1 AA target |
| **P8.1** | Phase 8: Showcase | `ComponentShowcase.jsx` | Development route (`/ui-components`) rendering all UI elements and design tokens | `NOT_STARTED` | Developer design system gallery |
| **P9.1** | Phase 9: QA & Verification | End-to-End User Flow | Auth -> Dashboard -> Analyze Screenshot -> OCR edit -> Result -> Save Incident -> Timeline -> Support -> Return | `NOT_STARTED` | Verified against running backend |
| **P9.2** | Phase 9: QA & Verification | End-to-End Admin Flow | Admin Login -> Overview -> Dataset Registry -> Model Comparison -> Drift Monitoring | `NOT_STARTED` | Verified against running backend |
