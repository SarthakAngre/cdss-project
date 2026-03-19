# 🏥 CDSS — Clinical Decision Support System

A production-grade FastAPI web app with login, patient management, billing, and AI-powered clinical suggestions.

## 📁 Folder Structure

```
cdss/
├── main.py                    # App entry point
├── requirements.txt
├── models/
│   ├── __init__.py
│   └── data.py                # Patient & Billing data models + in-memory DB
├── routers/
│   ├── __init__.py
│   ├── auth.py                # Login / Logout
│   ├── patients.py            # Patient CRUD + dashboard
│   └── billing.py             # Billing CRUD + status update
├── services/
│   ├── __init__.py
│   ├── session.py             # In-memory session store
│   └── ai_engine.py           # Rule-based clinical AI engine
├── templates/
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard (patients + billing)
│   └── ai_panel.html          # AI suggestion panel per patient
└── static/
    └── css/                   # (optional custom CSS)
```

## 🚀 Setup & Run

```bash
cd cdss
pip install -r requirements.txt
python main.py
# → Open http://localhost:8000
```

## 🔐 Login Credentials

| Username | Password   |
|----------|------------|
| admin    | admin123   |
| doctor   | clinic456  |

## 🧠 AI Engine — Supported Diseases

The rule-based AI engine (`services/ai_engine.py`) has built-in protocols for:

- Diabetes
- Hypertension
- Pneumonia
- Asthma
- Depression
- Heart Failure
- Tuberculosis
- Anemia
- Any other disease → general protocol

Each protocol returns:
- Clinical recommendations (6 steps)
- Drug & safety alerts
- Follow-up schedule
- Severity classification

## 🛠 Tech Stack

- **FastAPI** — Backend framework
- **Jinja2** — HTML templating
- **Uvicorn** — ASGI server
- **Python** — No database required (in-memory storage)

## 📌 Features

| Feature             | Details                                              |
|---------------------|------------------------------------------------------|
| Auth                | Session-cookie login/logout, multi-user              |
| Patient Management  | Add, list, delete patients with disease tags         |
| Billing System      | Add bills, change status (paid/pending/overdue)      |
| AI Suggestions      | Disease-specific clinical protocols + drug warnings  |
| Dashboard KPIs      | Patient count, revenue, pending, overdue totals      |