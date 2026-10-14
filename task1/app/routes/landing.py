from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templates import TemplateResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return await TemplateResponse("index.html", {"request": request})