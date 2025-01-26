import streamlit as st
import requests
import json
import logging
from datetime import datetime

# Configuration and Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

class N8NWorkflowManager:
    def __init__(self):
        # Configuration
        self.BASE_URL = "http://agentonline-u29564.vm.elestio.app/api/v1"
        self.API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NDI5NWRjYS01YTIxLTQzZDMtYTA1OS1jOTA5YTQ5ZjlkYTEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM3ODkxNTI0fQ.-JwLzCmtMVUcQ8NJTny6czBp963T8yJFtg_-S3RPxXo"
        self.HEADERS = {
            "accept": "application/json", 
            "X-N8N-API-KEY": self.API_KEY
        }

    def make_request(self, method, endpoint, data=None, params=None):
        """Generic API request method with error handling."""
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = requests.request(
                method, 
                url, 
                headers=self.HEADERS, 
                json=data, 
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API Request Error: {e}")
            st.error(f"API Error: {e}")
            return None

    def get_users(self):
        """Fetch detailed user information."""
        return self.make_request("GET", "users")

    def update_user_status(self, user_id, active):
        """Update user activation status."""
        data = {"active": active}
        return self.make_request("PATCH", f"users/{user_id}", data=data)

    def get_executions(self, workflow_id=None, status=None, limit=50):
        """Fetch workflow executions with optional filtering."""
        params = {"limit": limit}
        if workflow_id:
            params["workflowId"] = workflow_id
        if status:
            params["status"] = status
        return self.make_request("GET", "executions", params=params)

def main():
    st.set_page_config(page_title="n8n Workflow Manager", layout="wide")
    manager = N8NWorkflowManager()

    st.title("🔧 n8n Workflow Management Dashboard")
    
    # Sidebar Navigation
    page = st.sidebar.radio("Navigation", [
        "Workflows Overview", 
        "Create Workflow", 
        "Workflow Details", 
        "Executions", 
        "User Management"
    ])

    if page == "User Management":
        st.header("User Management")
        users = manager.get_users()
        
        if users and 'data' in users:
            st.subheader("Agent List")
            
            # Create columns for display
            cols = st.columns([2, 2, 1, 1])
            cols[0].write("**Agent Name**")
            cols[1].write("**Agent ID**")
            cols[2].write("**Status**")
            cols[3].write("**Actions**")
            
            for user in users['data']:
                # Create columns for each user
                cols = st.columns([2, 2, 1, 1])
                
                # Display user name
                cols[0].write(user.get('name', 'N/A'))
                
                # Display user ID
                cols[1].write(str(user.get('id', 'N/A')))
                
                # Display current status
                status = "Active" if user.get('active', False) else "Inactive"
                cols[2].write(status)
                
                # Toggle activation button
                toggle_key = f"toggle_{user.get('id')}"
                if cols[3].button(f"{'Deactivate' if user.get('active', False) else 'Activate'}", key=toggle_key):
                    new_status = not user.get('active', False)
                    result = manager.update_user_status(user.get('id'), new_status)
                    if result:
                        st.success(f"User {user.get('name')} {'activated' if new_status else 'deactivated'}")
                    else:
                        st.error("Failed to update user status")
        else:
            st.warning("No users found")

    elif page == "Executions":
        st.header("Workflow Executions")
        
        # Filtering options
        col1, col2 = st.columns(2)
        
        with col1:
            workflow_id = st.text_input("Filter by Workflow ID (Optional)")
        
        with col2:
            status = st.selectbox("Execution Status", ["", "success", "error", "waiting"])
        
        # Fetch executions
        executions = manager.get_executions(
            workflow_id=workflow_id or None, 
            status=status or None
        )
        
        if executions and 'data' in executions:
            # Create columns for display
            cols = st.columns([2, 2, 2, 1])
            cols[0].write("**Workflow Name**")
            cols[1].write("**Execution ID**")
            cols[2].write("**Execution Time**")
            cols[3].write("**Status**")
            
            for execution in executions['data']:
                # Create columns for each execution
                cols = st.columns([2, 2, 2, 1])
                
                # Workflow name (if available)
                workflow_name = execution.get('workflowName', 'N/A')
                cols[0].write(workflow_name)
                
                # Execution ID
                cols[1].write(str(execution.get('id', 'N/A')))
                
                # Execution time details
                start_time = execution.get('startedAt', 'N/A')
                stop_time = execution.get('stoppedAt', 'N/A')
                cols[2].write(f"Start: {start_time}\nStop: {stop_time}")
                
                # Execution status
                cols[3].write(execution.get('status', 'N/A'))
        else:
            st.warning("No executions found")

    # Previous pages remain the same...

if __name__ == "__main__":
    main()
