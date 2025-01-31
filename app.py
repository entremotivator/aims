import streamlit as st
import st_pages
from src import st_pages

# Set page config
st.set_page_config(page_title="AI Agent MS - Multi Agent Operations Interface", layout="wide", page_icon="🤖")

# Load custom CSS from file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('styles.css')

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Header
st.markdown(f"""
<div class="header">
    <div class="animated-bg"></div>
    <div class="header-content">
        <h1 class="header-title">AI Agent Management System</h1> 
        <p class="header-subtitle">Advanced Multi Agent Operations Interface & Intelligent systems</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced pages definition
PAGES = {
    "Home": {
        "icon": "house-door",
        "func": st_pages.home,
        "description": "Guidelines & Overview",
        "badge": "Informative",
        "color": "var(--primary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/"
    },
    "Agent Chat": {
        "icon": "chat-dots",
        "func": "pages.💭Agent Chat",
        "description": "Chat with AI Agents",
        "badge": "Application",
        "color": "var(--highlight-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Agent_Chat"
    },
    "Dashboard": {
        "icon": "bar-chart",
        "func": "pages.1_📊Dashboard",
        "description": "Interactive Data Overview",
        "badge": "Analytics",
        "color": "var(--secondary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Dashboard"
    },
    "Agent Projects": {
        "icon": "folder",
        "func": "pages.2_ 📁_Agent Projects",
        "description": "Manage Agent Projects",
        "badge": "Management",
        "color": "var(--primary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Agent_Projects"
    },
    "Internet Agent": {
        "icon": "search",
        "func": "pages.2_🔍_Internet Agent",
        "description": "Web-Savvy AI Agents",
        "badge": "Exploration",
        "color": "var(--highlight-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Internet_Agent"
    },
    "AI Agent Roster": {
        "icon": "person-workspace",
        "func": "pages.2_🧑‍💻_AI Agent Roster",
        "description": "AI Agent Directory",
        "badge": "Information",
        "color": "var(--secondary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/AI_Agent_Roster"
    },
    "Agent Headquarters": {
        "icon": "building",
        "func": "pages.3_ 🏢_Agent HeadQuaters",
        "description": "AI Base of Operations",
        "badge": "HQ",
        "color": "var(--primary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Agent_Headquarters"
    },
    "Agent Generator": {
        "icon": "gear",
        "func": "pages.3_⚙️_Agent Generator",
        "description": "Create Custom Agents",
        "badge": "Tool",
        "color": "var(--highlight-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Agent_Generator"
    },
    "LLM Agents": {
        "icon": "robot",
        "func": "pages.3_🛋_LLM Agents",
        "description": "Large Language Models",
        "badge": "Application",
        "color": "var(--secondary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/LLM_Agents"
    },
    "LLM Library": {
        "icon": "book",
        "func": "pages.3_📚LLM Libary",
        "description": "Central Model Repository",
        "badge": "Library",
        "color": "var(--primary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/LLM_Library"
    },
    "Agent Command": {
        "icon": "command",
        "func": "pages.3_🧠Agent Command",
        "description": "Control AI Agents",
        "badge": "Command",
        "color": "var(--highlight-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Agent_Command"
    },
    "Agent Tool Library": {
        "icon": "tool",
        "func": "pages.3_🧠Agent Tool Libary",
        "description": "Comprehensive Toolset",
        "badge": "Tools",
        "color": "var(--secondary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Agent_Tool_Library"
    },
    "Forms": {
        "icon": "pencil",
        "func": "pages.✍️ Forms",
        "description": "Manage Data Collection",
        "badge": "Forms",
        "color": "var(--primary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Forms"
    },
    "Visual Agent Flow": {
        "icon": "circle-fill",
        "func": "pages.🔀 Visual Agent Flow",
        "description": "Visualize AI Workflows",
        "badge": "Visualization",
        "color": "var(--highlight-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Visual_Agent_Flow"
    },
    "Content Agents": {
        "icon": "file-earmark-text",
        "func": "pages.📁 Content Agents",
        "description": "AI Content Generation",
        "badge": "Content",
        "color": "var(--secondary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Content_Agents"
    },
    "Active Agents": {
        "icon": "battery-charging",
        "func": "pages.🔋 Active Agents",
        "description": "Monitor Agent Activity",
        "badge": "Activity",
        "color": "var(--primary-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Active_Agents"
    },
    "Format Agents": {
        "icon": "file-code",
        "func": "pages.🤖 Format Agents",
        "description": "Formatting Assistance",
        "badge": "Tools",
        "color": "var(--highlight-color)",
        "url": "https://zrnrpwtg4wkiz7hgcbsl3a.streamlit.app/Format_Agents"
    }
}

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
""", unsafe_allow_html=True)

def navigate():
    with st.sidebar:
        st.markdown('''
        <a href="https://entremotivator.com" target="_blank" style="text-decoration: none; color: inherit; display: block;">
            <div class="header-container" style="cursor: pointer;">
                <div class="profile-section">
                    <div class="profile-info">
                        <h1 style="font-size: 32px;">AI AGENT MS</h1>
                        <span class="active-badge" style="font-size: 16px;">AI  Multi-Model Agent Manager </span>
                    </div>
                </div>
            </div>
        </a>
        ''', unsafe_allow_html=True)

        st.markdown('---')

        # Create menu items at the top of the sidebar
        for page, info in PAGES.items():
            if st.button(
                f"{page}",
                key=f"nav_{page}",
                use_container_width=True,
                type="secondary" if st.session_state.current_page == page else "primary"
            ):
                st.session_state.current_page = page
                st.experimental_set_query_params(page=page)
                st.experimental_rerun()

            st.markdown(f"""
                <div class="menu-item {'selected' if st.session_state.current_page == page else ''}">
                    <div class="menu-icon">
                        <i class="bi bi-{info['icon']}"></i>
                    </div>
                    <div class="menu-content">
                        <div class="menu-title">{page}</div>
                        <div class="menu-description">{info['description']}</div>
                    </div>
                    <div class="menu-badge">{info['badge']}</div>
                </div>
            """, unsafe_allow_html=True)

    return st.session_state.current_page

# Get selected page and run its function
try:
    selected_page = navigate()
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.experimental_rerun()

    # Redirect to the selected page
    st.markdown(f'<meta http-equiv="refresh" content="0;url={PAGES[selected_page]["url"]}">', unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st.pages.home.run()

# Display the footer
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <p>© 2025 Powered by <a href="https://Entremotivator.com" target="_blank">EntreMotivator</a>. 
        Advanced Multi Agent Operations Interface
        | Project Source: <a href="https://Entremotivator.com" target="_blank"> EntreMotivator</a></p>
    </div>
</div>
""", unsafe_allow_html=True)
