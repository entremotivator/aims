import streamlit as st
import pandas as pd
import random
import string

# Function to generate random employee ID
def generate_employee_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Function to generate random employee data for demo
def generate_demo_employees(num_employees=25):
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan', 'Judy', 
             'Karl', 'Leo', 'Mona', 'Nina', 'Oscar', 'Paul', 'Quincy', 'Rachel', 'Sam', 'Tracy', 
             'Ursula', 'Victor', 'Wendy', 'Xander', 'Yvonne', 'Zach']
    
    roles = ['AI Assistant', 'AI Manager', 'AI Developer', 'AI Content Creator', 'AI Designer', 
             'CFO', 'COO', 'CTO', 'CEO', 'Social Media Manager', 'Product Manager', 'HR Manager']
    
    specialties = ['Customer Support', 'Project Management', 'Web Development', 'Data Science', 'Content Creation',
                   'Financial Management', 'Operations', 'Product Development', 'Marketing', 'Employee Relations']
    
    skills = ['Python', 'JavaScript', 'Machine Learning', 'React', 'Node.js', 'AI', 'Data Analysis', 
              'SQL', 'Deep Learning', 'Cloud Computing', 'Financial Analysis', 'Business Strategy', 
              'Leadership', 'Team Management', 'SEO', 'Social Media Marketing', 'Project Management']
    
    statuses = ['Active', 'Inactive', 'On Leave']
    
    # New list of 50 AI Tools/Integrations
    ai_tools = [
        'n8n', 'Python', 'JavaScript', 'Node.js', 'SQL', 'Deep Learning', 'Data Analysis', 
        'Natural Language Processing', 'Cloud Computing', 'Machine Learning', 'Automation', 
        'AI Workflow', 'Team Management', 'GitHub Actions', 'AWS Lambda', 'Data Engineering', 'Azure',
        'Google Cloud', 'IBM Watson', 'RPA', 'UI/UX Design', 'Zapier', 'Salesforce Integration',
        'Content Creation', 'Digital Marketing', 'TensorFlow', 'Keras', 'OpenAI GPT', 'BERT', 
        'AI Chatbots', 'Python Flask', 'Hugging Face', 'AWS SageMaker', 'Trello Automation', 'Slack Bots',
        'Asana', 'Zoho CRM', 'Product Management', 'HR Automation', 'Social Media Management', 'SEO Tools',
        'Sales Automation', 'CRM Tools', 'Voice Assistants', 'AI-driven Analytics', 'Robotics Process Automation', 
        'AWS Polly', 'Customer Service AI', 'CI/CD Pipelines', 'Video Editing AI', 'Smart Contracts', 'Blockchain Automation'
    ]
    
    employees = []
    for _ in range(num_employees):
        name = random.choice(names)
        role = random.choice(roles)
        specialty = random.choice(specialties)
        skill_set = random.sample(skills, random.randint(2, 4))
        status = random.choice(statuses)
        
        employees.append({
            'id': generate_employee_id(),
            'name': name,
            'role': role,
            'specialty': specialty,
            'skills': skill_set,
            'status': status,
            'automation_tool': random.choice([True, False]),
            'tools': random.sample(ai_tools, random.randint(3, 6)),
            'automation_integration': 'n8n Workflow' if random.choice([True, False]) else 'None'
        })
    return employees

# Generate demo employees (now linked to more tools)
ai_employees = generate_demo_employees(50)

# Set page configuration
st.set_page_config(
    page_title="AI Employee Management System",
    page_icon="🤖",
    layout="wide",
)

# Sidebar for adding new employees
def add_employee_sidebar():
    st.sidebar.header("Add New AI Employee")

    # Employee Details
    name = st.sidebar.text_input("AI Employee Name", key="employee_name")
    role = st.sidebar.selectbox("Role", ['AI Assistant', 'AI Developer', 'AI Manager', 'AI Content Creator', 'AI Designer', 
                                        'CFO', 'COO', 'CTO', 'CEO', 'Social Media Manager', 'Product Manager', 'HR Manager'], key="role")
    specialty = st.sidebar.text_input("Specialty (Skill Area)", key="specialty")
    skills = st.sidebar.text_area("Skills (Comma Separated)", key="skills")
    status = st.sidebar.radio("Employee Status", ['Active', 'Inactive', 'On Leave'], key="status")

    # Automation and Tools Integration
    automation_tool = st.sidebar.checkbox("Activate n8n Automation Tool?", key="automation_tool")
    tools = st.sidebar.multiselect("Select AI Tools/Integrations", [
        'n8n', 'Python', 'JavaScript', 'Node.js', 'SQL', 'Deep Learning', 'Data Analysis', 'Natural Language Processing', 
        'Cloud Computing', 'Machine Learning', 'AI Workflow', 'Automation', 'AI Chatbots', 'GitHub Actions', 'Google Cloud', 
        'AWS Lambda', 'Azure', 'Zapier', 'Salesforce Integration', 'Content Creation', 'Digital Marketing', 'OpenAI GPT', 
        'TensorFlow', 'Keras', 'Hugging Face', 'AI-driven Analytics', 'Voice Assistants'], key="tools")

    if automation_tool:
        automation_integration = st.sidebar.text_input("Enter n8n Workflow Link or Script", key="automation_integration")

    # Generate a random employee ID
    employee_id = generate_employee_id()

    if st.sidebar.button("Add AI Employee"):
        if name and specialty and skills:
            new_employee = {
                'id': employee_id,
                'name': name,
                'role': role,
                'specialty': specialty,
                'skills': skills.split(','),
                'status': status,
                'automation_tool': automation_tool,
                'tools': tools,
                'automation_integration': automation_integration if automation_tool else 'None'
            }
            ai_employees.append(new_employee)
            st.sidebar.success(f"AI Employee {name} added successfully!")
        else:
            st.sidebar.error("Please fill all the required fields.")

# Display All AI Employees
def display_all_employees():
    st.header("AI Employee Overview")
    if ai_employees:
        employee_data = pd.DataFrame(ai_employees)
        st.dataframe(employee_data)
    else:
        st.write("No AI employees added yet.")

# AI Employee Profile
def view_employee_profile(employee_id):
    st.header(f"AI Employee Profile: {employee_id}")
    employee = next((emp for emp in ai_employees if emp['id'] == employee_id), None)

    if employee:
        st.write(f"**Name**: {employee['name']}")
        st.write(f"**Role**: {employee['role']}")
        st.write(f"**Specialty**: {employee['specialty']}")
        st.write(f"**Skills**: {', '.join(employee['skills'])}")
        st.write(f"**Status**: {employee['status']}")
        st.write(f"**Automation Tool Activated**: {employee['automation_tool']}")
        st.write(f"**n8n Workflow Integration**: {employee['automation_integration']}")
        st.write(f"**Tools/Integrations**: {', '.join(employee['tools'])}")
    else:
        st.warning(f"Employee with ID {employee_id} not found.")

# Main App Layout
def main():
    add_employee_sidebar()
    
    # Sidebar for navigating through different functionalities
    menu = ["Dashboard", "View All Employees", "View Employee Profile"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Dashboard":
        st.title("AI Employee Management System")
        st.write("Manage your AI-powered employees, assign tasks, automate workflows, and track performance.")
    
    elif choice == "View All Employees":
        display_all_employees()

    elif choice == "View Employee Profile":
        employee_id = st.text_input("Enter Employee ID", key="profile_id")
        if employee_id:
            view_employee_profile(employee_id)

if __name__ == "__main__":
    main()
