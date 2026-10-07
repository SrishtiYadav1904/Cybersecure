# CyberGuard Concept Drift & Vocabulary Evolution Report

## 1. Executive Summary
- **Metric Evaluated**: Population Stability Index (PSI) & Vocabulary OOV Frequency
- **Calculated PSI**: **4.8331**
- **Drift Evaluation Status**: **DRIFT_DETECTED**
- **Inference Sample Window**: 80 observations

## 2. Statistical Findings & Category Shifts
Significant concept drift detected! Recommending vocabulary update and model retraining.

| Category | Baseline % | Production % | Distribution Shift Term |
| :--- | :--- | :--- | :--- |
| **Age-based** | 8.0% | 0.01% | 0.5341 |
| **Gender-based** | 14.0% | 12.5% | 0.0017 |
| **Religion-based** | 12.0% | 0.01% | 0.8501 |
| **Ethnicity-based** | 11.0% | 0.01% | 0.7696 |
| **Appearance-based** | 10.0% | 0.01% | 0.6901 |
| **Mockery/Defamation** | 9.0% | 12.5% | 0.0115 |
| **Abusive/Insult** | 15.0% | 25.0% | 0.0511 |
| **Threat/Intimidation** | 6.0% | 50.0% | 0.9329 |
| **Personal Harassment** | 7.0% | 0.01% | 0.4579 |
| **Non-cyberbullying** | 8.0% | 0.01% | 0.5341 |

## 3. Detected Emerging Slang Candidates
The following high-frequency Out-of-Vocabulary (OOV) tokens were identified in production streams and queued for admin validation:
- `chapri`: Colloquial classist mockery term
- `doxx`: Digital privacy threat vector
- `noob`: Dismissive gaming insult
- `marja`: Extreme Hindi imperative threat term

## 4. Retraining Recommendations
1. Validate pending slang queue via Admin Portal.
2. Incorporate approved vocabulary into GloVe embedding projection cache.
3. Schedule periodic checkpoint retraining when PSI exceeds 0.25.
