import streamlit as st
import st_pages  # required modules

# Set page config
st.set_page_config(page_title="TalkNexus - Ollama Chatbot Multi-Model Interface", layout="wide", page_icon="🤖")

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
        <h1 class="header-title">Ollama Chatbot Multi-Model Interface</h1> 
        <p class="header-subtitle">Advanced Language Models & Intelligent Conversations</p>
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
        "color": "var(--primary-color)"
    },
    "Language Models Management": {
        "icon": "gear",
        "func": st_pages.model_management,
        "description": "Download Models",
        "badge": "Configurations",
        "color": "var(--secondary-color)"
    },
    "AI Conversation": {
        "icon": "chat-dots",
        "func": st_pages.ai_chatbot,
        "description": "Interactive AI Chat",
        "badge": "Application",
        "color": "var(--highlight-color)"
    },
    "RAG Conversation": {
        "icon": "chat-dots",
        "func": st_pages.rag_chat,
        "description": "PDF AI Chat Assistant",
        "badge": "Application",
        "color": "var(--highlight-color)"
    },
    "🔍 Internet Agent": {
        "icon": "globe",
        "func": st_pages.internet_agent,
        "description": "Search AI Agents",
        "badge": "Search",
        "color": "var(--highlight-color)"
    },
    "🤝 AI Agent Roster": {
        "icon": "people",
        "func": st_pages.agent_roster,
        "description": "Agent Overview",
        "badge": "Roster",
        "color": "var(--primary-color)"
    },
    "🏢 Agent Headquarters": {
        "icon": "building",
        "func": st_pages.agent_headquarters,
        "description": "Manage Headquarters",
        "badge": "Management",
        "color": "var(--secondary-color)"
    },
    "⚙️ Agent Generator": {
        "icon": "magic",
        "func": st_pages.agent_generator,
        "description": "Generate New Agents",
        "badge": "Generator",
        "color": "var(--highlight-color)"
    },
    "🖋️ Forms": {
        "icon": "file-text",
        "func": st_pages.forms,
        "description": "Create and Manage Forms",
        "badge": "Forms",
        "color": "var(--primary-color)"
    },
    "🌀 Visual Agent Flow": {
        "icon": "flow-chart",
        "func": st_pages.visual_agent_flow,
        "description": "Flowcharts for Agents",
        "badge": "Visualization",
        "color": "var(--secondary-color)"
    },
    "📁 Agent Projects": {
        "icon": "folder",
        "func": st_pages.agent_projects,
        "description": "Organize Projects",
        "badge": "Projects",
        "color": "var(--highlight-color)"
    },
    "📊 Dashboard": {
        "icon": "bar-chart",
        "func": st_pages.dashboard,
        "description": "Performance Overview",
        "badge": "Dashboard",
        "color": "var(--primary-color)"
    }
}

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
""", unsafe_allow_html=True)

def navigate():
    with st.sidebar:
        st.markdown('''
        <a href="https://github.com/TsLu1s/talknexus" target="_blank" style="text-decoration: none; color: inherit; display: block;">
            <div class="header-container" style="cursor: pointer;">
                <div class="profile-section">
                    <div class="profile-info">
                        <h1 style="font-size: 32px;">TalkNexus</h1>
                        <span class="active-badge" style="font-size: 16px;">AI Chatbot Multi-Model Application</span>
                    </div>
                </div>
            </div>
        </a>
        ''', unsafe_allow_html=True)

        st.markdown('---')

        # Create menu items
        for page, info in PAGES.items():
            selected = st.session_state.current_page == page

            # Create the button (invisible but clickable)
            if st.button(
                f"{page}",
                key=f"nav_{page}",
                use_container_width=True,
                type="secondary" if selected else "primary"
            ):
                st.session_state.current_page = page
                st.rerun()

            # Visual menu item
            st.markdown(f"""
                <div class="menu-item {'selected' if selected else ''}">
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

        # Close navigation container
        st.markdown('</div>', unsafe_allow_html=True)
        
        return st.session_state.current_page

# Get selected page and run its function
try:
    selected_page = navigate()
    # Update session state
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

    # Run the selected function
    page_function = PAGES[selected_page]["func"]
    page_function()
except Exception as e:
    st.error(f"Error loading page: {str(e)}")
    st_pages.home.run()

# Display the footer
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <p>© 2024 Powered by <a href="https://github.com/TsLu1s" target="_blank">TsLu1s </a>. 
        Advanced Language Models & Intelligent Conversations
        | Project Source: <a href="https://github.com/TsLu1s/talknexus" target="_blank"> TalkNexus</p>
    </div>
</div>
""", unsafe_allow_html=True)
