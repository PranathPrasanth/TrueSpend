from pydantic import BaseModel

class AuditResponse(BaseModel):
    category: str
    result: str