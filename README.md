# HireReady

HireReady is a Smart Placement Tracker and Prep Portal with a separated architecture:

- `frontend/` for UI pages and client-side scripts
- `backend/` for Flask APIs, business logic, and database access

## Quick Start

### 1) Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs at `http://127.0.0.1:5000`.

### 2) Frontend

Open `frontend/index.html` in a browser or serve `frontend/` with a static server.

## Phase 1 Status

- Separated frontend/backend structure created
- Flask app factory and baseline routes added
- Frontend shell and initial routes/pages scaffolded
# HireReady
