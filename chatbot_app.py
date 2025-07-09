import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Title
st.title("🩺 Ninette Medical Assistant")
st.write("Upload or write patient lab results to get an explanation and medical recommendations.")

# File uploader
uploaded_file = st.file_uploader("📤 Upload Lab Results (CSV)", type=["csv"])

# Text area for manual input
manual_input = st.text_area("✍️ Or Type/Paste Lab Results (example: 'Blood Pressure: 145/90, Blood Sugar: 180 mg/dL')")

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": message}
        ],
        temperature=0.5,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']

# If CSV is uploaded
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Patient Lab Results")
    st.dataframe(df)

    if st.button("🧠 Analyze Uploaded Results"):
        with st.spinner("Analyzing..."):
            prompt = f"""
You are Ninette medical assistant helping a doctor. Analyze the following lab results and provide:
1. A simple explanation of what the results mean.
2. Medical recommendations based on the values.

Results:
{df.to_string(index=False)}
"""
            result = ask_openai(prompt)
            st.subheader("📌 AI Explanation and Recommendation")
            st.write(result)

# If manual text is provided
elif manual_input.strip() != "":
    if st.button("🧠 Analyze Typed Results"):
        with st.spinner("Analyzing..."):
            prompt = f"""
You are a medical assistant helping a doctor. Analyze the following manually entered lab results and provide:
1. A simple explanation of what the results mean.
2. Medical recommendations based on the values.

Results:
{manual_input}
"""
            result = ask_openai(prompt)
            st.subheader("📌 AI Explanation and Recommendation")
            st.write(result)
