from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic
import uvicorn

from app.routers import auth, patients, billing
from app.services.session import SessionStore

app = FastAPI(title="CDSS - Clinical Decision Support System")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(billing.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id and SessionStore.get(session_id):
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)