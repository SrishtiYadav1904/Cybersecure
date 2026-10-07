# CyberGuard Advanced Machine Learning (AML) Pipeline

## 1. Mathematical Pipeline Specification

```
Raw Input Text (or OCR Output)
            |
            v
[1. Text Preprocessing & Script Detection]
      - Emoji-to-text semantic mapping
      - Devanagari Unicode decomposition & normalization
      - Hinglish Romanized phonetic normalization
      - Punctuation & character elongation reduction
            |
            v
[2. Parallel Feature Extraction]
      +-----------------------------------------+-----------------------------------------+
      | Branch A: GloVe Word Vectors + PCA       | Branch B: Contextual Semantic Encoder    |
      | 1. Tokenize into n-grams & words        | 1. Subword tokenization (WordPiece/BPE)  |
      | 2. Mean-pooled GloVe representation (100d)| 2. Attention-weighted contextual vector  |
      | 3. PCA Dimensionality Reduction:        |    (RoBERTa / MiniLM 384d / dense layer) |
      |    W_pca in R^{100 x 30}                | 3. Pooling: CLS or mean token state     |
      |    v_pca = W_pca^T * (v_glove - mu)     |    v_ctx in R^{384}                     |
      +-----------------------------------------+-----------------------------------------+
                                    |
                                    v
                     [3. Dense Feature Fusion Layer]
                     z = [ v_pca || v_ctx ] in R^{414}
                     L2-normalize(z)
                                    |
                                    v
            [4. Multi-Model AML Classifier Comparison & Stacking]
      +-------------------------------------------------------------------+
      | - Base 1: Linear & RBF Support Vector Machines (SVM)             |
      | - Base 2: Extreme Gradient Boosting (XGBoost)                    |
      | - Base 3: Light Gradient Boosted Machine (LightGBM)              |
      | - Base 4: CatBoost Classifier                                    |
      | - Meta-Learner: Calibrated Stacking Ensemble                      |
      +-------------------------------------------------------------------+
                                    |
                                    v
                   [5. Class-Wise Probability Output]
                      P(y_c | x) for c in {1..10}
                                    |
                                    v
              [6. Explainable AI (XAI) Attribution Engine]
        - Local token importance attribution: phi_i for word w_i
        - Salient term extraction ("ugly", "nobody likes you", etc.)
        - Confidence-calibrated narrative rationale
```

---

## 3. Empirical Model Comparison & Stacking Results

### Experiment A (Baseline `CB-BASE-001`) vs. Experiment B (Expanded `CB-EXP-002`)

| Model | Dataset | Accuracy | Macro-F1 | Weighted-F1 | Precision | Recall | PR-AUC | ROC-AUC | Training Time | Inference Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SVM** | `CB-BASE-001` | 0.9902 | 0.9908 | 0.9902 | 0.9911 | 0.9913 | 0.9942 | 0.9990 | 0.32s | 0.005ms |
| **XGBoost** | `CB-BASE-001` | 0.9314 | 0.9329 | 0.9314 | 0.9336 | 0.9330 | 0.9823 | 0.9974 | 8.50s | 0.000ms |
| **LightGBM** | `CB-BASE-001` | 0.9534 | 0.9549 | 0.9533 | 0.9561 | 0.9557 | 0.9943 | 0.9993 | 2.48s | 0.041ms |
| **CatBoost** | `CB-BASE-001` | 0.7083 | 0.7156 | 0.7107 | 0.7445 | 0.7027 | 0.8297 | 0.9572 | 29.70s | 0.041ms |
| **Stacking** | `CB-BASE-001` | 0.9706 | 0.9711 | 0.9705 | 0.9720 | 0.9715 | 0.9968 | 0.9996 | 29.80s | 0.063ms |
| **SVM** | `CB-EXP-002` | 0.7148 | 0.7320 | 0.7069 | 0.7680 | 0.7141 | 0.8020 | 0.9451 | 8.70s | 0.004ms |
| **XGBoost** | `CB-EXP-002` | 0.7480 | 0.7301 | 0.7435 | 0.8330 | 0.6808 | 0.8134 | 0.9619 | 16.83s | 0.009ms |
| **LightGBM** | `CB-EXP-002` | 0.7603 | 0.7079 | 0.7569 | 0.7559 | 0.6786 | 0.7613 | 0.9613 | 14.16s | 0.029ms |
| **CatBoost** | `CB-EXP-002` | 0.6518 | 0.4541 | 0.6291 | 0.5148 | 0.4474 | 0.6150 | 0.9242 | 42.36s | 0.004ms |
| **Stacking** | `CB-EXP-002` | 0.7553 | 0.7081 | 0.7569 | 0.7539 | 0.6760 | 0.7718 | 0.9523 | 44.00s | 0.043ms |

---

## 4. Dedicated Wellbeing Support Model Family (`SUP-001`)

Strictly decoupled from the cyberbullying classification taxonomy:
- **Crisis Triage Model (CatBoost)**: Trained on `Reddit-Crisis-Triage-v1` (1,888 samples) distinguishing acute crisis (`CRISIS_ESCALATION` with 68.03% recall) from depressive distress. Triggers emergency modal for Tele-MANAS (14416) and National Cybercrime Portal (1930).
- **Cognitive Distress / LoST Model (LightGBM)**: Trained on `Reddit-LoST-v1` (3,245 samples) detecting self-worth erosion and Loss of Self with 91.95% accuracy on external holdout.
- **Stress Severity Calibrator**: Calibrated classification into `LOW`, `MODERATE`, `HIGH`, `SEVERE`.
- **Ethical Non-Diagnostic Policy**: All outputs are presented as **support signals and crisis triage triggers**, NEVER as clinical or medical diagnoses.
  - `components.npy`: Orthogonal projection matrix.

---

## 3. Multilingual Support
- **English**: Processed directly through GloVe vocabulary and English-pretrained contextual representations.
- **Hindi (Devanagari)**: Normalized using Unicode standard forms (`NFC`), transliteration fallback, and multilingual subword token embeddings.
- **Hinglish (Roman Hindi)**: Code-mixed dictionary lookup with phonetic mapping (e.g. `bakwaas` $\rightarrow$ `nonsense`, `kutta` $\rightarrow$ `abusive animal insult`, `chup kar` $\rightarrow$ `silencing aggression`).

---

## 4. Evaluation Framework
- **Primary Metric**: Macro-F1 across 10 classes (handles severe class imbalance).
- **Secondary Metrics**: Precision-Recall AUC (PR-AUC), Weighted-F1, Multi-class ROC-AUC, Class-wise Confusion Matrices.
- **Model Comparison**: McNemar's statistical hypothesis test comparing classifier predictions on identical holdout splits.
