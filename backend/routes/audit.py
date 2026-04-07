from fastapi import APIRouter, UploadFile, Form
from services.ocr_service import extract_text
from services.policy_service import get_relevant_policy

router = APIRouter()

@router.post("/audit/")
async def audit_expense(file: UploadFile, purpose: str = Form(...)):
    try:
        # ------------------ STEP 1: OCR ------------------
        receipt_text = extract_text(file.file)
        print("OCR TEXT:", receipt_text)

        # ------------------ STEP 2: POLICY FETCH ------------------
        policy_data = get_relevant_policy(receipt_text)

        if policy_data is None:
            category = "other"
            policy = "No policy found"
        else:
            policy, category = policy_data

        print("CATEGORY:", category)
        print("POLICY:", policy)

        # ------------------ STEP 3: DECISION LOGIC ------------------
        if not receipt_text.strip():
            result = "Decision: Flagged\nExplanation: No text extracted from receipt"

        elif any(word in receipt_text.lower() for word in ["beer", "wine", "whiskey", "vodka"]):
            result = "Decision: Flagged\nExplanation: Alcohol expenses are not allowed"

        elif "hotel" in receipt_text.lower():
            result = "Decision: Approved\nExplanation: Accommodation expense within policy"

        elif any(word in receipt_text.lower() for word in ["restaurant", "food", "lunch", "dinner"]):
            result = "Decision: Approved\nExplanation: Meal expense is valid"

        else:
            result = "Decision: Approved\nExplanation: Expense appears valid"

        # ------------------ STEP 4: RESPONSE ------------------
        return {
            "category": category if category else "other",
            "result": result
        }

    except Exception as e:
        print("BACKEND ERROR:", e)

        return {
            "category": "error",
            "result": f"Backend failed: {str(e)}"
        }