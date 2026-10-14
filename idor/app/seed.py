"""Populate the database with sample users and posts."""
from datetime import datetime, timedelta

from .database import Base, engine, SessionLocal
from .models import User, Post


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed():
    reset_db()
    db = SessionLocal()
    try:
        admin = User(
            username="admin",
            email="admin@inkwell.io",
            password="Zephyr!nk-2024",
            role="admin",
            bio="Keeping the lights on at Inkwell.",
            created_at=datetime(2023, 1, 9),
        )
        maya = User(
            username="maya.r",
            email="maya@inkwell.io",
            password="sunflower-fields",
            role="user",
            bio="Writing about cities, transit, and the people who move through them.",
            created_at=datetime(2023, 3, 14),
        )
        theo = User(
            username="theo_k",
            email="theo.kessler@fastmail.com",
            password="GoldenRetriever7",
            role="user",
            bio="Software, coffee, and the occasional long walk.",
            created_at=datetime(2023, 6, 2),
        )
        nadia = User(
            username="nadia.w",
            email="nadia.writes@proton.me",
            password="orchid.season.88",
            role="user",
            bio="Essays on books I can't stop thinking about.",
            created_at=datetime(2024, 1, 20),
        )
        db.add_all([admin, maya, theo, nadia])
        db.commit()
        for u in (admin, maya, theo, nadia):
            db.refresh(u)

        posts = [
            Post(
                author_id=maya.id,
                title="The quiet revolution of the 15-minute city",
                visibility="public",
                created_at=datetime(2024, 2, 11),
                content=(
                    "Cities are rediscovering a simple idea: that most of what you "
                    "need should be a short walk or bike ride away.\n\n"
                    "## Why proximity matters\n\n"
                    "When daily errands collapse into a small radius, something shifts. "
                    "Streets fill with people instead of traffic. Local shops survive. "
                    "Kids walk to school again.\n\n"
                    "> Distance is a tax we pay without noticing.\n\n"
                    "It isn't about banning cars. It's about making the car optional."
                ),
            ),
            Post(
                author_id=theo.id,
                title="I rewrote our build pipeline and learned to stop worrying",
                visibility="public",
                created_at=datetime(2024, 4, 3),
                content=(
                    "Our CI used to take 22 minutes. Now it takes four. Here's roughly "
                    "how that happened.\n\n"
                    "```bash\n# the offending step\nnpm run build && npm run test:all\n```\n\n"
                    "The fix wasn't clever caching. It was **deleting work we never needed "
                    "to do**. Half the test suite was re-testing vendored code.\n\n"
                    "Lesson: measure before you optimize, then delete before you cache."
                ),
            ),
            Post(
                author_id=nadia.id,
                title="On rereading the books that raised you",
                visibility="public",
                created_at=datetime(2024, 5, 19),
                content=(
                    "There's a particular vertigo in returning to a novel you loved at "
                    "seventeen.\n\n"
                    "The words haven't changed. You have. The passages you underlined now "
                    "feel earnest; the ones you skipped now feel like the whole point.\n\n"
                    "Rereading isn't nostalgia. It's a way of measuring the distance you've "
                    "traveled."
                ),
            ),
            Post(
                author_id=maya.id,
                title="Draft: notes on night buses",
                visibility="private",
                created_at=datetime(2024, 6, 1),
                content=(
                    "Unfinished. Collecting observations from the 2am routes before I shape "
                    "them into something.\n\n"
                    "- The driver who knows every regular by name\n"
                    "- The strange solidarity of the last bus home\n"
                    "- How the city sounds different when it's nearly empty"
                ),
            ),
            Post(
                author_id=theo.id,
                title="Weekend project: a tiny terminal dashboard",
                visibility="public",
                created_at=datetime(2024, 7, 22),
                content=(
                    "I wanted one screen that shows the weather, my next meeting, and "
                    "whether the trains are running. So I built it.\n\n"
                    "It's 200 lines of Python and a cron job. Nothing fancy. But opening a "
                    "terminal and seeing my whole morning at a glance has quietly become my "
                    "favorite part of the day."
                ),
            ),
            Post(
                author_id=admin.id,
                title="Internal: platform credentials and recovery notes",
                visibility="private",
                created_at=datetime(2024, 8, 30),
                content=(
                    "Private operational notes. Do not share.\n\n"
                    "Recovery key for the staging environment is stored here for the on-call "
                    "rotation:\n\n"
                    "```\nFLAG{1d0r_l3ts_y0u_r34d_wh4t_isnt_y0urs}\n```\n\n"
                    "Rotate after the next incident review."
                ),
            ),
        ]
        db.add_all(posts)
        db.commit()
        print("Seeded users:")
        for u in (admin, maya, theo, nadia):
            print(f"  {u.username:10s} id={u.id}  role={u.role}")
        print(f"\nSeeded {len(posts)} posts.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
