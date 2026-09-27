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
   streamlit run app.py
   ```

5. **Open in Your Browser**:
   Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ How to Deploy for Free on Streamlit Community Cloud

Streamlit Community Cloud allows you to host Python applications for free with automated deployments from GitHub.

### Step 1: Push Code to GitHub
1. Initialize a git repository in the project folder:
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Initial commit of Personal Goal and Task Tracker"
   ```
2. Create a new public repository on [GitHub](https://github.com/new) (e.g., `personal-goal-tracker`).
3. Push your repository:
   ```bash
   git remote add origin https://github.com/<your-username>/personal-goal-tracker.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Connect to Streamlit Community Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io/) and sign in with your GitHub account.
2. Click **"New app"**.
3. Select your repository (`<your-username>/personal-goal-tracker`), branch (`main`), and main file path (`app.py`).
4. Click **"Deploy!"**.

Streamlit Cloud will install dependencies from `requirements.txt` and launch your live application at `https://<your-app-name>.streamlit.app` in under 2 minutes.

---

## 📁 Project Structure

```text
personal-goal-tracker/
├── app.py              # Main Streamlit web application
├── requirements.txt    # Project dependencies (streamlit, pandas, plotly)
└── README.md           # Documentation & deployment guide
```
