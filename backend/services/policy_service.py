import pdfplumber
import sqlite3
import spacy
import os
from sentence_transformers import SentenceTransformer, util

# ------------------ LOAD MODELS ------------------
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

# ------------------ PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))

policy_path = os.path.join(PROJECT_ROOT, "data/policy.pdf")
db_path = os.path.join(PROJECT_ROOT, "backend/db/policy.db")

# ------------------ LOAD POLICY ------------------
def load_policy_chunks():
    try:
        with pdfplumber.open(policy_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""

        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        return chunks if chunks else ["Default policy: No rules found."]

    except Exception as e:
        print("Policy loading failed:", e)
        return ["Default policy: No rules found."]

# SAFE INITIALIZATION (VERY IMPORTANT)
try:
    policy_chunks = load_policy_chunks()
    policy_embeddings = model.encode(policy_chunks, convert_to_tensor=True)
except Exception as e:
    print("Embedding load failed:", e)
    policy_chunks = ["Default policy fallback."]
    policy_embeddings = model.encode(policy_chunks, convert_to_tensor=True)

# ------------------ CATEGORY DETECTION ------------------
def detect_category(text):
    doc = nlp(text.lower())

    keywords = {
        "hotel": "accommodation",
        "stay": "accommodation",
        "restaurant": "food",
        "lunch": "food",
        "dinner": "food",
        "flight": "travel",
        "taxi": "travel",
        "uber": "travel"
    }

    for token in doc:
        if token.text in keywords:
            return keywords[token.text]

    return "other"

# ------------------ DATABASE ACCESS ------------------
def get_policy_from_db(category):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT rule FROM policies WHERE category=?", (category,))
        result = cursor.fetchone()

        conn.close()

        return result[0] if result else None

    except Exception as e:
        print("DB error:", e)
        return None

# ------------------ MAIN FUNCTION ------------------
def get_relevant_policy(receipt_text):
    category = detect_category(receipt_text)

    # Step 1: DB lookup
    db_policy = get_policy_from_db(category)
    if db_policy:
        return db_policy, category

    # Step 2: Semantic search fallback
    try:
        receipt_embedding = model.encode(receipt_text, convert_to_tensor=True)
        scores = util.cos_sim(receipt_embedding, policy_embeddings)
        best_idx = scores.argmax()

        return policy_chunks[best_idx], category

    except Exception as e:
        print("Semantic search failed:", e)
        return "Default policy fallback.", category