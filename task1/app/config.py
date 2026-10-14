from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "securinets_auth.db"

SECRET_KEY = "securinets-workshop-secret-change-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

# Flag revealed on the admin dashboard (overridable via env for deployments)
FLAG = os.environ.get("SECURINETS_FLAG", "SECURINETS{m4ss_4ss1gnm3nt_r0l3_3sc4l4t10n}")