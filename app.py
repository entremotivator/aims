import toml
import streamlit as st

# Load config file
config = toml.load("config.toml")

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

# Display the menu dynamically
st.sidebar.title("Navigation")

for item in config["menu"]["items"]:
    if st.sidebar.button(f" {item['icon']} {item['name']}", key=item['name']):
        st.markdown(f"[{item['name']}]({item['url']})")
