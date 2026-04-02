from fastapi import APIRouter, UploadFile, Form
from services.ocr_service import extract_text
from services.policy_service import get_relevant_policy
from services.ai_engine import audit_expense

router=APIRouter()

@router.post("/")
async def audit(file: UploadFile, purpose: str = Form(...)):
    receipt_text = extract_text(file)
    policy = get_relevant_policy(receipt_text)

    result = audit_expense(receipt_text,purpose,policy)
    return result