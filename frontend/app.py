import streamlit as st
import requests

st.title("📊 TrueSpend")

uploaded_file=st.file_uploader("Upload Receipt", type=["png","jpg","pdf"])
purpose=st.text_input("Business Purpose")

if st.button("Audit Expense"):
    if uploaded_file is None or purpose.strip()=="":
        st.warning("Please upload receipt and enter purpose")
    else:
        response=requests.post("http://localhost:8000/audit/",
                          files={"file":uploaded_file},
                          data={"purpose":purpose}
                          )
        data=response.json()

        st.success("Audit completed")

        st.write("### 📌 Category")
        st.write(data.get("category","N/A"))

        st.write("### 📊 Result")
        st.text(data.get("result","No result"))

if "Approved" in data.get("result", ""):
    st.success(data["result"])
else:
    st.error(data["result"])