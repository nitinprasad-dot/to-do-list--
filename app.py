"""
Local Streamlit shim for AchievePulse.

`streamlit run app.py` delegates to `streamlit_app.py`, which is the single
source of truth for the application logic.

The browser deployment (Vercel) does NOT use this file. index.html is a
self-contained static page that inlines the Python and pulls its assets from a
CDN, so it is served directly as a static file with no serverless function in
front of it.
"""
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Streamlit Execution Hook
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
