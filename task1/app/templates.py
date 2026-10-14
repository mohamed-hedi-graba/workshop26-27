from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from starlette.responses import HTMLResponse
from starlette.requests import Request

BASE_DIR = Path(__file__).parent.parent

# Create Jinja2 environment directly to avoid caching bug
_env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=True,
    enable_async=True,
    cache_size=0,  # Disable cache entirely
)

async def TemplateResponse(name: str, context: dict, status_code: int = 200, headers: dict = None, media_type: str = "text/html"):
    template = _env.get_template(name)
    if "request" not in context:
        raise ValueError("context must include 'request'")
    content = await template.render_async(context)
    return HTMLResponse(content=content, status_code=status_code, headers=headers, media_type=media_type)