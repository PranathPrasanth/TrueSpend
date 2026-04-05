import openai
import os
openai.api_key=os.getenv("OPENAI_API_KEY")

def audit_expense(receipt_text, purpose, policy, category):
    prompt=f"""
    You are a strict corporate expense auditor.
    Expense category: {category}

    Receipt:
    {receipt_text}

    Purpose:
    {purpose}

    Policy:
    {policy}

    Evaluate:
    - Policy compliance
    - Amount limits
    - Violations

    Output strictly in this format:

    Decision: Approved / Flagged / Rejected
    Explanation: <one sentence>
    Policy Reference: <rule used>
    Confidence: <0 to 1>
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return {
        "result":response.choices[0].message.content,
        "category":category
    }