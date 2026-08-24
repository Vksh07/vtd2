# NeuroPrep (VTD#2)

UPSC CSAT + Ethics + Current Affairs prep tool.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

```bash
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8001

## Features

- CSAT drill with timer, scoring, weak/strong topics
- Ethics template generator
- Current affairs mapper

## Deploy

- Backend: Railway, root = backend/, builder = dockerfile, start = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Frontend: Vercel, root = frontend/, build = `npm run build`, output = `dist`
