# VTD#2 NeuroPrep — Deploy Instructions

## Prerequisite
- Create GitHub repo first and share the exact repo URL.

## Step 1: Add remote and push
```bash
cd vtd2
git remote add origin <EXACT_GITHUB_REPO_URL>
git push -u origin master
```

## Step 2: Railway (backend)
- Connect the GitHub repo.
- Set root directory to: `backend/`
- Railway should auto-detect `railway.toml` and `Dockerfile`.
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- After deploy, copy backend URL, e.g. `https://neuroprep-api.up.railway.app`

## Step 3: Vercel (frontend)
- Connect the same GitHub repo.
- Set root directory to: `frontend/`
- Build command: `npm run build`
- Output directory: `dist`
- Add environment variable: `VITE_API_BASE = https://<your-railway-backend-url>`
- Deploy and copy frontend URL.

## Step 4: Verify
- Backend health: `curl <backend-url>/health/`
- Frontend: open frontend URL and test CSAT, Ethics, Current Affairs tabs.
- If CORS issues arise, add backend CORS middleware for frontend origin.
