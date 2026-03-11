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

# --- CUSTOM THEMING & CSS ---
# Brand Colors: Cyan #2ec4d1 | Navy #0b1a32 | Accent Navy #162a4a
st.markdown("""
    <style>
    .main { background-color: #0b1a32; color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #0b1a32; border-right: 1px solid #162a4a; }
    
    /* Portal Cards */
    .portal-card {
        background: #162a4a;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #243b61;
        margin-bottom: 20px;
    }
    
    /* Status Badges */
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
    
    /* Buttons */
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
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-user { background: #2ec4d1; color: #0b1a32; align-self: flex-end; margin-left: auto; border: 1px solid #2ec4d1; }
    .chat-agency { background: #243b61; color: #f8fafc; border: 1px solid #2ec4d1; align-self: flex-start; }
    
    .match-score { font-size: 24px; color: #2ec4d1; font-weight: bold; }
    
    /* Overlays & Modals */
    .payment-modal, .contract-viewer {
        background: #020617;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #2ec4d1;
        margin-top: 15px;
        margin-bottom: 25px;
    }

    /* FLOATING LOGO (Bottom Right) */
    .floating-logo-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 150px;
        z-index: 9999;
        pointer-events: none;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FLOATING LOGO OVERLAY ---
# This ensures the logo stays visible even if the sidebar is hidden
try:
    import base64
    def get_base64(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    bin_str = get_base64('Logo-1920*1080.jpg')
    st.markdown(
        f"""
        <div class="floating-logo-container">
            <img src="data:image/png;base64,{bin_str}" style="width: 100%;">
        </div>
        """,
        unsafe_allow_html=True
    )
except:
    # Fallback text watermark if file is missing
    st.markdown(
        """
        <div class="floating-logo-container">
            <h3 style="color: #2ec4d1; margin: 0;">AgencyKart</h3>
            <p style="color: #f8fafc; font-size: 10px; margin: 0;">Scale Smarter™</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- SESSION STATE INITIALIZATION ---
if 'active_projects' not in st.session_state:
    st.session_state.active_projects = [
        {
            "id": "AK-992", 
            "business": "PVR Cinemas", 
            "name": "Mobile App UI", 
            "agency": "PixelPerfect", 
            "status": "In Progress", 
            "progress": 65, 
            "total_quote": 100000, 
            "paid_history": [{"amount": 40000, "date": "2023-09-15"}],
            "milestone": "UI Design"
        }
    ]

if 'contracts' not in st.session_state:
    st.session_state.contracts = [
        {
            "id": "CON-881",
            "project_name": "Mobile App UI",
            "partner": "PixelPerfect",
            "status": "Awaiting Client Signature",
            "date_created": "2023-10-01",
            "signed_by_client": False,
            "signed_by_agency": True
        }
    ]

if 'proposals' not in st.session_state:
    st.session_state.proposals = [
        {
            "id": "PROP-101",
            "business": "PVR Cinemas",
            "project_name": "Web Dashboard",
            "agency": "CodeCrafters India",
            "amount": 75000,
            "status": "Review Required",
            "history": []
        }
    ]

if 'brief_generated' not in st.session_state:
    st.session_state.brief_generated = False
if 'generated_brief_data' not in st.session_state:
    st.session_state.generated_brief_data = {}
if 'project_submissions' not in st.session_state:
    st.session_state.project_submissions = []
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agency", "text": "Hi there! We've uploaded the moodboards. Please check the 'Projects' tab."}]
if 'paying_project_id' not in st.session_state:
    st.session_state.paying_project_id = None
if 'negotiating_prop_id' not in st.session_state:
    st.session_state.negotiating_prop_id = None
if 'viewing_contract_id' not in st.session_state:
    st.session_state.viewing_contract_id = None
if 'open_leads' not in st.session_state:
    st.session_state.open_leads = [
        {"id": "L-001", "title": "Fintech App Design", "desc": "Looking for a high-fidelity dashboard for a personal finance app.", "budget": "₹2.5L", "requested_from": "General"}
    ]

# --- MOCK AGENCY DATA ---
MATCH_AGENCIES = [
    {"name": "PixelPerfect Digital", "specialization": "UI/UX & Branding", "match": "98%", "bio": "Top-tier design studio focused on conversion-driven aesthetics."},
    {"name": "CodeCrafters India", "specialization": "Full-Stack Web Dev", "match": "92%", "bio": "Experts in scalable MERN stack applications for SMEs."}
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
    st.markdown("""
    **Agreement Summary:** All payments processed via **Secure Pay Vault**. 
    Intellectual Property transfers to Client upon final payout.
    """)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if "Business" in role_title and not contract['signed_by_client']:
            if st.button("🖊️ E-Sign Contract", key=f"sign_btn_{contract_id}"):
                contract['signed_by_client'] = True
                contract['status'] = "Fully Executed"
                st.rerun()
        elif contract['signed_by_client']:
            st.success("✅ Signed by Client")
        else:
            st.info("⏳ Awaiting Client")
    
    with c2:
        if contract.get('signed_by_agency'):
            st.success("✅ Signed by Agency")
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
    try:
        st.image("Logo-1920*1080.jpg", use_container_width=True)
    except:
        st.markdown("<h1 style='color: #2ec4d1;'>AgencyKart</h1>", unsafe_allow_html=True)
        
    st.markdown("<h2 style='text-align: center; color: #2ec4d1; font-size: 1.1rem;'>PORTAL ACCESS</h2>", unsafe_allow_html=True)
    st.markdown("---")
    user_role = st.selectbox("Select Workspace", ["Business Dashboard", "Agency Portal"])
    st.markdown("---")
    if st.button("Reset All Portal Data"):
        st.session_state.clear()
        st.rerun()

# --- BUSINESS DASHBOARD ---
if "Business" in user_role:
    st.title("🏢 Business Project Portal")
    tabs = st.tabs(["📊 Projects", "📥 Proposals", "📜 Contracts", "📩 Agency Chat", "📑 Hire Agencies"])
    
    with tabs[0]:
        indices_to_delete = []
        for i, p in enumerate(st.session_state.active_projects):
            total_paid = sum(item['amount'] for item in p['paid_history'])
            remaining = p['total_quote'] - total_paid
            with st.container():
                status_class = 'status-active'
                if remaining <= 0: status_class = 'status-paid'

                st.markdown(f"""
                <div class="portal-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color: #f8fafc; margin:0;">{p['name']} <span class="status-pill {status_class}">{p['status']}</span></h3>
                        <p style="color: #2ec4d1; font-weight: bold; margin:0;">{p['id']}</p>
                    </div>
                    <p style="margin-top:10px;">Partner: <b style="color: #2ec4d1;">{p['agency']} Digital</b> | Milestone: <b>{p['milestone']}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                subs = [s for s in st.session_state.project_submissions if s['project_id'] == p['id']]
                if subs:
                    st.write("📂 **New Deliverables for Review:**")
                    for sub in subs:
                        col_s1, col_s2 = st.columns([3, 1])
                        col_s1.info(f"📄 {sub['filename']} (Sent: {sub['timestamp']})")
                        if col_s2.button("Partial / Full Release", key=f"pay_trig_{sub['filename']}"):
                            st.session_state.paying_project_id = p['id']
                
                if st.session_state.paying_project_id == p['id']:
                    st.markdown('<div class="payment-modal">', unsafe_allow_html=True)
                    st.subheader("💰 Partial Payment Release")
                    st.write(f"Total Quote: ₹{p['total_quote']:,} | Remaining: ₹{remaining:,}")
                    amount_to_pay = st.number_input("Amount (₹)", min_value=0, max_value=remaining, step=1000, key=f"amt_{p['id']}")
                    c1, c2 = st.columns(2)
                    if c1.button("Confirm Release", key=f"conf_{p['id']}"):
                        st.session_state.active_projects[i]['paid_history'].append({"amount": amount_to_pay, "date": datetime.now().strftime("%Y-%m-%d")})
                        st.session_state.paying_project_id = None
                        st.rerun()
                    if c2.button("Cancel", key=f"canc_{p['id']}"):
                        st.session_state.paying_project_id = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.progress(p['progress'] / 100)
                m_col1, m_col2 = st.columns(2)
                if m_col1.button(f"Settle Full Balance (₹{remaining:,})", key=f"comp_{p['id']}"):
                    st.session_state.active_projects[i]['paid_history'].append({"amount": remaining, "date": datetime.now().strftime("%Y-%m-%d")})
                    st.rerun()
                if m_col2.button(f"🗑️ Delete Project", key=f"del_{p['id']}"):
                    indices_to_delete.append(i)
        
        if indices_to_delete:
            for idx in reversed(indices_to_delete): st.session_state.active_projects.pop(idx)
            st.rerun()

    with tabs[1]:
        st.subheader("📥 Incoming Proposals")
        for idx, prop in enumerate(st.session_state.proposals):
            with st.container():
                st.markdown(f'<div class="portal-card"><b>{prop["project_name"]}</b> (From: {prop["agency"]})<br>Quote: ₹{prop["amount"]:,}</div>', unsafe_allow_html=True)
                if st.button("Accept Proposal & Start Project", key=f"acc_{prop['id']}"):
                    st.session_state.active_projects.append({
                        "id": f"AK-{int(time.time())}", "business": "PVR Cinemas", "name": prop['project_name'],
                        "agency": prop['agency'], "status": "In Progress", "progress": 0, "total_quote": prop['amount'],
                        "paid_history": [], "milestone": "Initiation"
                    })
                    st.session_state.contracts.append({
                        "id": f"CON-{int(time.time())}", "project_name": prop['project_name'], "partner": prop['agency'],
                        "status": "Awaiting Client Signature", "date_created": datetime.now().strftime("%Y-%m-%d"), "signed_by_client": False
                    })
                    st.session_state.proposals.pop(idx)
                    st.rerun()

    with tabs[2]:
        st.subheader("📜 Project Contracts")
        if st.session_state.viewing_contract_id:
            render_contract_view(st.session_state.viewing_contract_id, "Business Dashboard")
        for contract in st.session_state.contracts:
            with st.container():
                st.markdown(f'<div class="portal-card"><b>{contract["project_name"]}</b><br>Status: {contract["status"]}</div>', unsafe_allow_html=True)
                if st.button("View & Sign", key=f"view_btn_{contract['id']}"):
                    st.session_state.viewing_contract_id = contract['id']
                    st.rerun()

    with tabs[3]: render_chat_hub('business')

    with tabs[4]:
        st.subheader("AI Briefing Assistant")
        with st.form("ai_brief"):
            h = st.text_input("Project Name")
            d = st.text_area("Requirements")
            budget = st.select_slider("Budget", options=["₹50k-₹1L", "₹1L-₹5L", "₹5L-₹20L", "₹20L+"])
            if st.form_submit_button("Generate Brief & Match"):
                st.session_state.brief_generated = True
                st.session_state.generated_brief_data = {"name": h, "desc": d, "budget": budget}
        
        if st.session_state.brief_generated:
            st.success("✅ AI Brief Generated!")
            for agency in MATCH_AGENCIES:
                with st.container():
                    st.markdown(f'<div class="portal-card"><b>{agency["name"]}</b> ({agency["match"]})</div>', unsafe_allow_html=True)
                    if st.button(f"Request Proposal from {agency['name']}", key=f"req_{agency['name']}"):
                        st.session_state.open_leads.append({"id": f"L-{int(time.time())}", "title": h, "desc": d, "budget": budget, "requested_from": agency['name']})
                        st.info(f"Proposal request sent.")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    tabs = st.tabs(["💼 My Projects", "📜 Contracts", "📩 Client Chat", "🔍 Lead Market", "💰 Payments"])
    
    with tabs[0]:
        biz_projects = st.session_state.active_projects
        for p in biz_projects:
            with st.container():
                st.markdown(f'<div class="portal-card"><b>Project: {p["name"]}</b> ({p["status"]})</div>', unsafe_allow_html=True)
                if p['status'] != 'Payment Completed':
                    f_up = st.file_uploader(f"Upload work for {p['name']}", key=f"up_{p['id']}")
                    if f_up and st.button("Submit Work", key=f"btn_{p['id']}"):
                        st.session_state.project_submissions.append({"project_id": p['id'], "filename": f_up.name, "timestamp": datetime.now().strftime("%H:%M")})
                        st.rerun()

    with tabs[1]:
        st.subheader("📜 Legal Contracts")
        if st.session_state.viewing_contract_id:
            render_contract_view(st.session_state.viewing_contract_id, "Agency Portal")
        for contract in st.session_state.contracts:
            with st.container():
                st.markdown(f'<div class="portal-card"><b>{contract["project_name"]}</b><br>Status: {contract["status"]}</div>', unsafe_allow_html=True)
                if st.button("View MSA", key=f"view_agency_{contract['id']}"):
                    st.session_state.viewing_contract_id = contract['id']
                    st.rerun()

    with tabs[2]: render_chat_hub('agency')

    with tabs[3]:
        st.subheader("Market Leads")
        for lead in st.session_state.open_leads:
            st.markdown(f'<div class="portal-card"><b>{lead["title"]}</b><br>{lead["desc"]}</div>', unsafe_allow_html=True)
            st.button("Submit Proposal", key=f"bid_{lead['id']}")

    with tabs[4]:
        st.subheader("Agency Financials")
        total_earned = sum(sum(item['amount'] for item in p['paid_history']) for p in st.session_state.active_projects)
        st.metric("Total Agency Earnings", f"₹{total_earned:,}")
        st.table(pd.DataFrame([{"Project": p['name'], "Date": pay['date'], "Amount": f"₹{pay['amount']:,}"} for p in st.session_state.active_projects for pay in p['paid_history']]))

st.markdown("---")
st.caption("AgencyKart Portal v3.6 | Secure B2B Infrastructure")
