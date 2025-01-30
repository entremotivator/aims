from pages.home import run as home
from st_pages.model_management import run as model_management
from st_pages.ai_chatbot import run as ai_chatbot
from st_pages.rag_chat import run as rag_chat
import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Define your pages
show_pages([
    Page("__init__.py", "Home", "🏠"),
    Page("pages/1_📊Dashboard.py", "Dashboard", "📊"),
    Page("pages/2_ 📁_Agent Projects.py", "Agent Projects", "📁"),
    Page("pages/2_🔍_Internet Agent.py", "Internet Agent", "🔍"),
    Page("pages/2_🧑‍💻_AI Agent Roster.py", "AI Agent Roster", "🧑‍💻"),
    Page("pages/3_ 🏢_Agent HeadQuaters.py", "Agent Headquarters", "🏢"),
    Page("pages/3_⚙️_Agent Generator.py", "Agent Generator", "⚙️"),
    Page("pages/3_💬_LLM Agents .py", "LLM Agents", "💬"),
    Page("pages/3_📚LLM Libary.py", "LLM Library", "📚"),
    Page("pages/3_🧠Agent Command.py", "Agent Command", "🧠"),
    Page("pages/3_🧠Agent Tool Libary.py", "Agent Tool Library", "🧠"),
    Page("pages/✍️ Forms .py", "Forms", "✍️"),
    Page("pages/🌀 Visual Agent Flow.py", "Visual Agent Flow", "🌀"),
    Page("pages/📑 Content Agents.py", "Content Agents", "📑"),
    Page("pages/🔋 Active Agents.py", "Active Agents", "🔋"),
    Page("pages/🤖 Format Agents.py", "Format Agents", "🤖")
])

# Add page title
add_page_title()

# Your main page content goes here
st.write("Welcome to the AI Agent Management System")
