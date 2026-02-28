import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="AgencyKart | Scale Smarter", layout="wide")

# --------- CUSTOM CSS ---------
st.markdown("""
<style>
html, body, [class*="css"]  {
    scroll-behavior: smooth;
    font-family: 'Arial', sans-serif;
}

.section {
    margin-top: 120px;
    text-align: center;
    animation: fadeUp 1.2s ease-in-out;
}

.big-text {
    font-size: 80px;
    font-weight: bold;
    margin-top: 200px;
    text-align: center;
    animation: fadeIn 2s ease-in-out;
}

.sub-text {
    font-size: 28px;
    opacity: 0.8;
}

.team-text {
    font-size: 22px;
    line-height: 1.8;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes fadeUp {
    from {opacity: 0; transform: translateY(50px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# --------- SECTION 1: HI ---------
st.markdown('<div class="big-text">Hi 👋</div>', unsafe_allow_html=True)

st.markdown('<div class="section sub-text">We are building the future of agency procurement in India.</div>', unsafe_allow_html=True)

# --------- SECTION 2: PROBLEM ---------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("The Problem")

st.write("""
Startups and SMEs struggle to find the right marketing, tech, or creative agency.

The process is:
• Unstructured  
• Time-consuming  
• Based on guesswork  

Businesses waste money.
Agencies pitch blindly.
""")

st.markdown('</div>', unsafe_allow_html=True)

# --------- SECTION 3: SOLUTION ---------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("Introducing AgencyKart")

st.subheader("An AI-powered B2B Marketplace")

st.write("""
AgencyKart intelligently matches businesses with the right agencies based on:

• Budget  
• Industry  
• Goals  
• Expertise  

We don’t just connect — we match intelligently.
""")

st.markdown('</div>', unsafe_allow_html=True)

# --------- SECTION 4: HOW IT WORKS ---------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("How It Works")

st.write("""
1️⃣ Business submits AI-powered brief  
2️⃣ Smart algorithm matches relevant agencies  
3️⃣ Agencies submit structured proposals  
4️⃣ Secure milestone-based payments  

Result: Faster decisions. Better partnerships.
""")

st.markdown('</div>', unsafe_allow_html=True)

# --------- SECTION 5: LOGO ---------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("Our Brand")

try:
    logo = Image.open("assets/agencykart_logo.jpeg")
    st.image(logo, width=450)
except:
    st.warning("Logo not found. Make sure it is inside the assets folder.")

st.markdown("<h2>Scale Smarter</h2>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------- SECTION 6: TEAM ---------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("Our Team")

st.markdown("""
<div class="team-text">
Kanishk <br>
Srivatsa <br>
Nikita <br>
Darshan <br>
Abhay <br>
Aditya Goel
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------- FINAL SECTION ---------
st.markdown('<div class="big-text">AgencyKart</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Scale Smarter</div>', unsafe_allow_html=True)
