import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AgencyKart Portal | Scale Smarter", page_icon="🚀", layout="wide")

# --- CUSTOM THEMING & CSS ---
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
    .status-pending { background-color: rgba(251, 146, 60, 0.2); color: #fb923c; border: 1px solid #fb923c; }
    .status-done { background-color: rgba(52, 211, 153, 0.2); color: #34d399; border: 1px solid #34d399; }
    
    .stButton>button {
        background-color: #2ec4d1;
        color: #0b1a32;
        border-radius: 10px;
        font-weight: 700;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #f8fafc;
        color: #2ec4d1;
    }
    
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-user { background: #2ec4d1; color: #0b1a32; align-self: flex-end; margin-left: auto; font-weight: 500; }
    .chat-agency { background: #243b61; color: #f8fafc; border: 1px solid #2ec4d1; }
    
    .match-score {
        font-size: 24px;
        color: #2ec4d1;
        font-weight: bold;
    }
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
        {"id": "L-001", "title": "Fintech Mobile App", "budget": "₹4L", "timeline": "3 Months", "desc": "Looking for a React Native expert."}
    ]

if 'project_submissions' not in st.session_state:
    st.session_state.project_submissions = [
        {"project_id": "AK-992", "filename": "Final_Moodboard_v2.pdf", "timestamp": "2023-10-20"}
    ]

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agency", "text": "Hi! We've started on the UI wireframes. Any specific feedback on the moodboard?"}]

if 'temp_brief' not in st.session_state:
    st.session_state.temp_brief = None

# --- MOCK AGENCY DATA FOR MATCHMAKING ---
MATCH_AGENCIES = [
    {"name": "PixelPerfect Digital", "specialization": "UI/UX & Branding", "match": "98%", "bio": "Top-tier design studio focused on conversion-driven aesthetics."},
    {"name": "CodeCrafters India", "specialization": "Full-Stack Web Dev", "match": "92%", "bio": "Experts in scalable MERN stack applications for SMEs."},
    {"name": "GrowthStream", "specialization": "Digital Marketing & SEO", "match": "85%", "bio": "Data-driven marketing agency with 10+ years in the Indian market."}
]

# --- SIDEBAR ROLE SWITCHER ---
with st.sidebar:
    st.image("Logo-1920*1080.jpg", use_container_width=True)
    st.markdown("<h2 style='text-align: center; color: #2ec4d1; font-size: 1.2rem;'>Control Center</h2>", unsafe_allow_html=True)
    st.markdown("---")
    user_role = st.selectbox("Switch Workspace", ["Business Dashboard", "Agency Portal"])
    st.markdown("---")
    st.caption(f"Logged in as: {'Client Admin' if 'Business' in user_role else 'Agency Lead'}")

# --- BUSINESS DASHBOARD ---
if "Business" in user_role:
    st.title("🏢 Business Project Portal")
    
    tabs = st.tabs(["📊 Active Projects", "📩 Messages", "📑 Create New Brief"])
    
    with tabs[0]:
        st.subheader("Current Engagements")
        for i, p in enumerate(st.session_state.active_projects):
            with st.container():
                st.markdown(f"""
                <div class="portal-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: #f8fafc;">{p['name']} <span class="status-pill status-active">{p['status']}</span></h3>
                        <p style="color: #2ec4d1; font-weight: bold;">{p['id']}</p>
                    </div>
                    <p>Partner: <b style="color: #2ec4d1;">{p['agency']} Digital</b></p>
                    <p>Current Milestone: <b>{p['milestone']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Show Submissions for this project
                subs = [s for s in st.session_state.project_submissions if s['project_id'] == p['id']]
                if subs:
                    st.markdown("🔍 **New Deliverables for Review:**")
                    for sub in subs:
                        col_s1, col_s2 = st.columns([3, 1])
                        col_s1.write(f"📂 {sub['filename']} (Submitted: {sub['timestamp']})")
                        if col_s2.button("Review", key=f"rev_{sub['filename']}"):
                            st.toast(f"Opening {sub['filename']}...")
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("Mark Milestone as Done", key=f"done_{p['id']}"):
                        st.session_state.active_projects[i]['status'] = "Milestone Approved"
                        st.session_state.active_projects[i]['progress'] = 100
                        st.success(f"Milestone '{p['milestone']}' marked as complete. Funds released.")
                        st.rerun()
                with col2:
                    st.info(f"💰 Escrow: ₹{p['escrow']:,}")
                with col3:
                    st.progress(p['progress'] / 100)

    with tabs[1]:
        st.subheader(f"Communication Channel")
        for msg in st.session_state.messages:
            div_class = "chat-agency" if msg['role'] == "agency" else "chat-user"
            st.markdown(f'<div class="chat-bubble {div_class}">{msg["text"]}</div>', unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Message the agency...")
            if st.form_submit_button("Send"):
                st.session_state.messages.append({"role": "user", "text": user_msg})
                st.rerun()

    with tabs[2]:
        st.subheader("Generate Technical Brief")
        with st.form("new_brief"):
            headline = st.text_input("Project Title")
            details = st.text_area("What do you want to build?")
            budget_sel = st.selectbox("Budget Range", ["₹50k - ₹1L", "₹1L - ₹5L", "₹5L - ₹20L", "₹20L+"])
            if st.form_submit_button("Run AI Briefing & Match Agencies"):
                with st.spinner("AI Analyzing requirements..."):
                    time.sleep(1.5)
                    st.session_state.temp_brief = {
                        "id": f"L-{int(time.time())}",
                        "title": headline,
                        "desc": details,
                        "budget": budget_sel,
                        "timeline": "TBD"
                    }
                    # Add to Agency Leads
                    st.session_state.open_leads.append(st.session_state.temp_brief)

        if st.session_state.temp_brief:
            st.success("Brief Generated & Listed Successfully!")
            st.markdown("### 🎯 Recommended Matches")
            for agency in MATCH_AGENCIES:
                with st.container():
                    st.markdown(f"""
                    <div class="portal-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <h4 style="color: #2ec4d1;">{agency['name']}</h4>
                                <p style="font-size: 14px; color: #94a3b8;">Specialization: <b>{agency['specialization']}</b></p>
                            </div>
                            <div class="match-score">{agency['match']}</div>
                        </div>
                        <p style="font-size: 14px;">{agency['bio']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Request Proposal from {agency['name']}", key=f"req_{agency['name']}"):
                        st.balloons()
                        st.info(f"Proposal request sent to {agency['name']}.")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    
    tabs = st.tabs(["💼 Active Work-room", "🔍 New Lead Discovery", "💰 Payments & Escrow"])
    
    with tabs[0]:
        st.subheader("Manage Active Projects")
        sel_proj_name = st.selectbox("Select Project", [p['name'] for p in st.session_state.active_projects])
        sel_proj = next(p for p in st.session_state.active_projects if p['name'] == sel_proj_name)
        
        st.markdown(f"""
        <div class="portal-card">
            <h4>Work-room: {sel_proj['name']}</h4>
            <p>Milestone: <b>{sel_proj['milestone']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        col_u1, col_u2 = st.columns([2, 1])
        with col_u1:
            st.write("### Upload Work")
            up_file = st.file_uploader("Upload Deliverable", key="up_v1")
            if up_file and st.button("Submit to Client"):
                st.session_state.project_submissions.append({
                    "project_id": sel_proj['id'],
                    "filename": up_file.name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("Deliverable submitted for review.")
                st.rerun()

        st.markdown("---")
        st.write("### Submission Management")
        proj_subs = [s for s in st.session_state.project_submissions if s['project_id'] == sel_proj['id']]
        if not proj_subs:
            st.caption("No submissions found.")
        else:
            for s_idx, s in enumerate(proj_subs):
                c_f1, c_f2 = st.columns([3, 1])
                c_f1.write(f"📄 {s['filename']}")
                if c_f2.button("Delete / Retract", key=f"del_{s_idx}"):
                    st.session_state.project_submissions.remove(s)
                    st.warning("Submission retracted.")
                    st.rerun()

    with tabs[1]:
        st.subheader("Leads Matching Your Profile")
        for lead in st.session_state.open_leads:
            with st.container():
                st.markdown(f"""
                <div class="portal-card">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="color: #f8fafc; font-size: 1.2rem;">{lead['title']}</b>
                        <span class="status-pill status-pending">New Lead</span>
                    </div>
                    <p style="margin-top:10px;">{lead['desc']}</p>
                    <p style="font-size: 14px; color: #2ec4d1;">Budget: {lead['budget']} | Timeline: {lead['timeline']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Submit Proposal", key=f"bid_{lead['id']}"):
                    st.success("Proposal Submitted! Client will be notified.")

    with tabs[2]:
        st.metric("Secured in Escrow", f"₹{sum(p['escrow'] for p in st.session_state.active_projects):,}")
        st.write("### Payment History")
        st.table(pd.DataFrame({
            "Project": [p['name'] for p in st.session_state.active_projects],
            "Milestone": [p['milestone'] for p in st.session_state.active_projects],
            "Amount": [f"₹{p['escrow']:,}" for p in st.session_state.active_projects],
            "Status": ["Awaiting Approval" if p['status'] != "Milestone Approved" else "Released" for p in st.session_state.active_projects]
        }))

# --- FOOTER ---
st.markdown("---")
st.caption("AgencyKart Portal v2.5 | End-to-End Aggregator Infrastructure")
