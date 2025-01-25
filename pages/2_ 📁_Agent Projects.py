import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Initialize Streamlit app
st.set_page_config(page_title="Media Company Checklist")

# UI
st.title("***Media Company Checklist***")
st.subheader("Organize, Prioritize, and Manage your tasks effectively!")

# Local Database
@st.cache(allow_output_mutation=True)
def get_local_data():
    return pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed", "Subtasks"])

data = get_local_data()

# Functions for interacting with local data
def save_local_data():
    data.to_csv("local_data.csv", index=False)

def load_local_data():
    return pd.read_csv("local_data.csv") if "local_data.csv" in os.listdir() else pd.DataFrame(columns=["Task", "Category", "Due Date", "Priority", "Completed", "Subtasks"])

def add_task(task, category, due_date, priority, completed, subtasks):
    global data
    new_task = {"Task": task, "Category": category, "Due Date": due_date, "Priority": priority, "Completed": completed, "Subtasks": subtasks}
    data = data.append(new_task, ignore_index=True)
    save_local_data()

def edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed, updated_subtasks):
    global data
    task_index = task_id
    data.at[task_index, "Task"] = updated_task
    data.at[task_index, "Category"] = updated_category
    data.at[task_index, "Due Date"] = updated_due_date
    data.at[task_index, "Priority"] = updated_priority
    data.at[task_index, "Completed"] = completed
    data.at[task_index, "Subtasks"] = updated_subtasks
    save_local_data()

def clone_task(task_id):
    global data
    task_to_clone = data.iloc[task_id]
    clone_task = task_to_clone.copy()
    clone_task["Task"] = f"Copy of {clone_task['Task']}"
    data = data.append(clone_task, ignore_index=True)
    save_local_data()

def delete_task(task_id):
    global data
    data = data.drop(index=task_id).reset_index(drop=True)
    save_local_data()

# Load data from CSV
load_local_data()

# Add example to-do list tasks with subtasks
example_tasks = [
    {
        "Task": "Evaluate AI Agent Performance",
        "Category": "AI Management",
        "Due Date": "2024-04-15",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Monitor task completion rate",
            "Assess agent decision-making accuracy",
            "Evaluate agent's response time and latency",
            "Track agent learning curve and improvement",
            "Analyze user feedback for performance issues",
            "Compare AI agent performance with human benchmarks",
            "Implement performance optimization strategies"
        ]
    },
    {
        "Task": "Build New AI Agent",
        "Category": "Agent Development",
        "Due Date": "2024-05-05",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Define agent's purpose and functionalities",
            "Create detailed agent blueprint",
            "Select AI models and algorithms",
            "Develop agent's knowledge base and reasoning capabilities",
            "Test agent's decision-making and adaptability",
            "Validate agent's training with real-world scenarios",
            "Optimize agent's performance before deployment",
            "Document agent's capabilities and limitations"
        ]
    },
    {
        "Task": "Review AI Agent's Ethical Considerations",
        "Category": "Ethics & Governance",
        "Due Date": "2024-05-10",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Ensure compliance with privacy regulations",
            "Assess agent's potential for bias and discrimination",
            "Implement fairness audits",
            "Review decision-making transparency",
            "Establish protocols for addressing ethical concerns",
            "Evaluate the impact of AI decisions on users"
        ]
    },
    {
        "Task": "Create Task Flow for AI Agent",
        "Category": "System Design",
        "Due Date": "2024-05-15",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Define input-output parameters for the agent",
            "Map out decision-making steps and processes",
            "Ensure the task flow aligns with business goals",
            "Identify potential bottlenecks and optimize flow",
            "Test task flow with sample data"
        ]
    },
    {
        "Task": "Conduct Continuous Training for AI Agent",
        "Category": "AI Training",
        "Due Date": "2024-05-20",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Review initial training datasets for adequacy",
            "Feed new data and scenarios for continuous learning",
            "Assess AI agent's performance after training updates",
            "Monitor training quality and adjust parameters as needed",
            "Ensure real-time learning feedback mechanisms are in place"
        ]
    },
    {
        "Task": "Develop AI Agent Monitoring Dashboard",
        "Category": "System Monitoring",
        "Due Date": "2024-06-01",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Create UI/UX for monitoring agent performance",
            "Integrate real-time data feeds into the dashboard",
            "Track key performance metrics such as task completion, latency, and accuracy",
            "Implement alerts for performance dips or failures",
            "Develop custom reporting features for stakeholders"
        ]
    },
    {
        "Task": "Optimize Agent's Interaction with Users",
        "Category": "User Experience",
        "Due Date": "2024-06-05",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Review current user-agent interactions",
            "Identify friction points in user engagement",
            "Implement conversational UI improvements",
            "Optimize agent's response clarity and helpfulness",
            "Test interactions for better user satisfaction"
        ]
    },
    {
        "Task": "Integrate AI Agent with Existing Systems",
        "Category": "System Integration",
        "Due Date": "2024-06-10",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Map out required system integrations",
            "Ensure data flow compatibility with external platforms",
            "Test API connections and data exchanges",
            "Optimize data synchronization and latency",
            "Conduct end-to-end system validation"
        ]
    },
    {
        "Task": "Run Simulations and Stress Tests for AI Agent",
        "Category": "Quality Assurance",
        "Due Date": "2024-06-15",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Simulate high-stress scenarios to test agent robustness",
            "Evaluate agent's scalability in different environments",
            "Assess agent's ability to handle unpredictable inputs",
            "Implement stress test findings to improve agent's resilience"
        ]
    },
    {
        "Task": "Establish Metrics for AI Agent Evaluation",
        "Category": "Performance Metrics",
        "Due Date": "2024-06-20",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Define key performance indicators (KPIs) for agent performance",
            "Create real-time tracking for evaluation metrics",
            "Evaluate metrics for continuous improvement opportunities",
            "Ensure metrics align with business objectives and user needs"
        ]
    },
    # Additional Tasks
    {
        "Task": "Implement Natural Language Processing in AI Agent",
        "Category": "AI Development",
        "Due Date": "2024-06-30",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Research and select NLP models",
            "Integrate NLP model into AI agent",
            "Test AI agent's text comprehension and response generation",
            "Ensure multilingual support and language understanding",
            "Validate the accuracy of NLP model in various contexts"
        ]
    },
    {
        "Task": "Deploy AI Agent to Cloud Infrastructure",
        "Category": "Deployment",
        "Due Date": "2024-07-10",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Select cloud provider (AWS, Azure, GCP)",
            "Prepare cloud infrastructure for deployment",
            "Deploy AI agent to cloud environment",
            "Test agent's performance in the cloud",
            "Monitor cloud resource usage and optimize"
        ]
    },
    {
        "Task": "Implement AI Agent Security Protocols",
        "Category": "Security",
        "Due Date": "2024-07-15",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Define security standards for AI agent",
            "Integrate encryption and authentication mechanisms",
            "Test agent's security vulnerabilities",
            "Perform penetration testing on AI agent systems",
            "Ensure compliance with data protection laws"
        ]
    },
    {
        "Task": "Conduct AI Agent User Acceptance Testing",
        "Category": "Testing",
        "Due Date": "2024-07-20",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Create UAT plan and test cases",
            "Invite internal users for testing",
            "Collect feedback on user experience",
            "Resolve issues and enhance usability",
            "Confirm system's stability post-testing"
        ]
    },
    {
        "Task": "Optimize AI Agent's Computational Efficiency",
        "Category": "Optimization",
        "Due Date": "2024-07-25",
        "Priority": "High",
        "Completed": False,
        "Subtasks": [
            "Review current computation resources and usage",
            "Implement model optimization techniques",
            "Reduce inference time and improve throughput",
            "Test optimized agent performance under varying loads",
            "Monitor long-term agent performance after optimizations"
        ]
    },
    {
        "Task": "Create Post-Launch Monitoring Plan",
        "Category": "Post-launch",
        "Due Date": "2024-07-30",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Define key performance indicators for post-launch",
            "Set up automated monitoring for agent behavior",
            "Create escalation procedures for system failures",
            "Evaluate user feedback and optimize"
        ]
    },
    {
        "Task": "Research advertising opportunities",
        "Category": "Marketing",
        "Due Date": "2024-04-25",
        "Priority": "Medium",
        "Completed": False,
        "Subtasks": [
            "Identify target demographics and media channels",
            "Explore advertising options such as PPC, display ads, and sponsored content",
            "Analyze competitors' advertising strategies",
            "Allocate budget and negotiate ad placements",
            "Track ad performance and adjust campaigns for optimal results"
        ]
    },
]

# Display tasks with additional features
for task_id, task_data in enumerate(example_tasks):
    task_key = f"task-{task_id}"
    with st.expander(task_data["Task"]):
        st.write(f"- Category: {task_data['Category']}")
        st.write(f"- Due Date: {task_data['Due Date']}")
        st.write(f"- Priority: {task_data['Priority']}")
        st.write("- Subtasks:")
        subtask_checkboxes = []
        for subtask_id, subtask in enumerate(task_data["Subtasks"]):
            subtask_completed = st.checkbox(subtask, key=f"{task_key}-subtask-{subtask_id}")
            subtask_checkboxes.append(subtask_completed)
        completed = st.checkbox("Completed", key=f"{task_key}-completed")
        if st.button("Edit Task", key=f"{task_key}-edit"):
            updated_task = st.text_input("Task", value=task_data["Task"])
            updated_category = st.text_input("Category", value=task_data["Category"])
            updated_due_date = st.date_input("Due Date", value=datetime.strptime(task_data["Due Date"], "%Y-%m-%d") if task_data["Due Date"] else None, key=f"{task_key}-due-date")
            updated_priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(task_data["Priority"]), key=f"{task_key}-priority")
            updated_subtasks = st.text_area("Subtasks (one per line)", value="\n".join(task_data["Subtasks"]), key=f"{task_key}-subtasks")
            edit_task(task_id, updated_task, updated_category, updated_due_date, updated_priority, completed, updated_subtasks.split("\n"))
        if st.button("Delete Task", key=f"{task_key}-delete"):
            delete_task(task_id)
        if st.button("Clone Task", key=f"{task_key}-clone"):
            clone_task(task_id)
