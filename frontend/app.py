import streamlit as st
import requests

API_URL = "https://truespend.onrender.com"

st.set_page_config(
    page_title="TrueSpend",
    page_icon="💳",   # or "📊", "💰", etc.
    layout="centered"
)

st.title("📊 TrueSpend")

uploaded_file = st.file_uploader("Upload Receipt", type=["png", "jpg", "jpeg", "pdf"])
purpose = st.text_input("Business Purpose")

if st.button("Audit Expense"):
    if uploaded_file is None or purpose.strip() == "":
        st.warning("Please upload receipt and enter purpose")
    else:
        try:
            response = requests.post(
                "https://truespend.onrender.com/audit",
                files={"file": uploaded_file},
                data={"purpose": purpose}
            )

            data = response.json()

            st.success("Audit completed")

            st.write("### 📌 Category")
            st.write(data.get("category", "N/A"))

            st.write("### 📊 Result")
            st.write(data.get("result", "No result"))

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")