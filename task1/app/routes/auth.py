from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.templates import TemplateResponse
from app.db import get_db
from app.auth import verify_password, hash_password, create_token, decode_token
from app.config import FLAG

router = APIRouter()

async def get_current_user(request: Request, db=Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    user = db.execute("SELECT * FROM users WHERE id = ?", (payload.get("sub"),)).fetchone()
    return user


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None, registered: bool = False):
    return await TemplateResponse("login.html", {"request": request, "error": error, "registered": registered})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user or not verify_password(password, user["password_hash"]):
        return await TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"}, status_code=401)
    token = create_token({"sub": user["id"]})
    response = RedirectResponse(url="/profile", status_code=303)
    response.set_cookie("access_token", token, httponly=True, max_age=60*24*7*60, samesite="lax")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, error: str = None):
    return await TemplateResponse("register.html", {"request": request, "error": error})


# Attributes a user record may carry. The registration form only exposes
# username/email/password, but the record itself also owns "role"
# (which defaults to "user").
USER_ATTRIBUTES = ("username", "email", "password_hash", "role")


@router.post("/register")
async def register(request: Request, db=Depends(get_db)):
    form = await request.form()

    username = form.get("username", "")
    email = form.get("email", "")
    password = form.get("password", "")
    confirm = form.get("confirm", "")

    if password != confirm:
        return await TemplateResponse("register.html", {"request": request, "error": "Passwords do not match"}, status_code=400)
    if len(password) < 8:
        return await TemplateResponse("register.html", {"request": request, "error": "Password must be at least 8 characters"}, status_code=400)

    # Build the new user record from the defaults...
    new_user = {
        "username": username,
        "email": email,
        "password_hash": hash_password(password),
        "role": "user",
    }

    # ...then merge in every field the client submitted (mass assignment).
    for key, value in form.items():
        if key in ("password", "confirm"):
            continue
        new_user[key] = value

    # Persist whatever attributes ended up on the record.
    columns = [c for c in new_user if c in USER_ATTRIBUTES]
    placeholders = ", ".join("?" for _ in columns)
    values = [new_user[c] for c in columns]
    try:
        db.execute(
            f"INSERT INTO users ({', '.join(columns)}) VALUES ({placeholders})",
            values,
        )
        db.commit()
    except Exception:
        return await TemplateResponse("register.html", {"request": request, "error": "Username or email already exists"}, status_code=400)
    return RedirectResponse(url="/login?registered=1", status_code=303)


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return await TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    granted = user["role"] == "admin"
    return await TemplateResponse(
        "admin.html",
        {"request": request, "granted": granted, "user": user, "flag": FLAG if granted else ""},
    )


@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response