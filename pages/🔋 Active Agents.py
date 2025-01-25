import streamlit as st

# Directory of all AI agents, including the newly added ones
directory = [
    {"name": "YouTube Like to TG", "status": "Inactive", "created": "10 September, 2022"},
    {"name": "Spotify Like to TG", "status": "Inactive", "created": "10 September, 2022"},
    {"name": "GitHub Activities to TG", "status": "Inactive", "created": "10 September, 2022"},
    {"name": "ListenNotes to TG", "status": "Inactive", "created": "11 September, 2022"},
    {"name": "GitHub Issues to TG", "status": "Inactive", "created": "10 September, 2022"},
    {"name": "Douban Activities to TG", "status": "Inactive", "created": "10 September, 2022"},
    {"name": "New Blog", "status": "Inactive", "created": "12 September, 2022"},
    {"name": "Error to TG", "status": "Inactive", "created": "10 September, 2022"},
    {"name": "Autonomous AI Crawler", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Automate LinkedIn Outreach with Notion and OpenAI", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Auto-label Incoming Gmail Messages with AI Nodes", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "AI Crew to Automate Fundamental Stock Analysis - Q&A Workflow", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Scrape and Summarize Posts of a News Site without RSS Feed using AI and Save to NocoDB", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Use an Open-Source LLM (via HuggingFace)", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Slack Chatbot Powered by AI", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Suggest Meeting Slots using AI", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Discord AI-Powered Bot", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Reddit AI Digest", "status": "Inactive", "created": "8 October, 2024"},
    {"name": "Share YouTube Videos with Ollama Summaries on Discord", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Share YouTube Videos with AI Summaries on Discord", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "AI Chat with Any Data Source (using the n8n Workflow Tool)", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Notion Knowledge Base AI Assistant", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Flux AI Image Generator", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Ask Questions About a PDF Using AI", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Basic AI Agent Chat", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Local RAG AI Agent", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Siri/Tobby AI Agent Apple Shortcut", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Enrich FAQ Sections on Your Website Pages at Scale with AI", "status": "Inactive", "created": "30 September, 2024"},
    {"name": "Notion Knowledge Base AI Assistant 2", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "AI Autonomous Agents", "status": "Inactive", "created": "29 September, 2024"},
    {"name": "Automate Your RFP Process with OpenAI Assistants", "status": "Inactive", "created": "29 September, 2024"},
]

# App title
st.title("Manage AI Agent Directory")

# Sidebar filter
view_option = st.sidebar.selectbox("Filter Agents by Status", ["All", "Active", "Inactive"])
filtered_directory = directory if view_option == "All" else [agent for agent in directory if agent["status"] == view_option]

# Display agents in the directory
st.subheader(f"Agent List: {view_option}")
for agent in filtered_directory:
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.write(f"**{agent['name']}**")
        st.caption(f"Created: {agent['created']}")
    with col2:
        # Toggle status button
        if st.button(f"Toggle Status ({agent['status']})", key=agent['name']):
            # Simulate toggle (this won't persist changes after a refresh)
            agent["status"] = "Active" if agent["status"] == "Inactive" else "Inactive"
            st.experimental_rerun()
    with col3:
        st.button("View Details", key=f"details-{agent['name']}")

# Add a new agent via sidebar
st.sidebar.subheader("Add New Agent")
new_agent_name = st.sidebar.text_input("New Agent Name")
if st.sidebar.button("Add Agent"):
    if new_agent_name.strip():
        directory.append({"name": new_agent_name.strip(), "status": "Inactive", "created": "15 December, 2024"})
        st.sidebar.success(f"Added new agent: {new_agent_name}")
        st.experimental_rerun()
    else:
        st.sidebar.error("Agent name cannot be empty!")
