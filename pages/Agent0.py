import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration
st.set_page_config(page_title="Agent001 Chat", layout="wide")

# Function to create the chat page with the permanent link
def create_chat_page():
    # Custom CSS for the chat theme
    custom_css = """
    <style>
        body {
            background-color: #000000;
            font-family: Arial, sans-serif;
        }
        #n8n-chat {
            background-color: #222222;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(255, 255, 255, 0.1);
            color: white;
        }
        .chat-header {
            font-size: 1.5em;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """
    
    # Chat widget HTML with the permanent webhook URL
    chatbot_html = f"""
    {custom_css}
    <link href="https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css" rel="stylesheet" />
    <script type="module">
        import {{ createChat }} from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';
        createChat({{
            webhookUrl: 'https://agentonline-u29564.vm.elestio.app/webhook/f406671e-c954-4691-b39a-66c90aa2f103/chat',
            mode: 'fullscreen',
            chatInputKey: 'chatInput',
            chatSessionKey: 'sessionId',
            initialMessages: ['Welcome to Agent001 Chat! How can I assist you today?'],
            showWelcomeScreen: true,
        }});
    </script>
    <div id="n8n-chat" style="width: 100%; height: 100%;"></div>
    """
    
    # Embed the chat widget in the Streamlit app
    components.html(chatbot_html, height=800)

# Display the chat page
st.title("Agent001 Chat")
st.markdown("Welcome to **Agent001 Chat**! Engage with the AI agent below:")
create_chat_page()
