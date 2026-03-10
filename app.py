import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AgencyKart Portal | Scale Smarter", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM THEMING & CSS (Logo Matched: Navy & Cyan) ---
st.markdown("""
    <style>
    .main { background-color: #0b1a32; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0b1a32; border-right: 1px solid #162a4a; }
    
    .portal-card {
        background: #162a4a;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #243b61;
        margin-bottom: 20px;
    }
    
    .status-pill {
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .status-active { background-color: rgba(46, 196, 209, 0.2); color: #2ec4d1; border: 1px solid #2ec4d1; }
    .status-done { background-color: rgba(52, 211, 153, 0.2); color: #34d399; border: 1px solid #34d399; }
    
    .stButton>button {
        background-color: #2ec4d1;
        color: #0b1a32;
        border-radius: 10px;
        font-weight: 700;
        border: none;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #f8fafc;
        color: #2ec4d1;
        transform: translateY(-2px);
    }
    
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-user { background: #2ec4d1; color: #0b1a32; align-self: flex-end; margin-left: auto; }
    .chat-agency { background: #243b61; color: #f8fafc; border: 1px solid #2ec4d1; }
    
    .match-score { font-size: 24px; color: #2ec4d1; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION (Linking the Portals) ---
if 'active_projects' not in st.session_state:
    st.session_state.active_projects = [
        {"id": "AK-992", "name": "E-Commerce Rebranding", "agency": "PixelPerfect", "status": "In Progress", "progress": 65, "escrow": 45000, "milestone": "UI Design"},
        {"id": "AK-401", "name": "AI Chatbot Integration", "agency": "TechFlow", "status": "Pending Brief", "progress": 10, "escrow": 12000, "milestone": "Setup"}
    ]

if 'open_leads' not in st.session_state:
    st.session_state.open_leads = [
        {"id": "L-001", "title": "Fintech Mobile App", "budget": "₹4L", "timeline": "3 Months", "desc": "Looking for a React Native expert to build a secure wallet app."}
    ]

if 'project_submissions' not in st.session_state:
    st.session_state.project_submissions = []

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agency", "text": "Hi! We've started on the UI moodboards. Any specific preferences for the color palette?"}]

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    try:
        st.image("Logo-1920*1080.jpg", use_container_width=True)
    except:
        st.markdown("<h1 style='color: #2ec4d1;'>AgencyKart</h1>", unsafe_allow_html=True)
        
    st.markdown("<h2 style='text-align: center; color: #2ec4d1; font-size: 1.1rem;'>PORTAL ACCESS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    user_role = st.selectbox("Select Workspace", ["Business Dashboard", "Agency Portal"])
    st.markdown("---")
    if st.button("Reset Portal Data"):
        st.session_state.clear()
        st.rerun()
    st.caption(f"Active View: {user_role}")

# --- BUSINESS DASHBOARD ---
if "Business" in user_role:
    st.title("🏢 Business Project Portal")
    st.markdown("Manage agency deliverables and verify project milestones.")
    
    tabs = st.tabs(["📊 Active Projects", "📩 Communication", "📑 Launch New Brief"])
    
    with tabs[0]:
        for i, p in enumerate(st.session_state.active_projects):
            with st.container():
                st.markdown(f"""
                <div class="portal-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: #f8fafc; margin:0;">{p['name']} <span class="status-pill {'status-active' if p['status'] != 'Complete' else 'status-done'}">{p['status']}</span></h3>
                        <p style="color: #2ec4d1; font-weight: bold; margin:0;">{p['id']}</p>
                    </div>
                    <p style="margin-top:10px;">Agency: <b style="color: #2ec4d1;">{p['agency']} Digital</b> | Milestone: <b>{p['milestone']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic Submissions from Agency
                subs = [s for s in st.session_state.project_submissions if s['project_id'] == p['id']]
                if subs:
                    st.write("📂 **New Deliverables Received:**")
                    for sub in subs:
                        col_s1, col_s2 = st.columns([3, 1])
                        col_s1.info(f"📄 {sub['filename']} (Sent: {sub['timestamp']})")
                        if col_s2.button("Approve & Release Funds", key=f"app_{sub['filename']}"):
                            st.session_state.active_projects[i]['status'] = "Complete"
                            st.session_state.active_projects[i]['progress'] = 100
                            st.balloons()
                            st.rerun()
                
                st.progress(p['progress'] / 100)

    with tabs[1]:
        st.subheader("Messaging Hub")
        for msg in st.session_state.messages:
            div_class = "chat-agency" if msg['role'] == "agency" else "chat-user"
            st.markdown(f'<div class="chat-bubble {div_class}">{msg["text"]}</div>', unsafe_allow_html=True)
        
        with st.form("chat_bus", clear_on_submit=True):
            user_input = st.text_input("Reply to your agency...")
            if st.form_submit_button("Send"):
                st.session_state.messages.append({"role": "user", "text": user_input})
                st.rerun()

    with tabs[2]:
        st.subheader("AI Briefing & Matchmaking")
        with st.form("ai_brief"):
            h = st.text_input("Project Name")
            d = st.text_area("Detailed Requirements")
            if st.form_submit_button("Generate Brief & Match"):
                st.session_state.open_leads.append({"id": f"L-{int(time.time())}", "title": h, "desc": d, "budget": "TBD", "timeline": "TBD"})
                st.success("AI Brief Generated! Project listed for agencies.")
                st.markdown("### 🎯 Top Matches Found")
                st.markdown("1. **PixelPerfect** (98% Match) - UI/UX Experts  \n2. **CodeCrafters** (92% Match) - App Dev")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    st.markdown("Submit work, manage escrow, and discover new business opportunities.")
    
    tabs = st.tabs(["💼 Current Work", "🔍 New Lead Market", "💰 Financials"])
    
    with tabs[0]:
        st.subheader("Project Deliverables")
        sel_proj_name = st.selectbox("Select Project", [p['name'] for p in st.session_state.active_projects])
        sel_proj = next(p for p in st.session_state.active_projects if p['name'] == sel_proj_name)
        
        st.write("### Upload Submission")
        file_up = st.file_uploader("Upload milestone file (PDF/ZIP/Figma)", key="agency_up")
        if file_up and st.button("Submit to Client"):
            st.session_state.project_submissions.append({
                "project_id": sel_proj['id'], "filename": file_up.name, "timestamp": datetime.now().strftime("%H:%M")
            })
            st.success("Work submitted! The client will be notified.")
            st.rerun()
            
        st.write("---")
        st.write("### Review Your Submissions")
        for s in [s for s in st.session_state.project_submissions if s['project_id'] == sel_proj['id']]:
            col_f1, col_f2 = st.columns([3, 1])
            col_f1.write(f"📄 {s['filename']}")
            if col_f2.button("Delete / Retract", key=f"del_{s['filename']}"):
                st.session_state.project_submissions.remove(s)
                st.warning("Submission retracted.")
                st.rerun()

    with tabs[1]:
        st.subheader("Marketplace Leads")
        for lead in st.session_state.open_leads:
            st.markdown(f"""
            <div class="portal-card">
                <h4 style="color: #2ec4d1;">{lead['title']}</h4>
                <p>{lead['desc']}</p>
                <small>Budget: {lead['budget']}</small>
            </div>
            """, unsafe_allow_html=True)
            st.button("Submit Proposal", key=f"bid_{lead['id']}")

    with tabs[2]:
        st.metric("Total Secured in Escrow", f"₹{sum(p['escrow'] for p in st.session_state.active_projects if p['status'] != 'Complete'):,}")
        st.table(pd.DataFrame(st.session_state.active_projects))

st.markdown("---")
st.caption("AgencyKart Portal v2.7 | Use top-left arrow to hide sidebar for Presentation Mode.")
