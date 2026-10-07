# CyberGuard Design System Specification

**Version:** 2.0.0  
**Design Persona:** Senior Product Designer + Frontend Architect  
**Visual Aesthetic:** Sophisticated modern cybersecurity SaaS with subtle AI technology accents (dark/light slate palette, deep indigo/violet accents, calibrated semantic severity colors, no neon hacker tropes, restrained micro-interactions).

---

## 1. Design Principles

1. **Clarity & Trust Over Flash:** Cybersecurity and wellbeing users need confidence, transparency, and calmness. Never overwhelm with chaotic animations or neon glows.
2. **Multi-Modal Severity Communication:** Never communicate danger or risk using color alone. Every severity indicator must combine an icon, text label, and visual badge.
3. **Calm Mental-Health & Wellbeing Tone:** Support interfaces must feel human, private, and reassuring—never clinical, psychiatric, or punitive.
4. **Predictable Component Visual Language:** A primary button, badge, or input must look and behave identically across all pages.
5. **No Fake Data or UI Dead Ends:** Every metric, probability bar, and timeline node reflects active backend state. Every screen provides clear next steps.

---

## 2. Color Palette & Semantic Tokens

### 2.1 Base Canvas & Surface Tokens

| Token | CSS Variable | Hex / RGBA Value | Purpose |
|---|---|---|---|
| Background Canvas | `--color-bg-base` | `#080b11` | Root application background |
| Surface Primary | `--color-surface-primary` | `#0f141f` | Main card surface, sidebar |
| Surface Secondary | `--color-surface-secondary` | `#151c2b` | Nested cards, table headers, hover states |
| Surface Elevated | `--color-surface-elevated` | `#1c2538` | Modals, dropdowns, floating panels |
| Border Subtle | `--color-border-subtle` | `rgba(255, 255, 255, 0.07)` | Secondary card dividers, inactive borders |
| Border Default | `--color-border-default` | `rgba(255, 255, 255, 0.12)` | Standard card and input borders |
| Border Strong | `--color-border-strong` | `rgba(255, 255, 255, 0.20)` | Active cards, focused elements |
| Border Accent | `--color-border-accent` | `rgba(99, 102, 241, 0.45)` | Highlighted cybersecurity indicators |

### 2.2 Typography Colors

| Token | CSS Variable | Hex Value | Purpose |
|---|---|---|---|
| Text Primary | `--color-text-primary` | `#f8fafc` | Main headings, body text, emphasis |
| Text Secondary | `--color-text-secondary` | `#cbd5e1` | Descriptions, labels, secondary content |
| Text Muted | `--color-text-muted` | `#94a3b8` | Timestamps, helper text, inactive tabs |
| Text Faint | `--color-text-faint` | `#64748b` | Disabled states, subtle placeholders |

### 2.3 Brand & Technology Accents

| Token | CSS Variable | Hex Value | Purpose |
|---|---|---|---|
| Primary Indigo | `--color-primary` | `#6366f1` | Primary CTA, active states, active tab |
| Primary Hover | `--color-primary-hover` | `#4f46e5` | Primary button hover |
| Primary Muted | `--color-primary-muted` | `rgba(99, 102, 241, 0.15)`| Primary badge background, highlights |
| Violet Accent | `--color-accent-violet` | `#8b5cf6` | AI and ML indicators |
| Cyan Accent | `--color-accent-cyan` | `#06b6d4` | Network, forensic hashes, telemetry |

### 2.4 Cyberbullying & Safety Severity Tokens

| Severity Level | Border / Accent | Background Tint | Text Color | Icon | Semantic Meaning |
|---|---|---|---|---|---|
| **Safe** | `#10b981` (Emerald) | `rgba(16, 185, 129, 0.12)` | `#34d399` | `ShieldCheck` | Non-cyberbullying, respectful discourse |
| **Concerning / Moderate** | `#f59e0b` (Amber) | `rgba(245, 158, 11, 0.12)` | `#fbbf24` | `AlertCircle` | Questionable tone, slang check, moderate risk |
| **Harmful / High** | `#f97316` (Orange) | `rgba(249, 115, 22, 0.12)` | `#fb923c` | `AlertTriangle` | Direct insult, personal harassment |
| **Severe / Critical** | `#ef4444` (Rose/Red) | `rgba(239, 68, 68, 0.15)` | `#f87171` | `ShieldAlert` | Violent threat, sexual harassment, hate crime |
| **Unknown** | `#64748b` (Slate) | `rgba(100, 116, 139, 0.15)`| `#94a3b8` | `HelpCircle` | Insufficient text length, unclassified |

---

## 3. Typography Scale

Font Families:
- **Body & Display:** `'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif`
- **Code, Telemetry, Hashes:** `'JetBrains Mono', monospace`

| Scale Role | Font Size | Line Height | Weight | Tailwind Class | Usage |
|---|---|---|---|---|---|
| **Display Heading** | 2rem (32px) | 2.5rem | 800 | `text-2xl sm:text-3xl font-extrabold` | Hero headlines, landing callouts |
| **Page Heading** | 1.5rem (24px) | 2rem | 700 | `text-xl sm:text-2xl font-bold` | Page titles (H1) |
| **Section Heading** | 1.125rem (18px) | 1.75rem | 600 | `text-lg font-semibold` | Section divides (H2) |
| **Card Heading** | 0.9375rem (15px) | 1.375rem | 600 | `text-sm font-semibold` | Card titles (H3) |
| **Body Regular** | 0.875rem (14px) | 1.375rem | 400 / 500 | `text-sm font-normal` | Main paragraph text |
| **Body Small** | 0.8125rem (13px) | 1.25rem | 400 / 500 | `text-xs font-normal` | Table cells, form descriptions |
| **Caption / Meta** | 0.6875rem (11px) | 1rem | 500 | `text-[11px] font-medium` | Timestamps, token attributions |
| **Badge / Label** | 0.625rem (10px) | 0.875rem | 700 | `text-[10px] font-bold uppercase` | Status pills, severity badges |

---

## 4. Spacing, Radii & Shadow Tokens

### 4.1 Spacing Grid
- Baseline 4px grid: `4px` (`space-1`), `8px` (`space-2`), `12px` (`space-3`), `16px` (`space-4`), `20px` (`space-5`), `24px` (`space-6`), `32px` (`space-8`), `48px` (`space-12`).

### 4.2 Border Radii
- Small (Badges, tags): `6px` (`rounded-md`)
- Medium (Buttons, inputs): `10px` (`rounded-lg` / `rounded-xl`)
- Large (Cards, panels): `16px` (`rounded-2xl`)
- Extra Large (Modals, hero banners): `20px` (`rounded-3xl`)
- Pill (Avatar, pill badges): `9999px` (`rounded-full`)

### 4.3 Shadows
- Subtle Card Shadow: `0 4px 20px -2px rgba(0, 0, 0, 0.45)`
- Elevated Modal Shadow: `0 20px 40px -10px rgba(0, 0, 0, 0.7)`
- Primary Button Glow: `0 4px 14px 0 rgba(99, 102, 241, 0.35)`
- Danger Glow: `0 4px 14px 0 rgba(239, 68, 68, 0.30)`

---

## 5. Iconography Standard (Lucide Icons)

| Concept | Lucide Icon | Usage |
|---|---|---|
| Dashboard | `LayoutDashboard` | Main overview |
| Analyze / Scan | `Search` / `Scan` | Text & screenshot analysis |
| Incidents | `ShieldAlert` | Evidence case management |
| Reports | `FileText` | Downloadable PDF artifacts |
| Support AI | `HeartHandshake` / `MessageCircle` | Wellbeing assistant |
| Seek Help / Crisis | `AlertOctagon` / `PhoneCall` | Human escalation form |
| Consultant Portal | `ClipboardList` | Consultant triage queue |
| Admin Portal | `Sliders` / `ShieldCheck` | Admin dashboard |
| Datasets | `Database` | Ingested benchmarks & catalog |
| Models | `Cpu` / `Brain` | Model registry & promotion |
| Concept Drift | `Activity` / `TrendingUp` | PSI, KS test, distribution drift |
| Slang Queue | `BookOpen` / `Tag` | Emerging terms review |
| User Profile | `User` | Profile & settings |
| Logout | `LogOut` | Authentication termination |

---

## 6. Accessibility Requirements

- **Focus States:** High-visibility outline `focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none`.
- **Keyboard Navigation:** Tabindex on all interactive elements, modal `Escape` key close, Enter/Space activation on cards.
- **Color Contrast:** All text meets WCAG AA contrast ratio of at least `4.5:1` against dark backgrounds.
- **Motion Reduction:** Media query `@media (prefers-reduced-motion: reduce)` disables transition transforms and keyframe loops.
