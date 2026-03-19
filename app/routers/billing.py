from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from app.services.session import SessionStore
from app.data import BillingDB, PatientDB
router = APIRouter()

def get_user(request: Request):
    sid = request.cookies.get("session_id")
    return SessionStore.get(sid) if sid else None

@router.post("/billing/add")
async def add_bill(
    request: Request,
    patient_id: str = Form(...),
    amount: float = Form(...),
    status: str = Form(...),
    description: str = Form(...),
):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    patient = PatientDB.get(patient_id)
    patient_name = patient.name if patient else "Unknown"
    BillingDB.add(patient_id=patient_id, patient_name=patient_name, amount=amount, status=status, description=description)
    return RedirectResponse(url="/dashboard#billing", status_code=302)

@router.get("/billing/delete/{bill_id}")
async def delete_bill(bill_id: str, request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    BillingDB.delete(bill_id)
    return RedirectResponse(url="/dashboard#billing", status_code=302)

@router.get("/billing/status/{bill_id}/{new_status}")
async def update_status(bill_id: str, new_status: str, request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    if new_status in ("paid", "pending", "overdue"):
        BillingDB.update_status(bill_id, new_status)
    return RedirectResponse(url="/dashboard#billing", status_code=302)