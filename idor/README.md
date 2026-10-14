# Inkwell

A small blogging platform where writers publish posts in Markdown, add a cover
image, and choose whether each post is public or private.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# seed the database with sample accounts and posts
python -m app.seed

# start the server
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000

## Running with Docker

```bash
docker compose up --build
```

The container seeds the sample data automatically on first start and serves on
http://127.0.0.1:5008. The SQLite database and uploaded images are kept in named
volumes (`db`, `uploads`), so they survive restarts. To start completely fresh:

```bash
docker compose down -v
```

## Sample accounts

Created by `python -m app.seed`:

| username | password         |
|----------|------------------|
| admin    | Zephyr!nk-2024   |
| maya.r   | sunflower-fields |
| theo_k   | GoldenRetriever7 |
| nadia.w  | orchid.season.88 |

## API

Interactive reference: **http://127.0.0.1:8000/api/swagger** (Swagger UI).
ReDoc is at `/api/redoc` and the raw spec at `/api/openapi.json`.

- `POST /api/auth/register` — create an account
- `POST /api/auth/login` — sign in
- `POST /api/auth/logout` — sign out
- `GET  /api/users/me` — the signed-in user's profile
- `GET  /api/users` — directory of all users
- `GET  /api/users/{user_id}` — a user's details
- `GET  /api/users/{user_id}/posts` — posts by a given user
- `GET  /api/posts` — public feed
- `GET  /api/posts/mine` — your own posts
- `POST /api/posts` — publish a post (multipart form)
- `GET  /api/posts/{post_id}` — a single post
