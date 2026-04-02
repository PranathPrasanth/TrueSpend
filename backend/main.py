from fastapi import FastAPI
from routes.audit import router as audit_router

app=FastAPI(title="TrueSpend")

app.include_router(audit_router,prefix="/audit")