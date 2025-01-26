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
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = requests.request(method, url, headers=self.HEADERS, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API Request Error: {e}")
            st.error(f"API Error: {e}")
            return None

    def get_workflows(self, active=None, search=None, limit=50):
        params = {"limit": limit}
        if active is not None:
            params["active"] = str(active).lower()
        if search:
            params["search"] = search
        return self.make_request("GET", "workflows", params=params)

    def get_workflow_details(self, workflow_id):
        return self.make_request("GET", f"workflows/{workflow_id}")

    def create_workflow(self, name, nodes=None, connections=None, active=True, tags=None):
        data = {
            "name": name,
            "active": active,
            "nodes": nodes or [],
            "connections": connections or {},
            "tags": tags or []
        }
        return self.make_request("POST", "workflows", data=data)

    def update_workflow(self, workflow_id, data):
        return self.make_request("PATCH", f"workflows/{workflow_id}", data=data)

    def delete_workflow(self, workflow_id):
        return self.make_request("DELETE", f"workflows/{workflow_id}")

    def get_executions(self, workflow_id=None, status=None, limit=50):
        params = {"limit": limit}
        if workflow_id:
            params["workflowId"] = workflow_id
        if status:
            params["status"] = status
        return self.make_request("GET", "executions", params=params)

    def get_tags(self):
        return self.make_request("GET", "tags")

    def get_users(self):
        return self.make_request("GET", "users")

    def toggle_workflow_status(self, workflow_id, active):
        data = {"active": active}
        return self.make_request("PATCH", f"workflows/{workflow_id}", data=data)

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
        "Tags Management", 
        "User Management"
    ])

    # Fetch all workflows for use across pages
    all_workflows = manager.get_workflows()
    workflow_names = [w['name'] for w in all_workflows['data']] if all_workflows and 'data' in all_workflows else []

    if page == "Workflows Overview":
        st.header("Workflow Management")
        
        if workflow_names:
            selected_workflow = st.selectbox("Select Workflow", workflow_names)
            selected_workflow_data = next((w for w in all_workflows['data'] if w['name'] == selected_workflow), None)
            
            if selected_workflow_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.json(selected_workflow_data)
                
                with col2:
                    st.subheader("Workflow Actions")
                    current_status = selected_workflow_data['active']
                    new_status = st.toggle("Active", value=current_status)
                    
                    if new_status != current_status:
                        if st.button("Apply Status Change"):
                            result = manager.toggle_workflow_status(selected_workflow_data['id'], new_status)
                            if result:
                                st.success(f"Workflow status updated to {'active' if new_status else 'inactive'}")
                            else:
                                st.error("Failed to update workflow status")
        else:
            st.warning("No workflows found")

    elif page == "Create Workflow":
        st.header("Create New Workflow")
        with st.form("workflow_creation"):
            name = st.text_input("Workflow Name")
            active = st.checkbox("Active", value=True)
            tags = st.multiselect("Select Tags", ["Automation", "Data Processing", "Integration"])
            submitted = st.form_submit_button("Create Workflow")
            
            if submitted:
                result = manager.create_workflow(name, active=active, tags=tags)
                if result:
                    st.success("Workflow created successfully!")
                    st.json(result)

    elif page == "Workflow Details":
        st.header("Workflow Inspection")
        selected_workflow = st.selectbox("Select Workflow", workflow_names)
        if selected_workflow:
            workflow_data = next((w for w in all_workflows['data'] if w['name'] == selected_workflow), None)
            if workflow_data:
                st.json(workflow_data)
            else:
                st.warning("Workflow details not found")

    elif page == "Executions":
        st.header("Workflow Executions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_workflow = st.selectbox("Select Workflow", ["All Workflows"] + workflow_names)
        
        with col2:
            status = st.selectbox("Execution Status", ["All", "success", "error", "waiting"])
        
        workflow_id = next((w['id'] for w in all_workflows['data'] if w['name'] == selected_workflow), None) if selected_workflow != "All Workflows" else None
        executions = manager.get_executions(
            workflow_id=workflow_id, 
            status=status if status != "All" else None
        )
        
        if executions and 'data' in executions:
            cols = st.columns([2, 2, 2, 1])
            cols[0].write("**Workflow Name**")
            cols[1].write("**Execution ID**")
            cols[2].write("**Execution Time**")
            cols[3].write("**Status**")
            
            for execution in executions['data']:
                cols = st.columns([2, 2, 2, 1])
                cols[0].write(execution.get('workflowName', 'N/A'))
                cols[1].write(str(execution.get('id', 'N/A')))
                cols[2].write(f"Start: {execution.get('startedAt', 'N/A')}\nStop: {execution.get('stoppedAt', 'N/A')}")
                cols[3].write(execution.get('status', 'N/A'))
        else:
            st.warning("No executions found")

    elif page == "Tags Management":
        st.header("Tags Overview")
        tags = manager.get_tags()
        if tags and 'data' in tags:
            for tag in tags['data']:
                st.write(f"**{tag['name']}**")
        else:
            st.warning("No tags found")

    elif page == "User Management":
        st.header("User Information")
        users = manager.get_users()
        if users and 'data' in users:
            for user in users['data']:
                st.write(f"**{user['email']}**")
        else:
            st.warning("No users found")

if __name__ == "__main__":
    main()
