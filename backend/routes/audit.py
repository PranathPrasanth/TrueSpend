from fastapi import APIRouter, UploadFile, Form
from services.ocr_service import extract_text

router = APIRouter()

@router.post("/audit/")
async def audit_expense(file: UploadFile, purpose: str = Form(...)):
    try:
        # Step 1: OCR
        receipt_text = extract_text(file.file)
        print("OCR TEXT:", receipt_text)

        # ------------------ FORCE CATEGORY ------------------
        if any(word in receipt_text.lower() for word in ["restaurant", "food", "lunch", "dinner"]):
            category = "food"
        elif any(word in receipt_text.lower() for word in ["hotel", "stay"]):
            category = "accommodation"
        elif any(word in receipt_text.lower() for word in ["taxi", "uber", "flight"]):
            category = "travel"
        else:
            category = "other"

        # ------------------ FORCE RESULT ------------------
        if not receipt_text.strip():
            result = "Decision: Flagged\nExplanation: No text extracted"
        elif any(word in receipt_text.lower() for word in ["beer", "wine", "whiskey"]):
            result = "Decision: Flagged\nExplanation: Alcohol not allowed"
        else:
            result = "Decision: Approved\nExplanation: Expense looks valid"

        print("CATEGORY:", category)
        print("RESULT:", result)

        return {
            "category": category,
            "result": result
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "category": "error",
            "result": str(e)
        }