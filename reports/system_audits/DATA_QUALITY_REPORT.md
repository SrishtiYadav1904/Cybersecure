# CyberGuard Data Quality Report

## 1. Summary Statistics
- **Raw Samples Ingested**: 2036
- **Empty / Malformed Records Excluded**: 0
- **Duplicate Records Removed**: 0
- **Final High-Quality Samples**: 2036
- **Deduplication Rate**: 0.0%

---

## 2. Unified Class Distribution
| Category | Sample Count | Percentage |
| :--- | :--- | :--- |
| **Threat/Intimidation** | 292 | 14.34% |
| **Non-cyberbullying** | 256 | 12.57% |
| **Abusive/Insult** | 228 | 11.2% |
| **Appearance-based** | 204 | 10.02% |
| **Gender-based** | 176 | 8.64% |
| **Age-based** | 176 | 8.64% |
| **Mockery/Defamation** | 176 | 8.64% |
| **Ethnicity-based** | 176 | 8.64% |
| **Religion-based** | 176 | 8.64% |
| **Personal Harassment** | 176 | 8.64% |

---

## 3. Multilingual Distribution
| Language | Sample Count | Percentage |
| :--- | :--- | :--- |
| **English** | 1196 | 58.74% |
| **Hindi** | 524 | 25.74% |
| **Hinglish** | 316 | 15.52% |

---

## 4. Leakage & Quality Validation
- **Train/Test Leakage**: Distinct MD5 hash sets verify zero overlapping text instances between partitions.
- **Normalization Integrity**: Devanagari NFC Unicode decomposition applied uniformly; character elongations normalized to standard lexical roots.
- **Slang Preservation**: Hinglish phonetic vocabulary preserved and standardized without loss of colloquial semantic markers.
