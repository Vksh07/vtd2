# NeuroPrep Deployment

## Backend — Railway
1. Push repo to GitHub
2. Create new Railway project
3. Connect repo, set root to `backend/`
4. Railway auto-detects `railway.toml` and `Dockerfile`
5. After deploy, set env `PORT` if needed
6. Copy backend URL, e.g. `https://neuroprep-api.up.railway.app`

## Frontend — Vercel
1. Push repo to GitHub
2. Create new Vercel project
3. Set root to `frontend/`
4. Build command: `npm run build`
5. Output directory: `dist`
6. Add env var: `VITE_API_BASE = https://neuroprep-api.up.railway.app`
7. Deploy and copy frontend URL

## Post-Deploy
- Open frontend URL
- Test CSAT drill, ethics template, current affairs mapper
- If CORS issues arise, add backend CORS middleware for frontend origin
