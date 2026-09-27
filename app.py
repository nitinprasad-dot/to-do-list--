"""
Vercel Serverless Entrypoint & Multi-Platform Handler for AchievePulse
Exports 'app', 'application', and 'handler' to satisfy Vercel's Python runtime.
Serves the Stlite WebAssembly application on Vercel while preserving direct Streamlit compatibility.
"""
from http.server import BaseHTTPRequestHandler
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1. Streamlit Execution Hook
# If launched via `streamlit run app.py`, delegate to streamlit_app.py
# ---------------------------------------------------------------------------
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    if get_script_run_ctx() is not None:
        target_script = os.path.join(CURRENT_DIR, "streamlit_app.py")
        if os.path.exists(target_script):
            with open(target_script, "r", encoding="utf-8") as _f:
                exec(compile(_f.read(), target_script, "exec"), globals())
except Exception:
    pass

# ---------------------------------------------------------------------------
# 2. Vercel File Delivery & Routing
# ---------------------------------------------------------------------------
def get_file_response(request_path, headers=None):
    orig_path = request_path or ""
    if headers:
        orig_path = (
            headers.get("x-matched-path")
            or headers.get("x-vercel-matched-path")
            or request_path
            or ""
        )

    clean_path = orig_path.split("?")[0].lstrip("/")

    if "streamlit_app.py" in clean_path:
        target = "streamlit_app.py"
        mime = "text/plain; charset=utf-8"
    elif clean_path.endswith(".css"):
        target = clean_path
        mime = "text/css; charset=utf-8"
    elif clean_path.endswith(".js"):
        target = clean_path
        mime = "application/javascript; charset=utf-8"
    elif clean_path.endswith(".json"):
        target = clean_path
        mime = "application/json; charset=utf-8"
    elif clean_path.endswith(".png"):
        target = clean_path
        mime = "image/png"
    elif clean_path.endswith(".svg"):
        target = clean_path
        mime = "image/svg+xml"
    elif clean_path.endswith(".ico"):
        target = clean_path
        mime = "image/x-icon"
    else:
        # Default for root (''), /app.py, /index.html, or any web navigation:
        target = "index.html"
        mime = "text/html; charset=utf-8"

    file_path = os.path.join(CURRENT_DIR, target)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        return 200, mime, content

    # Fallback to index.html for any SPA navigation
    fallback_path = os.path.join(CURRENT_DIR, "index.html")
    if os.path.exists(fallback_path):
        with open(fallback_path, "rb") as f:
            content = f.read()
        return 200, "text/html; charset=utf-8", content

    return 404, "text/plain; charset=utf-8", b"404 Not Found"

# ---------------------------------------------------------------------------
# 3. WSGI Handler (Exports 'app' and 'application')
# ---------------------------------------------------------------------------
def app(environ, start_response):
    path = environ.get("PATH_INFO", "")
    headers = {
        "x-matched-path": environ.get("HTTP_X_MATCHED_PATH", ""),
        "x-vercel-matched-path": environ.get("HTTP_X_VERCEL_MATCHED_PATH", ""),
    }
    status_code, mime, content = get_file_response(path, headers)
    status_str = "200 OK" if status_code == 200 else "404 Not Found"
    res_headers = [
        ("Content-Type", mime),
        ("Content-Length", str(len(content))),
        ("Content-Disposition", "inline"),
        ("Cache-Control", "public, max-age=0, must-revalidate"),
    ]
    start_response(status_str, res_headers)
    return [content]

application = app

# ---------------------------------------------------------------------------
# 4. BaseHTTPRequestHandler (Exports 'handler')
# ---------------------------------------------------------------------------
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status_code, mime, content = get_file_response(self.path, self.headers)
        self.send_response(status_code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Content-Disposition", "inline")
        self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        return
