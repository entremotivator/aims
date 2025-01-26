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

    if page == "Workflows Overview":
        st.header("Workflow Management")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Active Workflows")
            active_workflows = manager.get_workflows(active=True)
            if active_workflows and 'data' in active_workflows:
                for workflow in active_workflows['data']:
                    with st.expander(workflow['name']):
                        st.json(workflow)
                        if st.button(f"Deactivate {workflow['name']}", key=f"deactivate_{workflow['id']}"):
                            result = manager.toggle_workflow_status(workflow['id'], False)
                            if result:
                                st.success(f"{workflow['name']} deactivated successfully!")
                                st.rerun()
            else:
                st.warning("No active workflows found")
        
        with col2:
            st.subheader("Inactive Workflows")
            inactive_workflows = manager.get_workflows(active=False)
            if inactive_workflows and 'data' in inactive_workflows:
                for workflow in inactive_workflows['data']:
                    with st.expander(workflow['name']):
                        st.json(workflow)
                        if st.button(f"Activate {workflow['name']}", key=f"activate_{workflow['id']}"):
                            result = manager.toggle_workflow_status(workflow['id'], True)
                            if result:
                                st.success(f"{workflow['name']} activated successfully!")
                                st.rerun()
            else:
                st.warning("No inactive workflows found")

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
        workflow_id = st.text_input("Enter Workflow ID")
        if workflow_id:
            details = manager.get_workflow_details(workflow_id)
            if details:
                st.json(details)

    elif page == "Executions":
        st.header("Workflow Executions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            workflow_id = st.text_input("Filter by Workflow ID (Optional)")
        
        with col2:
            status = st.selectbox("Execution Status", ["", "success", "error", "waiting"])
        
        executions = manager.get_executions(
            workflow_id=workflow_id or None, 
            status=status or None
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

