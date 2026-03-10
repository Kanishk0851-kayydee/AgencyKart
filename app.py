import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AgencyKart Portal | Scale Smarter", page_icon="🚀", layout="wide")

# --- CUSTOM THEMING & CSS ---
st.markdown("""
    <style>
    .main { background-color: #020617; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e293b; }
    
    /* Portal Cards */
    .portal-card {
        background: #1e293b;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    
    /* Status Badges */
    .status-pill {
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .status-active { background-color: #065f46; color: #34d399; }
    .status-pending { background-color: #7c2d12; color: #fb923c; }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-user { background: #0ea5e9; color: white; align-self: flex-end; margin-left: auto; }
    .chat-agency { background: #334155; color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Business"
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agency", "text": "Hi! We've started on the UI wireframes. Any specific feedback on the moodboard?"}]
if 'project_submissions' not in st.session_state:
    st.session_state.project_submissions = []

# --- MOCK DATA ---
PROJECTS = [
    {"id": "AK-992", "name": "E-Commerce Rebranding", "agency": "PixelPerfect", "status": "In Progress", "progress": 65, "escrow": "₹45,000 Locked"},
    {"id": "AK-401", "name": "AI Chatbot Integration", "agency": "TechFlow", "status": "Pending Brief", "progress": 10, "escrow": "₹12,000 Locked"}
]

# --- SIDEBAR ROLE SWITCHER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3140/3140343.png", width=80)
    st.title("AgencyKart")
    st.markdown("---")
    st.session_state.user_role = st.selectbox("Switch Workspace", ["Business Dashboard", "Agency Portal"])
    st.markdown("---")
    st.caption("Logged in as: " + ("Client Admin" if "Business" in st.session_state.user_role else "Lead Developer"))

# --- BUSINESS DASHBOARD ---
if "Business" in st.session_state.user_role:
    st.title("🏢 Business Project Portal")
    st.markdown("Manage your agencies and monitor project health in real-time.")
    
    tabs = st.tabs(["📊 Active Projects", "📩 Messages", "📑 Create New Brief"])
    
    with tabs[0]:
        for p in PROJECTS:
            with st.container():
                st.markdown(f"""
                <div class="portal-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3>{p['name']} <span class="status-pill status-active">{p['status']}</span></h3>
                        <p style="color: #2dd4bf; font-weight: bold;">{p['id']}</p>
                    </div>
                    <p>Agency: <b>{p['agency']} Digital</b></p>
                    <div style="margin: 15px 0;">
                        <small>Completion Progress: {p['progress']}%</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(p['progress'] / 100)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button(f"View Deliverables", key=f"view_{p['id']}"):
                        st.write("📂 Milestone_1_Final.pdf")
                with col2:
                    st.button(f"Release Payment", key=f"pay_{p['id']}")
                with col3:
                    st.info(f"💰 Escrow Status: {p['escrow']}")

    with tabs[1]:
        st.subheader(f"Chat with {PROJECTS[0]['agency']} Digital")
        for msg in st.session_state.messages:
            div_class = "chat-agency" if msg['role'] == "agency" else "chat-user"
            st.markdown(f'<div class="chat-bubble {div_class}">{msg["text"]}</div>', unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            user_msg = st.text_input("Type your message...")
            if st.form_submit_button("Send"):
                st.session_state.messages.append({"role": "user", "text": user_msg})
                st.rerun()

    with tabs[2]:
        st.subheader("Launch a New Requirement")
        with st.form("new_brief"):
            st.text_input("Project Headline")
            st.text_area("Detailed Requirements")
            st.file_uploader("Attach Brand Guidelines (Optional)")
            if st.form_submit_button("Generate AI Brief"):
                st.success("AI is processing your requirements. Matching agencies will appear shortly.")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    st.markdown("Submit work, find new leads, and manage client expectations.")
    
    tabs = st.tabs(["💼 Project Work-room", "🔍 Open Leads", "💰 Financials"])
    
    with tabs[0]:
        st.subheader("Current Assignments")
        selected_proj = st.selectbox("Select Project to Manage", [p['name'] for p in PROJECTS])
        
        st.markdown(f"""
        <div class="portal-card">
            <h4>Work-room: {selected_proj}</h4>
            <p>Milestone 2: Backend API Integration</p>
            <p>Deadline: Oct 25, 2023</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### Upload Deliverables")
        uploaded_file = st.file_uploader("Upload files for client approval (PDF, ZIP, Figma Links)", key="deliverable_upload")
        if uploaded_file:
            if st.button("Submit to Client"):
                st.session_state.project_submissions.append(uploaded_file.name)
                st.success(f"File '{uploaded_file.name}' submitted! Client has been notified for Escrow release.")
        
        st.markdown("---")
        st.write("### History of Submissions")
        if not st.session_state.project_submissions:
            st.caption("No files submitted for this milestone yet.")
        else:
            for f in st.session_state.project_submissions:
                st.write(f"✅ {f} - *Pending Review*")

    with tabs[1]:
        st.subheader("New Opportunities for You")
        st.markdown("""
        <div class="portal-card">
            <div style="display: flex; justify-content: space-between;">
                <b>Mobile App for Fintech Startup</b>
                <span class="status-pill status-pending">High Match</span>
            </div>
            <p style="font-size: 14px; margin-top:10px;">Budget: ₹2.5L - ₹4L | Timeline: 3 Months</p>
            <button style="width: 100%; padding: 8px; margin-top: 10px; background: #2dd4bf; border: none; border-radius: 5px; color: #020617; font-weight: bold;">Apply with Proposal</button>
        </div>
        """, unsafe_allow_html=True)

    with tabs[2]:
        st.metric("Total in Escrow", "₹57,000", delta="₹12,000 this week")
        st.write("### Payment Milestones")
        st.table(pd.DataFrame({
            "Project": ["E-Commerce", "E-Commerce", "Chatbot"],
            "Milestone": ["UI Design", "Deployment", "Setup"],
            "Amount": ["₹20,000", "₹25,000", "₹12,000"],
            "Status": ["Released", "In Escrow", "In Escrow"]
        }))

# --- FOOTER ---
st.markdown("---")
st.caption("AgencyKart Portal v2.0 - Encrypted Milestone-based Ecosystem")
