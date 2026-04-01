# 🚀 TrueSpend — Context-Aware Expense Auditor

## 📌 Problem
Corporate finance teams manually verify employee expense receipts against lengthy policy documents. This process is slow, inconsistent, and error-prone, leading to delayed reimbursements and policy violations (spend leakage).

## 💡 Solution
TrueSpend automates expense auditing by:
- Extracting data from receipts using OCR
- Understanding employee intent through natural language input
- Cross-referencing expenses with company policy using AI
- Providing instant decisions with clear explanations

---

## ⚙️ Features

### 1. Receipt & Narrative Ingestion
- Upload receipts (JPG, PNG, PDF)
- Extract:
  - Merchant Name
  - Date
  - Amount
  - Currency
- Input business purpose
- Detect blurry or invalid uploads

### 2. Automated Policy Audit Engine
- Reads policy documents
- Matches expense with relevant policy rules
- Outputs:
  - ✅ Approved
  - ⚠️ Flagged
  - ❌ Rejected
- Provides:
  - Explanation
  - Policy reference

### ⭐ Bonus Features
- Confidence Score
- Risk Level (Low / Medium / High)
- Explainable AI reasoning

---

## 🏗️ Architecture

Frontend → FastAPI Backend → AI Engine → Policy Matching → Decision Output

---

## 🛠️ Tech Stack

### Backend
- Python (FastAPI)

### Frontend
- Streamlit

### AI / NLP
- OpenAI GPT API
- Sentence Transformers

### OCR
- Tesseract OCR

### Database
- SQLite

---

## 🚀 Setup Instructions

### 1. Clone Repo
```bash
git clone <your-repo-link>
cd policylens-ai
