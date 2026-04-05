import pdfplumber
import sqlite3
import spacy
from sentence_transformers import SentenceTransformer, util

nlp=spacy.load("en_core_web_sm")
model=SentenceTransformer('all-MiniLM-L6-v2')

<<<<<<< HEAD
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT=os.path.abspath(os.path.join(BASE_DIR, "../../"))
policy_path=os.path.join(PROJECT_ROOT, "data/policy.pdf")

=======
>>>>>>> 018ce99b814e6b083bfcd9dedbeec2e34e628f27
def load_policy_chunks():
    with pdfplumber.open("data/policy.pdf") as pdf:
        text=""
        for page in pdf.pages:
            text+=page.extract_text() or ""
<<<<<<< HEAD
            
=======
>>>>>>> 018ce99b814e6b083bfcd9dedbeec2e34e628f27
    chunks=[chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    return chunks
policy_chunks=load_policy_chunks()
policy_embeddings=model.encode(policy_chunks,convert_to_tensor=True)

def detect_category(text):
    doc=nlp(text.lower())

    keywords={
        "hotel":"accommodation",
        "stay":"accommodation",
        "restaurant":"food",
        "lunch":"food",
        "dinner":"food",
        "flight":"travel",
        "taxi":"travel",
        "uber":"travel"
    }

    for token in doc:
        if token.text in keywords:
            return keywords[token.text]
    
    return "other"

def get_policy_from_db(category):
    conn=sqlite3.connect("backend/db/policy.db")
    cursor=conn.cursor()

    cursor.execute("SELECT rule FROM policies WHERE category=?",(category,))
    result=cursor.fetchone()

    conn.close()

    return result[0] if result else None

def get_relevant_policy(receipt_text):
    category=detect_category(receipt_text)

    db_policy=get_policy_from_db(category)
    if db_policy:
        return db_policy, category
    
    receipt_embedding=model.encode(receipt_text, convert_to_tensor=True)
    scores=util.cos_sim(receipt_embedding, policy_embeddings)
    best_idx=scores.argmax()

    return policy_chunks[best_idx],category