import streamlit as st
import streamlit_survey as ss
import json

# Function to render home/website questionnaire
def render_home_website_questionnaire(edit_mode=False):
    if edit_mode:
        st.write("## Edit Home/Website Questionnaire")
    else:
        st.write("## Home/Website Questionnaire")
    
    # Create a survey instance for Home/Website Questionnaire
    website_survey = ss.StreamlitSurvey("Home/Website Questionnaire")

    # General Information
    st.subheader("General Information")
    website_survey.text_input("Client's Name:", id="client_name")
    website_survey.text_input("Company Name:", id="company_name")
    website_survey.text_input("Contact Email:", id="contact_email")

    # Project Overview
    st.subheader("Project Overview")
    website_survey.text_area("Briefly describe your project:", id="project_description")
    website_survey.radio("What is the primary goal of your website/app/funnel?", options=["Generate leads", "Increase sales", "Provide information", "Other"], id="project_goal")

    # Target Audience
    st.subheader("Target Audience")
    website_survey.text_area("Describe your target audience:", id="target_audience")
    website_survey.text_input("Do you have any specific demographics in mind?", id="demographics")

    # Design Preferences
    st.subheader("Design Preferences")
    website_survey.text_area("Do you have any design preferences or inspirations? (Include links if possible)", id="design_preferences")
    website_survey.selectbox("Which platform are you targeting?", options=["Web", "iOS", "Android", "Cross-platform"], id="platform_target")
    website_survey.multiselect("Which design elements do you like?", options=["Minimalistic", "Modern", "Traditional", "Bold", "Other"], id="design_elements")

    # Functionality Requirements
    st.subheader("Functionality Requirements")
    website_survey.multiselect("Which features do you need?", options=["User authentication", "Payment gateway", "Search functionality", "Social media integration", "Analytics", "Other"], id="features_needed")

    # Additional Questions
    st.subheader("Additional Questions")
    website_survey.radio("How soon do you need the project completed?", options=["Within 1 month", "1-3 months", "3-6 months", "6+ months"], id="project_timeline")
    website_survey.radio("What is your estimated budget for this project?", options=["Less than $1,000", "$1,000 - $5,000", "$5,000 - $10,000", "$10,000 - $20,000", "More than $20,000"], id="project_budget")
    website_survey.text_input("Do you have an existing website or app that needs to be redesigned or updated?", id="existing_website")
    website_survey.text_input("Are there any specific technical requirements or constraints we should be aware of?", id="technical_requirements")
    website_survey.text_area("Do you have any competitors' websites/apps you admire or wish to emulate?", id="competitor_sites")
    website_survey.multiselect("What languages should the website/app support?", options=["English", "Spanish", "French", "German", "Other"], id="language_support")
    website_survey.radio("How do you plan to market your website/app?", options=["Search engine optimization (SEO)", "Social media marketing", "Email marketing", "Paid advertising", "Other"], id="marketing_strategy")
    website_survey.text_input("Do you have any specific branding guidelines or assets we should follow?", id="branding_guidelines")
    website_survey.text_area("Are there any legal or regulatory considerations we should be aware of?", id="legal_regulatory")
    website_survey.text_area("Is there any additional information you would like to provide?", id="additional_info")

    # Add submit button for home/website questionnaire
    if not edit_mode:
        if st.button("Submit - Home/Website Questionnaire"):
            # Check if required fields are filled
            if website_survey.data.get("client_name") and website_survey.data.get("project_description"):
                st.success("Home/Website Questionnaire Submitted!")
                # Save survey data to JSON file
                with open("website_survey_data.json", "w") as f:
                    json.dump(website_survey.data, f)
            else:
                st.error("Please fill in the required fields (Client's Name, Project Description)")
    else:
        if st.button("Update - Home/Website Questionnaire"):
            st.success("Home/Website Questionnaire Updated!")
            # Update survey data in JSON file
            with open("website_survey_data.json", "w") as f:
                json.dump(website_survey.data, f)

# Function to render marketing strategy questionnaire
def render_marketing_strategy_questionnaire(edit_mode=False):
    if edit_mode:
        st.write("## Edit Marketing Strategy Questionnaire")
    else:
        st.write("## Marketing Strategy Questionnaire")

    # Create a survey instance for Marketing Strategy Questionnaire
    marketing_survey = ss.StreamlitSurvey("Marketing Strategy Questionnaire")

    # Marketing Goals
    st.subheader("Marketing Goals")
    marketing_survey.multiselect("What are your marketing goals?", options=["Increase brand awareness", "Drive website traffic", "Generate leads", "Increase sales", "Other"], id="marketing_goals")
    marketing_survey.slider("On a scale of 1-10, how important is digital marketing to your business?", min_value=1, max_value=10, step=1, id="digital_marketing_importance")

    # Target Audience
    st.subheader("Target Audience")
    marketing_survey.text_area("Describe your target audience:", id="target_audience_marketing")
    marketing_survey.text_input("Do you have any specific demographics in mind?", id="demographics_marketing")

    # Channels and Strategies
    st.subheader("Channels and Strategies")
    marketing_survey.multiselect("Which marketing channels do you currently use?", options=["Social media", "Email marketing", "Content marketing", "Paid advertising", "SEO", "Other"], id="current_marketing_channels")
    marketing_survey.multiselect("Which new channels/strategies are you considering?", options=["Influencer marketing", "Video marketing", "Podcast advertising", "Community building", "Other"], id="new_marketing_channels")

    # Budget and Timeline
    st.subheader("Budget and Timeline")
    marketing_survey.text_input("What is your marketing budget for the next quarter?", id="marketing_budget")
    marketing_survey.radio("How soon do you plan to implement your marketing strategy?", options=["Within 1 month", "1-3 months", "3-6 months", "6+ months"], id="marketing_timeline")

    # Add submit button for marketing strategy questionnaire
    if not edit_mode:
        if st.button("Submit - Marketing Strategy Questionnaire"):
            # Check if required fields are filled
            if marketing_survey.data.get("marketing_goals"):
                st.success("Marketing Strategy Questionnaire Submitted!")
                # Save survey data to JSON file
                with open("marketing_survey_data.json", "w") as f:
                    json.dump(marketing_survey.data, f)
            else:
                st.error("Please select at least one marketing goal")
    else:
        if st.button("Update - Marketing Strategy Questionnaire"):
            st.success("Marketing Strategy Questionnaire Updated!")
            # Update survey data in JSON file
            with open("marketing_survey_data.json", "w") as f:
                json.dump(marketing_survey.data, f)

# Function to render customer satisfaction survey
def render_customer_satisfaction_survey(edit_mode=False):
    if edit_mode:
        st.write("## Edit Customer Satisfaction Survey")
    else:
        st.write("## Customer Satisfaction Survey")

    # Create a survey instance for Customer Satisfaction Survey
    customer_survey = ss.StreamlitSurvey("Customer Satisfaction Survey")

    # Service Experience
    st.subheader("Service Experience")
    customer_survey.slider("On a scale of 1-10, how satisfied are you with our product/service?", min_value=1, max_value=10, step=1, id="satisfaction_rating")
    customer_survey.text_area("Please share any comments or suggestions for improvement:", id="customer_feedback")

    # Add submit button for customer satisfaction survey
    if not edit_mode:
        if st.button("Submit - Customer Satisfaction Survey"):
            # Check if required fields are filled
            if customer_survey.data.get("satisfaction_rating"):
                st.success("Customer Satisfaction Survey Submitted!")
                # Save survey data to JSON file
                with open("customer_survey_data.json", "w") as f:
                    json.dump(customer_survey.data, f)
            else:
                st.error("Please rate your satisfaction")
    else:
        if st.button("Update - Customer Satisfaction Survey"):
            st.success("Customer Satisfaction Survey Updated!")
            # Update survey data in JSON file
            with open("customer_survey_data.json", "w") as f:
                json.dump(customer_survey.data, f)

# Function to render employee feedback form
def render_employee_feedback_form(edit_mode=False):
    if edit_mode:
        st.write("## Edit Employee Feedback Form")
    else:
        st.write("## Employee Feedback Form")

    # Create a survey instance for Employee Feedback Form
    employee_survey = ss.StreamlitSurvey("Employee Feedback Form")

    # Feedback Questions
    st.subheader("Feedback Questions")
    employee_survey.slider("On a scale of 1-10, how satisfied are you with your current role?", min_value=1, max_value=10, step=1, id="job_satisfaction")
    employee_survey.text_area("Please share any comments or suggestions for improvement:", id="employee_feedback")

    # Add submit button for employee feedback form
    if not edit_mode:
        if st.button("Submit - Employee Feedback Form"):
            # Check if required fields are filled
            if employee_survey.data.get("job_satisfaction"):
                st.success("Employee Feedback Form Submitted!")
                # Save survey data to JSON file
                with open("employee_survey_data.json", "w") as f:
                    json.dump(employee_survey.data, f)
            else:
                st.error("Please rate your job satisfaction")
    else:
        if st.button("Update - Employee Feedback Form"):
            st.success("Employee Feedback Form Updated!")
            # Update survey data in JSON file
            with open("employee_survey_data.json", "w") as f:
                json.dump(employee_survey.data, f)

# Function to render videography questionnaire
def render_videography_questionnaire(edit_mode=False):
    if edit_mode:
        st.write("## Edit Videography Questionnaire")
    else:
        st.write("## Videography Questionnaire")

    # Create a survey instance for Videography Questionnaire
    videography_survey = ss.StreamlitSurvey("Videography Questionnaire")

    # Project Details
    st.subheader("Project Details")
    videography_survey.text_area("Briefly describe your project or video needs:", id="project_description_video")
    videography_survey.radio("What is your deadline for this project?", options=["Within 1 week", "1-2 weeks", "2-4 weeks", "More than 1 month"], id="project_timeline_video")
    videography_survey.radio("What is your estimated budget for this project?", options=["Less than $500", "$500 - $1,000", "$1,000 - $2,000", "$2,000 - $5,000", "More than $5,000"], id="project_budget_video")
    videography_survey.file_uploader("Upload any reference images or files:", type=["png", "jpg", "jpeg", "pdf"], id="reference_files_video")

    # Add submit button for videography questionnaire
    if not edit_mode:
        if st.button("Submit - Videography Questionnaire"):
            # Check if required fields are filled
            if videography_survey.data.get("project_description_video"):
                st.success("Videography Questionnaire Submitted!")
                # Save survey data to JSON file
                with open("videography_survey_data.json", "w") as f:
                    json.dump(videography_survey.data, f)
            else:
                st.error("Please provide a project description")
    else:
        if st.button("Update - Videography Questionnaire"):
            st.success("Videography Questionnaire Updated!")
            # Update survey data in JSON file
            with open("videography_survey_data.json", "w") as f:
                json.dump(videography_survey.data, f)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ("Home/Website Questionnaire", "Marketing Strategy Questionnaire", "Customer Satisfaction Survey", "Employee Feedback Form", "Videography Questionnaire"))

# Render selected page
if page == "Home/Website Questionnaire":
    render_home_website_questionnaire()
elif page == "Marketing Strategy Questionnaire":
    render_marketing_strategy_questionnaire()
elif page == "Customer Satisfaction Survey":
    render_customer_satisfaction_survey()
elif page == "Employee Feedback Form":
    render_employee_feedback_form()
elif page == "Videography Questionnaire":
    render_videography_questionnaire()

