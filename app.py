import streamlit as st
import toml

# Load config file
config = toml.load("config.toml")

# Set page config
st.set_page_config(
    page_title=config['general']['title'],
    layout="wide",
    page_icon="🤖"")

# Load custom CSS from file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('styles.css')

# Display the header
st.markdown(f"""
<div class="header">
    <div class="animated-bg"></div>
    <div class="header-content">
        <h1 class="header-title">{config['general']['title']}</h1> 
        <p class="header-subtitle">{config['general']['subtitle']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Sidebar navigation
st.sidebar.title("Navigation")

for item in config["menu"]["items"]:
    if st.sidebar.button(f" {item['icon']} {item['name']}", key=item['name']):
        st.session_state.current_page = item['name']

# Render selected page
st.markdown(f"### {st.session_state.current_page}")
