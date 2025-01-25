import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
import streamlit.components.v1 as components
import json
from fpdf import FPDF

# Initialize agent data for both teams
super_agents = [
    {"name": "Task Executor", "manager": "Operation Manager", "tasks": ["Execute daily tasks", "Monitor KPIs", "Prepare status reports"]},
    {"name": "Coordinator", "manager": "Operation Manager", "tasks": ["Coordinate with other departments", "Manage scheduling", "Resolve conflicts"]},
    {"name": "Budget Analyst", "manager": "Finance Manager", "tasks": ["Analyze financial statements", "Prepare budget reports", "Forecast future financial needs"]},
    {"name": "Account Manager", "manager": "Finance Manager", "tasks": ["Reconcile accounts", "Track expenses", "Generate financial reports"]},
    {"name": "Customer Liaison", "manager": "Support Manager", "tasks": ["Handle customer inquiries", "Resolve complaints", "Monitor service quality"]},
    {"name": "Support Specialist", "manager": "Support Manager", "tasks": ["Assist customers", "Update FAQs", "Provide technical support"]}
]

full_agents = [
    {"name": "LinkedIn Agent", "manager": "Communication Manager", 
     "tasks": ["Query LinkedIn database", "Find similar posts"]},
    {"name": "Email Agent", "manager": "Communication Manager",
     "tasks": ["Get Emails", "Send Emails"]},
    {"name": "CRM Agent", "manager": "Project Manager",
     "tasks": ["Add contact to CRM", "Update a contact"]},
    {"name": "Voice Agent",  "manager":  'Executive Director',
     'tasks': ['Call people', 'Get phone number from name']},
    {"name": 'Travel Research', 'manager': 'Research Manager',
     'tasks': ['Check Google Flights', 'Check Google Hotels']}
]

# Function to create a NetworkX graph for agents
def create_networkx_graph(agents):
    G = nx.DiGraph()
    G.add_edges_from([
        ("Agent Team", agents[0]["manager"]),
        ("Agent Team", agents[1]["manager"]),
        ("Agent Team", agents[2]["manager"]),
        ("Agent Team", agents[3]["manager"]),
        ("Agent Team", agents[4]["manager"]),
        ("Agent Team", agents[5]["manager"])
    ])
    
    for agent in agents:
        G.add_edge(agent["manager"], agent["name"])
    
    return G

# Function to render a Graphviz diagram for agents
def create_graphviz_diagram(agents):
    diagram = Digraph("Agent Team")
    diagram.attr(rankdir="TB")

    # Add main node
    diagram.node("Agent Team", shape="rectangle")

    # Add managers and their responsibilities
    managers = {}
    
    for agent in agents:
        if agent["manager"] not in managers:
            managers[agent["manager"]] = []
        managers[agent["manager"]].append(agent)

    for manager, agents_list in managers.items():
        diagram.node(manager, manager, shape="rectangle")
        diagram.edge("Agent Team", manager)
        
        for agent in agents_list:
            task_details = "\n".join(agent["tasks"])
            diagram.node(agent["name"], f"{agent['name']}\n{task_details}", shape="ellipse")
            diagram.edge(manager, agent["name"])

    return diagram

# Streamlit Layout
st.title("Team Structure and Responsibilities")
st.write("This application provides a breakdown of different teams, including roles, responsibilities, and tasks.")

# Create tabs for each team
team_selection = st.sidebar.radio("Select Team:", ("Super Agent Team", "Full Agent Team"))

if team_selection == 'Super Agent Team':
    st.subheader("Super Agent Team Structure")
    
    # Choose visualization type for Super Agents
    vis_type_super = st.sidebar.radio("Select a visualization type:", ("NetworkX Graph", "Graphviz Diagram"))
    
    if vis_type_super == 'NetworkX Graph':
        G_super = create_networkx_graph(super_agents)
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G_super)
        nx.draw(G_super, pos, with_labels=True, node_color="skyblue",
                node_size=3000, font_size=10, font_weight="bold")
        
        st.pyplot(plt)

    elif vis_type_super == 'Graphviz Diagram':
        diagram_super = create_graphviz_diagram(super_agents)
        st.graphviz_chart(diagram_super.source)

elif team_selection == 'Full Agent Team':
    st.subheader("Full Agent Team Structure")
    
    # Choose visualization type for Full Agents
    vis_type_full = st.sidebar.radio("Select a visualization type:", ("NetworkX Graph", "Graphviz Diagram"))
    
    if vis_type_full == 'NetworkX Graph':
        G_full = create_networkx_graph(full_agents)
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G_full)
        nx.draw(G_full, pos, with_labels=True, node_color="lightgreen",
                node_size=3000, font_size=10, font_weight="bold")
        
        st.pyplot(plt)

    elif vis_type_full == 'Graphviz Diagram':
        diagram_full = create_graphviz_diagram(full_agents)
        st.graphviz_chart(diagram_full.source)

# Form to add a new agent
st.sidebar.header("Add New Agent")
new_agent_name = st.sidebar.text_input("Enter New Agent Name")
new_agent_manager = st.sidebar.selectbox("Select Manager:", ["Operation Manager",
                                                              "Finance Manager",
                                                              "Support Manager",
                                                              'Communication Manager',
                                                              'Project Manager',
                                                              'Executive Director',
                                                              'Research Manager'])
new_agent_tasks = st.sidebar.text_area("Enter Tasks for New Agent (separate tasks with commas)").split(",")

if st.sidebar.button("Add New Agent"):
    new_agent = {
        "name": new_agent_name,
        "manager": new_agent_manager,
        "tasks": [task.strip() for task in new_agent_tasks]
    }
    
    if team_selection == 'Super Agent Team':
        super_agents.append(new_agent)
        st.sidebar.success(f"New agent {new_agent_name} added under {new_agent_manager}!")
        
    else:
        full_agents.append(new_agent)
        st.sidebar.success(f"New agent {new_agent_name} added under {new_agent_manager}!")

# Export Agents as JSON or PDF with confirmation messages
st.sidebar.header("Export Agents")
json_export = st.sidebar.button("Export Agents as JSON")
if json_export:
   if team_selection == 'Super Agent Team':
       with open("super_agents.json","w") as json_file:
           json.dump(super_agents,json_file,indent=4)
       st.sidebar.success("Super Agents exported as super_agents.json!")
   else:
       with open("full_agents.json","w") as json_file:
           json.dump(full_agents,json_file,indent=4)
       st.sidebar.success("Full Agents exported as full_agents.json!")

pdf_export = st.sidebar.button("Export Agents as PDF")
if pdf_export:
   pdf = FPDF()
   pdf.set_auto_page_break(auto=True, margin=15)
   pdf.add_page()
   pdf.set_font("Arial", size=12)

   if team_selection == 'Super Agent Team':
       pdf.cell(200, 10, txt="Super Agent Team Overview:", ln=True, align="C")
       pdf.ln(10)

       for agent in super_agents:
           pdf.cell(200, 10, txt=f"Agent: {agent['name']}", ln=True)
           pdf.cell(200, 10, txt=f"Manager: {agent['manager']}", ln=True)
           pdf.cell(200, 10, txt="Tasks:", ln=True)
           for task in agent["tasks"]:
               pdf.cell(200, 10, txt=f"- {task}", ln=True)
           pdf.ln(5)

       pdf.output("super_agents.pdf")
       st.sidebar.success("Super Agents exported as super_agents.pdf!")
   else:
       pdf.cell(200, 10, txt="Full Agent Team Overview:", ln=True, align="C")
       pdf.ln(10)

       for agent in full_agents:
           pdf.cell(200, 10, txt=f"Agent: {agent['name']}", ln=True)
           pdf.cell(200, 10, txt=f"Manager: {agent['manager']}", ln=True)
           pdf.cell(200, 10, txt="Tasks:", ln=True)
           for task in agent["tasks"]:
               pdf.cell(200, 10, txt=f"- {task}", ln=True)
           pdf.ln(5)

       pdf.output("full_agents.pdf")
       st.sidebar.success("Full Agents exported as full_agents.pdf!")

# Import Agents from JSON with error handling
st.sidebar.header("Import Agents")
uploaded_file = st.sidebar.file_uploader("Choose a JSON file to upload:", type=["json"])
if uploaded_file is not None:
   try:
       imported_agents = json.load(uploaded_file)
       if team_selection == 'Super Agent Team':
           super_agents.extend(imported_agents)
           st.sidebar.success(f"{len(imported_agents)} agents imported successfully into Super Agents!")
       else:
           full_agents.extend(imported_agents)
           st.sidebar.success(f"{len(imported_agents)} agents imported successfully into Full Agents!")
       
       st.experimental_rerun()
   except json.JSONDecodeError:
       st.sidebar.error("Failed to decode JSON file.")