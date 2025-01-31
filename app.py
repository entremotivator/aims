import streamlit as st

# Load config from secrets
config = st.secrets["config"]

# Set page config
st.set_page_config(
    page_title=config['general']['title'],
    layout="wide",
    page_icon="🤖"
)

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
        st.experimental_set_query_params(page=item['name'])

# Render selected page
st.markdown(f"### {st.session_state.current_page}")

# Fetch the URL for the selected page and display it as a link
selected_item = next(item for item in config["menu"]["items"] if item["name"] == st.session_state.current_page)
st.markdown(f"[Go to {selected_item['name']}]({selected_item['url']})")

