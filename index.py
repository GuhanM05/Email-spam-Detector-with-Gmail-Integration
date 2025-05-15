
import streamlit as st
from rf_predict import predict_rf
import shap

st.title("Spam Detector App")

email_text = st.text_area("Paste your email content:")
if st.button("Analyze"):
    if email_text.strip():
        result, score = predict_rf(email_text)
        st.write(f"Prediction: **{result.upper()}** with confidence {score:.2f}")
        st.info("SHAP explanation would go here (visuals not shown in this demo).")
