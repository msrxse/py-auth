# py-auth

FastAPI authentication & authorization showcase.

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

API available at http://localhost:8000

Health check: http://localhost:8000/health
