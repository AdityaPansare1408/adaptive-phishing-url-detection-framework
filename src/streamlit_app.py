import streamlit as st
import pickle
import numpy as np

from feature_extraction import extract_all_features
from deception_analysis_engine import get_deception_score
from intent_analysis_engine import compute_intent_score
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "xgb_model.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


FEATURE_COLUMNS = sorted([
    'domain_length','subdomain_length','tld_length','count_dots','count_hyphens',
    'count_underscores','count_letters','count_digits','ratio_digits','ratio_uppercase',
    'vowel_ratio','avg_token_len','max_token_len','char_entropy','has_https',
    'suspicious_in_path','suspicious_in_subdomain','suspicious_in_domain'
])


def compute_final_score(ml_prob, imp_score, ctx_score):

    ml_risk = ml_prob ** 1.1

    score = (
        0.30 * ml_risk +
        0.45 * imp_score +
        0.25 * ctx_score
    )

    score += 0.12 * (imp_score * ctx_score)

    if imp_score > 0.3 and ctx_score > 0.3:
        score += 0.12

    if ctx_score >= 0.3:
        score += 0.05


    if imp_score >= 0.55:
        score = max(score, 0.65)

    if imp_score >= 0.45 and ctx_score >= 0.3:
        score = max(score, 0.60)

   
    if ml_risk >= 0.65 and ctx_score >= 0.3:
        score = max(score, 0.60)


    if deception_score >= 0.65:

        adaptive_score = (
            0.15 * ml_risk +
            0.65 * deception_score +
            0.20 * intent_score
        )

        
        score = max(score, adaptive_score)


    
    elif intent_score >= 0.55 and deception_score < 0.45:

        adaptive_score = (
            0.20 * ml_risk +
            0.55 * ctx_score +
            0.25 * imp_score
        )

       
        score = max(score, adaptive_score)



    return max(0, min(score, 1))


def classify(score):
    if score >= 0.45:
        return "Phishing"
    elif score >= 0.35:
        return "Suspicious"
    else:
        return "Legitimate"



st.set_page_config(page_title="Phishing URL Detector", layout="centered")

st.title("🔐 Phishing URL Detection System")
st.caption("Smart detection using multiple security signals")

url = st.text_input("Enter URL")

if st.button("Analyze"):

    if not url:
        st.warning("Please enter a URL")
        st.stop()

    
    features_dict = extract_all_features(url)
    features_list = [features_dict[col] for col in FEATURE_COLUMNS]
    features_array = np.array(features_list).reshape(1, -1)

   
    ml_prob = float(model.predict_proba(features_array)[0][1])

    
    deception_score, deception_reasons = get_deception_score(url)
    intent_score, intent_reasons = compute_intent_score(url)

    deception_score = float(deception_score)
    intent_score = float(intent_score)

    
    final_score = compute_final_score(ml_prob, deception_score, intent_score)
    decision = classify(final_score)

    
    st.markdown("## 🔍 Result")

    if decision == "Phishing":
        st.error("⚠️ High Risk: Phishing URL Detected")
        risk_label = "High"
    elif decision == "Suspicious":
        st.warning("⚠️ Medium Risk: Suspicious URL")
        risk_label = "Medium"
    else:
        st.success("✅ Low Risk: Legitimate URL")
        risk_label = "Low"

    
    st.progress(final_score)
    st.caption(f"Risk Level: {risk_label}")

   
    st.markdown("### 🔎 Key Indicators")

    indicators = []

    if deception_score > 0.5:
        indicators.append("Domain resembles a well-known brand")

    if intent_score > 0.4:
        indicators.append("Contains suspicious or phishing-related keywords")

    if deception_score > 0.3 and intent_score > 0.3:
        indicators.append("Combination of deception and suspicious intent")

    if not indicators:
        indicators.append("No strong phishing indicators detected")

    for i in indicators:
        st.write(f"- {i}")

    
    st.markdown("### 📄 URL Summary")

    domain = url.replace("http://", "").replace("https://", "").split("/")[0]

    st.write(f"**Domain:** {domain}")
    st.write(f"**Length:** {len(url)}")
    st.write(f"**Contains Numbers:** {any(c.isdigit() for c in url)}")
    st.write(f"**Subdomains:** {domain.count('.') - 1 if domain.count('.') > 1 else 0}")

    
    with st.expander("🧠 Why this was flagged"):

        reasons = list(set(deception_reasons + intent_reasons))

        if reasons:
            for r in reasons:
                st.write(f"- {r}")
        else:
            st.write("- No detailed indicators found")