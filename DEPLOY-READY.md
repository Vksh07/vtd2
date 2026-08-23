# NeuroPrep — Deploy Ready

## What’s ready
- Backend API: `/health`, `/csat/drill`, `/ethics/template`, `/current-affairs/map`
- Frontend: Home, CSAT, Ethics, Current Affairs tabs
- Local profile + score history via localStorage
- Production build in `frontend/dist`
- Deployment configs: `backend/Dockerfile`, `backend/railway.toml`, `frontend/vercel.json`

## Exact next steps
1. Push `vtd2/` repo to GitHub
2. Railway: connect repo, root = `backend/`
3. Vercel: connect repo, root = `frontend/`, env `VITE_API_BASE` = Railway URL
4. Open frontend and verify all tabs end-to-end

## Note
Local dev is healthy, but the live URL is the only real validation. I can assist with the GitHub/Railway/Vercel steps once you’re ready.
