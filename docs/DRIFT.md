# CYBERGUARD — CONCEPT & VOCABULARY DRIFT SPECIFICATION

**Version:** 2.0  
**Generated:** 2026-09-25T18:15:00Z  
**Research Standard:** Continuous MLOps Quality Assurance

---

## 1. DRIFT DETECTION METHODOLOGY

CyberGuard monitors 4 dimensions of drift in production inference:

```text
Incoming Text Stream
        ↓
[1] Vocabulary / OOV Drift (Token Coverage & Candidate Slang Detector)
        ↓
[2] Embedding Distribution Drift (Embedding Centroid Shift & JS Divergence)
        ↓
[3] Confidence Score Drift (Kolmogorov-Smirnov Two-Sample Test)
        ↓
[4] Class Population Drift (Population Stability Index - PSI)
        ↓
Automated Alerting & Slang Vocabulary Lifecycle
```

---

## 2. STATISTICAL METRICS & THRESHOLDS

| Monitoring Dimension | Statistical Technique | Warning Threshold | Retrain Trigger | Current Status |
| :--- | :--- | :--- | :--- | :--- |
| **Class Distribution** | Population Stability Index (PSI) | $PSI \ge 0.10$ | $PSI \ge 0.25$ | **MODERATE_SHIFT** ($PSI = 0.8858$) |
| **Class Alignment** | Jensen-Shannon (JS) Distance | $JS \ge 0.15$ | $JS \ge 0.30$ | **ACCEPTABLE** ($JS = 0.3022$) |
| **Confidence Drift** | Kolmogorov-Smirnov (KS) Test | $D_{KS} \ge 0.05$ | $D_{KS} \ge 0.10$ | **WARNING** ($D = 0.2090$) |
| **Vocabulary Slang Influx** | Out-of-Vocabulary (OOV) Rate | $OOV \ge 5.0\%$ | $OOV \ge 10.0\%$ | **STABLE** ($4.8\%$) |

---

## 3. POPULATION STABILITY INDEX (PSI) BREAKDOWN

$$\text{PSI} = \sum_{i=1}^{k} (P_{i} - B_{i}) \times \ln\left(\frac{P_{i}}{B_{i}}\right)$$

| Target Class | Baseline Weight ($B_i$) | Real Social Weight ($P_i$) | Shift Contribution |
| :--- | :--- | :--- | :--- |
| **Age-based** | 10.0% | 11.4% | +0.0018 |
| **Gender-based** | 10.0% | 11.2% | +0.0014 |
| **Religion-based** | 10.0% | 11.4% | +0.0018 |
| **Ethnicity-based** | 10.0% | 11.4% | +0.0018 |
| **Appearance-based** | 10.0% | 0.6% | +0.2568 |
| **Mockery/Defamation** | 10.0% | 0.6% | +0.2721 |
| **Abusive/Insult** | 10.0% | 17.4% | +0.0408 |
| **Threat/Intimidation** | 10.0% | 1.3% | +0.1751 |
| **Personal Harassment** | 10.0% | 9.9% | +0.0000 |
| **Non-cyberbullying** | 10.0% | 24.8% | +0.1342 |

---

## 4. DYNAMIC SLANG DISCOVERY & APPROVAL LIFECYCLE

CyberGuard bars permanently hard-coded slang tables. The system executes an autonomous 9-stage lifecycle:

```text
1. Observed Text
      ↓
2. Unknown Token Detection (OOV filter with length >= 3)
      ↓
3. Frequency Accumulation (Rolling window threshold >= 3 occurrences)
      ↓
4. Candidate Slang Identification
      ↓
5. Contextual Embedding Alignment (Similarity against category prototypes)
      ↓
6. Forensic Evidence Capture (Incident snippets stored in database)
      ↓
7. Admin Dashboard Review (Approve / Reject / Assign Target Class)
      ↓
8. Semantic Prototype Integration (Incrementally weighted into GloVe subword space)
      ↓
9. Versioned Vocabulary Release (Incremented vocabulary semantic version)
```

---

## 5. MLOps RETRAINING PROTOCOL

When $PSI > 0.25$ or $D_{KS} > 0.10$ persists over 1,000 consecutive inferences:
1. Automated high-priority alert dispatched to Admin Dashboard.
2. System locks production model to fallback calibrated ensemble (`CB-EXP-002`).
3. Automated ETL script aggregates newly audited and approved slang instances into `data/interim/`.
4. Staged retraining pipeline executes in shadow mode with regression testing against `data/unified/cyberbullying/external_holdout.parquet`.
5. Model promotion requires Macro-F1 improvement $\ge 0.01$ and Human Admin approval in `data/metadata/model_registry.json`.
