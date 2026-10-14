from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn

from app.db import init_db
from app.routes.landing import router as landing_router
from app.routes.auth import router as auth_router

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Securinets Web Pentesting Workshop")

# Initialize database on startup
init_db()

# Static files
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Routers
app.include_router(landing_router)
app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)