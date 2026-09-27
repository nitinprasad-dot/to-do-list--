import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import uuid
import json

# ==========================================
# 1. PAGE CONFIGURATION & DESIGN SYSTEM
# ==========================================
st.set_page_config(
    page_title="AchievePulse • Goal & Task Tracker",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism, Vibrant Accents, Modern Typography)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.12) 50%, rgba(236, 72, 153, 0.08) 100%);
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.2);
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1, #A855F7, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #94A3B8;
    margin-bottom: 0;
}

/* Metric Cards */
.metric-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 18px 22px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #F8FAFC;
    line-height: 1.2;
}
.metric-label {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94A3B8;
}

/* Task Item Styling */
.task-item {
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.task-item.completed {
    background: rgba(16, 185, 129, 0.06);
    border-color: rgba(16, 185, 129, 0.2);
}

/* Pill Badges */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.badge-work { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
.badge-study { background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.3); }
.badge-fitness { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-coding { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-personal { background: rgba(236, 72, 153, 0.15); color: #F472B6; border: 1px solid rgba(236, 72, 153, 0.3); }

.badge-high { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.badge-medium { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
.badge-low { background: rgba(100, 116, 139, 0.2); color: #94A3B8; border: 1px solid rgba(100, 116, 139, 0.3); }

/* Public Profile Card */
.public-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.85) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    padding: 36px;
    box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.5);
}

.mono-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #A5B4FC;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

if "goal" not in st.session_state:
    st.session_state.goal = {
        "title": "Master Full-Stack & Python Systems",
        "category": "Coding",
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=30))
    }

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "dashboard"  # 'dashboard', 'public'


# Category Icons and Badges mapping
CATEGORY_CONFIG = {
    "Study": {"icon": "📚", "class": "badge-study"},
    "Work": {"icon": "💼", "class": "badge-work"},
    "Fitness": {"icon": "🏃‍♂️", "class": "badge-fitness"},
    "Coding": {"icon": "💻", "class": "badge-coding"},
    "Personal": {"icon": "🌟", "class": "badge-personal"},
    "Health": {"icon": "🧘", "class": "badge-fitness"}
}

def get_category_config(cat_name):
    return CATEGORY_CONFIG.get(cat_name, {"icon": "🎯", "class": "badge-personal"})


# Format timedelta nicely
def format_duration(start_dt, end_dt):
    if not start_dt or not end_dt:
        return "N/A"
    delta = end_dt - start_dt
    total_seconds = int(delta.total_seconds())
    if total_seconds < 0:
        return "Instant"
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or not parts:
        parts.append(f"{minutes}m")
    return " ".join(parts)


# Load Starter Data for immediate delight
def load_sample_tasks(purpose):
    sample_bank = {
        "Coding": [
            ("Review System Architecture & Database schema", "Coding", "High", 0, 120),
            ("Build Streamlit Dashboard with Real-time metrics", "Coding", "High", 0, 45),
            ("Write unit tests for task completion logic", "Coding", "Medium", 1, None),
            ("Deploy application to Streamlit Community Cloud", "Coding", "High", 2, None),
        ],
        "Study": [
            ("Read Chapter 4 on Distributed Algorithms", "Study", "High", 0, 90),
            ("Summarize key concepts in flashcards", "Study", "Medium", 0, 30),
            ("Solve 10 practice questions from mock exam", "Study", "High", 1, None),
            ("Participate in group study session", "Study", "Low", 2, None),
        ],
        "Fitness": [
            ("Morning 5km tempo run & stretching", "Fitness", "High", 0, 40),
            ("Upper body resistance training (Chest & Triceps)", "Fitness", "High", 0, 60),
            ("Prep high-protein meals for the week", "Fitness", "Medium", 1, None),
            ("Hydration goal: 3.5 Liters of water", "Fitness", "Low", 0, None),
        ],
        "Work": [
            ("Complete quarterly roadmap slide deck", "Work", "High", 0, 110),
            ("Team standup and blocker sync", "Work", "Medium", 0, 20),
            ("Client presentation preparation", "Work", "High", 1, None),
            ("Inbox zero and follow-up emails", "Work", "Low", 0, None),
        ],
        "Personal": [
            ("Morning 15-minute mindfulness meditation", "Personal", "Medium", 0, 15),
            ("Review monthly budget and savings goals", "Personal", "High", 0, 45),
            ("Read 25 pages of non-fiction book", "Personal", "Low", 1, None),
            ("Call family / close friend", "Personal", "Low", 2, None),
        ]
    }
    
    selected_samples = sample_bank.get(purpose, sample_bank["Coding"])
    now = datetime.now()
    generated_tasks = []
    
    for title, cat, prio, due_offset, comp_mins in selected_samples:
        created_time = now - timedelta(hours=4, minutes=30)
        due_d = date.today() + timedelta(days=due_offset)
        
        is_done = comp_mins is not None
        comp_time = None
        if is_done:
            comp_time = (created_time + timedelta(minutes=comp_mins)).isoformat()
            
        generated_tasks.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "category": cat,
            "priority": prio,
            "due_date": str(due_d),
            "completed": is_done,
            "created_at": created_time.isoformat(),
            "completed_at": comp_time
        })
    return generated_tasks


# ==========================================
# 3. ONBOARDING / REGISTRATION PAGE
# ==========================================
def render_onboarding():
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; margin-bottom: 30px;">
        <div style="display: inline-block; padding: 6px 16px; border-radius: 9999px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #818CF8; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">
            ✨ WELCOME TO ACHIEVEPULSE
        </div>
        <h1 style="font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #6366F1, #A855F7, #EC4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;">
            Personal Goal & Task Tracker
        </h1>
        <p style="color: #94A3B8; font-size: 1.15rem; max-width: 600px; margin: 0 auto;">
            Empower your daily routine. Set clear timeframes, track completion velocity, and celebrate your milestone achievements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 👤 Create Your Profile")
            st.caption("Tell us a little bit about yourself and your primary focus area.")
            
            with st.form("onboarding_form", clear_on_submit=False):
                name = st.text_input("Full Name / Display Name", placeholder="e.g. Alex Johnson")
                
                fcol1, fcol2 = st.columns(2)
                with fcol1:
                    age = st.number_input("Age", min_value=10, max_value=100, value=25, step=1)
                with fcol2:
                    purpose = st.selectbox(
                        "Primary Focus / Purpose",
                        ["Coding", "Study", "Fitness", "Work", "Personal"],
                        help="You can still add tasks from other categories later."
                    )
                
                st.divider()
                st.markdown("### 🎯 Your Target Milestone Goal")
                goal_title = st.text_input(
                    "Primary Goal Objective",
                    value=f"Master {purpose} Objectives & Stay Consistent",
                    placeholder="e.g. Finish Python Course & Build Portfolio"
                )
                
                dcol1, dcol2 = st.columns(2)
                with dcol1:
                    start_date = st.date_input("Goal Start Date", value=date.today())
                with dcol2:
                    end_date = st.date_input("Goal Target Deadline", value=date.today() + timedelta(days=30))
                
                sample_data_toggle = st.checkbox(
                    "✨ Pre-populate with sample tasks for my focus area (recommended)",
                    value=True,
                    help="Loads a few active and completed starter tasks so your analytics look great immediately!"
                )
                
                submitted = st.form_submit_button("🚀 Launch My Tracker", use_container_width=True, type="primary")
                
                if submitted:
                    if not name.strip():
                        st.error("Please enter your name to continue.")
                    elif end_date < start_date:
                        st.error("Target deadline cannot be earlier than start date.")
                    else:
                        st.session_state.user_profile = {
                            "name": name.strip(),
                            "age": int(age),
                            "purpose": purpose,
                            "joined_date": str(date.today())
                        }
                        st.session_state.goal = {
                            "title": goal_title.strip() if goal_title.strip() else f"Achieve {purpose} Excellence",
                            "category": purpose,
                            "start_date": str(start_date),
                            "end_date": str(end_date)
                        }
                        if sample_data_toggle:
                            st.session_state.tasks = load_sample_tasks(purpose)
                        else:
                            st.session_state.tasks = []
                            
                        st.success("Profile created successfully! Redirecting...")
                        st.rerun()


# ==========================================
# 4. DASHBOARD & MANAGEMENT LOGIC
# ==========================================
def render_dashboard():
    user = st.session_state.user_profile
    goal = st.session_state.goal
    tasks = st.session_state.tasks
    
    # Calculate Goal Timeframe metrics
    try:
        g_start = datetime.strptime(goal["start_date"], "%Y-%m-%d").date()
        g_end = datetime.strptime(goal["end_date"], "%Y-%m-%d").date()
    except Exception:
        g_start = date.today()
        g_end = date.today() + timedelta(days=30)
        
    today = date.today()
    total_days = max(1, (g_end - g_start).days)
    days_elapsed = max(0, (today - g_start).days)
    days_left = (g_end - today).days

    # ======================================
    # SIDEBAR: Profile & Settings
    # ======================================
    with st.sidebar:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 18px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                <div style="font-size: 2rem; background: rgba(99, 102, 241, 0.2); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                    {get_category_config(user['purpose'])['icon']}
                </div>
                <div>
                    <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #F8FAFC;">{user['name']}</h3>
                    <span class="badge {get_category_config(user['purpose'])['class']}">{user['purpose']} • Age {user['age']}</span>
                </div>
            </div>
            <div style="font-size: 0.8rem; color: #94A3B8; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 8px; margin-top: 8px;">
                Joined: {user.get('joined_date', 'Today')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🎯 Active Goal Target")
        st.info(f"**{goal['title']}**\n\n📅 {g_start.strftime('%b %d, %Y')} ➔ {g_end.strftime('%b %d, %Y')}")
        
        if days_left < 0:
            st.error(f"⚠️ Goal deadline expired {abs(days_left)} days ago.")
        else:
            st.caption(f"⏳ **{days_left} days** remaining out of {total_days} total days.")
        
        st.divider()
        
        # Navigation / View Mode
        view_selection = st.radio(
            "Navigation Mode",
            ["📊 Dashboard & Tasks", "🌐 Public Shareable View"],
            index=0 if st.session_state.view_mode == "dashboard" else 1
        )
        if "Public" in view_selection and st.session_state.view_mode != "public":
            st.session_state.view_mode = "public"
            st.rerun()
        elif "Dashboard" in view_selection and st.session_state.view_mode != "dashboard":
            st.session_state.view_mode = "dashboard"
            st.rerun()

        st.divider()
        
        # Edit Goal Timeframe Expander
        with st.expander("⚙️ Edit Goal & Timeframe"):
            with st.form("edit_goal_form"):
                new_goal_title = st.text_input("Goal Title", value=goal["title"])
                ncol1, ncol2 = st.columns(2)
                with ncol1:
                    new_start = st.date_input("Start Date", value=g_start)
                with ncol2:
                    new_end = st.date_input("End Date", value=g_end)
                if st.form_submit_button("Update Goal Timeframe", use_container_width=True):
                    if new_end < new_start:
                        st.error("End date cannot precede start date.")
                    else:
                        st.session_state.goal["title"] = new_goal_title
                        st.session_state.goal["start_date"] = str(new_start)
                        st.session_state.goal["end_date"] = str(new_end)
                        st.success("Goal timeframe updated!")
                        st.rerun()

        # Data Backup / Export & Reset
        with st.expander("💾 Backup & Reset"):
            export_payload = {
                "profile": st.session_state.user_profile,
                "goal": st.session_state.goal,
                "tasks": st.session_state.tasks
            }
            st.download_button(
                label="📥 Export Tasks (JSON)",
                data=json.dumps(export_payload, indent=2),
                file_name=f"achievepulse_backup_{user['name'].lower().replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            if st.button("🔄 Reset Profile / Log Out", use_container_width=True, type="secondary"):
                st.session_state.user_profile = None
                st.session_state.tasks = []
                st.rerun()

    # If the user toggled the Public view, show that view!
    if st.session_state.view_mode == "public":
        render_public_view()
        return

    # ======================================
    # TOP HERO & GOAL HEADER
    # ======================================
    st.markdown(f"""
    <div class="hero-container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div>
                <div class="hero-title">Welcome back, {user['name']}! 👋</div>
                <p class="hero-subtitle">
                    Tracking <strong>{goal['title']}</strong> • Focus: <span style="color: #F8FAFC; font-weight: 600;">{goal['category']}</span>
                </p>
            </div>
            <div style="text-align: right; background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); padding: 8px 16px; border-radius: 12px;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 600;">GOAL TIMEFRAME</div>
                <div style="font-size: 0.95rem; color: #E2E8F0; font-weight: 700;">{g_start.strftime('%b %d')} – {g_end.strftime('%b %d, %Y')}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ======================================
    # CALCULATE TASK METRICS
    # ======================================
    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t.get("completed", False)]
    active_tasks = [t for t in tasks if not t.get("completed", False)]
    num_completed = len(completed_tasks)
    num_active = len(active_tasks)
    progress_pct = int((num_completed / total_tasks * 100)) if total_tasks > 0 else 0

    # Calculate Overdue and Pending Reminders
    overdue_tasks = []
    due_today_tasks = []
    for t in active_tasks:
        try:
            task_due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
            if task_due < today:
                overdue_tasks.append(t)
            elif task_due == today:
                due_today_tasks.append(t)
        except Exception:
            pass

    # ======================================
    # 4. REMINDER SYSTEM (Highlighted Widget)
    # ======================================
    if overdue_tasks or due_today_tasks:
        with st.container(border=True):
            rcol1, rcol2 = st.columns([0.08, 0.92])
            with rcol1:
                st.markdown("<div style='font-size: 2rem;'>🚨</div>", unsafe_allow_html=True)
            with rcol2:
                warning_text = []
                if overdue_tasks:
                    warning_text.append(f"**{len(overdue_tasks)} Overdue Task(s)**")
                if due_today_tasks:
                    warning_text.append(f"**{len(due_today_tasks)} Due Today**")
                
                st.markdown(f"#### Reminder Alert: {' & '.join(warning_text)}")
                st.caption("Stay on track with your timeframe! Here are the urgent tasks needing your attention:")
                
                urgent_items = overdue_tasks + due_today_tasks
                for item in urgent_items:
                    is_overdue = item in overdue_tasks
                    tag = "🚨 OVERDUE" if is_overdue else "⏰ DUE TODAY"
                    tag_color = "#EF4444" if is_overdue else "#F59E0B"
                    
                    ucol1, ucol2 = st.columns([0.75, 0.25])
                    with ucol1:
                        st.markdown(f"<span style='color: {tag_color}; font-weight: 700; font-size: 0.8rem;'>[{tag}]</span> **{item['title']}** (Due: {item['due_date']})", unsafe_allow_html=True)
                    with ucol2:
                        if st.button("Mark Done", key=f"quick_done_{item['id']}", use_container_width=True):
                            for t in st.session_state.tasks:
                                if t["id"] == item["id"]:
                                    t["completed"] = True
                                    t["completed_at"] = datetime.now().isoformat()
                            st.rerun()

    # ======================================
    # 3. REAL-TIME PROGRESS BAR & KPI METRICS
    # ======================================
    st.markdown("### 📊 Progress & Performance")
    
    # Progress Bar with dynamic color
    prog_color = "#6366F1" if progress_pct < 40 else ("#A855F7" if progress_pct < 80 else "#10B981")
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.6); padding: 16px 20px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; font-size: 1rem; color: #F8FAFC;">Overall Goal Completion</span>
            <span style="font-weight: 800; font-size: 1.25rem; color: {prog_color};">{progress_pct}%</span>
        </div>
        <div style="background: rgba(255, 255, 255, 0.08); border-radius: 9999px; height: 14px; overflow: hidden; width: 100%;">
            <div style="background: linear-gradient(90deg, #6366F1, {prog_color}); width: {progress_pct}%; height: 100%; border-radius: 9999px; transition: width 0.4s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94A3B8; margin-top: 8px;">
            <span>{num_completed} of {total_tasks} tasks completed</span>
            <span>{f"{days_left} days remaining" if days_left >= 0 else "Timeframe ended"}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric Cards Row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Tasks</div>
            <div class="metric-value">{total_tasks}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Completed</div>
            <div class="metric-value" style="color: #34D399;">{num_completed}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active / Pending</div>
            <div class="metric-value" style="color: #60A5FA;">{num_active}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Completion Velocity</div>
            <div class="metric-value" style="color: #C084FC;">{progress_pct}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Days Left</div>
            <div class="metric-value" style="color: {'#F87171' if days_left < 3 else '#FBBF24'};">{max(0, days_left)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # ======================================
    # TABS: TASKS vs ANALYTICS
    # ======================================
    tab_tasks, tab_analytics = st.tabs(["📝 Task Management", "📈 Detailed Analytics & Time Taken"])

    # ----------------------------------------------------
    # TAB 1: TASK MANAGEMENT
    # ----------------------------------------------------
    with tab_tasks:
        col_list, col_add = st.columns([1.5, 1])

        # Left Column: Active & Completed Task List
        with col_list:
            st.markdown("#### 📋 Your Tasks")
            
            # Filter bar
            f_col1, f_col2 = st.columns([1, 1])
            with f_col1:
                filter_status = st.selectbox("Filter Status", ["All Tasks", "Active Only", "Completed Only"], label_visibility="collapsed")
            with f_col2:
                filter_cat = st.selectbox("Filter Category", ["All Categories", "Study", "Work", "Fitness", "Coding", "Personal"], label_visibility="collapsed")

            # Filter logic
            displayed_tasks = tasks
            if filter_status == "Active Only":
                displayed_tasks = [t for t in displayed_tasks if not t.get("completed", False)]
            elif filter_status == "Completed Only":
                displayed_tasks = [t for t in displayed_tasks if t.get("completed", False)]
                
            if filter_cat != "All Categories":
                displayed_tasks = [t for t in displayed_tasks if t.get("category") == filter_cat]

            if not displayed_tasks:
                st.info("No tasks found matching your filters. Add one on the right to get started! 🚀")
            else:
                for idx, t in enumerate(displayed_tasks):
                    task_id = t["id"]
                    is_completed = t.get("completed", False)
                    prio = t.get("priority", "Medium")
                    cat = t.get("category", "General")
                    cat_conf = get_category_config(cat)
                    
                    prio_class = f"badge-{prio.lower()}"
                    
                    # Compute duration if completed
                    duration_str = ""
                    if is_completed and t.get("completed_at"):
                        try:
                            c_in = datetime.fromisoformat(t["created_at"])
                            c_out = datetime.fromisoformat(t["completed_at"])
                            duration_str = f"⏱️ Completed in {format_duration(c_in, c_out)}"
                        except Exception:
                            duration_str = "⏱️ Completed"

                    with st.container(border=True):
                        t_col1, t_col2, t_col3 = st.columns([0.1, 0.75, 0.15])
                        
                        with t_col1:
                            # Completion Checkbox
                            checked = st.checkbox(
                                "Done",
                                value=is_completed,
                                key=f"task_chk_{task_id}",
                                label_visibility="collapsed"
                            )
                            # Handle checkbox change
                            if checked != is_completed:
                                for real_task in st.session_state.tasks:
                                    if real_task["id"] == task_id:
                                        real_task["completed"] = checked
                                        if checked:
                                            real_task["completed_at"] = datetime.now().isoformat()
                                        else:
                                            real_task["completed_at"] = None
                                st.rerun()

                        with t_col2:
                            strike_style = "text-decoration: line-through; opacity: 0.6;" if is_completed else ""
                            st.markdown(f"""
                            <div>
                                <span style="font-size: 1.05rem; font-weight: 600; {strike_style}">{t['title']}</span>
                                <div style="display: flex; gap: 8px; align-items: center; margin-top: 4px; flex-wrap: wrap;">
                                    <span class="badge {cat_conf['class']}">{cat_conf['icon']} {cat}</span>
                                    <span class="badge {prio_class}">{prio}</span>
                                    <span style="font-size: 0.78rem; color: #94A3B8;">📅 Due: {t.get('due_date', 'N/A')}</span>
                                    {f'<span class="mono-time">{duration_str}</span>' if duration_str else ''}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        with t_col3:
                            if st.button("🗑️", key=f"del_{task_id}", help="Delete task"):
                                st.session_state.tasks = [x for x in st.session_state.tasks if x["id"] != task_id]
                                st.rerun()

        # Right Column: Add Task Box
        with col_add:
            st.markdown("#### ➕ Add New Daily Task")
            with st.container(border=True):
                with st.form("add_task_form", clear_on_submit=True):
                    task_title = st.text_input("Task Description", placeholder="e.g. Solve 2 LeetCode problems or 30m Run")
                    
                    acol1, acol2 = st.columns(2)
                    with acol1:
                        task_category = st.selectbox(
                            "Category",
                            ["Coding", "Study", "Fitness", "Work", "Personal"],
                            index=["Coding", "Study", "Fitness", "Work", "Personal"].index(user["purpose"]) if user["purpose"] in ["Coding", "Study", "Fitness", "Work", "Personal"] else 0
                        )
                    with acol2:
                        task_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
                        
                    task_due = st.date_input("Target Due Date", value=date.today())
                    
                    add_submitted = st.form_submit_button("Add Task to Tracker", use_container_width=True, type="primary")
                    if add_submitted:
                        if not task_title.strip():
                            st.error("Please enter a task description.")
                        else:
                            new_task = {
                                "id": str(uuid.uuid4()),
                                "title": task_title.strip(),
                                "category": task_category,
                                "priority": task_priority,
                                "due_date": str(task_due),
                                "completed": False,
                                "created_at": datetime.now().isoformat(),
                                "completed_at": None
                            }
                            st.session_state.tasks.append(new_task)
                            st.success(f"Task '{task_title}' added!")
                            st.rerun()

    # ----------------------------------------------------
    # TAB 2: DETAILED ANALYTICS & TIME TAKEN
    # ----------------------------------------------------
    with tab_analytics:
        st.markdown("#### 📈 Analytics & Time-to-Complete Breakdown")
        
        if total_tasks == 0:
            st.info("No tasks to analyze yet! Add some tasks in the Task Management tab.")
        else:
            # Breakdown Charts Row
            c1, c2 = st.columns(2)
            
            with c1:
                # Donut Chart for Status
                status_df = pd.DataFrame([
                    {"Status": "Completed", "Count": num_completed},
                    {"Status": "Active", "Count": num_active}
                ])
                fig_status = px.pie(
                    status_df, 
                    names="Status", 
                    values="Count", 
                    hole=0.6,
                    color="Status",
                    color_discrete_map={"Completed": "#10B981", "Active": "#6366F1"},
                    title="Task Completion Breakdown"
                )
                fig_status.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#F8FAFC",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_status, use_container_width=True)

            with c2:
                # Bar Chart by Category
                categories = [t.get("category", "Other") for t in tasks]
                cat_df = pd.DataFrame(categories, columns=["Category"]).value_counts().reset_index()
                cat_df.columns = ["Category", "Count"]
                
                fig_cat = px.bar(
                    cat_df,
                    x="Category",
                    y="Count",
                    color="Category",
                    title="Tasks by Category",
                    color_discrete_sequence=["#6366F1", "#A855F7", "#EC4899", "#F59E0B", "#10B981"]
                )
                fig_cat.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#F8FAFC",
                    showlegend=False,
                    margin=dict(t=40, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_cat, use_container_width=True)

            # Completion Time Breakdown Table
            st.markdown("#### ⏱️ Time Taken to Complete Tasks")
            st.caption("Automatically calculated from task creation timestamp to completion timestamp.")
            
            completed_records = []
            durations_in_mins = []
            
            for t in completed_tasks:
                c_created = t.get("created_at")
                c_completed = t.get("completed_at")
                if c_created and c_completed:
                    try:
                        dt_start = datetime.fromisoformat(c_created)
                        dt_end = datetime.fromisoformat(c_completed)
                        diff = dt_end - dt_start
                        diff_minutes = max(1, int(diff.total_seconds() / 60))
                        durations_in_mins.append(diff_minutes)
                        
                        completed_records.append({
                            "Task": t["title"],
                            "Category": t.get("category", "General"),
                            "Priority": t.get("priority", "Medium"),
                            "Created At": dt_start.strftime("%Y-%m-%d %I:%M %p"),
                            "Completed At": dt_end.strftime("%Y-%m-%d %I:%M %p"),
                            "Time Taken": format_duration(dt_start, dt_end)
                        })
                    except Exception:
                        pass
                        
            if completed_records:
                avg_time = sum(durations_in_mins) / len(durations_in_mins)
                avg_hours = avg_time / 60
                
                kcol1, kcol2, kcol3 = st.columns(3)
                with kcol1:
                    st.metric("Total Completed Tasks", f"{len(completed_records)}")
                with kcol2:
                    if avg_hours < 1:
                        st.metric("Avg Completion Time", f"{int(avg_time)} mins")
                    else:
                        st.metric("Avg Completion Time", f"{avg_hours:.1f} hours")
                with kcol3:
                    fastest = min(durations_in_mins)
                    st.metric("Fastest Turnaround", f"{fastest} mins" if fastest < 60 else f"{fastest/60:.1f} hrs")
                
                df_completed = pd.DataFrame(completed_records)
                st.dataframe(df_completed, use_container_width=True, hide_index=True)
            else:
                st.info("Check off some tasks above to generate turnaround time records!")


# ==========================================
# 5. PUBLIC PROFILE / SHAREABLE VIEW
# ==========================================
def render_public_view():
    user = st.session_state.user_profile
    goal = st.session_state.goal
    tasks = st.session_state.tasks
    
    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t.get("completed", False)]
    progress_pct = int((len(completed_tasks) / total_tasks * 100)) if total_tasks > 0 else 0
    cat_conf = get_category_config(user["purpose"])
    
    try:
        g_start = datetime.strptime(goal["start_date"], "%Y-%m-%d").date()
        g_end = datetime.strptime(goal["end_date"], "%Y-%m-%d").date()
    except Exception:
        g_start = date.today()
        g_end = date.today() + timedelta(days=30)
        
    days_left = (g_end - date.today()).days

    # Top Control Bar
    pcol1, pcol2 = st.columns([0.8, 0.2])
    with pcol1:
        st.markdown("### 🌐 Public Achievement & Progress Showcase")
        st.caption("A clean, verified snapshot of your goals and daily progress that you can share with peers, mentors, or on social media.")
    with pcol2:
        if st.button("⬅️ Back to Dashboard", use_container_width=True):
            st.session_state.view_mode = "dashboard"
            st.rerun()

    # The Shareable Card
    st.markdown(f"""
    <div class="public-card" style="margin-top: 15px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 20px; margin-bottom: 24px; flex-wrap: wrap; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 2.8rem; background: rgba(99, 102, 241, 0.25); border: 2px solid rgba(99, 102, 241, 0.5); width: 68px; height: 68px; border-radius: 20px; display: flex; align-items: center; justify-content: center;">
                    {cat_conf['icon']}
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.9rem; font-weight: 800; color: #FFFFFF;">{user['name']}</h2>
                    <div style="display: flex; gap: 8px; margin-top: 6px;">
                        <span class="badge {cat_conf['class']}">{user['purpose']} Enthusiast</span>
                        <span class="badge badge-low">Age {user['age']}</span>
                        <span class="badge badge-fitness">Verified Learner</span>
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.05em; font-weight: 600;">TIMEFRAME WINDOW</div>
                <div style="font-size: 1.1rem; color: #F1F5F9; font-weight: 700;">{g_start.strftime('%b %d, %Y')} ➔ {g_end.strftime('%b %d, %Y')}</div>
                <div style="font-size: 0.85rem; color: {'#34D399' if days_left >= 0 else '#F87171'}; font-weight: 600;">
                    {f'⏳ {days_left} Days Remaining' if days_left >= 0 else 'Timeframe Concluded'}
                </div>
            </div>
        </div>

        <div style="margin-bottom: 28px;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #A5B4FC; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">Target Goal</div>
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #F8FAFC;">"{goal['title']}"</h3>
        </div>

        <div style="background: rgba(15, 23, 42, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 28px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 0.95rem; font-weight: 700; color: #E2E8F0;">Overall Goal Progress</span>
                <span style="font-size: 1.4rem; font-weight: 800; color: #34D399;">{progress_pct}%</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.08); border-radius: 9999px; height: 16px; overflow: hidden; width: 100%;">
                <div style="background: linear-gradient(90deg, #6366F1, #10B981); width: {progress_pct}%; height: 100%; border-radius: 9999px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #94A3B8; margin-top: 10px;">
                <span>🎯 {len(completed_tasks)} Completed / {total_tasks} Total Tasks</span>
                <span>🔥 {progress_pct}% Completed</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Shareable Summary Text generator
    st.markdown("#### 📋 Copy Shareable Status Snippet")
    shareable_text = f"""🎯 Goal Progress Update: {user['name']}
Focus Area: {user['purpose']}
Primary Objective: "{goal['title']}"
Timeframe: {g_start.strftime('%b %d, %Y')} to {g_end.strftime('%b %d, %Y')} ({max(0, days_left)} days remaining)
📊 Current Velocity: {progress_pct}% Completed ({len(completed_tasks)}/{total_tasks} tasks achieved)
#AchievePulse #Productivity #{user['purpose']}"""

    st.text_area("Shareable Markdown / Post Text", value=shareable_text, height=120)
    st.info("💡 You can copy the text above and post it directly to LinkedIn, Twitter/X, Discord, or your daily standup!")


# ==========================================
# 6. MAIN ROUTER
# ==========================================
def main():
    if st.session_state.user_profile is None:
        render_onboarding()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
