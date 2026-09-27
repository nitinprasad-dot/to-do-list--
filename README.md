# 🎯 AchievePulse — Personal Goal & Task Tracker

A full-featured, modern web application built with **Python**, **Streamlit**, and **Plotly** to track long-term goals, manage daily tasks, calculate time-to-completion analytics, trigger smart reminders, and generate public shareable achievement showcases.

---

## 🌟 Key Features

### 1. 👤 Registration & Onboarding (Front Page)
- Clean, welcoming onboarding page for first-time visitors.
- Capture **Display Name**, **Age**, and **Primary Focus Area** (Coding, Study, Fitness, Work, Personal).
- Define target milestone goals with start and end dates.
- Option to pre-populate starter tasks for instant analytics visualization.
- Stored reliably in Streamlit's `st.session_state` with smooth transition to the dashboard.

### 2. 🎯 Goal & Task Management
- Set and manage specific timeframe windows (Start Date ➔ End Date).
- Real-time countdown timer showing days elapsed, days remaining, and status indicators.
- Quick input form to add daily tasks with:
  - Task description
  - Category selector with vibrant pill badges
  - Priority levels (🔴 High, 🟡 Medium, 🟢 Low)
  - Target Due Date
- Interactive task completion checkbox that **automatically records completion timestamps** (`completed_at`).
- Filter tasks by status (*All*, *Active Only*, *Completed Only*) and category.
- Single-click delete option for task lifecycle cleanup.

### 3. 📊 Visual Progress Bar & Turnaround Analytics
- **Dynamic Real-Time Progress Bar**: Scales seamlessly from 0% to 100% based on completed tasks vs total tasks.
- **KPI Metric Cards**: Total Tasks, Completed, Active/Pending, Velocity (%), and Days Left.
- **Interactive Visual Charts**:
  - Donut chart displaying Task Status breakdown (*Active* vs *Completed*).
  - Bar chart showing task distribution across categories.
- **Completion Velocity Table**:
  - Automatically calculates exact time elapsed between task creation and completion (e.g. `1h 45m`, `35m`, `2d 4h`).
  - Summarizes **Average Turnaround Time** and **Fastest Completed Task**.

### 4. 🚨 Smart Reminder System
- Intelligent alert banner prominently featured at the top of the dashboard.
- Highlights:
  - 🚨 **Overdue Tasks**: Due date has passed and task remains pending.
  - ⏰ **Due Today**: Tasks scheduled for today that need attention.
- Includes quick-action **"Mark Done"** buttons directly inside the reminder widget.

### 5. 🌐 Public Shareable View & Export
- Toggle between private dashboard mode and public showcase mode.
- Renders an achievement card highlighting:
  - User name, category badge, age, and verified learner tag.
  - Goal title and timeframe window.
  - Progress bar and completion metrics.
- **One-Click Shareable Snippet**: Pre-formatted Markdown status update ready to paste into LinkedIn, Twitter/X, Discord, or team standup notes.
- **Data Backup**: Export state to JSON anytime to ensure zero data loss across sessions.

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.9, 3.10, 3.11, 3.12, or 3.13 installed on your machine.
- Git (optional, for version control).

### Step-by-Step Instructions

1. **Clone or Navigate to the Project Folder**:
   ```bash
   cd /path/to/personal-goal-tracker
   ```

2. **Create a Virtual Environment**:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application**:
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open in Your Browser**:
   Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ⚡ Deployment Options

### Option 1: Deploy on Vercel (Instant Browser Wasm via Stlite)
This project is deployed as a **fully static site**. `index.html` inlines the entire Python application and loads its assets from a CDN, so there is no server or serverless function in the request path:
1. Connect your GitHub repository to [Vercel](https://vercel.com/).
2. Keep default settings (Framework preset: `Other`, Root Directory: `./`).
3. Click **Deploy** — Vercel serves `index.html` globally via CDN!

> **Note:** In the browser (Wasm) build there is no Python server behind the app, so `st.download_button` cannot work — the JSON export only works in the Streamlit deployments below. The in-page data is still fully usable.

### Option 2: Deploy for Free on Streamlit Community Cloud
Streamlit Community Cloud provides native containerized Python hosting with live backend WebSockets:
1. Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository, branch (`main`), and set the main file path to `streamlit_app.py`.
4. Click **"Deploy!"**.

---

## 📁 Project Structure

```text
to-do-list--/
├── streamlit_app.py    # Single source of truth for the application logic
├── index.html          # Static Vercel build: inlines the same Python + Stlite/Wasm runner
├── requirements.txt    # Python dependencies (streamlit, pandas, plotly)
└── README.md           # Documentation & deployment guide
```

> **Do not add a reserved entrypoint filename at the project root.** Vercel builds a
> root-level `app.py`, `index.py`, `server.py`, `main.py`, `wsgi.py`, or `asgi.py` as
> a Python serverless function, and the build fails unless that file exports a
> top-level `app` / `application` / `handler`. `index.html` needs no server, so the
> repo intentionally ships none of those names. `streamlit_app.py` is a non-reserved
> filename and is ignored by Vercel. `requirements.txt` exists only for the local
> and Streamlit Cloud setups.

### Keeping the two copies of the app in sync
`index.html` embeds a copy of `streamlit_app.py` inside a
`<script type="text/python">` block so the page is self-contained. The two must
stay identical. After editing the Python, re-embed it:

```bash
python3 - <<'PY'
import re, pathlib
p = pathlib.Path("index.html")
html = p.read_text()
app = pathlib.Path("streamlit_app.py").read_text().strip()
m = re.search(r'(<script type="text/python" id="st-app-code">)(.*?)(</script>)', html, re.S)
p.write_text(html[:m.start(2)] + app + "\n" + html[m.end(2):])
print("re-embedded", len(app), "chars")
PY
```

