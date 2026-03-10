import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIG ---
# Setting initial_sidebar_state to "expanded" but allowing the native toggle
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
        border-radius: 999px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .status-active { background-color: rgba(46, 196, 209, 0.2); color: #2ec4d1; border: 1px solid #2ec4d1; }
    .status-pending { background-color: rgba(251, 146, 60, 0.2); color: #fb923c; border: 1px solid #fb923c; }
    .status-done { background-color: rgba(52, 211, 153, 0.2); color: #34d399; border: 1px solid #34d399; }
    
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
    
    /* Secondary/Delete Buttons */
    .stButton.delete-btn>button {
        background-color: transparent;
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    .stButton.delete-btn>button:hover {
        background-color: #ef4444;
        color: white;
    }
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-user { background: #2ec4d1; color: #0b1a32; align-self: flex-end; margin-left: auto; font-weight: 500; }
    .chat-agency { background: #243b61; color: #
