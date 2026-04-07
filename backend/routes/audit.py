from fastapi import APIRouter, UploadFile, File, Form
from services.ocr_service import extract_text
from services.policy_service import evaluate_policy

router = APIRouter()

@router.post("/audit/")
async def audit_expense(file: UploadFile = File(...), purpose: str = Form(...)):
    try:
        contents = await file.read()

        receipt_text = extract_text(contents)
        print("OCR TEXT:", receipt_text)

        # Handle OCR failure
        if receipt_text in ["EMPTY_OCR", "ERROR"]:
            return {
                "category": "unknown",
                "result": "Receipt is unclear or unreadable"
            }

        result = evaluate_policy(receipt_text, purpose)
        print("FINAL RESULT:", result)

        # Ensure proper JSON response
        return {
            "category": result.get("category", "unknown"),
            "result": result.get("result", "No result")
        }

    except Exception as e:
        print("AUDIT ERROR:", str(e))
        return {
            "category": "error",
            "result": f"Backend crashed: {str(e)}"
        }