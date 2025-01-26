import streamlit as st
import requests
import json
import uuid
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Define the n8n API base URL and authentication details
N8N_HOST = "agentonline-u29564.vm.elestio.app"
N8N_PORT = ""
N8N_BASE_PATH = "api/v1"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NDI5NWRjYS01YTIxLTQzZDMtYTA1OS1jOTA5YTQ5ZjlkYTEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzM3ODkxNTI0fQ.-JwLzCmtMVUcQ8NJTny6czBp963T8yJFtg_-S3RPxXo"

# n8n API URLs
API_URLS = {
    "workflows": f"{N8N_BASE_PATH}/workflows",
    "executions": f"{N8N_BASE_PATH}/executions",
    "credentials": f"{N8N_BASE_PATH}/credentials",
    "tags": f"{N8N_BASE_PATH}/tags",
    "users": f"{N8N_BASE_PATH}/users",
    "variables": f"{N8N_BASE_PATH}/variables"
}

def make_api_request(method, endpoint, headers=None, data=None, params=None):
    url = f"http://{N8N_HOST}:{N8N_PORT}/{endpoint}"
    headers = headers or {"accept": "application/json", "X-N8N-API-KEY": API_KEY}
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Invalid HTTP method")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"API error: {e}")
        st.error(f"API error: {e}")
        return None

# Enhanced Fetch Workflows with Pagination and Search
def fetch_workflows(cursor=None, limit=10, search_query=None):
    params = {"active": "true", "limit": limit}
    if cursor:
        params["cursor"] = cursor
    if search_query:
        params["search"] = search_query
    return make_api_request("GET", API_URLS["workflows"], params=params)

def fetch_workflow_by_id(workflow_id):
    return make_api_request("GET", f"{API_URLS['workflows']}/{workflow_id}")

def toggle_workflow_status(workflow_id, status):
    data = {"active": status}
    return make_api_request("PATCH", f"{API_URLS['workflows']}/{workflow_id}", data=data)

def create_workflow(name, active):
    data = {
        "name": name,
        "active": active,
    }
    return make_api_request("POST", API_URLS["workflows"], data=data)

def delete_workflow(workflow_id):
    return make_api_request("DELETE", f"{API_URLS['workflows']}/{workflow_id}")

def fetch_executions(workflow_id=None, limit=10):
    params = {"limit": limit}
    if workflow_id:
        params["workflowId"] = workflow_id
    return make_api_request("GET", API_URLS["executions"], params=params)

def fetch_variables():
    return make_api_request("GET", API_URLS["variables"])

def create_update_variable(key, value):
    data = {"key": key, "value": value}
    return make_api_request("POST", API_URLS["variables"], data=data)

# Enhanced Fetch Users and Tags
def fetch_users():
    return make_api_request("GET", API_URLS["users"])

def fetch_tags():
    return make_api_request("GET", API_URLS["tags"])

# Streamlit App Layout
st.title("n8n Workflow Manager")

page = st.sidebar.radio("Navigation", ["View Workflows", "Manage Workflow", "Executions", "Variables", "Create Workflow", "Upload Workflow", "View Users", "View Tags"])

# View Workflows with Search Functionality and Pagination
if page == "View Workflows":
    st.subheader("Active Workflows:")
    search_query = st.text_input("Search for workflows (optional)")
    cursor = None
    all_workflows = []
    while True:
        result = fetch_workflows(cursor, search_query=search_query)
        if result and "data" in result:
            all_workflows.extend(result["data"])
            cursor = result.get("nextCursor")
            if not cursor:
                break
        else:
            break
    
    if all_workflows:
        for workflow in all_workflows:
            with st.expander(f"Workflow: {workflow['name']} ({workflow['id']})"):
                st.write(f"**Status**: {'Active' if workflow['active'] else 'Inactive'}")
                st.write(f"**Created At**: {workflow['createdAt']}")
                st.write(f"**Updated At**: {workflow['updatedAt']}")
                if st.button(f"Delete {workflow['name']}", key=f"delete_{workflow['id']}"):
                    if delete_workflow(workflow['id']):
                        st.success(f"Workflow {workflow['name']} deleted successfully!")
                    else:
                        st.error(f"Failed to delete workflow {workflow['name']}")
    else:
        st.warning("No workflows found.")

# Manage Workflow with Improved Status Update and Node View
elif page == "Manage Workflow":
    st.subheader("Manage Workflow")
    workflow_id = st.text_input("Enter Workflow ID:")
    if workflow_id:
        workflow = fetch_workflow_by_id(workflow_id)
        if workflow:
            st.write(f"### Workflow: {workflow['name']}")
            st.write(f"**Status**: {'Active' if workflow['active'] else 'Inactive'}")
            new_status = st.radio("Set Workflow Status", ["Activate", "Deactivate"], index=0 if workflow["active"] else 1)
            if st.button("Update Workflow Status"):
                result = toggle_workflow_status(workflow_id, new_status == "Activate")
                if result:
                    st.success("Workflow status updated successfully!")
            
            st.write("### Workflow Nodes:")
            for node in workflow.get("nodes", []):
                with st.expander(f"Node: {node.get('name')}"):
                    st.write(f"**Type**: {node.get('type')}")
                    st.write(f"**Position**: {node.get('position')}")
                    st.write(f"**Disabled**: {node.get('disabled')}")
        else:
            st.warning(f"Workflow with ID {workflow_id} not found.")

# Enhanced Execution View with Pagination
elif page == "Executions":
    st.subheader("Workflow Executions")
    workflow_id = st.text_input("Enter Workflow ID (optional):")
    limit = st.slider("Number of Executions to Display", 1, 50, 10)
    executions = fetch_executions(workflow_id, limit)
    if executions and "data" in executions:
        for execution in executions["data"]:
            with st.expander(f"Execution: {execution['id']}"):
                st.write(f"**Status**: {execution['status']}")
                st.write(f"**Started At**: {execution['startedAt']}")
                st.write(f"**Finished At**: {execution['stoppedAt']}")
                st.write(f"**Mode**: {execution['mode']}")
    else:
        st.warning("No executions found.")

# Manage Variables with Update Option and List View
elif page == "Variables":
    st.subheader("Manage Variables")
    variables = fetch_variables()
    if variables and "data" in variables:
        for variable in variables["data"]:
            st.write(f"**{variable['key']}**: {variable['value']}")
    
    st.write("### Create/Update Variable")
    key = st.text_input("Variable Key:")
    value = st.text_input("Variable Value:")
    if st.button("Save Variable"):
        result = create_update_variable(key, value)
        if result:
            st.success("Variable saved successfully!")
        else:
            st.error("Failed to save variable.")

# Create New Workflow with Validation
elif page == "Create Workflow":
    st.subheader("Create New Workflow")
    name = st.text_input("Enter Workflow Name:")
    active = st.checkbox("Activate Workflow", value=True)
    if st.button("Create Workflow"):
        if not name:
            st.error("Please provide a workflow name.")
        else:
            result = create_workflow(name, active)
            if result:
                st.success("Workflow created successfully!")
                st.json(result)
            else:
                st.error("Failed to create workflow.")

# Upload Workflow with API Integration
elif page == "Upload Workflow":
    st.subheader("Upload Workflow")
    api_url = st.text_input("API URL", "http://localhost:5678/rest/workflows")
    auth_type = st.selectbox("Authentication Type", ["Basic", "JWT"])
    if auth_type == "Basic":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        credentials = f"{username}:{password}".encode('utf-8').decode('latin1')
    elif auth_type == "JWT":
        jwt_token = st.text_input("JWT Token", type="password")
        credentials = jwt_token
    
    uploaded_file = st.file_uploader("Choose a .json file", type="json")
    if uploaded_file is not None:
        file_content = json.load(uploaded_file)
        if st.button("Upload Workflow"):
            result, error = upload_workflow(file_content, api_url, auth_type, credentials)
            if result:
                st.success("Workflow uploaded successfully!")
            else:
                st.error(f"Failed to upload workflow: {error}")

# Handle Users and Tags
elif page == "View Users":
    st.subheader("View Users")
    users = fetch_users()
    if users:
        st.write(users)

elif page == "View Tags":
    st.subheader("View Tags")
    tags = fetch_tags()
    if tags:
        st.write(tags)
