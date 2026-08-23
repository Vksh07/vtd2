from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, csat, ethics, current_affairs

app = FastAPI(title="NeuroPrep API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])  
app.include_router(csat.router, prefix="/csat", tags=["csat"])  
app.include_router(ethics.router, prefix="/ethics", tags=["ethics"])  
app.include_router(current_affairs.router, prefix="/current-affairs", tags=["current-affairs"])  

@app.get("/")
def root():
    return {"app": "neuroprep", "status": "ok"}
