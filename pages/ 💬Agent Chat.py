import streamlit as st
import streamlit.components.v1 as components
import uuid
import json
import os
from typing import List, Dict, Optional

class AgentChatManager:
    def __init__(self, config_file='agent_chats.json'):
        self.config_file = config_file
        self.load_chats()
        self.initialize_demo_chats()

    def initialize_demo_chats(self):
        """Initialize demo chats if no chats exist"""
        if not st.session_state.chats:
            # Demo Chatbot
            demo_chat_webhook = "https://agentonline-u29564.vm.elestio.app/webhook/0c9d895a-1ba3-449c-b3d4-b1a2baa39507/chat"
            self.add_chat(
                webhook_url=demo_chat_webhook,
                name="Demo AI Assistant",
                description="A versatile AI assistant ready to help with various tasks",
                theme_color="#3498db",
                agent_type="General",
                tags=["AI", "Chatbot", "Assistant"]
            )

            # Demo Form
            demo_form_webhook = "https://agentonline-u29564.vm.elestio.app/form/f5fd4fda-c366-40ed-af99-b0bae89ed022"
            self.add_chat(
                webhook_url=demo_form_webhook,
                name="Quick Feedback Form",
                description="Collect user feedback and insights efficiently",
                theme_color="#2ecc71",
                agent_type="Support",
                tags=["Form", "Feedback", "Survey"]
            )

    def load_chats(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                st.session_state.chats = json.load(f)
        else:
            st.session_state.chats = []

    def save_chats(self):
        with open(self.config_file, 'w') as f:
            json.dump(st.session_state.chats, f, indent=4)

    def add_chat(self, 
                 webhook_url: str, 
                 name: Optional[str] = None, 
                 description: Optional[str] = None, 
                 theme_color: str = "#ffffff",
                 agent_type: str = "General",
                 tags: List[str] = None):
        chat_id = str(uuid.uuid4())
        new_chat = {
            'id': chat_id,
            'webhook_url': webhook_url,
            'name': name or webhook_url.split('/')[-1],
            'description': description or "No description provided",
            'theme_color': theme_color,
            'agent_type': agent_type,
            'tags': tags or [],
            'created_at': str(uuid.uuid4())
        }
        st.session_state.chats.append(new_chat)
        self.save_chats()
        return chat_id

    def delete_chat(self, chat_id: str):
        st.session_state.chats = [
            chat for chat in st.session_state.chats if chat['id'] != chat_id
        ]
        self.save_chats()

    def render_advanced_chat_form(self):
        st.sidebar.header("🤖 Add New Agent Chat")
        with st.sidebar.form(key='advanced_chat_form'):
            webhook_url = st.text_input("Webhook URL *")
            name = st.text_input("Agent Name")
            description = st.text_area("Agent Description")
            
            col1, col2 = st.columns(2)
            with col1:
                agent_type = st.selectbox(
                    "Agent Type", 
                    ["General", "Technical", "Creative", "Support", "Sales", "Custom"]
                )
            with col2:
                theme_color = st.color_picker("Theme Color", value="#3498db")
            
            tags = st.multiselect(
                "Agent Tags", 
                ["AI", "Chatbot", "Assistant", "Customer Service", "Development", "Research"]
            )
            
            submit_button = st.form_submit_button("Add Agent Chat")

            if submit_button and webhook_url:
                try:
                    self.add_chat(
                        webhook_url, 
                        name=name, 
                        description=description, 
                        theme_color=theme_color,
                        agent_type=agent_type,
                        tags=tags
                    )
                    st.sidebar.success(f"Agent '{name or 'Unnamed'}' added successfully!")
                except Exception as e:
                    st.sidebar.error(f"Error adding agent: {e}")

    def render_agent_selector(self):
        st.sidebar.header("🔍 Agent Selector")
        
        filter_type = st.sidebar.selectbox(
            "Filter by Type", 
            ["All"] + list(set(chat['agent_type'] for chat in st.session_state.chats))
        )
        
        filtered_chats = [
            chat for chat in st.session_state.chats 
            if filter_type == "All" or chat['agent_type'] == filter_type
        ]
        
        for chat in filtered_chats:
            with st.sidebar.expander(f"{chat['name']} ({chat['agent_type']})"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Select: {chat['name']}", key=f"select_{chat['id']}"):
                        st.session_state.selected_chat = chat
                with col2:
                    if st.button("🗑️", key=f"delete_{chat['id']}"):
                        self.delete_chat(chat['id'])
                        st.experimental_rerun()
                
                st.write(f"**Description:** {chat['description']}")
                st.write(f"**Tags:** {', '.join(chat['tags'])}")

    def render_selected_chat(self):
        if not hasattr(st.session_state, 'selected_chat') or st.session_state.selected_chat is None:
            st.info("Select an agent chat from the sidebar to begin.")
            return

        chat = st.session_state.selected_chat
        
        st.markdown(f"""
        ## 🤖 {chat['name']} 
        **Type:** {chat['agent_type']} | **Tags:** {', '.join(chat['tags'])}
        """)
        
        st.markdown(f"*{chat['description']}*")
        
        chatbot_html = f"""
        <style>
            body {{ background-color: #f4f4f8; font-family: 'Arial', sans-serif; }}
            #n8n-chat {{ 
                background-color: {chat['theme_color']}; 
                border-radius: 15px; 
                padding: 20px; 
                box-shadow: 0 6px 12px rgba(0,0,0,0.1); 
            }}
        </style>
        <link href="https://cdn.jsdelivr.net/npm/@n8n/chat/dist/style.css" rel="stylesheet" />
        <script type="module">
            import {{ createChat }} from 'https://cdn.jsdelivr.net/npm/@n8n/chat/dist/chat.bundle.es.js';
            createChat({{
                webhookUrl: '{chat['webhook_url']}',
                mode: 'fullscreen',
                chatInputKey: 'chatInput',
                chatSessionKey: 'sessionId',
                initialMessages: [
                    'Hi there! 👋', 
                    'I am the {chat['name']}. How can I assist you today?'
                ],
                showWelcomeScreen: true,
            }});
        </script>
        <div id="n8n-chat" style="width: 100%; height: 700px;"></div>
        """
        
        components.html(chatbot_html, height=800)

def main():
    st.set_page_config(
        page_title="Multi-Agent Chat Platform", 
        page_icon="🤖", 
        layout="wide"
    )
    
    st.title("🌐 Multi-Agent Chat Platform")
    st.markdown("""
    Interact with multiple AI agents and forms seamlessly.
    """)
    
    chat_manager = AgentChatManager()
    
    chat_manager.render_advanced_chat_form()
    chat_manager.render_agent_selector()
    chat_manager.render_selected_chat()

if __name__ == "__main__":
    main()
