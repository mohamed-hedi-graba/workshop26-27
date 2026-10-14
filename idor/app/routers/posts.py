import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Post, User
from ..schemas import PostOut
from ..security import get_current_user

router = APIRouter(prefix="/api/posts", tags=["posts"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "uploads")
ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


@router.get("", response_model=List[PostOut])
@router.get("/", response_model=List[PostOut])
def public_feed(db: Session = Depends(get_db)):
    return (
        db.query(Post)
        .filter(Post.visibility == "public")
        .order_by(Post.created_at.desc())
        .all()
    )


@router.get("/mine", response_model=List[PostOut])
def my_posts(current: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Post)
        .filter(Post.author_id == current.id)
        .order_by(Post.created_at.desc())
        .all()
    )


@router.post("", response_model=PostOut)
@router.post("/", response_model=PostOut)
def create_post(
    title: str = Form(...),
    content: str = Form(""),
    visibility: str = Form("public"),
    image: Optional[UploadFile] = File(None),
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if visibility not in ("public", "private"):
        visibility = "public"

    image_path = None
    if image is not None and image.filename:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in ALLOWED_EXT:
            raise HTTPException(status_code=400, detail="Unsupported image type")
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        fname = f"{uuid.uuid4().hex}{ext}"
        dest = os.path.join(UPLOAD_DIR, fname)
        with open(dest, "wb") as f:
            f.write(image.file.read())
        image_path = f"/static/uploads/{fname}"

    post = Post(
        author_id=current.id,
        title=title,
        content=content,
        visibility=visibility,
        image_path=image_path,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
