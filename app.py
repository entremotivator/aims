import streamlit as st
from PIL import Image
import os

# Verify and load the image
image_path = os.path.join(
    "/Users/donmenicohudson/Downloads/AGENTSYSTEM", "agent.png"
)
assert os.path.exists(image_path), f"File not found: {image_path}"
image = Image.open(image_path)

# Page Configuration
st.set_page_config(
    page_title="AI Agent Management Systems",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Styles
def load_css():
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .header {
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .header img {
            max-width: 100px;
            border-radius: 50%;
        }
        .header h1 {
            margin-top: 10px;
            font-size: 2rem;
        }
        .card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: 0.3s ease;
        }
        .card:hover {
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        .card-title {
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        .card-content {
            font-size: 1rem;
            color: #555;
        }
        .sidebar .menu-item {
            margin-bottom: 1rem;
            padding: 0.75rem;
            font-size: 1rem;
            border-radius: 8px;
            background: #f8f9fa;
            transition: 0.3s;
        }
        .sidebar .menu-item:hover {
            background: #e9ecef;
        }
        </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# Sidebar Navigation
st.sidebar.image(image, width=150)
st.sidebar.title("AI Agent Management")
st.sidebar.markdown("---")

# Define Pages
PAGES = {
    "Logs Overview": "View logs and recent activities",
    "Agent Management": "Manage and configure AI agents",
    "System Status": "Monitor system health and usage",
}

for page, description in PAGES.items():
    if st.sidebar.button(page):
        st.write(f"### {page}")
        st.write(description)

# Main Header
st.markdown("""
    <div class="header">
        <img src="data:image/png;base64,{}" alt="Agent Logo">
        <h1>AI Agent Management Systems</h1>
    </div>
""".format(base64.b64encode(image.tobytes()).decode("utf-8")), unsafe_allow_html=True)

# Log Overview Section
st.write("## Logs Overview")
log_entries = [
    {"time": "2025-01-19 14:23:12", "entry": "Agent Alpha completed Task 132."},
    {"time": "2025-01-19 14:25:10", "entry": "System health check passed."},
    {"time": "2025-01-19 14:30:02", "entry": "New agent Omega added to roster."},
]

for log in log_entries:
    st.markdown(f"""
        <div class="card">
            <div class="card-title">Timestamp: {log['time']}</div>
            <div class="card-content">{log['entry']}</div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        © 2025 AI Agent Management Systems. All rights reserved.
    </div>
""", unsafe_allow_html=True)
