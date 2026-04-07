from fastapi import APIRouter, UploadFile, Form
from services.ocr_service import extract_text
from services.policy_service import get_relevant_policy
from services.ai_engine import audit_expense
from services.validator import validate_receipt
from models.schemas import AuditResponse

router=APIRouter()

@router.post("/")

async def audit(file: UploadFile, purpose: str = Form(...)):
    receipt_text = extract_text(file)
    print("OCR TEXT:", receipt_text)
    
    valid,message=validate_receipt(receipt_text)

    if not valid:
        return {
            "category":"unknown",
            "result":f"Decision: Flagged\nExplanation: {message}"
        }

    policy,category = get_relevant_policy(receipt_text)
    
    result = audit_expense(receipt_text,purpose,policy,category)
    
    return result