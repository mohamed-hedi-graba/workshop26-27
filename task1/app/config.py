from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
# SQLite location (overridable via env so a Docker volume can persist it)
DB_PATH = Path(os.environ.get("SECURINETS_DB", BASE_DIR / "securinets_auth.db"))

SECRET_KEY = os.environ.get("SECURINETS_SECRET", "securinets-workshop-secret-change-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

# Flag revealed on the admin dashboard (overridable via env for deployments)
FLAG = os.environ.get("SECURINETS_FLAG", "Securinets{m4ss_4ss1gnm3nt_r0l3_3sc4l4t10n}")