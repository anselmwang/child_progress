import streamlit as st

# Page configuration - this will be the main entry point
st.set_page_config(
    page_title="儿童学习进度追踪",
    page_icon="📚",
    layout="wide"
)

# Automatic redirect to input_progress page
st.switch_page("pages/1_input_progress.py")
