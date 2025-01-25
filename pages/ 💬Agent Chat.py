import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration
st.set_page_config(page_title="AI AgentChat", layout="wide")

# Function to add chat pages dynamically with a custom theme
def add_chat_page(webhook_url, page_name, theme_color):
    # Custom CSS for chat theme
    custom_css = f"""
    <style>
        body {{
            background-color: #f0f0f5;
            font-family: Arial, sans-serif;
        }}
        #n8n-chat {{
            background-color: {theme_color};
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
        .chat-header {{
            font-size: 1.5em;
            color: #333;
        }}
    </style>
    """
    
    # Chat widget HTML
    chatbot_html = f"""
    {custom_css}
    <link href="https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css" rel="stylesheet" />
    <script type="module">
        import {{ createChat }} from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';
        createChat({{
            webhookUrl: '{webhook_url}',
            mode: 'fullscreen',
            chatInputKey: 'chatInput',
            chatSessionKey: 'sessionId',
            initialMessages: ['Hi there! 👋', `Hello from {page_name}! How can I assist you today?`],
            showWelcomeScreen: true,
        }});
    </script>
    <div id="n8n-chat" style="width: 100%; height: 100%;"></div>
    """
    
    components.html(chatbot_html, height=800)

# Sidebar for adding multiple webhook URLs and theme customization
st.sidebar.header("AI AgentChat Configuration")
webhook_urls = st.sidebar.text_area("Enter Webhook URLs (comma-separated):", "").split(',')
theme_color = st.sidebar.color_picker("Select Chat Theme Color:", "#ffffff")

# Validate webhook URLs and display chat pages
if webhook_urls and webhook_urls[0].strip():
    for url in webhook_urls:
        cleaned_url = url.strip()
        if cleaned_url:
            page_name = cleaned_url.split('/')[-1]  # Use the last part of the URL as a page name
            add_chat_page(cleaned_url, page_name, theme_color)
else:
    st.warning("Please enter valid Webhook URLs in the sidebar to start chatting.")
