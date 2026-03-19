from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.session import SessionStore
router = APIRouter()
templates = Jinja2Templates(directory="templates")

USERS = {"admin": "admin123", "doctor": "clinic456"}

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = ""):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if USERS.get(username) == password:
        session_id = SessionStore.create(username)
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie("session_id", session_id, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid username or password"
    })

@router.get("/logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        SessionStore.delete(session_id)
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_id")
    return response