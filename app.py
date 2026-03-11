import streamlit as st
import pandas as pd
import time
from datetime import datetime
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AgencyKart Portal | Scale Smarter", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL MOCK DATA (Defined at top to prevent NameErrors) ---
MATCH_AGENCIES = [
    {"name": "PixelPerfect Digital", "specialization": "UI/UX & Branding", "match": "98%", "bio": "Top-tier design studio focused on conversion-driven aesthetics."},
    {"name": "CodeCrafters India", "specialization": "Full-Stack Web Dev", "match": "92%", "bio": "Experts in scalable MERN stack applications for SMEs."}
]

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
        border-radius: 9999px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .status-active { background-color: rgba(46, 196, 209, 0.2); color: #2ec4d1; border: 1px solid #2ec4d1; }
    .status-done { background-color: rgba(52, 211, 153, 0.2); color: #34d399; border: 1px solid #34d399; }
    .status-paid { background-color: rgba(46, 196, 209, 0.4); color: #ffffff; border: 1px solid #2ec4d1; }
    .status-neg { background-color: rgba(251, 146, 60, 0.2); color: #fb923c; border: 1px solid #fb923c; }
    .status-signed { background-color: rgba(46, 196, 209, 0.3); color: #2ec4d1; border: 1px solid #2ec4d1; }
    
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
    .chat-user { background: #2ec4d1; color: #0b1a32; align-self: flex-end; margin-left: auto; border: 1px solid #2ec4d1; }
    .chat-agency { background: #243b61; color: #f8fafc; border: 1px solid #2ec4d1; align-self: flex-start; }
    
    .match-score { font-size: 24px; color: #2ec4d1; font-weight: bold; }
    
    .payment-modal, .contract-viewer {
        background: #020617;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #2ec4d1;
        margin-top: 15px;
        margin-bottom: 25px;
    }

    .floating-logo-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 150px;
        z-index: 9999;
        pointer-events: none;
        opacity: 0.8;
    }

    .welcome-card {
        text-align: center;
        padding: 60px;
        background: linear-gradient(135deg, #162a4a 0%, #0b1a32 100%);
        border-radius: 30px;
        border: 1px solid #2ec4d1;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FLOATING LOGO OVERLAY ---
try:
    def get_base64(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    bin_str = get_base64('Logo-1920*1080.jpg')
    st.markdown(f'<div class="floating-logo-container"><img src="data:image/png;base64,{bin_str}" style="width: 100%;"></div>', unsafe_allow_html=True)
except:
    st.markdown('<div class="floating-logo-container"><h3 style="color: #2ec4d1; margin: 0;">AgencyKart</h3><p style="color: #f8fafc; font-size: 10px; margin: 0;">Scale Smarter™</p></div>', unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Home"

if 'active_projects' not in st.session_state:
    st.session_state.active_projects = [
        {
            "id": "AK-992", "business": "PVR Cinemas", "name": "Mobile App UI", "agency": "PixelPerfect", 
            "status": "In Progress", "progress": 65, "total_quote": 12000, "paid_history": [{"amount": 4000, "date": "2023-09-15"}],
            "milestone": "UI Design"
        }
    ]

if 'contracts' not in st.session_state:
    st.session_state.contracts = [
        {
            "id": "CON-881", "project_name": "Mobile App UI", "partner": "PixelPerfect", "status": "Awaiting Client Signature",
            "date_created": "2023-10-01", "signed_by_client": False, "signed_by_agency": True
        }
    ]

if 'proposals' not in st.session_state:
    st.session_state.proposals = [
        {
            "id": "PROP-101", "business": "PVR Cinemas", "project_name": "Web Dashboard", "agency": "CodeCrafters India",
            "amount": 8500, "status": "Review Required", "history": []
        }
    ]

if 'brief_generated' not in st.session_state:
    st.session_state.brief_generated = False
if 'project_submissions' not in st.session_state:
    st.session_state.project_submissions = []
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agency", "text": "Hi there! We've uploaded the moodboards. Please check the 'Projects' tab."}]
if 'paying_project_id' not in st.session_state:
    st.session_state.paying_project_id = None
if 'viewing_contract_id' not in st.session_state:
    st.session_state.viewing_contract_id = None
if 'open_leads' not in st.session_state:
    st.session_state.open_leads = [
        {"id": "L-001", "title": "Fintech App Design", "desc": "Looking for a high-fidelity dashboard.", "budget": "$3,000", "requested_from": "General"}
    ]

# --- SHARED COMPONENTS ---
def render_chat_hub(current_role):
    st.subheader(f"Direct Communication Hub")
    chat_col, action_col = st.columns([3, 1])
    with chat_col:
        for msg in st.session_state.messages:
            div_class = "chat-agency" if msg['role'] == "agency" else "chat-user"
            st.markdown(f'<div class="chat-bubble {div_class}">{msg["text"]}</div>', unsafe_allow_html=True)
        with st.form(f"chat_form_{current_role}", clear_on_submit=True):
            user_input = st.text_input("Type message...")
            if st.form_submit_button("Send"):
                if user_input:
                    role_key = "user" if current_role == 'business' else "agency"
                    st.session_state.messages.append({"role": role_key, "text": user_input})
                    st.rerun()

def render_contract_view(contract_id, role_title):
    contract = next((c for c in st.session_state.contracts if c['id'] == contract_id), None)
    if not contract: return
    st.markdown('<div class="contract-viewer">', unsafe_allow_html=True)
    st.subheader(f"📄 MSA: {contract['project_name']}")
    st.write("Agreement Summary: All payments processed via Secure Pay Vault. IP transfers to Client upon final payout.")
    c1, c2, c3 = st.columns(3)
    with c1:
        if "Business" in role_title and not contract['signed_by_client']:
            if st.button("🖊️ E-Sign Contract", key=f"sign_btn_{contract_id}"):
                contract['signed_by_client'] = True
                contract['status'] = "Fully Executed"
                st.rerun()
        elif contract['signed_by_client']: st.success("✅ Signed by Client")
        else: st.info("⏳ Awaiting Client")
    with c2:
        if contract.get('signed_by_agency'): st.success("✅ Signed by Agency")
        else:
            if st.button("🖊️ Agency E-Sign", key=f"agency_sign_{contract_id}"):
                contract['signed_by_agency'] = True
                st.rerun()
    with c3:
        if st.button("Close Viewer", key=f"close_{contract_id}"):
            st.session_state.viewing_contract_id = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    try: st.image("Logo-1920*1080.jpg", use_container_width=True)
    except: st.markdown("<h1 style='color: #2ec4d1;'>AgencyKart</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.session_state.user_role = st.selectbox("Switch Workspace", ["Home", "Business Dashboard", "Agency Portal"],
                                             index=["Home", "Business Dashboard", "Agency Portal"].index(st.session_state.user_role))
    st.markdown("---")
    if st.button("Reset Portal"): st.session_state.clear(); st.rerun()

# --- HOME SCREEN ---
if st.session_state.user_role == "Home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<div class="welcome-card"><h1 style="color: #f8fafc; font-size: 80px; margin-bottom: 0;">AGENCYKART</h1><h2 style="color: #2ec4d1; letter-spacing: 12px; margin-top: 0; font-size: 32px;">SCALE SMARTER</h2><p style="font-size: 24px; color: #94a3b8; margin-top: 20px;">The AI-Driven Operating System for Modern B2B Partnerships.</p></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_center, _ = st.columns([0.5, 3, 0.5])
        with btn_center:
            btn_col1, btn_col2 = st.columns(2)
            if btn_col1.button("🏢 ENTER BUSINESS PORTAL"): st.session_state.user_role = "Business Dashboard"; st.rerun()
            if btn_col2.button("🚀 ENTER AGENCY PORTAL"): st.session_state.user_role = "Agency Portal"; st.rerun()

# --- BUSINESS DASHBOARD ---
elif "Business" in st.session_state.user_role:
    st.title("🏢 Business Project Portal")
    tabs = st.tabs(["📊 Projects", "📥 Proposals", "📜 Contracts", "📩 Agency Chat", "📑 Hire Agencies"])
    
    with tabs[0]:
        for i, p in enumerate(st.session_state.active_projects):
            total_paid = sum(item['amount'] for item in p['paid_history'])
            remaining = p['total_quote'] - total_paid
            with st.container():
                st.markdown(f'<div class="portal-card"><h3 style="color: #f8fafc; margin:0;">{p["name"]} <span class="status-pill status-active">{p["status"]}</span></h3><p>Partner: <b style="color: #2ec4d1;">{p["agency"]}</b> | Milestone: <b>{p["milestone"]}</b></p></div>', unsafe_allow_html=True)
                subs = [s for s in st.session_state.project_submissions if s['project_id'] == p['id']]
                if subs:
                    for sub in subs:
                        col_s1, col_s2 = st.columns([3, 1])
                        col_s1.info(f"📄 {sub['filename']}")
                        if col_s2.button("Release Payment", key=f"pay_{sub['filename']}"): st.session_state.paying_project_id = p['id']
                if st.session_state.paying_project_id == p['id']:
                    st.markdown('<div class="payment-modal">', unsafe_allow_html=True)
                    amt = st.number_input("Amount ($)", min_value=0, max_value=int(remaining), step=500)
                    if st.button("Confirm Release"):
                        st.session_state.active_projects[i]['paid_history'].append({"amount": amt, "date": datetime.now().strftime("%Y-%m-%d")})
                        st.session_state.paying_project_id = None; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                st.progress(p['progress'] / 100); st.write(f"Remaining: ${remaining:,}")

    with tabs[2]:
        if st.session_state.viewing_contract_id: render_contract_view(st.session_state.viewing_contract_id, "Business")
        for c in st.session_state.contracts:
            if st.button(f"View MSA: {c['project_name']}", key=f"v_{c['id']}"): st.session_state.viewing_contract_id = c['id']; st.rerun()

    with tabs[3]: render_chat_hub('business')

    with tabs[4]:
        st.subheader("AI Briefing Assistant")
        with st.form("ai_brief"):
            h = st.text_input("Project Name")
            d = st.text_area("Requirements")
            budget = st.select_slider("Budget ($)", options=["$500-$1.5k", "$1.5k-$5k", "$5k-$20k", "$20k+"])
            if st.form_submit_button("Generate Brief & Match"):
                st.session_state.brief_generated = True
        if st.session_state.brief_generated:
            st.success("✅ AI Brief Generated!")
            for agency in MATCH_AGENCIES:
                with st.container():
                    st.markdown(f'<div class="portal-card"><b>{agency["name"]}</b> ({agency["match"]})</div>', unsafe_allow_html=True)
                    if st.button(f"Request Proposal from {agency['name']}", key=f"req_{agency['name']}"):
                        st.info("Proposal request sent.")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    tabs = st.tabs(["💼 My Projects", "📜 Contracts", "📩 Client Chat", "🔍 Lead Market", "💰 Payments"])
    with tabs[0]:
        for p in st.session_state.active_projects:
            st.markdown(f'<div class="portal-card"><b>{p["name"]}</b> ({p["status"]})</div>', unsafe_allow_html=True)
            f = st.file_uploader(f"Upload work for {p['name']}", key=f"up_{p['id']}")
            if f and st.button("Submit", key=f"btn_{p['id']}"):
                st.session_state.project_submissions.append({"project_id": p['id'], "filename": f.name, "timestamp": datetime.now().strftime("%H:%M")})
                st.rerun()
    with tabs[1]:
        if st.session_state.viewing_contract_id: render_contract_view(st.session_state.viewing_contract_id, "Agency")
        for c in st.session_state.contracts:
            if st.button(f"View MSA: {c['project_name']}", key=f"va_{c['id']}"): st.session_state.viewing_contract_id = c['id']; st.rerun()
    with tabs[2]: render_chat_hub('agency')
    with tabs[4]:
        earned = sum(sum(item['amount'] for item in p['paid_history']) for p in st.session_state.active_projects)
        st.metric("Total Earnings", f"${earned:,}")

st.markdown("---")
st.caption("AgencyKart Portal v3.8 | Secure B2B Infrastructure | $ USD Metrics")
