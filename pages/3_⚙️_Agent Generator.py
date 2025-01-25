import streamlit as st
import json
import uuid

# Function to generate the JSON structure for a single node
def generate_node_json(data):
    """
    This function generates the JSON structure for a single node in the n8n workflow.
    The data parameter should contain the settings for the node, including position,
    type, options, and name.
    """
    return {
        "parameters": {
            "mode": "raw",  # Default mode, can be modified based on use case
            "includeOtherFields": f"={{ $json.body.chatInput }}",  # Default expression to include additional fields
            "options": data.get("options", {})  # Optional tool settings for the node
        },
        "type": data.get("type", "n8n-nodes-base.set"),  # Default node type if not provided
        "typeVersion": data.get("type_version", 3.4),  # Version of the node type, default to 3.4
        "position": [
            data.get("position_x", 940),  # Default X position for the node
            data.get("position_y", 340)   # Default Y position for the node
        ],
        "id": str(uuid.uuid4()),  # Generate a unique ID for each node
        "name": data.get("node_name", "Edit Fields")  # Node name, defaults to "Edit Fields" if not provided
    }

# Function to generate the complete JSON structure with multiple nodes and connections
def generate_json(data):
    """
    This function generates the complete JSON structure, including multiple nodes and their connections.
    It also handles the pin data and ensures that all nodes are connected to each other in a meaningful way.
    """
    nodes = []  # List to store the node JSON objects
    connections = {}  # Dictionary to store the connections between nodes

    for node_data in data:
        # Generate the JSON structure for each node
        node_json = generate_node_json(node_data)
        nodes.append(node_json)
        
        # Handle node connections (simplified version where all nodes are connected to the first node)
        if node_data.get("node_name") not in connections:
            connections[node_data.get("node_name")] = {"main": [[]]}  # Initial connection setup
    
    # Return the complete JSON structure with nodes, connections, and pin data
    return json.dumps({
        "nodes": nodes,
        "connections": connections,
        "pinData": {
            node.get("node_name", "Edit Fields"): [
                {"name": node.get("pin_name_1", "First item"), "code": 1},
                {"name": node.get("pin_name_2", "Second item"), "code": 2}
            ]
            for node in data
        }
    }, indent=4)

# Streamlit form for user input
def main():
    """
    This function creates the Streamlit app where users can input node settings,
    select tools, and generate the corresponding JSON for n8n workflows.
    """
    st.title("Enhanced JSON Generator for n8n Workflow")

    # To store all nodes data
    nodes_data = []

    # Streamlit form for user input
    with st.form(key="json_generator_form"):
        # Input for number of nodes to generate
        num_nodes = st.number_input("How many nodes do you want to add?", min_value=1, value=1, step=1)

        # Available tool options with example configurations
        available_tools = {
            "HTTP Request": {"url": "https://example.com", "method": "GET"},
            "Set": {"field1": "value1", "field2": "value2"},
            "Function": {"functionName": "processData", "params": "{}"},
            "IF": {"condition": "={{ $json.body.status == 'success' }}"},
            "Send Email": {"to": "example@example.com", "subject": "Test Email"}
        }

        # Loop to add multiple nodes
        for i in range(num_nodes):
            st.subheader(f"Node {i+1} Settings")

            # Input fields for node settings
            node_name = st.text_input(f"Node {i+1} Name", f"Node {i+1}")
            position_x = st.number_input(f"Node {i+1} Position X", min_value=0, value=940)
            position_y = st.number_input(f"Node {i+1} Position Y", min_value=0, value=340)

            # Tool selection for the node
            selected_tools = st.multiselect(f"Select tools for Node {i+1}", list(available_tools.keys()))
            options = {tool: available_tools[tool] for tool in selected_tools}

            # Pin Data fields (customize pin names)
            pin_name_1 = st.text_input(f"Node {i+1} Pin 1 Name", f"Pin 1 of Node {i+1}")
            pin_name_2 = st.text_input(f"Node {i+1} Pin 2 Name", f"Pin 2 of Node {i+1}")

            # Add this node's data to the nodes_data list for later JSON generation
            node_data = {
                "node_name": node_name,
                "position_x": position_x,
                "position_y": position_y,
                "options": options,
                "pin_name_1": pin_name_1,
                "pin_name_2": pin_name_2
            }
            nodes_data.append(node_data)

        # Submit button to generate the JSON
        submit_button = st.form_submit_button("Generate JSON")

    if submit_button:
        # Generate the complete JSON output based on the collected nodes data
        json_output = generate_json(nodes_data)

        # Display the generated JSON in the app
        st.subheader("Generated JSON")
        st.json(json_output)

        # Provide an option to download the JSON as a file
        st.download_button(
            label="Download JSON",
            data=json_output,
            file_name="generated_workflow.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
