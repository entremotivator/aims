import streamlit as st
import requests
import json
import logging
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

class N8NWorkflowManager:
    def __init__(self):
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

    def get_workflow_executions_stats(self, workflow_id, days=7):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        params = {
            "workflowId": workflow_id,
            "startedAfter": start_date.isoformat(),
            "startedBefore": end_date.isoformat(),
            "limit": 1000
        }
        executions = self.make_request("GET", "executions", params=params)
        if executions and 'data' in executions:
            return executions['data']
        return []

def main():
    st.set_page_config(page_title="n8n Workflow Manager", layout="wide")
    manager = N8NWorkflowManager()

    st.title("🔧 n8n Workflow Management Dashboard")
    
    page = st.sidebar.radio("Navigation", [
        "Workflows Overview", 
        "Create Workflow", 
        "Workflow Details", 
        "Executions", 
        "Analytics",
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
            
            st.subheader("Add Nodes")
            node_types = ["HTTP Request", "Function", "IF", "Switch", "Email"]
            nodes = []
            for i in range(3):
                node_type = st.selectbox(f"Node {i+1} Type", [""] + node_types, key=f"node_type_{i}")
                if node_type:
                    nodes.append({"type": node_type, "name": f"{node_type} {i+1}"})
            
            submitted = st.form_submit_button("Create Workflow")
            
            if submitted:
                result = manager.create_workflow(name, active=active, tags=tags, nodes=nodes)
                if result:
                    st.success("Workflow created successfully!")
                    st.json(result)

    elif page == "Workflow Details":
        st.header("Workflow Inspection")
        workflows = manager.get_workflows()
        if workflows and 'data' in workflows:
            selected_workflow = st.selectbox("Select Workflow", [w['name'] for w in workflows['data']])
            workflow = next((w for w in workflows['data'] if w['name'] == selected_workflow), None)
            if workflow:
                st.json(workflow)
                if st.button("Delete Workflow"):
                    if st.confirm(f"Are you sure you want to delete {workflow['name']}?"):
                        result = manager.delete_workflow(workflow['id'])
                        if result:
                            st.success(f"{workflow['name']} deleted successfully!")
                            st.rerun()
            else:
                st.warning("Workflow not found")
        else:
            st.warning("No workflows found")

    elif page == "Executions":
    st.header("Workflow Executions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        workflows = manager.get_workflows()
        workflow_names = ["All Workflows"] + [w['name'] for w in workflows['data']] if workflows and 'data' in workflows else ["All Workflows"]
        selected_workflow = st.selectbox("Select Workflow", workflow_names)
    
    with col2:
        status = st.selectbox("Execution Status", ["All", "success", "error", "waiting"])
    
    with col3:
        limit = st.number_input("Number of executions to show", min_value=1, max_value=250, value=100)
    
    with col4:
        include_data = st.checkbox("Include Detailed Data", value=False)
    
    workflow_id = next((w['id'] for w in workflows['data'] if w['name'] == selected_workflow), None) if selected_workflow != "All Workflows" else None
    
    params = {
        "limit": limit,
        "includeData": include_data,
        "status": status if status != "All" else None,
        "workflowId": workflow_id
    }
    
    executions = manager.get_executions(**params)
    
    if executions and 'data' in executions:
        df = pd.DataFrame(executions['data'])
        df['startedAt'] = pd.to_datetime(df['startedAt'])
        df['stoppedAt'] = pd.to_datetime(df['stoppedAt'])
        df['duration'] = df['stoppedAt'] - df['startedAt']
        
        st.dataframe(df[['id', 'workflowId', 'status', 'startedAt', 'stoppedAt', 'duration']])
        
        st.subheader("Execution Details")
        selected_execution = st.selectbox("Select an execution to view details", df['id'])
        if selected_execution:
            execution_details = manager.get_execution_details(selected_execution, include_data=include_data)
            if execution_details:
                st.json(execution_details)
        
        st.subheader("Execution Visualizations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Status Distribution")
            fig = px.pie(df, names='status', title='Execution Status Distribution')
            st.plotly_chart(fig)
        
        with col2:
            st.write("Execution Duration Over Time")
            fig = px.scatter(df, x='startedAt', y='duration', color='status', hover_data=['workflowId', 'id'],
                             title='Execution Duration Over Time')
            st.plotly_chart(fig)
        
        if 'nextCursor' in executions:
            st.write(f"Next Cursor: {executions['nextCursor']}")
    else:
        st.warning("No executions found")

def get_executions(self, workflow_id=None, status=None, limit=100, include_data=False, cursor=None):
    params = {
        "limit": min(limit, 250),
        "includeData": str(include_data).lower(),
    }
    if workflow_id:
        params["workflowId"] = workflow_id
    if status:
        params["status"] = status
    if cursor:
        params["cursor"] = cursor
    return self.make_request("GET", "executions", params=params)

def get_execution_details(self, execution_id, include_data=False):
    params = {"includeData": str(include_data).lower()}
    return self.make_request("GET", f"executions/{execution_id}", params=params)


    elif page == "Analytics":
        st.header("Workflow Analytics")
        workflows = manager.get_workflows()
        if workflows and 'data' in workflows:
            selected_workflow = st.selectbox("Select Workflow for Analysis", [w['name'] for w in workflows['data']])
            workflow = next((w for w in workflows['data'] if w['name'] == selected_workflow), None)
            if workflow:
                days = st.slider("Number of days to analyze", 1, 30, 7)
                executions = manager.get_workflow_executions_stats(workflow['id'], days)
                if executions:
                    df = pd.DataFrame(executions)
                    df['startedAt'] = pd.to_datetime(df['startedAt'])
                    df['duration'] = pd.to_timedelta(df['stoppedAt']) - pd.to_timedelta(df['startedAt'])
                    
                    st.subheader("Execution Trend")
                    daily_executions = df.groupby(df['startedAt'].dt.date).size().reset_index(name='count')
                    fig = px.line(daily_executions, x='startedAt', y='count', title='Daily Executions')
                    st.plotly_chart(fig)
                    
                    st.subheader("Execution Duration Statistics")
                    fig = px.box(df, y='duration', title='Execution Duration Distribution')
                    st.plotly_chart(fig)
                    
                    st.subheader("Status Distribution")
                    status_counts = df['status'].value_counts()
                    fig = px.bar(x=status_counts.index, y=status_counts.values, title='Execution Status Distribution')
                    st.plotly_chart(fig)
                else:
                    st.warning("No execution data found for the selected period")
            else:
                st.warning("Workflow not found")
        else:
            st.warning("No workflows found")

    elif page == "Tags Management":
        st.header("Tags Overview")
        tags = manager.get_tags()
        if tags and 'data' in tags:
            tag_df = pd.DataFrame(tags['data'])
            st.dataframe(tag_df)
            
            st.subheader("Create New Tag")
            with st.form("create_tag"):
                new_tag_name = st.text_input("New Tag Name")
                if st.form_submit_button("Create Tag"):
                    st.success(f"Tag '{new_tag_name}' created successfully!")
        else:
            st.warning("No tags found")

    elif page == "User Management":
        st.header("User Information")
        users = manager.get_users()
        if users and 'data' in users:
            user_df = pd.DataFrame(users['data'])
            st.dataframe(user_df)
            
            st.subheader("User Statistics")
            fig = px.bar(user_df['role'].value_counts(), title='User Roles Distribution')
            st.plotly_chart(fig)
        else:
            st.warning("No users found")

if __name__ == "__main__":
    main()
