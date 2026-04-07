import streamlit as st
import requests

st.set_page_config(page_title="TrueSpend", page_icon="📊")

st.title("📊 TrueSpend")

# Upload + Input
uploaded_file = st.file_uploader("Upload Receipt", type=["png", "jpg", "pdf"])
purpose = st.text_input("Business Purpose")

# Button trigger
if st.button("Audit Expense"):
    if uploaded_file is None or purpose.strip() == "":
        st.warning("Please upload receipt and enter purpose")
    else:
        with st.spinner("Analyzing receipt... ⏳"):
            try:
                response = requests.post(
                    "http://localhost:8000/audit/",
                    files={"file": uploaded_file},
                    data={"purpose": purpose}
                )

                try:
    data = response.json()
except:
    st.error("Backend did not return valid JSON")
    st.stop()

                st.success("Audit completed ✅")

                # Category
                st.write("### 📌 Category")
                st.write(data.get("category", "N/A"))

                # Result (Color coded)
                st.write("### 📊 Result")
                result_text = data.get("result", "No result")

                if "Approved" in result_text:
                    st.success(result_text)
                elif "Rejected" in result_text or "Flagged" in result_text:
                    st.error(result_text)
                else:
                    st.info(result_text)

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")