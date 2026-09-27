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
# 2. Vercel Static / Serverless File Delivery
# ---------------------------------------------------------------------------
def get_file_response(request_path):
    clean_path = request_path.split("?")[0].lstrip("/")
    if clean_path in ("", "index.html"):
        target = "index.html"
        mime = "text/html; charset=utf-8"
    elif clean_path == "streamlit_app.py":
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
    else:
        target = clean_path
        mime = "application/octet-stream"

    file_path = os.path.join(CURRENT_DIR, target)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        return 200, mime, content
    return 404, "text/plain; charset=utf-8", b"404 Not Found"

# ---------------------------------------------------------------------------
# 3. WSGI Handler (Exports 'app' and 'application')
# ---------------------------------------------------------------------------
def app(environ, start_response):
    path = environ.get("PATH_INFO", "")
    status_code, mime, content = get_file_response(path)
    status_str = "200 OK" if status_code == 200 else "404 Not Found"
    headers = [
        ("Content-Type", mime),
        ("Content-Length", str(len(content))),
        ("Cache-Control", "public, max-age=0, must-revalidate"),
    ]
    start_response(status_str, headers)
    return [content]

application = app

# ---------------------------------------------------------------------------
# 4. BaseHTTPRequestHandler (Exports 'handler')
# ---------------------------------------------------------------------------
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        status_code, mime, content = get_file_response(self.path)
        self.send_response(status_code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "public, max-age=0, must-revalidate")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        return
