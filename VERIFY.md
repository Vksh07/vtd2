# NeuroPrep Local Verification

## Backend
- [ ] `curl http://127.0.0.1:8001/health/` returns `{"status":"ok"}`
- [ ] `curl -X POST http://127.0.0.1:8001/csat/drill -H 'Content-Type: application/json' -d '{"topic":"General","count":3}'` returns questions
- [ ] `curl -X POST http://127.0.0.1:8001/ethics/template -H 'Content-Type: application/json' -d '{"question":"General ethics"}'` returns template
- [ ] `curl -X POST http://127.0.0.1:8001/current-affairs/map -H 'Content-Type: application/json' -d '{"headline":"India space policy"}'` returns mapping

## Frontend
- [ ] Open `http://127.0.0.1:5173`
- [ ] Home: save profile and see recent drill history
- [ ] CSAT: select topic + count, start drill, choose answers, submit, see score
- [ ] Ethics: generate template and see intro/body/conclusion
- [ ] Current Affairs: enter headline, map, see GS mapping + outline + keywords

## Notes
- If frontend uses another port, update base URL accordingly.
- For deployed Railway backend, set `VITE_API_BASE` in Vercel env.
