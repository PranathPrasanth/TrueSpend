from fastapi import APIRouter, UploadFile, Form
from services.ocr_service import extract_text
from services.policy_service import get_relevant_policy

router = APIRouter()

@router.post("/audit/")
async def audit_expense(file: UploadFile, purpose: str = Form(...)):
    try:
        # Step 1: Extract text from receipt
        receipt_text = extract_text(file.file)
        print("OCR TEXT:", receipt_text)

        # Step 2: Get relevant policy + category
        policy, category = get_relevant_policy(receipt_text)

        # Step 3: Simple decision logic (stable for demo)
        if "alcohol" in receipt_text.lower():
            result = "Decision: Flagged\nExplanation: Alcohol expenses are not reimbursable"
        else:
            result = "Decision: Approved\nExplanation: Expense complies with company policy"

        # Step 4: Return response
        return {
            "category": category,
            "result": result
        }

    except Exception as e:
        print("BACKEND ERROR:", e)

        # Always return JSON (prevents frontend crash)
        return {
            "category": "error",
            "result": f"Backend failed: {str(e)}"
        }