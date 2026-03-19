from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.session import SessionStore
from app.data import PatientDB, BillingDB
from app.services.ai_engine import get_suggestions

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_user(request: Request):
    sid = request.cookies.get("session_id")
    return SessionStore.get(sid) if sid else None

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    patients = PatientDB.all()
    bills = BillingDB.all()
    total_revenue = sum(b.amount for b in bills if b.status == "paid")
    pending_amount = sum(b.amount for b in bills if b.status == "pending")
    overdue_amount = sum(b.amount for b in bills if b.status == "overdue")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "username": user["username"],
        "patients": patients,
        "bills": bills,
        "total_revenue": total_revenue,
        "pending_amount": pending_amount,
        "overdue_amount": overdue_amount,
        "patient_count": len(patients),
    })

@router.post("/patients/add")
async def add_patient(request: Request, name: str = Form(...), age: int = Form(...), disease: str = Form(...)):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    PatientDB.add(name=name, age=age, disease=disease)
    return RedirectResponse(url="/dashboard#patients", status_code=302)

@router.get("/patients/delete/{patient_id}")
async def delete_patient(patient_id: str, request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    PatientDB.delete(patient_id)
    return RedirectResponse(url="/dashboard#patients", status_code=302)

@router.get("/patients/{patient_id}/ai", response_class=HTMLResponse)
async def ai_suggestion(patient_id: str, request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    patient = PatientDB.get(patient_id)
    if not patient:
        return RedirectResponse(url="/dashboard", status_code=302)
    suggestion = get_suggestions(patient.disease)
    return templates.TemplateResponse("ai_panel.html", {
        "request": request,
        "username": user["username"],
        "patient": patient,
        "suggestion": suggestion,
    })