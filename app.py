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

# --- SESSION STATE INITIALIZATION ---
if 'active_projects' not in st.session_state:
    st.session_state.active_projects = [
        {"id": "AK-992", "business": "PVR Cinemas", "name": "Mobile App UI", "agency": "PixelPerfect", "status": "In Progress", "progress": 65, "vault": 45000, "milestone": "UI Design"},
        {"id": "AK-401", "business": "Zomato", "name": "Chatbot API", "agency": "PixelPerfect", "status": "Pending Brief", "progress": 10, "vault": 12000, "milestone": "Setup"}
    ]

if 'brief_generated' not in st.session_state:
    st.session_state.brief_generated = False

if 'generated_brief_data' not in st.session_state:
    st.session_state.generated_brief_data = {}

if 'project_submissions' not in st.session_state:
    st.session_state.project_submissions = []

if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "agency", "text": "Hi! We've started on the UI moodboards. Any specific preferences?"}]

# --- MOCK AGENCY DATA FOR MATCHMAKING ---
MATCH_AGENCIES = [
    {"name": "PixelPerfect Digital", "specialization": "UI/UX & Branding", "match": "98%", "bio": "Top-tier design studio focused on conversion-driven aesthetics."},
    {"name": "CodeCrafters India", "specialization": "Full-Stack Web Dev", "match": "92%", "bio": "Experts in scalable MERN stack applications for SMEs."}
]

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
    if st.button("Reset All Portal Data"):
        st.session_state.clear()
        st.rerun()
    st.caption(f"Active View: {user_role}")

# --- BUSINESS DASHBOARD ---
if "Business" in user_role:
    st.title("🏢 Business Project Portal")
    st.markdown("Manage your agency partners, track work, and release vault payments.")
    
    tabs = st.tabs(["📊 My Active Projects", "📩 Agency Chat", "📑 Hire & Brief Agencies"])
    
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
                    st.write("📂 **New Deliverables for Review:**")
                    for sub in subs:
                        col_s1, col_s2 = st.columns([3, 1])
                        col_s1.info(f"📄 {sub['filename']} (Sent: {sub['timestamp']})")
                        if col_s2.button("Approve & Release Vault Payment", key=f"app_{sub['filename']}"):
                            st.session_state.active_projects[i]['status'] = "Complete"
                            st.session_state.active_projects[i]['progress'] = 100
                            st.balloons()
                            st.rerun()
                
                col_p1, col_p2 = st.columns([3, 1])
                col_p1.progress(p['progress'] / 100)
                col_p2.write(f"Secure Vault: ₹{p['vault']:,}")

    with tabs[1]:
        st.subheader("Direct Communication Hub")
        st.caption("Ask your agency for a status update or share feedback.")
        
        chat_col, action_col = st.columns([3, 1])
        
        with chat_col:
            for msg in st.session_state.messages:
                div_class = "chat-agency" if msg['role'] == "agency" else "chat-user"
                st.markdown(f'<div class="chat-bubble {div_class}">{msg["text"]}</div>', unsafe_allow_html=True)
            
            with st.form("chat_bus", clear_on_submit=True):
                user_input = st.text_input("Message the agency...")
                if st.form_submit_button("Send"):
                    st.session_state.messages.append({"role": "user", "text": user_input})
                    st.rerun()
        
        with action_col:
            st.markdown("### Quick Nudges")
            if st.button("Request Status Update"):
                st.session_state.messages.append({"role": "user", "text": "Hi, could you please provide a quick status update on the current milestone?"})
                st.toast("Status request sent!")
                st.rerun()

    with tabs[2]:
        st.subheader("AI Briefing & Discovery")
        st.write("Input your project goals to generate a technical brief and find the best agency match.")
        
        with st.form("ai_brief"):
            h = st.text_input("Project Name", placeholder="e.g. E-commerce App")
            d = st.text_area("What are you looking to build?", placeholder="Describe features, goals, and style...")
            # Re-added the Budget Selection Slider
            budget = st.select_slider(
                "Select Budget Range", 
                options=["₹50k - ₹1L", "₹1L - ₹5L", "₹5L - ₹20L", "₹20L+"]
            )
            
            if st.form_submit_button("Generate AI Brief & Match Agencies"):
                with st.spinner("AI analyzing requirements and vetting agencies..."):
                    time.sleep(1.5)
                    st.session_state.brief_generated = True
                    st.session_state.generated_brief_data = {
                        "name": h,
                        "desc": d,
                        "budget": budget
                    }
        
        if st.session_state.brief_generated:
            st.success("✅ Technical Brief Generated! Your project is now being matched with top Indian agencies.")
            
            # Show a summary of the generated brief
            st.markdown(f"""
            <div class="portal-card" style="border-left: 5px solid #2ec4d1;">
                <h4 style="color: #2ec4d1;">Brief Summary: {st.session_state.generated_brief_data['name']}</h4>
                <p><b>Requirements:</b> {st.session_state.generated_brief_data['desc']}</p>
                <p><b>Target Budget:</b> {st.session_state.generated_brief_data['budget']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 Recommended Top Agency Matches")
            for agency in MATCH_AGENCIES:
                with st.container():
                    st.markdown(f"""
                    <div class="portal-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <h4 style="color: #2ec4d1; margin:0;">{agency['name']}</h4>
                                <p style="font-size: 14px; color: #94a3b8; margin:5px 0;">Specialization: <b>{agency['specialization']}</b></p>
                            </div>
                            <div class="match-score">{agency['match']}</div>
                        </div>
                        <p style="font-size: 14px;">{agency['bio']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Request Proposal from {agency['name']}", key=f"req_{agency['name']}"):
                        st.info(f"Proposal request sent to {agency['name']}. They will contact you shortly.")

# --- AGENCY PORTAL ---
else:
    st.title("🚀 Agency Operations Hub")
    st.markdown("Manage client projects, submit work for review, and discover new business.")
    
    tabs = st.tabs(["💼 Manage Clients", "🔍 New Market Leads", "💰 Payment Vaults"])
    
    with tabs[0]:
        st.subheader("Your Active Clients")
        businesses = list(set([p['business'] for p in st.session_state.active_projects]))
        
        selected_biz = st.selectbox("Select Business Name to View Projects", businesses)
        
        if selected_biz:
            st.write(f"### Projects for **{selected_biz}**")
            biz_projects = [p for p in st.session_state.active_projects if p['business'] == selected_biz]
            
            for p in biz_projects:
                with st.container():
                    st.markdown(f"""
                    <div class="portal-card">
                        <div style="display: flex; justify-content: space-between;">
                            <b>Project: {p['name']}</b>
                            <span class="status-pill status-active">Active Milestone: {p['milestone']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_u1, col_u2 = st.columns([3, 1])
                    with col_u1:
                        f_up = st.file_uploader(f"Upload work for {p['name']}", key=f"up_{p['id']}")
                        if f_up and st.button("Submit Work to Client", key=f"btn_{p['id']}"):
                            st.session_state.project_submissions.append({
                                "project_id": p['id'], 
                                "filename": f_up.name, 
                                "timestamp": datetime.now().strftime("%H:%M")
                            })
                            st.success("Work submitted! Client notified.")
                            st.rerun()
                    
                    with col_u2:
                        st.write("### Manage Submissions")
                        # Show and delete submissions
                        p_subs = [s for s in st.session_state.project_submissions if s['project_id'] == p['id']]
                        for s in p_subs:
                            st.caption(f"📄 {s['filename']}")
                            if st.button("Delete / Retract", key=f"del_{s['filename']}_{p['id']}"):
                                st.session_state.project_submissions.remove(s)
                                st.warning("Work retracted.")
                                st.rerun()

    with tabs[1]:
        st.subheader("Qualified Market Opportunities")
        st.markdown("""
        <div class="portal-card">
            <h4 style="color: #2ec4d1;">Fintech Dashboard Design</h4>
            <p>SME looking for a secure dashboard with data visualization. Budget: ₹1.5L - ₹3L.</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Submit Proposal for Lead")

    with tabs[2]:
        st.subheader("Secure Pay Vaults (Protected Payments)")
        st.metric("Total Funds Protected", f"₹{sum(p['vault'] for p in st.session_state.active_projects if p['status'] != 'Complete'):,}")
        
        # Payment Table
        pay_data = []
        for p in st.session_state.active_projects:
            pay_data.append({
                "Business": p['business'],
                "Project": p['name'],
                "Vault Amount": f"₹{p['vault']:,}",
                "Status": "Released" if p['status'] == "Complete" else "Protected"
            })
        st.table(pd.DataFrame(pay_data))

st.markdown("---")
st.caption("AgencyKart Portal v2.9 | Built for Secure B2B Partnerships")
