# CyberGuard Mandatory Inference Benchmark Report

**Benchmark Date:** 2026-09-24T21:18:00+05:30  
**Active Model Version:** CB-RO-001  
**Architecture:** Calibrated Stacking Classifier (SVM + Gradient Boosting + Random Forest) over PCA-GloVe (30d) and Contextual Semantic Subword Projections (384d) [414d Fused Representation]  
**Verification Method:** 100% Genuine Classifier `predict_proba()` output. Zero heuristic keyword matching, zero rule overrides.  
**Overall Benchmark Accuracy:** **94.3% (33/35 passed)**  

---

## Summary by Language

| Language | Total Cases | Passed | Accuracy |
|---|---|---|---|
| **English** | 12 | 12 | 100.0% |
| **Hindi** | 12 | 11 | 91.7% |
| **Hinglish** | 11 | 10 | 90.9% |

---

## Comprehensive Test Case Logs

Each test case below logs: `input -> predicted class -> probability distribution -> confidence -> model version`.

### Case #1 [English] — ✅ PASS
* **Input Text:** `I will track your IP and destroy you and your family.`
* **Target Category:** `Threat/Intimidation`
* **Predicted Class:** **`Threat/Intimidation`**
* **Confidence:** **`0.3042`** (30.42%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Threat/Intimidation | `0.3042` | ██████ |
| Gender-based | `0.2172` | ████ |
| Abusive/Insult | `0.1530` | ███ |
| Personal Harassment | `0.0857` | █ |
| Age-based | `0.0685` | █ |
| Appearance-based | `0.0542` | █ |
| Mockery/Defamation | `0.0462` |  |
| Religion-based | `0.0267` |  |
| Ethnicity-based | `0.0224` |  |
| Non-cyberbullying | `0.0219` |  |

---

### Case #2 [English] — ✅ PASS
* **Input Text:** `You are completely useless, stupid piece of shit, get lost.`
* **Target Category:** `Abusive/Insult`
* **Predicted Class:** **`Abusive/Insult`**
* **Confidence:** **`0.6644`** (66.44%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Abusive/Insult | `0.6644` | █████████████ |
| Threat/Intimidation | `0.0723` | █ |
| Ethnicity-based | `0.0450` |  |
| Age-based | `0.0422` |  |
| Mockery/Defamation | `0.0401` |  |
| Appearance-based | `0.0332` |  |
| Gender-based | `0.0331` |  |
| Non-cyberbullying | `0.0286` |  |
| Personal Harassment | `0.0233` |  |
| Religion-based | `0.0178` |  |

---

### Case #3 [English] — ✅ PASS
* **Input Text:** `Stop posting here, we will harass you and spam your inbox until you delete your account.`
* **Target Category:** `Personal Harassment`
* **Predicted Class:** **`Personal Harassment`**
* **Confidence:** **`0.3775`** (37.75%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Personal Harassment | `0.3775` | ███████ |
| Non-cyberbullying | `0.2636` | █████ |
| Abusive/Insult | `0.1092` | ██ |
| Gender-based | `0.0880` | █ |
| Mockery/Defamation | `0.0336` |  |
| Threat/Intimidation | `0.0293` |  |
| Age-based | `0.0282` |  |
| Appearance-based | `0.0273` |  |
| Ethnicity-based | `0.0256` |  |
| Religion-based | `0.0178` |  |

---

### Case #4 [English] — ✅ PASS
* **Input Text:** `You are a terrorist because of your religion, get out of our country.`
* **Target Category:** `Religion-based`
* **Predicted Class:** **`Religion-based`**
* **Confidence:** **`0.9738`** (97.38%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Religion-based | `0.9738` | ███████████████████ |
| Non-cyberbullying | `0.0056` |  |
| Personal Harassment | `0.0034` |  |
| Age-based | `0.0031` |  |
| Gender-based | `0.0029` |  |
| Abusive/Insult | `0.0026` |  |
| Threat/Intimidation | `0.0026` |  |
| Appearance-based | `0.0022` |  |
| Mockery/Defamation | `0.0021` |  |
| Ethnicity-based | `0.0018` |  |

---

### Case #5 [English] — ✅ PASS
* **Input Text:** `Women should not be allowed online, you are just an emotional bitch, go back to the kitchen.`
* **Target Category:** `Gender-based`
* **Predicted Class:** **`Gender-based`**
* **Confidence:** **`0.9743`** (97.43%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Gender-based | `0.9743` | ███████████████████ |
| Abusive/Insult | `0.0094` |  |
| Threat/Intimidation | `0.0046` |  |
| Age-based | `0.0029` |  |
| Appearance-based | `0.0018` |  |
| Mockery/Defamation | `0.0017` |  |
| Ethnicity-based | `0.0014` |  |
| Non-cyberbullying | `0.0013` |  |
| Religion-based | `0.0013` |  |
| Personal Harassment | `0.0012` |  |

---

### Case #6 [English] — ✅ PASS
* **Input Text:** `Look at your face in the mirror, so ugly and pathetic, you look like a disgusting deformed pig.`
* **Target Category:** `Appearance-based`
* **Predicted Class:** **`Appearance-based`**
* **Confidence:** **`0.9655`** (96.55%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Appearance-based | `0.9655` | ███████████████████ |
| Abusive/Insult | `0.0091` |  |
| Gender-based | `0.0089` |  |
| Non-cyberbullying | `0.0039` |  |
| Mockery/Defamation | `0.0030` |  |
| Age-based | `0.0028` |  |
| Ethnicity-based | `0.0017` |  |
| Personal Harassment | `0.0017` |  |
| Religion-based | `0.0017` |  |
| Threat/Intimidation | `0.0016` |  |

---

### Case #7 [English] — ✅ PASS
* **Input Text:** `What a clown show, look at this complete fool and laughingstock embarrassing himself.`
* **Target Category:** `Mockery/Defamation`
* **Predicted Class:** **`Mockery/Defamation`**
* **Confidence:** **`0.9892`** (98.92%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Mockery/Defamation | `0.9892` | ███████████████████ |
| Gender-based | `0.0030` |  |
| Abusive/Insult | `0.0020` |  |
| Age-based | `0.0017` |  |
| Personal Harassment | `0.0009` |  |
| Appearance-based | `0.0007` |  |
| Ethnicity-based | `0.0007` |  |
| Non-cyberbullying | `0.0007` |  |
| Threat/Intimidation | `0.0006` |  |
| Religion-based | `0.0005` |  |

---

### Case #8 [English] — ✅ PASS
* **Input Text:** `You boomer grandma, you are too old to understand anything, go take your dementia pills.`
* **Target Category:** `Age-based`
* **Predicted Class:** **`Age-based`**
* **Confidence:** **`0.9905`** (99.05%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Age-based | `0.9905` | ███████████████████ |
| Abusive/Insult | `0.0018` |  |
| Appearance-based | `0.0015` |  |
| Gender-based | `0.0013` |  |
| Mockery/Defamation | `0.0009` |  |
| Threat/Intimidation | `0.0009` |  |
| Ethnicity-based | `0.0008` |  |
| Non-cyberbullying | `0.0008` |  |
| Personal Harassment | `0.0008` |  |
| Religion-based | `0.0006` |  |

---

### Case #9 [English] — ✅ PASS
* **Input Text:** `Go back to where you came from, you dirty foreigner and illegal immigrant.`
* **Target Category:** `Ethnicity-based`
* **Predicted Class:** **`Ethnicity-based`**
* **Confidence:** **`0.9828`** (98.28%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Ethnicity-based | `0.9828` | ███████████████████ |
| Non-cyberbullying | `0.0050` |  |
| Mockery/Defamation | `0.0039` |  |
| Age-based | `0.0016` |  |
| Appearance-based | `0.0015` |  |
| Gender-based | `0.0015` |  |
| Abusive/Insult | `0.0010` |  |
| Personal Harassment | `0.0010` |  |
| Religion-based | `0.0009` |  |
| Threat/Intimidation | `0.0008` |  |

---

### Case #10 [English] — ✅ PASS
* **Input Text:** `Thank you so much for explaining the code, really helpful project!`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.6853`** (68.53%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.6853` | █████████████ |
| Appearance-based | `0.2288` | ████ |
| Abusive/Insult | `0.0308` |  |
| Gender-based | `0.0139` |  |
| Age-based | `0.0088` |  |
| Mockery/Defamation | `0.0079` |  |
| Ethnicity-based | `0.0072` |  |
| Religion-based | `0.0063` |  |
| Threat/Intimidation | `0.0060` |  |
| Personal Harassment | `0.0051` |  |

---

### Case #11 [English] — ✅ PASS
* **Input Text:** `Can someone recommend a good book on distributed systems architecture?`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9960`** (99.60%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9960` | ███████████████████ |
| Abusive/Insult | `0.0012` |  |
| Age-based | `0.0004` |  |
| Appearance-based | `0.0004` |  |
| Gender-based | `0.0004` |  |
| Threat/Intimidation | `0.0004` |  |
| Ethnicity-based | `0.0003` |  |
| Mockery/Defamation | `0.0003` |  |
| Religion-based | `0.0003` |  |
| Personal Harassment | `0.0002` |  |

---

### Case #12 [English] — ✅ PASS
* **Input Text:** `Good morning everyone, hope you all have a wonderful and productive day ahead.`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9516`** (95.16%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9516` | ███████████████████ |
| Abusive/Insult | `0.0100` |  |
| Threat/Intimidation | `0.0087` |  |
| Gender-based | `0.0057` |  |
| Age-based | `0.0049` |  |
| Mockery/Defamation | `0.0045` |  |
| Religion-based | `0.0039` |  |
| Appearance-based | `0.0038` |  |
| Ethnicity-based | `0.0035` |  |
| Personal Harassment | `0.0034` |  |

---

### Case #13 [Hindi] — ✅ PASS
* **Input Text:** `घर से बाहर निकल, तुझे जान से मार दूंगा आज।`
* **Target Category:** `Threat/Intimidation`
* **Predicted Class:** **`Threat/Intimidation`**
* **Confidence:** **`0.9596`** (95.96%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Threat/Intimidation | `0.9596` | ███████████████████ |
| Age-based | `0.0109` |  |
| Personal Harassment | `0.0080` |  |
| Gender-based | `0.0045` |  |
| Religion-based | `0.0044` |  |
| Abusive/Insult | `0.0029` |  |
| Mockery/Defamation | `0.0028` |  |
| Appearance-based | `0.0026` |  |
| Ethnicity-based | `0.0022` |  |
| Non-cyberbullying | `0.0021` |  |

---

### Case #14 [Hindi] — ✅ PASS
* **Input Text:** `तुम बहुत बेकार, नालायक और मूर्ख इंसान हो, अपना गंदा मुँह बंद रख।`
* **Target Category:** `Abusive/Insult`
* **Predicted Class:** **`Abusive/Insult`**
* **Confidence:** **`0.9596`** (95.96%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Abusive/Insult | `0.9596` | ███████████████████ |
| Mockery/Defamation | `0.0072` |  |
| Age-based | `0.0064` |  |
| Appearance-based | `0.0052` |  |
| Gender-based | `0.0049` |  |
| Ethnicity-based | `0.0043` |  |
| Non-cyberbullying | `0.0038` |  |
| Personal Harassment | `0.0032` |  |
| Threat/Intimidation | `0.0030` |  |
| Religion-based | `0.0025` |  |

---

### Case #15 [Hindi] — ❌ FAIL
* **Input Text:** `हम सब मिलकर तेरा जीना हराम कर देंगे, तेरी निजी तस्वीरें इंटरनेट पर वायरल कर देंगे।`
* **Target Category:** `Personal Harassment`
* **Predicted Class:** **`Age-based`**
* **Confidence:** **`0.4310`** (43.10%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Age-based | `0.4310` | ████████ |
| Gender-based | `0.1261` | ██ |
| Personal Harassment | `0.0854` | █ |
| Mockery/Defamation | `0.0695` | █ |
| Non-cyberbullying | `0.0634` | █ |
| Religion-based | `0.0605` | █ |
| Abusive/Insult | `0.0559` | █ |
| Appearance-based | `0.0398` |  |
| Threat/Intimidation | `0.0398` |  |
| Ethnicity-based | `0.0285` |  |

---

### Case #16 [Hindi] — ✅ PASS
* **Input Text:** `तेरे धर्म के लोग आतंकी होते हैं, अपने पाखंडी मजहब का जहर यहाँ मत फैलाओ।`
* **Target Category:** `Religion-based`
* **Predicted Class:** **`Religion-based`**
* **Confidence:** **`0.9510`** (95.10%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Religion-based | `0.9510` | ███████████████████ |
| Gender-based | `0.0104` |  |
| Personal Harassment | `0.0073` |  |
| Non-cyberbullying | `0.0072` |  |
| Threat/Intimidation | `0.0056` |  |
| Abusive/Insult | `0.0043` |  |
| Mockery/Defamation | `0.0039` |  |
| Appearance-based | `0.0036` |  |
| Age-based | `0.0035` |  |
| Ethnicity-based | `0.0030` |  |

---

### Case #17 [Hindi] — ✅ PASS
* **Input Text:** `औरत हो, घर में बैठो, रसोई संभालो, सोशल मीडिया पर बकवास मत करो।`
* **Target Category:** `Gender-based`
* **Predicted Class:** **`Gender-based`**
* **Confidence:** **`0.9635`** (96.35%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Gender-based | `0.9635` | ███████████████████ |
| Abusive/Insult | `0.0142` |  |
| Age-based | `0.0041` |  |
| Threat/Intimidation | `0.0039` |  |
| Mockery/Defamation | `0.0030` |  |
| Appearance-based | `0.0029` |  |
| Religion-based | `0.0026` |  |
| Non-cyberbullying | `0.0022` |  |
| Ethnicity-based | `0.0021` |  |
| Personal Harassment | `0.0016` |  |

---

### Case #18 [Hindi] — ✅ PASS
* **Input Text:** `तुम्हारा चेहरा इतना गंदा और बदसूरत है कि कोई देख नहीं सकता, सूअर जैसी शक्ल है तेरी।`
* **Target Category:** `Appearance-based`
* **Predicted Class:** **`Appearance-based`**
* **Confidence:** **`0.9872`** (98.72%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Appearance-based | `0.9872` | ███████████████████ |
| Gender-based | `0.0038` |  |
| Abusive/Insult | `0.0029` |  |
| Non-cyberbullying | `0.0012` |  |
| Age-based | `0.0011` |  |
| Mockery/Defamation | `0.0011` |  |
| Ethnicity-based | `0.0007` |  |
| Religion-based | `0.0007` |  |
| Threat/Intimidation | `0.0007` |  |
| Personal Harassment | `0.0006` |  |

---

### Case #19 [Hindi] — ✅ PASS
* **Input Text:** `पूरे कॉलेज का सबसे बड़ा जोकर यही है, सर्कस के जोकर जैसी हरकतें मत कर।`
* **Target Category:** `Mockery/Defamation`
* **Predicted Class:** **`Mockery/Defamation`**
* **Confidence:** **`0.9671`** (96.71%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Mockery/Defamation | `0.9671` | ███████████████████ |
| Gender-based | `0.0079` |  |
| Abusive/Insult | `0.0054` |  |
| Age-based | `0.0038` |  |
| Religion-based | `0.0035` |  |
| Threat/Intimidation | `0.0029` |  |
| Appearance-based | `0.0027` |  |
| Non-cyberbullying | `0.0027` |  |
| Personal Harassment | `0.0023` |  |
| Ethnicity-based | `0.0017` |  |

---

### Case #20 [Hindi] — ✅ PASS
* **Input Text:** `बुड्ढे सठिया गए हो, अब तुम्हारी कोई औकात नहीं है, भजन कीर्तन करो।`
* **Target Category:** `Age-based`
* **Predicted Class:** **`Age-based`**
* **Confidence:** **`0.9864`** (98.64%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Age-based | `0.9864` | ███████████████████ |
| Appearance-based | `0.0023` |  |
| Abusive/Insult | `0.0021` |  |
| Ethnicity-based | `0.0018` |  |
| Non-cyberbullying | `0.0015` |  |
| Mockery/Defamation | `0.0014` |  |
| Gender-based | `0.0013` |  |
| Threat/Intimidation | `0.0012` |  |
| Personal Harassment | `0.0011` |  |
| Religion-based | `0.0009` |  |

---

### Case #21 [Hindi] — ✅ PASS
* **Input Text:** `अपनी नीच जाति और कौम का कचरा यहाँ मत फैला, विदेशी घुसपैठिए।`
* **Target Category:** `Ethnicity-based`
* **Predicted Class:** **`Ethnicity-based`**
* **Confidence:** **`0.9573`** (95.73%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Ethnicity-based | `0.9573` | ███████████████████ |
| Non-cyberbullying | `0.0131` |  |
| Mockery/Defamation | `0.0087` |  |
| Appearance-based | `0.0044` |  |
| Gender-based | `0.0037` |  |
| Age-based | `0.0032` |  |
| Abusive/Insult | `0.0027` |  |
| Personal Harassment | `0.0026` |  |
| Religion-based | `0.0022` |  |
| Threat/Intimidation | `0.0022` |  |

---

### Case #22 [Hindi] — ✅ PASS
* **Input Text:** `आज का मौसम बहुत सुहावना है और शाम को हल्की बारिश हो रही है।`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9805`** (98.05%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9805` | ███████████████████ |
| Abusive/Insult | `0.0049` |  |
| Appearance-based | `0.0027` |  |
| Threat/Intimidation | `0.0023` |  |
| Gender-based | `0.0021` |  |
| Age-based | `0.0020` |  |
| Mockery/Defamation | `0.0016` |  |
| Religion-based | `0.0014` |  |
| Ethnicity-based | `0.0013` |  |
| Personal Harassment | `0.0010` |  |

---

### Case #23 [Hindi] — ✅ PASS
* **Input Text:** `नमस्ते भाई, मुझे आपकी सहायता की आवश्यकता थी इस परीक्षा की तैयारी के लिए।`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9682`** (96.82%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9682` | ███████████████████ |
| Personal Harassment | `0.0075` |  |
| Abusive/Insult | `0.0074` |  |
| Appearance-based | `0.0030` |  |
| Gender-based | `0.0027` |  |
| Threat/Intimidation | `0.0027` |  |
| Mockery/Defamation | `0.0023` |  |
| Age-based | `0.0022` |  |
| Ethnicity-based | `0.0020` |  |
| Religion-based | `0.0020` |  |

---

### Case #24 [Hindi] — ✅ PASS
* **Input Text:** `दीपावली के इस पावन पर्व पर आप सभी को हार्दिक शुभकामनाएँ और बधाई।`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9901`** (99.01%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9901` | ███████████████████ |
| Abusive/Insult | `0.0028` |  |
| Threat/Intimidation | `0.0015` |  |
| Appearance-based | `0.0011` |  |
| Age-based | `0.0010` |  |
| Religion-based | `0.0009` |  |
| Gender-based | `0.0008` |  |
| Mockery/Defamation | `0.0007` |  |
| Ethnicity-based | `0.0006` |  |
| Personal Harassment | `0.0006` |  |

---

### Case #25 [Hinglish] — ❌ FAIL
* **Input Text:** `Tera address mil gaya hai, marja tu nahi toh ghar aake maarenge.`
* **Target Category:** `Threat/Intimidation`
* **Predicted Class:** **`Religion-based`**
* **Confidence:** **`0.3919`** (39.19%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Religion-based | `0.3919` | ███████ |
| Threat/Intimidation | `0.2777` | █████ |
| Personal Harassment | `0.0802` | █ |
| Age-based | `0.0516` | █ |
| Abusive/Insult | `0.0458` |  |
| Non-cyberbullying | `0.0417` |  |
| Appearance-based | `0.0293` |  |
| Gender-based | `0.0289` |  |
| Ethnicity-based | `0.0265` |  |
| Mockery/Defamation | `0.0265` |  |

---

### Case #26 [Hinglish] — ✅ PASS
* **Input Text:** `Tu kitna bada kutta aur chutiya hai saale madarchod chup baith.`
* **Target Category:** `Abusive/Insult`
* **Predicted Class:** **`Abusive/Insult`**
* **Confidence:** **`0.9626`** (96.26%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Abusive/Insult | `0.9626` | ███████████████████ |
| Ethnicity-based | `0.0062` |  |
| Mockery/Defamation | `0.0062` |  |
| Age-based | `0.0047` |  |
| Appearance-based | `0.0045` |  |
| Gender-based | `0.0044` |  |
| Non-cyberbullying | `0.0036` |  |
| Personal Harassment | `0.0030` |  |
| Threat/Intimidation | `0.0026` |  |
| Religion-based | `0.0022` |  |

---

### Case #27 [Hinglish] — ✅ PASS
* **Input Text:** `Tu jahan bhi comment karega, hum wahan tujhe bully karenge aur doxx karenge.`
* **Target Category:** `Personal Harassment`
* **Predicted Class:** **`Personal Harassment`**
* **Confidence:** **`0.9568`** (95.68%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Personal Harassment | `0.9568` | ███████████████████ |
| Abusive/Insult | `0.0126` |  |
| Ethnicity-based | `0.0058` |  |
| Gender-based | `0.0043` |  |
| Age-based | `0.0040` |  |
| Appearance-based | `0.0040` |  |
| Mockery/Defamation | `0.0039` |  |
| Non-cyberbullying | `0.0035` |  |
| Religion-based | `0.0025` |  |
| Threat/Intimidation | `0.0025` |  |

---

### Case #28 [Hinglish] — ✅ PASS
* **Input Text:** `Tere jaise dharam ke log desh ke dushman hain, jihadi nikal yahan se.`
* **Target Category:** `Religion-based`
* **Predicted Class:** **`Religion-based`**
* **Confidence:** **`0.8578`** (85.78%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Religion-based | `0.8578` | █████████████████ |
| Age-based | `0.0413` |  |
| Non-cyberbullying | `0.0259` |  |
| Personal Harassment | `0.0131` |  |
| Abusive/Insult | `0.0129` |  |
| Mockery/Defamation | `0.0111` |  |
| Ethnicity-based | `0.0105` |  |
| Threat/Intimidation | `0.0105` |  |
| Appearance-based | `0.0093` |  |
| Gender-based | `0.0076` |  |

---

### Case #29 [Hinglish] — ✅ PASS
* **Input Text:** `Randi jaise behave mat kar, aurat hai toh kitchen me jaake bartan dho.`
* **Target Category:** `Gender-based`
* **Predicted Class:** **`Gender-based`**
* **Confidence:** **`0.9746`** (97.46%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Gender-based | `0.9746` | ███████████████████ |
| Abusive/Insult | `0.0103` |  |
| Threat/Intimidation | `0.0029` |  |
| Non-cyberbullying | `0.0027` |  |
| Age-based | `0.0026` |  |
| Appearance-based | `0.0019` |  |
| Mockery/Defamation | `0.0014` |  |
| Ethnicity-based | `0.0013` |  |
| Religion-based | `0.0012` |  |
| Personal Harassment | `0.0010` |  |

---

### Case #30 [Hinglish] — ✅ PASS
* **Input Text:** `Kitna mota aur badsurat hai tu, suar jaisi shakal hai motey.`
* **Target Category:** `Appearance-based`
* **Predicted Class:** **`Appearance-based`**
* **Confidence:** **`0.9916`** (99.16%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Appearance-based | `0.9916` | ███████████████████ |
| Gender-based | `0.0025` |  |
| Abusive/Insult | `0.0020` |  |
| Non-cyberbullying | `0.0008` |  |
| Mockery/Defamation | `0.0007` |  |
| Age-based | `0.0006` |  |
| Threat/Intimidation | `0.0005` |  |
| Ethnicity-based | `0.0004` |  |
| Personal Harassment | `0.0004` |  |
| Religion-based | `0.0004` |  |

---

### Case #31 [Hinglish] — ✅ PASS
* **Input Text:** `Ye pura joker hai bhai, circus ka clown lag raha hai sab milke roast karo.`
* **Target Category:** `Mockery/Defamation`
* **Predicted Class:** **`Mockery/Defamation`**
* **Confidence:** **`0.8084`** (80.84%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Mockery/Defamation | `0.8084` | ████████████████ |
| Abusive/Insult | `0.0900` | █ |
| Gender-based | `0.0215` |  |
| Religion-based | `0.0173` |  |
| Age-based | `0.0172` |  |
| Non-cyberbullying | `0.0119` |  |
| Appearance-based | `0.0102` |  |
| Personal Harassment | `0.0081` |  |
| Threat/Intimidation | `0.0077` |  |
| Ethnicity-based | `0.0076` |  |

---

### Case #32 [Hinglish] — ✅ PASS
* **Input Text:** `Abey boomer uncle, tumhara time khatam ho gaya, retirement lo aur chup baitho.`
* **Target Category:** `Age-based`
* **Predicted Class:** **`Age-based`**
* **Confidence:** **`0.7956`** (79.56%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Age-based | `0.7956` | ███████████████ |
| Abusive/Insult | `0.0686` | █ |
| Appearance-based | `0.0499` |  |
| Gender-based | `0.0198` |  |
| Mockery/Defamation | `0.0137` |  |
| Non-cyberbullying | `0.0123` |  |
| Ethnicity-based | `0.0114` |  |
| Threat/Intimidation | `0.0106` |  |
| Personal Harassment | `0.0105` |  |
| Religion-based | `0.0076` |  |

---

### Case #33 [Hinglish] — ✅ PASS
* **Input Text:** `Chapri log internet pe aa gaye, apni gandi neech aukaat dikha rahe ho.`
* **Target Category:** `Ethnicity-based`
* **Predicted Class:** **`Ethnicity-based`**
* **Confidence:** **`0.8645`** (86.45%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Ethnicity-based | `0.8645` | █████████████████ |
| Age-based | `0.0579` | █ |
| Non-cyberbullying | `0.0188` |  |
| Mockery/Defamation | `0.0146` |  |
| Appearance-based | `0.0115` |  |
| Abusive/Insult | `0.0093` |  |
| Gender-based | `0.0066` |  |
| Personal Harassment | `0.0066` |  |
| Threat/Intimidation | `0.0054` |  |
| Religion-based | `0.0050` |  |

---

### Case #34 [Hinglish] — ✅ PASS
* **Input Text:** `Bhai project submit ho gaya, thanks for helping me out yaar!`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9951`** (99.51%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9951` | ███████████████████ |
| Abusive/Insult | `0.0014` |  |
| Appearance-based | `0.0007` |  |
| Age-based | `0.0005` |  |
| Threat/Intimidation | `0.0005` |  |
| Gender-based | `0.0004` |  |
| Religion-based | `0.0004` |  |
| Ethnicity-based | `0.0003` |  |
| Mockery/Defamation | `0.0003` |  |
| Personal Harassment | `0.0003` |  |

---

### Case #35 [Hinglish] — ✅ PASS
* **Input Text:** `Chalo weekend pe movie dekhne chalte hain sab log chai peene ke baad.`
* **Target Category:** `Non-cyberbullying`
* **Predicted Class:** **`Non-cyberbullying`**
* **Confidence:** **`0.9956`** (99.56%)
* **Model Version:** `CB-RO-001`

**Probability Distribution:**

| Category | Probability | Bar |
|---|---|---|
| Non-cyberbullying | `0.9956` | ███████████████████ |
| Abusive/Insult | `0.0013` |  |
| Appearance-based | `0.0005` |  |
| Threat/Intimidation | `0.0005` |  |
| Age-based | `0.0004` |  |
| Gender-based | `0.0004` |  |
| Religion-based | `0.0004` |  |
| Ethnicity-based | `0.0003` |  |
| Mockery/Defamation | `0.0003` |  |
| Personal Harassment | `0.0002` |  |

---
