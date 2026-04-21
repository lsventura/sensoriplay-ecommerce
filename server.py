"""
SensoriPlay entrypoint — mounts static frontend on top of the FastAPI backend.
Does NOT modify backend/main.py. Just adds StaticFiles mounts at the root.
"""
import os, sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# backend/main.py does "import database" — add backend to path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "backend"))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.main import app

# Mount static directories
app.mount("/assets", StaticFiles(directory=ROOT / "assets"), name="assets")
app.mount("/admin", StaticFiles(directory=ROOT / "admin", html=True), name="admin")
app.mount("/auth", StaticFiles(directory=ROOT / "auth", html=True), name="auth")
app.mount("/pages", StaticFiles(directory=ROOT / "pages", html=True), name="pages")

# Root: serve index.html
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(ROOT / "index.html")

# Favicon fallback
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    favicon_path = ROOT / "assets" / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(favicon_path)
    return FileResponse(ROOT / "assets" / "sensori-play-logo.png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8090, reload=False)
