import streamlit as st

# Define categories and their capabilities and prompts
data_formats = {
    "CSV": {
        "capabilities": [
            "Data analysis",
            "Visualization",
            "Data cleaning",
            "Data merging and transformation"
        ],
        "prompts": [
            "Analyze this CSV file and find the top 5 most frequent items in column B.",
            "Clean the dataset in this CSV by removing rows with missing values.",
            "Sort this CSV file by the 'Sales' column in descending order.",
            "Create a summary of the average values in each column of this CSV.",
            "Combine two CSV files based on the 'ID' column.",
            "Visualize the data in column A as a bar chart.",
            "Filter rows where column C is greater than 50 and save it as a new CSV.",
            "Explain the trends in column D over time based on this CSV.",
            "Convert this CSV into a JSON file while maintaining data structure.",
            "Add a new column to this CSV where each value is the square of column E."
        ]
    },
    "PDF": {
        "capabilities": [
            "Text extraction",
            "Summarization",
            "Redaction",
            "Content conversion"
        ],
        "prompts": [
            "Extract all text from this PDF and provide it in plain text format.",
            "Summarize the key points in this legal document PDF.",
            "Redact personal information from this PDF, including names and SSNs.",
            "Convert this PDF into an editable Word document.",
            "Highlight all instances of the word 'contract' in this PDF.",
            "Split this PDF into separate files, one for each page.",
            "Extract all tables from this PDF and save them as CSV files.",
            "Translate the content of this PDF into Spanish.",
            "Create an index of all the headings and subheadings in this PDF.",
            "Annotate this PDF with notes summarizing each section."
        ]
    },
    "SQL": {
        "capabilities": [
            "Query writing",
            "Database optimization",
            "Data relationships analysis",
            "Insights generation"
        ],
        "prompts": [
            "Write an SQL query to find the top 10 customers by total purchase amount.",
            "Optimize this SQL query for better performance.",
            "Explain the relationship between the 'Orders' and 'Customers' tables.",
            "Create an SQL script to back up the entire database.",
            "Write a query to calculate the average sales per month for the last year.",
            "Find duplicate entries in the 'Products' table.",
            "Create a new table schema for storing user feedback.",
            "Generate a query to update all user emails to lowercase.",
            "Delete all rows in the 'Logs' table older than 90 days.",
            "Explain the purpose of each JOIN type with examples."
        ]
    },
    "CLI": {
        "capabilities": [
            "Command execution",
            "Automation",
            "File and process management"
        ],
        "prompts": [
            "Write a CLI command to list all files in the current directory sorted by size.",
            "How do I check the memory usage of a process using the CLI?",
            "Create a Bash script to automate daily backups.",
            "Generate a command to find and delete all '.tmp' files in a folder.",
            "Explain the difference between 'grep' and 'awk' commands.",
            "How can I create a new user in Linux using CLI?",
            "Write a command to compress all '.csv' files into a single ZIP file.",
            "Generate a command to monitor changes in a log file in real-time.",
            "Explain how to install Python via CLI on a Mac.",
            "Create a script to automatically update all installed packages."
        ]
    },
    "FTP": {
        "capabilities": [
            "File upload/download",
            "Directory synchronization",
            "Data backup"
        ],
        "prompts": [
            "Write an FTP command to upload a file to the server.",
            "How do I download all files from a specific directory using FTP?",
            "Explain the difference between active and passive FTP modes.",
            "Generate a script to synchronize a local folder with an FTP server.",
            "Create a command to check the connection to an FTP server.",
            "What steps are required to secure an FTP server connection?",
            "Write a command to delete a file from the FTP server.",
            "Explain how to transfer files over FTP with encryption.",
            "How do I resume an interrupted file transfer using FTP?",
            "Generate a script to back up website files to an FTP server."
        ]
    },
    "API": {
        "capabilities": [
            "API consumption",
            "Data retrieval",
            "Integration and automation"
        ],
        "prompts": [
            "Write a Python script to fetch weather data from an API.",
            "How do I authenticate with an API using OAuth2?",
            "Create a REST API endpoint for a 'GET' request to fetch user details.",
            "Explain the difference between REST and GraphQL APIs.",
            "Generate an API request to update user information in a database.",
            "What is the purpose of API rate limiting?",
            "Create an API call to retrieve data in JSON format.",
            "Write a function to handle API errors gracefully.",
            "Explain how to secure an API with API keys.",
            "Create a Python function to fetch data from a public API and save it to a CSV."
        ]
    },
    "JSON": {
        "capabilities": [
            "Parsing and manipulation",
            "Data transformation",
            "Configuration management"
        ],
        "prompts": [
            "Extract the value of 'name' from this JSON object.",
            "Convert this JSON data into a readable table.",
            "Write a Python script to merge two JSON files.",
            "How can I validate if this JSON is correctly formatted?",
            "Generate a JSON object to represent a library with books and authors.",
            "Explain how to parse JSON in JavaScript.",
            "Write a function to flatten nested JSON data.",
            "Create a JSON object for storing API configuration details.",
            "How can I convert JSON to XML programmatically?",
            "Generate a script to find and replace a value in a JSON file."
        ]
    },
    "Computer Vision": {
        "capabilities": [
            "Image recognition",
            "Object detection",
            "Facial recognition",
            "Image processing"
        ],
        "prompts": [
            "Identify all objects in this image and provide their labels and bounding boxes.",
            "Detect faces in an image and highlight them with rectangles.",
            "Enhance the resolution of a low-quality image using AI.",
            "Classify images into predefined categories.",
            "Segment an image into different regions based on color and texture.",
            "Create a script to count the number of cars in a traffic image.",
            "Recognize and extract text from images using OCR.",
            "Generate captions for images using a computer vision model.",
            "Explain how convolutional neural networks are used in image recognition.",
            "Convert handwritten notes into typed text using AI."
        ]
    },
    "OCR": {
        "capabilities": [
            "Text extraction from images",
            "Handwriting recognition",
            "Document scanning and digitization",
            "Multi-language text recognition"
        ],
        "prompts": [
            "Extract text from this scanned document image.",
            "Recognize and digitize handwritten notes into editable text.",
            "Create a Python script to extract text from images using Tesseract OCR.",
            "Explain the process of training a custom OCR model.",
            "Convert text in images into a searchable PDF format.",
            "Recognize and extract multi-language text from an image.",
            "Explain the challenges of OCR for low-quality or distorted images.",
            "Highlight all instances of specific words in a scanned document image.",
            "Convert old printed books into digital text using OCR.",
            "Extract and tabulate numerical data from scanned receipts."
        ]
    },
    "Python Libraries": {
        "capabilities": [
            "Data manipulation",
            "Visualization",
            "Machine learning",
            "Web scraping"
        ],
        "prompts": [
            "Explain how to use pandas for data manipulation and analysis.",
            "Generate a matplotlib plot for visualizing sales trends over time.",
            "Create a script to train a machine learning model using scikit-learn.",
            "How can I use Beautiful Soup to scrape data from a website?",
            "Explain the difference between NumPy arrays and Python lists.",
            "Create an interactive dashboard using Streamlit.",
            "Generate a script to process large datasets using Dask.",
            "Explain the usage of TensorFlow for deep learning applications.",
            "Write a script to automate web interactions using Selenium.",
            "How can I use OpenCV for real-time video processing?"
        ]
    }
}

# Streamlit app
st.title("AI Capabilities for Various Data Formats")
st.sidebar.title("Select a Data Format")
format_choice = st.sidebar.selectbox("Data Format", list(data_formats.keys()))

if format_choice:
    st.header(format_choice)
    
    st.subheader("Capabilities")
    st.write("\n".join(f"- {cap}" for cap in data_formats[format_choice]["capabilities"]))

    st.subheader("Example Prompts")
    for prompt in data_formats[format_choice]["prompts"]:
        st.write(f"- {prompt}")
