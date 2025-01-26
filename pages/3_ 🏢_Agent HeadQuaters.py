import streamlit as st
import requests
import json
import uuid
from datetime import datetime
import logging
import pandas as pd

# Advanced Logging Configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='n8n_workflow_manager.log'
)

class N8NWorkflowManager:
    def __init__(self):
        # Configuration Management
        self.N8N_HOST = "agentonline-u29564.vm.elestio.app"
        self.N8N_PORT = ""
        self.N8N_BASE_PATH = "api/v1"
        self.API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NDI5NWRjYS01YTIxLTQzZDMtYTA1OS1jOTA5YTQ5ZjlkYTEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM3MTI2NTEwfQ.R2doAECbp1CCGzebWxG0XMqpA-_WHDM40nauk3tvuO4"
        
        # API Endpoint Mapping
        self.API_URLS = {
            "workflows": f"{self.N8N_BASE_PATH}/workflows",
            "executions": f"{self.N8N_BASE_PATH}/executions",
            "credentials": f"{self.N8N_BASE_PATH}/credentials",
            "tags": f"{self.N8N_BASE_PATH}/tags",
            "users": f"{self.N8N_BASE_PATH}/users",
            "variables": f"{self.N8N_BASE_PATH}/variables"
        }

    def make_api_request(self, method, endpoint, headers=None, data=None, params=None):
        """Enhanced API request method with comprehensive error handling."""
        url = f"http://{self.N8N_HOST}:{self.N8N_PORT}/{endpoint}"
        headers = headers or {"accept": "application/json", "X-N8N-API-KEY": self.API_KEY}
        
        try:
            # Dynamically select request method
            request_methods = {
                "GET": requests.get,
                "POST": requests.post,
                "PATCH": requests.patch,
                "DELETE": requests.delete
            }
            
            response = request_methods[method](
                url, 
                headers=headers, 
                json=data, 
                params=params
            )
            
            # Advanced error handling
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            logging.error(f"API Request Error: {e}")
            st.error(f"API Request Failed: {e}")
            return None
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON response")
            st.error("Invalid JSON response from server")
            return None

    def fetch_workflows(self, active=True, search_query=None, limit=50, cursor=None):
        """Comprehensive workflow fetching with advanced filtering."""
        params = {
            "active": str(active).lower(),
            "limit": limit
        }
        
        if search_query:
            params["search"] = search_query
        if cursor:
            params["cursor"] = cursor
        
        return self.make_api_request("GET", self.API_URLS["workflows"], params=params)

    def fetch_workflow_details(self, workflow_id):
        """Retrieve comprehensive workflow details."""
        return self.make_api_request("GET", f"{self.API_URLS['workflows']}/{workflow_id}")

    def create_workflow(self, name, nodes=None, connections=None, active=True, tags=None):
        """Advanced workflow creation with optional configurations."""
        data = {
            "name": name,
            "active": active,
            "nodes": nodes or [],
            "connections": connections or {},
            "tags": tags or []
        }
        return self.make_api_request("POST", self.API_URLS["workflows"], data=data)

    def update_workflow(self, workflow_id, update_data):
        """Flexible workflow update method."""
        return self.make_api_request("PATCH", f"{self.API_URLS['workflows']}/{workflow_id}", data=update_data)

    def delete_workflow(self, workflow_id):
        """Workflow deletion with logging."""
        result = self.make_api_request("DELETE", f"{self.API_URLS['workflows']}/{workflow_id}")
        if result:
            logging.info(f"Workflow {workflow_id} deleted successfully")
        return result

    def fetch_executions(self, workflow_id=None, status=None, limit=50):
        """Advanced execution tracking with multiple filters."""
        params = {"limit": limit}
        
        if workflow_id:
            params["workflowId"] = workflow_id
        if status:
            params["status"] = status
        
        return self.make_api_request("GET", self.API_URLS["executions"], params=params)

def main():
    st.set_page_config(
        page_title="n8n Workflow Management", 
        page_icon="🤖", 
        layout="wide"
    )
    
    manager = N8NWorkflowManager()
    
    # Advanced Sidebar Navigation
    st.sidebar.title("🔧 Workflow Management")
    page = st.sidebar.radio("Navigation", [
        "Dashboard", 
        "Workflow Explorer", 
        "Create Workflow", 
        "Workflow Details", 
        "Execution Tracker", 
        "Tags & Users"
    ])

    # Dashboard Page
    if page == "Dashboard":
        st.title("n8n Workflow Management Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Active Workflows")
            active_workflows = manager.fetch_workflows(active=True, limit=10)
            if active_workflows and 'data' in active_workflows:
                df = pd.DataFrame(active_workflows['data'])
                st.dataframe(df[['name', 'id', 'createdAt']])
        
        with col2:
            st.subheader("Recent Executions")
            recent_executions = manager.fetch_executions(limit=10)
            if recent_executions and 'data' in recent_executions:
                df = pd.DataFrame(recent_executions['data'])
                st.dataframe(df[['id', 'status', 'startedAt']])

    # Workflow Explorer Page
    elif page == "Workflow Explorer":
        st.header("Workflow Explorer")
        
        search_query = st.text_input("Search Workflows")
        active_filter = st.checkbox("Show Active Workflows", value=True)
        
        workflows = manager.fetch_workflows(
            active=active_filter, 
            search_query=search_query, 
            limit=50
        )
        
        if workflows and 'data' in workflows:
            for workflow in workflows['data']:
                with st.expander(f"{workflow['name']} (ID: {workflow['id']})"):
                    st.json(workflow)

    # Create Workflow Page
    elif page == "Create Workflow":
        st.header("Create New Workflow")
        
        with st.form("workflow_creation"):
            name = st.text_input("Workflow Name")
            active = st.checkbox("Active", value=True)
            tags = st.multiselect("Select Tags", 
                ["Automation", "Data Processing", "Integration", "Custom"])
            
            nodes = st.text_area("Workflow Nodes (JSON)", height=200)
            connections = st.text_area("Workflow Connections (JSON)", height=200)
            
            submitted = st.form_submit_button("Create Workflow")
            
            if submitted:
                try:
                    parsed_nodes = json.loads(nodes) if nodes else None
                    parsed_connections = json.loads(connections) if connections else None
                    
                    result = manager.create_workflow(
                        name, 
                        nodes=parsed_nodes, 
                        connections=parsed_connections, 
                        active=active, 
                        tags=tags
                    )
                    
                    if result:
                        st.success("Workflow created successfully!")
                        st.json(result)
                    else:
                        st.error("Failed to create workflow")
                
                except json.JSONDecodeError:
                    st.error("Invalid JSON for nodes or connections")

    # Rest of the implementation would follow similar patterns...

    # Add error handling, comprehensive logging, and advanced features

if __name__ == "__main__":
    main()
