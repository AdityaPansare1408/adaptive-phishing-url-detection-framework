# Adaptive Phishing URL Detection Framework

## Overview

Phishing attacks have evolved beyond simple malicious URLs and increasingly rely on domain spoofing, character substitution, homograph attacks, deceptive branding, and phishing-oriented intent signals to bypass traditional security mechanisms.

This project presents an Adaptive Phishing URL Detection Framework that combines Machine Learning with Multi-Level Security Intelligence to improve detection of sophisticated phishing attacks.

Unlike conventional URL classifiers that rely solely on machine learning predictions, this framework integrates:

* Machine Learning Detection Layer
* Deception Analysis Layer
* Intent Analysis Layer
* Adaptive Trust-Aware Fusion Framework
* Risk Assessment and Explanation Layer

The system analyzes URLs using multiple independent security signals and dynamically adapts trust allocation based on the detected attack profile.

---

## Key Features

### Machine Learning Detection

* XGBoost-based phishing URL classification
* Trained on approximately 1.49 million URLs
* Uses 18 engineered lexical, structural, statistical, and security-related features

### Deception Analysis Engine

Detects advanced URL manipulation techniques including:

* Character substitution attacks
* Homograph attacks
* Unicode anomalies
* Punycode abuse
* Repeated-character manipulation
* Domain deception patterns

### Intent Analysis Engine

Identifies phishing-oriented intent through:

* Suspicious keyword detection
* Risk-based keyword scoring
* Nonlinear intent escalation
* Multi-keyword threat assessment

### Adaptive Trust-Aware Fusion

Combines:

* Machine Learning Risk
* Deception Risk
* Intent Risk

into a unified phishing risk score.

The framework includes:

* Dynamic profile switching
* Agreement boosting
* Context reinforcement
* Nonlinear risk fusion
* Adaptive risk promotion

### Explainable Risk Assessment

Provides:

* Final classification result
* Risk level indication
* Key phishing indicators
* Detection explanations
* URL summary information

---

## Dataset

The machine learning model was trained using a large-scale URL dataset compiled from multiple sources:

* PhishTank
* Tranco
* Additional Benign URL Sources

Dataset Statistics:

* Total URLs: 1,489,337
* Training Samples: 1,191,469
* Testing Samples: 297,868

---

## Engineered Feature Set

The framework extracts 18 handcrafted URL features grouped into:

### Lexical Features

* Character counts
* Token statistics
* URL composition metrics

### Structural Features

* Domain characteristics
* Subdomain characteristics
* TLD analysis

### Statistical Features

* Character entropy
* Digit ratio
* Uppercase ratio
* Vowel ratio

### Security Features

* HTTPS usage
* Suspicious keyword indicators

---

## System Architecture

![System Architecture](docs/architecture.png)

---

## Application Screenshots

### Home Interface

![Home Interface](screenshots/home_page.png)

### Phishing Detection Example

![Phishing Detection](screenshots/phishing_url_result.png)

### Legitimate URL Example

![Legitimate URL](screenshots/legitimate_url_result.png)

---

## Performance

Experimental evaluation achieved:

| Metric    | Value  |
| --------- | ------ |
| Accuracy  | 98.96% |
| Precision | 83.00% |
| Recall    | 93.95% |
| F1 Score  | 88.13% |

---

## Technology Stack

* Python
* XGBoost
* Scikit-Learn
* Pandas
* NumPy
* Streamlit
* tldextract

---

## Installation

Clone the repository:

```bash
git clone https://github.com/AdityaPansare1408/adaptive-phishing-url-detection-framework.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run src/streamlit_app.py
```

---

## Future Enhancements

* Browser extension deployment
* Real-time domain reputation lookup
* Threat intelligence integration
* Deep learning based URL analysis
* Cloud deployment

---

## Author

Aditya Pansare

M.Tech Computer Engineering
Pune Institute of Computer Technology (PICT)
