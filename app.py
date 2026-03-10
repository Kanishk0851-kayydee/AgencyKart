import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AgencyKart | Scale Smarter", page_icon="🚀", layout="wide")

# --- CUSTOM CSS ---
# Fixed the parameter from 'unsafe_base64' to 'unsafe_allow_html' to resolve deployment crashes
st.markdown("""
    <style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { background-color: #2dd4bf; color: #020617; border-radius: 8px; font-weight: bold; border: none; width: 100%; }
    .stButton>button:hover { background-color: #14b8a6; color: white; }
    .metric-card { background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #2dd4bf; }
    .agency-card { background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 15px; border: 1px solid #334155; margin-bottom: 10px; }
    .priority-badge { background-color: #2dd4bf; color: #020617; padding: 2px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'briefs' not in st.session_state:
    st.session_state.briefs = []
if 'escrow_status' not in st.session_state:
    st.session_state.escrow_status = "Pending"

# --- MOCK DATA ---
MOCK_AGENCIES = [
    {"name": "PixelPerfect Digital", "score": 4.9, "niche": "Web Dev", "priority": True, "price": "₹₹₹"},
    {"name": "GrowthHackers India", "score": 4.7, "niche": "Marketing", "priority": True, "price": "₹₹"},
    {"name": "Boutique Creative Co.", "score": 4.8, "niche": "Branding", "priority": False, "price": "₹₹₹"},
    {"name": "TechFlow Systems", "score": 4.5, "niche": "App Dev", "priority": False, "price": "₹"},
]

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 AgencyKart")
page = st.sidebar.radio("Navigate", ["Home", "For Businesses (AI Brief)", "For Agencies (Leads)", "Project Dashboard (Escrow)"])

# --- HOME PAGE ---
if page == "Home":
    st.title("Scale Smarter with AgencyKart")
    st.subheader("The AI-integrated aggregator for Indian SMEs and Enterprises.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'><h3>63M+</h3><p>MSMEs in India</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h3>₹1.2L</h3><p>Avg. Loss per Bad Hire</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h3>100%</h3><p>Escrow Security</p></div>", unsafe_allow_html=True)

    st.write("---")
    st.write("### Why AgencyKart?")
    st.write("✅ **AI Brief Generator:** Turn your ideas into technical specs instantly.")
    st.write("✅ **Smart Matching:** Connect with vetted agencies in minutes.")
    st.write("✅ **Secure Escrow:** Your money stays safe until the work is delivered.")

# --- BUSINESS SIDE: AI BRIEF GENERATOR ---
elif page == "For Businesses (AI Brief)":
    st.title("📝 AI Brief Generator")
    st.write("Tell us what you need, and our AI will create a professional Technical Brief for you.")
    
    with st.form("brief_form"):
        project_name = st.text_input("Project Name", placeholder="e.g., E-commerce App for Bakery")
        raw_idea = st.text_area("What are you looking to build?", placeholder="Describe your idea in simple words...")
        budget = st.select_slider("Budget Range", options=["₹50k - ₹1L", "₹1L - ₹5L", "₹5L - ₹20L", "₹20L+"])
        submitted = st.form_submit_button("Generate AI Brief & Match Agencies")

    if submitted:
        with st.spinner("AI is analyzing requirements and generating Technical SOW..."):
            time.sleep(2)
            st.success("Brief Generated Successfully!")
            
            # Simulated AI output
            generated_brief = {
                "id": len(st.session_state.briefs) + 1,
                "name": project_name,
                "tech_specs": f"Project Scope: {raw_idea}\nKey Requirements: Responsive UI, Payment Integration, User Auth.\nTarget Budget: {budget}\nDeliverables: High-fidelity Prototype, Source Code, Documentation.",
                "status": "Matching"
            }
            st.session_state.briefs.append(generated_brief)
            
            st.markdown(f"### 📄 Technical Brief: {project_name}")
            st.code(generated_brief["tech_specs"], language="markdown")
            
            st.write("---")
            st.subheader("🎯 Top Recommended Agencies")
            for agency in MOCK_AGENCIES:
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        priority_tag = "<span class='priority-badge'>FEATURED</span>" if agency['priority'] else ""
                        st.markdown(f"**{agency['name']}** {priority_tag}", unsafe_allow_html=True)
                        st.caption(f"Rating: ⭐ {agency['score']} | Niche: {agency['niche']} | Cost: {agency['price']}")
                    with col_b:
                        if st.button(f"Hire {agency['name']}", key=agency['name']):
                            st.session_state.escrow_status = "Locked in Escrow"
                            st.info(f"Connected with {agency['name']}! Payment moved to Escrow.")

# --- AGENCY SIDE: LEADS ---
elif page == "For Agencies (Leads)":
    st.title("💼 Agency Lead Center")
    st.write("High-intent leads pre-qualified by AgencyKart AI.")
    
    if not st.session_state.briefs:
        st.info("No active leads currently. Ensure businesses have generated briefs!")
    else:
        for b in st.session_state.briefs:
            with st.expander(f"Lead #{b['id']}: {b['name']}"):
                st.write("**Technical Requirements:**")
                st.text(b['tech_specs'])
                st.button("Submit Proposal", key=f"prop_{b['id']}")

    st.write("---")
    st.subheader("📈 Boost Your Agency Visibility")
    st.info("Agencies using **Priority Placement** receive 3.4x more leads.")
    if st.button("Enable Priority Placement"):
        st.success("Your agency is now a 'Featured Partner'!")

# --- PROJECT DASHBOARD: ESCROW ---
elif page == "Project Dashboard (Escrow)":
    st.title("📊 Project Dashboard")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Payment Status", st.session_state.escrow_status)
    with col2:
        st.metric("Project Progress", "45%" if "Escrow" in st.session_state.escrow_status else "0%")
    
    st.write("---")
    st.subheader("Milestone Tracking")
    m1, m2 = st.columns(2)
    with m1:
        st.write("**Milestone 1:** UI/UX Design")
        st.write("Status: ✅ Completed")
    with m2:
        st.write("**Milestone 2:** Backend Integration")
        st.write("Status: ⏳ In Progress")

    if "Locked" in st.session_state.escrow_status:
        if st.button("Approve Milestone 1 & Release Funds"):
            st.session_state.escrow_status = "Funds Released (M1)"
            st.balloons()
            st.success("Payment released to the agency.")
