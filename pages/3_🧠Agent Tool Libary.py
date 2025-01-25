import streamlit as st

# Define Categories and Tools
categories_with_tools = {
    "Messaging and Communication": [
        {"name": "Slack", "description": "Collaborative messaging platform for teams."},
        {"name": "Discord", "description": "Community communication via voice, video, and text."},
        {"name": "Gmail", "description": "Google's email management system with automation."},
        {"name": "Telegram", "description": "Secure messaging and bot support."},
        {"name": "Twilio", "description": "SMS, voice, and messaging workflows."},
        {"name": "WhatsApp", "description": "WhatsApp Business API for automated messaging."},
        {"name": "Microsoft Teams", "description": "Enterprise team collaboration."},
        {"name": "Zoom", "description": "Video conferencing and webinar management."},
        {"name": "Intercom", "description": "Customer messaging platform for sales and support."},
        {"name": "Google Chat", "description": "Google Workspace messaging for teams."}
    ],
    "Database Management": [
        {"name": "MySQL", "description": "Relational database for structured queries."},
        {"name": "PostgreSQL", "description": "Powerful, open-source relational database."},
        {"name": "MongoDB", "description": "NoSQL database for modern applications."},
        {"name": "Airtable", "description": "Database-spreadsheet hybrid for collaboration."},
        {"name": "OracleDB", "description": "Robust, enterprise-grade database."},
        {"name": "SQLite", "description": "Lightweight, file-based relational database."},
        {"name": "Redis", "description": "In-memory database for caching and real-time data."},
        {"name": "Cassandra", "description": "Distributed NoSQL database for scalability."},
        {"name": "Neo4j", "description": "Graph database for relationship modeling."},
        {"name": "DynamoDB", "description": "Serverless database from AWS."}
    ],
    "Cloud Storage": [
        {"name": "Google Drive", "description": "Cloud file storage with collaboration tools."},
        {"name": "Dropbox", "description": "File hosting for personal and team use."},
        {"name": "OneDrive", "description": "Microsoft's cloud storage solution."},
        {"name": "Amazon S3", "description": "Highly scalable object storage by AWS."},
        {"name": "Box", "description": "Enterprise-level content management."},
        {"name": "Backblaze B2", "description": "Affordable cloud backup and storage."},
        {"name": "pCloud", "description": "Secure cloud storage with encryption."},
        {"name": "Wasabi", "description": "Fast, low-cost cloud storage solution."},
        {"name": "iCloud Drive", "description": "Apple's cloud storage for personal files."},
        {"name": "Mega", "description": "Secure and private cloud storage platform."}
    ],
    "AI and Machine Learning": [
        {"name": "OpenAI", "description": "Generative AI for text and image workflows."},
        {"name": "Hugging Face", "description": "Natural language processing tools and APIs."},
        {"name": "Pinecone", "description": "Vector database for AI applications."},
        {"name": "IBM Watson", "description": "AI-powered analytics and automation."},
        {"name": "LangChain", "description": "Framework for LLM-based workflows."},
        {"name": "Google Vertex AI", "description": "AI platform for deploying ML models."},
        {"name": "Clarifai", "description": "AI tools for image and video analysis."},
        {"name": "Replicate", "description": "Run machine learning models in the cloud."},
        {"name": "Cohere", "description": "Large language models for NLP tasks."},
        {"name": "Anthropic Claude", "description": "AI assistant for enterprise workflows."}
    ],
    "E-commerce and Payments": [
        {"name": "Shopify", "description": "E-commerce platform for online stores."},
        {"name": "WooCommerce", "description": "WordPress plugin for e-commerce."},
        {"name": "Magento", "description": "Open-source e-commerce system."},
        {"name": "BigCommerce", "description": "Scalable e-commerce for businesses."},
        {"name": "Stripe", "description": "Online payment processing."},
        {"name": "PayPal", "description": "Secure payment gateway services."},
        {"name": "Square", "description": "Payment systems for in-person and online sales."},
        {"name": "Klarna", "description": "Buy now, pay later solutions for e-commerce."},
        {"name": "Amazon Pay", "description": "Simple checkout for Amazon customers."},
        {"name": "Adyen", "description": "Global payment platform for large enterprises."}
    ],
    "Marketing and Analytics": [
        {"name": "HubSpot", "description": "CRM for inbound marketing."},
        {"name": "Google Analytics", "description": "Website performance and traffic insights."},
        {"name": "Mailchimp", "description": "Email marketing and automation."},
        {"name": "Marketo", "description": "Enterprise-grade marketing automation."},
        {"name": "Zoho CRM", "description": "Customer relationship management solution."},
        {"name": "Hotjar", "description": "User behavior analytics for websites."},
        {"name": "Ahrefs", "description": "SEO tools and competitive analysis."},
        {"name": "SEMrush", "description": "Marketing insights and analytics."},
        {"name": "Google Ads", "description": "Pay-per-click advertising management."},
        {"name": "ActiveCampaign", "description": "Email marketing and customer journeys."}
    ],
    "Project Management and Collaboration": [
        {"name": "Asana", "description": "Task and project management platform."},
        {"name": "Jira", "description": "Issue tracking for software teams."},
        {"name": "Trello", "description": "Kanban boards for project workflows."},
        {"name": "ClickUp", "description": "All-in-one productivity app."},
        {"name": "Monday.com", "description": "Work operating system for teams."},
        {"name": "Basecamp", "description": "Team project management and collaboration."},
        {"name": "Notion", "description": "Workspace for notes, projects, and databases."},
        {"name": "Wrike", "description": "Advanced work management platform."},
        {"name": "Microsoft Planner", "description": "Task management for Office 365 users."},
        {"name": "Smartsheet", "description": "Spreadsheet-like project management tool."}
    ]
}

# Sidebar Navigation
st.sidebar.title("n8n Tools Directory")
selected_category = st.sidebar.selectbox("Select a Category", list(categories_with_tools.keys()))

# Display Selected Category Tools
st.title(f"Tools in '{selected_category}' Category")
tabs = st.tabs([tool["name"] for tool in categories_with_tools[selected_category]])

for i, tool in enumerate(categories_with_tools[selected_category]):
    with tabs[i]:
        st.subheader(tool["name"])
        st.write(tool["description"])
        st.button(f"Learn More about {tool['name']}")

st.sidebar.info("Explore 500+ tools and integrations powered by n8n.")
