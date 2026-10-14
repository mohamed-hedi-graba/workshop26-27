import os

import markdown2
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Post, User
from .routers import auth, users, posts
from .security import get_optional_user

BASE_DIR = os.path.dirname(__file__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inkwell API",
    description="Inkwell — a blogging platform. Interactive API reference.",
    version="1.0.0",
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


def render_md(text: str) -> str:
    return markdown2.markdown(
        text or "",
        extras=["fenced-code-blocks", "tables", "strike", "break-on-newline"],
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request, db: Session = Depends(get_db), user=Depends(get_optional_user)):
    feed = (
        db.query(Post)
        .filter(Post.visibility == "public")
        .order_by(Post.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": user, "posts": feed}
    )


@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request, user=Depends(get_optional_user)):
    return templates.TemplateResponse("login.html", {"request": request, "user": user})


@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_page(request: Request, user=Depends(get_optional_user)):
    return templates.TemplateResponse("register.html", {"request": request, "user": user})


@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request, db: Session = Depends(get_db), user=Depends(get_optional_user)):
    if user is None:
        return templates.TemplateResponse(
            "login.html", {"request": request, "user": None, "redirect": True}
        )
    mine = (
        db.query(Post)
        .filter(Post.author_id == user.id)
        .order_by(Post.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user, "posts": mine}
    )


@app.get("/new", response_class=HTMLResponse, include_in_schema=False)
def new_post_page(request: Request, user=Depends(get_optional_user)):
    if user is None:
        return templates.TemplateResponse(
            "login.html", {"request": request, "user": None, "redirect": True}
        )
    return templates.TemplateResponse("new_post.html", {"request": request, "user": user})


@app.get("/profile", response_class=HTMLResponse, include_in_schema=False)
def profile_page(request: Request, user=Depends(get_optional_user)):
    if user is None:
        return templates.TemplateResponse(
            "login.html", {"request": request, "user": None, "redirect": True}
        )
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@app.get("/authors", response_class=HTMLResponse, include_in_schema=False)
def authors_page(request: Request, db: Session = Depends(get_db), user=Depends(get_optional_user)):
    all_users = db.query(User).order_by(User.username).all()
    return templates.TemplateResponse(
        "authors.html", {"request": request, "user": user, "authors": all_users}
    )


@app.get("/posts/{post_id}", response_class=HTMLResponse, include_in_schema=False)
def post_page(post_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_optional_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    author = db.query(User).filter(User.id == post.author_id).first()
    return templates.TemplateResponse(
        "post_detail.html",
        {
            "request": request,
            "user": user,
            "post": post,
            "author": author,
            "content_html": render_md(post.content),
        },
    )
