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
    
    .payment-modal {
        background: #020617;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #2ec4d1;
        margin-top: 15px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

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
    st.session_state.messages = [{"role": "agency", "text": "Hi there! We've uploaded the initial moodboards. Please check the 'Active Projects' tab."}]
if 'paying_project_id' not in st.session_state:
    st.session_state.paying_project_id = None
if 'negotiating_prop_id' not in st.session_state:
    st.session_state.negotiating_prop_id = None
if 'open_leads' not in st.session_state:
    st.session_state.open_leads = [
        {"id": "L-001", "title": "Fintech App Design", "desc": "Looking for a high-fidelity dashboard for a personal finance app.", "budget": "₹2.5L", "requested_from": "General"}
    ]

# --- MOCK AGENCY DATA ---
MATCH_AGENCIES = [
    {"name": "PixelPerfect Digital", "specialization": "UI/UX & Branding", "match": "98%", "bio": "Top-tier design studio focused on conversion-driven aesthetics."},
    {"name": "CodeCrafters India", "specialization": "Full-Stack Web Dev", "match": "92%", "bio": "Experts in scalable MERN stack applications for SMEs."}
]

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

# --- SHARED CHAT ---
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

# --- BUSINESS DASHBOARD ---
if "Business" in user_role:
    st.title("🏢 Business Project Portal")
    tabs = st.tabs(["📊 Projects", "📥 Proposals", "📩 Agency Chat", "📑 Hire & Brief Agencies"])
    
    with tabs[0]:
        indices_to_delete = []
        for i, p in enumerate(st.session_state.active_projects):
            total_paid = sum(item['amount'] for item in p['paid_history'])
            remaining = p['total_quote'] - total_paid
            with st.container():
                status_class = 'status-active'
                if remaining <= 0:
                    status_class = 'status-paid'
                    st.session_state.active_projects[i]['status'] = 'Payment Completed'

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
                        if col_s2.button("Release Payment", key=f"pay_trig_{sub['filename']}"):
                            st.session_state.paying_project_id = p['id']
                
                if st.session_state.paying_project_id == p['id']:
                    st.markdown('<div class="payment-modal">', unsafe_allow_html=True)
                    st.subheader("💰 Release Vault Payment")
                    st.write(f"Total Quote: ₹{p['total_quote']:,} | Remaining: ₹{remaining:,}")
                    amount_to_pay = st.number_input("Amount (₹)", min_value=0, max_value=remaining, step=1000, key=f"amt_{p['id']}")
                    c1, c2 = st.columns(2)
                    if c1.button("Confirm", key=f"conf_{p['id']}"):
                        st.session_state.active_projects[i]['paid_history'].append({"amount": amount_to_pay, "date": datetime.now().strftime("%Y-%m-%d")})
                        st.session_state.paying_project_id = None
                        st.rerun()
                    if c2.button("Cancel", key=f"canc_{p['id']}"):
                        st.session_state.paying_project_id = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                st.progress(p['progress'] / 100)
                m_col1, m_col2 = st.columns(2)
                if m_col1.button(f"Settle Balance (₹{remaining:,})", key=f"comp_{p['id']}"):
                    st.session_state.active_projects[i]['paid_history'].append({"amount": remaining, "date": datetime.now().strftime("%Y-%m-%d")})
                    st.rerun()
                if m_col2.button(f"🗑️ Delete Project", key=f"del_{p['id']}"):
                    indices_to_delete.append(i)
        
        if indices_to_delete:
            for idx in reversed(indices_to_delete):
                st.session_state.active_projects.pop(idx)
            st.rerun()

    with tabs[1]:
        st.subheader("📥 Incoming Proposals")
        if not st.session_state.proposals:
            st.info("No proposals received yet.")
        else:
            for idx, prop in enumerate(st.session_state.proposals):
                with st.container():
                    st.markdown(f"""
                    <div class="portal-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h3 style="color: #f8fafc; margin:0;">{prop['project_name']}</h3>
                                <p style="color: #2ec4d1; font-weight: bold; margin-top:5px;">From: {prop['agency']}</p>
                            </div>
                            <div style="text-align: right;">
                                <h2 style="color: #2ec4d1; margin:0;">₹{prop['amount']:,}</h2>
                                <span class="status-pill status-neg">{prop['status']}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state.negotiating_prop_id == prop['id']:
                        st.markdown('<div class="payment-modal">', unsafe_allow_html=True)
                        st.write("### 🤝 Pitch Counter Offer")
                        new_pitch = st.number_input("Your Counter Offer (₹)", value=prop['amount'], step=1000)
                        neg_col1, neg_col2 = st.columns(2)
                        if neg_col1.button("Send Counter Offer", key=f"send_neg_{prop['id']}"):
                            st.session_state.proposals[idx]['amount'] = new_pitch
                            st.session_state.proposals[idx]['status'] = "Negotiating"
                            st.session_state.negotiating_prop_id = None
                            st.toast("Counter offer sent to agency!")
                            st.rerun()
                        if neg_col2.button("Cancel", key=f"canc_neg_{prop['id']}"):
                            st.session_state.negotiating_prop_id = None
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        c_acc, c_neg, c_dec = st.columns(3)
                        if c_acc.button("Accept Proposal", key=f"acc_{prop['id']}"):
                            st.session_state.active_projects.append({
                                "id": f"AK-{int(time.time())}",
                                "business": prop['business'],
                                "name": prop['project_name'],
                                "agency": prop['agency'].replace(" India", "").replace(" Digital", ""),
                                "status": "In Progress",
                                "progress": 0,
                                "total_quote": prop['amount'],
                                "paid_history": [],
                                "milestone": "Initiation"
                            })
                            st.session_state.proposals.pop(idx)
                            st.balloons()
                            st.rerun()
                        if c_neg.button("Negotiate / Counter", key=f"neg_{prop['id']}"):
                            st.session_state.negotiating_prop_id = prop['id']
                            st.rerun()
                        if c_dec.button("Decline", key=f"dec_{prop['id']}"):
                            st.session_state.proposals.pop(idx)
                            st.rerun()

    with tabs[2]:
        render_chat_hub('business')

    with tabs[3]:
        st.subheader("AI Briefing & Discovery")
        with st.form("ai_brief"):
            h = st.text_input("Project Name")
            d = st.text_area("Requirements")
            budget = st.select_slider("Budget Range", options=["₹50k - ₹1L", "₹1L - ₹5L", "₹5L - ₹20L", "₹20L+"])
            if st.form_submit_button("Generate & Match Agencies"):
                if h and d:
                    st.session_state.brief_generated = True
                    st.session_state.generated_brief_data = {"name": h, "desc": d, "budget": budget}
        
        if st.session_state.brief_generated:
            st.success("✅ AI Brief Ready!")
            for agency in MATCH_AGENCIES:
                with st.container():
                    st.markdown(f'<div class="portal-card"><b>{agency["name"]}</b> ({agency["match"]})<br><small>{agency["specialization"]}</small></div>', unsafe_allow_html=True)
                    if st.button(f"Request Proposal from {agency['name']}", key=f"req_{agency['name']}"):
                        st.session_state.proposals.append({
                            "id": f"PROP-{int(time.time())}",
                            "business": "Your Company",
                            "project_name": st.session_state.generated_brief_data["name"],
                            "agency": agency['name'],
                            "amount": 0,
                            "status": "Awaiting Quote",
                            "history": []
                        })
                        st.info(f"Request sent to {agency['name']}.")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    tabs = st.tabs(["💼 My Projects", "📩 Client Chat", "🔍 Lead Market", "💰 Payments & Vaults"])
    
    with tabs[0]:
        businesses = list(set([p['business'] for p in st.session_state.active_projects]))
        selected_biz = st.selectbox("Select Business", businesses)
        if selected_biz:
            biz_projects = [p for p in st.session_state.active_projects if p['business'] == selected_biz]
            for p in biz_projects:
                with st.container():
                    st.markdown(f'<div class="portal-card"><b>Project: {p["name"]}</b> ({p["status"]})</div>', unsafe_allow_html=True)
                    if p['status'] != 'Payment Completed':
                        f_up = st.file_uploader(f"Upload work for {p['name']}", key=f"up_{p['id']}")
                        if f_up and st.button("Submit Work", key=f"btn_{p['id']}"):
                            st.session_state.project_submissions.append({"project_id": p['id'], "filename": f_up.name, "timestamp": datetime.now().strftime("%H:%M")})
                            st.rerun()

    with tabs[1]:
        render_chat_hub('agency')

    with tabs[2]:
        st.subheader("New Opportunities & Direct Inquiries")
        # Direct inquiries are listed from proposals with "Awaiting Quote" status
        direct_inquiries = [p for p in st.session_state.proposals if p['status'] in ["Awaiting Quote", "Negotiating"]]
        if direct_inquiries:
            for idx, lead in enumerate(direct_inquiries):
                st.markdown(f"""
                <div class="portal-card" style="border-left: 5px solid #2ec4d1;">
                    <b>DIRECT REQUEST: {lead['project_name']}</b><br>
                    Client: {lead['business']} | Current Status: {lead['status']}<br>
                    Budget / Counter: ₹{lead['amount']:,}
                </div>
                """, unsafe_allow_html=True)
                with st.form(f"submit_prop_{lead['id']}"):
                    quote_val = st.number_input("Your Quote (₹)", value=lead['amount'], step=1000)
                    if st.form_submit_button("Submit / Update Proposal"):
                        for i, p in enumerate(st.session_state.proposals):
                            if p['id'] == lead['id']:
                                st.session_state.proposals[i]['amount'] = quote_val
                                st.session_state.proposals[i]['status'] = "Review Required"
                        st.success("Proposal sent to client!")
                        st.rerun()

    with tabs[3]:
        st.subheader("Financial Dashboard")
        total_earned = sum(sum(item['amount'] for item in p['paid_history']) for p in st.session_state.active_projects)
        total_vault = sum(p['total_quote'] - sum(item['amount'] for item in p['paid_history']) for p in st.session_state.active_projects)
        m1, m2 = st.columns(2)
        m1.metric("Total Agency Earnings", f"₹{total_earned:,}")
        m2.metric("Secure Vault (Locked)", f"₹{total_vault:,}")
        st.table(pd.DataFrame([{"Client": p['business'], "Project": p['name'], "Amount": f"₹{payment['amount']:,}", "Date": payment['date']} for p in st.session_state.active_projects for payment in p['paid_history']]))

st.markdown("---")
st.caption("AgencyKart Portal v3.5 | End-to-End Negotiation Infrastructure")
