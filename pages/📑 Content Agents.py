import streamlit as st
from langchain.llms import Ollama
import datetime



# Function to generate content using Ollama
def generate_content(title, content, options):
    llm = Ollama(model="llama3.2")
    generated_content = f"{title}:\n{llm.predict(content)}\nOptions: {', '.join(options)}"
    return generated_content

def generate_sms_campaign(campaign_type, campaign_name, sender_name, message_content, recipients, send_date, send_time):
    options = ["Promotional Campaign", "Transactional Campaign", "Reminder Campaign", "Event Invitation Campaign", "Feedback Campaign", "Survey Campaign"]
    content = f"Campaign Type: {campaign_type}\nCampaign Name: {campaign_name}\nSender Name: {sender_name}\nMessage Content: {message_content}\nRecipients: {recipients}\nSend Date: {send_date}\nSend Time: {send_time}"
    return generate_content("SMS Campaign", content, options)

# Page: Real Estate Letter Generation
def generate_real_estate_letter(letter_type, recipient_name, property_address, seller_name, buyer_name, purchase_price, closing_date, earnest_money_deposit, wholesale_buyer_name=None, wholesale_purchase_price=None, wholesale_closing_date=None, assignment_fee=None, lender_name=None, outstanding_loan_amount=None, proposed_solution=None):
    options = ["Purchase Agreement", "Sales Contract", "Property Offer Letter", "Property Acceptance Letter", "Property Rejection Letter", "Lease Agreement", "Rental Application", "Notice to Vacate", "Property Appraisal Letter", "Property Inspection Report", "Property Valuation Letter", "Property Transfer Letter", "Property Closing Letter", "Wholesale Agreement", "Foreclosure Avoidance Letter"]
    content = f"Letter Type: {letter_type}\nRecipient Name: {recipient_name}\nProperty Address: {property_address}\nSeller's Name: {seller_name}\nBuyer's Name: {buyer_name}\nPurchase Price: {purchase_price}\nClosing Date: {closing_date}\nEarnest Money Deposit: {earnest_money_deposit}"
    if letter_type == "Wholesale Agreement":
        content += f"\nWholesale Buyer's Name: {wholesale_buyer_name}\nWholesale Purchase Price: {wholesale_purchase_price}\nWholesale Closing Date: {wholesale_closing_date}\nAssignment Fee: {assignment_fee}"
    elif letter_type == "Foreclosure Avoidance Letter":
        content += f"\nLender's Name: {lender_name}\nOutstanding Loan Amount: {outstanding_loan_amount}\nProposed Solution: {proposed_solution}"
    return generate_content("Real Estate Letter", content, options)

# Page: Credit Letter Generation
def generate_credit_letter(credit_letter_type, recipient_name, company_name, credit_limit, account_number, current_balance, past_due_amount, due_date, late_fee):
    options = ["Credit Limit Increase Request", "Past Due Reminder", "Payment Confirmation", "Account Closure Notification", "Late Payment Forgiveness", "Credit Score Update", "Credit Line Reduction Notice", "Account Termination Letter", "Payment Plan Agreement", "Credit Report Dispute"]
    content = f"Credit Letter Type: {credit_letter_type}\nRecipient Name: {recipient_name}\nCompany Name: {company_name}\nCredit Limit: {credit_limit}\nAccount Number: {account_number}\nCurrent Balance: {current_balance}\nPast Due Amount: {past_due_amount}\nDue Date: {due_date}\nLate Fee: {late_fee}"
    return generate_content("Credit Letter", content, options)

# Page: Recipe Generation
def generate_recipe(ingredients, cuisine_type, diet_type, meal_type):
    options = ["Italian", "Mexican", "Indian", "Chinese", "Mediterranean", "Japanese", "French", "Thai", "American", "Greek"]
    content = f"Ingredients: {ingredients}\nCuisine Type: {cuisine_type}\nDiet Type: {', '.join(diet_type)}\nMeal Type: {', '.join(meal_type)}"
    return generate_content("Recipe", content, options)

# Page: Business Contracts Generation
def generate_contract(contract_type, company_name, counterparty_name, contract_date, job_title=None, salary=None, start_date=None, end_date=None, responsibilities=None, benefits=None, scope=None, term=None, disclosure_party=None, receiving_party=None, services_rendered=None, service_provider=None, service_recipient=None, payment_terms=None):
    options = ["Employment Agreement", "Non-Disclosure Agreement (NDA)", "Service Agreement", "Partnership Agreement", "Sales Agreement", "Consulting Agreement", "Lease Agreement", "Freelance Contract", "Investment Agreement", "Confidentiality Agreement"]
    content = f"Contract Type: {contract_type}\nCompany Name: {company_name}\nCounterparty Name: {counterparty_name}\nContract Date: {contract_date}"
    if contract_type == "Employment Agreement":
        content += f"\nJob Title: {job_title}\nSalary: {salary}\nStart Date: {start_date}\nEnd Date: {end_date}\nResponsibilities: {responsibilities}\nBenefits: {benefits}"
    elif contract_type == "Non-Disclosure Agreement (NDA)":
        content += f"\nScope of Confidentiality: {scope}\nTerm: {term}\nDisclosure Party: {disclosure_party}\nReceiving Party: {receiving_party}"
    elif contract_type == "Service Agreement":
        content += f"\nServices Rendered: {services_rendered}\nService Provider: {service_provider}\nService Recipient: {service_recipient}\nPayment Terms: {payment_terms}"
    return generate_content("Contract", content, options)

# Page: Blog Generation
def generate_blog_post(blog_title, blog_author, blog_date, blog_category, blog_content):
    options = ["Technology", "Health", "Travel", "Food", "Fashion", "Finance", "Business", "Lifestyle", "Fitness", "Education"]
    content = f"Blog Title: {blog_title}\nAuthor: {blog_author}\nPublish Date: {blog_date}\nCategory: {blog_category}\nContent: {blog_content}"
    return generate_content("Blog Post", content, options)

# Page: Event Details Generator
def generate_event_details(event_title, event_description, event_date, event_time, event_location, event_type, event_topics, speaker_name, speaker_bio, speaker_photo):
    options = ["Conference", "Seminar", "Workshop", "Webinar", "Networking Event", "Trade Show", "Panel Discussion", "Meetup", "Exhibition", "Hackathon"]
    content = f"Event Title: {event_title}\nEvent Description: {event_description}\nEvent Date: {event_date}\nEvent Time: {event_time}\nEvent Location: {event_location}\nEvent Type: {event_type}\nEvent Topics: {', '.join(event_topics)}"
    speaker_content = f"Speaker Name: {speaker_name}\nSpeaker Bio: {speaker_bio}\nSpeaker Photo: {speaker_photo}"
    return generate_content("Event Details", content + "\n\n" + speaker_content, options)

# Page: Course and Quiz Generator
def generate_course_and_quiz(course_title, course_description, course_duration, course_difficulty, course_topics, quiz_title, quiz_description, quiz_questions, quiz_difficulty, quiz_topics):
    options = ["Course", "Quiz"]
    content = f"Course Title: {course_title}\nCourse Description: {course_description}\nCourse Duration: {course_duration}\nCourse Difficulty: {course_difficulty}\nCourse Topics: {', '.join(course_topics)}"
    quiz_content = f"Quiz Title: {quiz_title}\nQuiz Description: {quiz_description}\nNumber of Questions: {quiz_questions}\nQuiz Difficulty: {quiz_difficulty}\nQuiz Topics: {', '.join(quiz_topics)}"
    return generate_content("Course and Quiz", content + "\n\n" + quiz_content, options)

# Page: Sales Funnel Copy Generator
def generate_sales_funnel_copy(page_type, product_name, target_audience, pain_points, benefits, call_to_action):
    options = ["Landing Page", "Product Page", "Upsell Page", "Downsell Page"]
    content = f"Page Type: {page_type}\nProduct Name: {product_name}\nTarget Audience: {target_audience}\nPain Points: {pain_points}\nBenefits: {benefits}\nCall to Action: {call_to_action}"
    return generate_content("Sales Funnel Copy", content, options)

# Page: RFP Generator
def generate_rfp(recipient_name, project_name, project_description, project_requirements, deadline):
    options = []
    content = f"Recipient Name: {recipient_name}\nProject Name: {project_name}\nProject Description: {project_description}\nProject Requirements: {project_requirements}\nDeadline: {deadline}"
    return generate_content("RFP", content, options)

# Page: Google Listing Generator
def generate_google_listing(name, address, phone, website, categories):
    options = ["Restaurant", "Hotel", "Cafe", "Bar", "Store", "Service", "Attraction"]
    content = f"Name: {name}\nAddress: {address}\nPhone: {phone}\nWebsite: {website}\nCategories: {', '.join(categories)}"
    return generate_content("Google Listing", content, options)

# Define the Streamlit app title and navigation
st.set_page_config(page_title="Content Generator", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

# Define the sidebar navigation
page = st.sidebar.selectbox("Choose a page", ["Generate Post", "Grant Application", "Website Sections", "Marketing Plan", "Lesson Plan", "Business Plan", "Real Estate", "E-commerce Listing", "Email Sequences","SMS Campaign", "Real Estate Letter", "Credit Letter", "Recipe", "Business Contract", "Blog", "Event Details", "Course and Quiz", "Sales Funnel Copy", "RFP", "Google Listing", "About", "Settings"])

# Page: Generate Post
if page == "Generate Post":
    st.title("Social Media Post Generator")
    st.write("Craft engaging social media posts for multiple platforms with ease.")

    # Define the form fields for social media post generation
    post_title = st.text_input("Post Title", "")
    post_content = st.text_area("Post Content", "")
    hashtags = st.text_input("Hashtags (separated by commas)", "")
    platforms = st.multiselect("Select Platforms", ["Facebook", "Twitter", "Instagram", "LinkedIn", "Pinterest", "Snapchat", "TikTok", "YouTube", "Reddit", "Tumblr"], default=["Facebook", "Twitter", "Instagram"])

    # Button to generate social media posts
    if st.button("Generate Social Media Posts"):
        # Generate social media posts for selected platforms
        for platform in platforms:
            social_media_post = generate_content(f"{platform.capitalize()} Post", post_content, hashtags.split(", "))
            st.markdown(social_media_post)

            # Add a separator between posts for better readability
            st.markdown("---")

elif page == "RFP":
    st.title("RFP Generator")
    st.write("Generate customized Request for Proposals (RFPs).")

    # Input fields
    recipient_name = st.text_input("Recipient Name")
    project_name = st.text_input("Project Name")
    project_description = st.text_area("Project Description")
    project_requirements = st.text_area("Project Requirements")
    deadline = st.date_input("Deadline", min_value=datetime.date.today())

    # Button to generate RFP
    if st.button("Generate RFP"):
        rfp_content = generate_rfp(recipient_name, project_name, project_description, project_requirements, deadline)
        st.text_area("Generated RFP", value=rfp_content, height=300)

# Page: Grant Application
elif page == "Grant Application":
    st.title("Grant Application Generator")
    st.write("Generate grant applications tailored to your needs.")

    num_grants = st.number_input("Number of Grants", min_value=1, value=1)

    grant_data = []
    for i in range(num_grants):
        st.write(f"Grant {i + 1}")
        grant_name = st.text_input(f"Grant Name {i + 1}", "")
        grant_type = st.selectbox(f"Grant Type {i + 1}", ["Research Grant", "Education Grant", "Nonprofit Grant", "Startup Grant", "Arts Grant", "Healthcare Grant", "Environmental Grant", "Community Grant", "Technology Grant", "Travel Grant"])
        organization = st.text_input(f"Organization {i + 1}", "")
        purpose = st.text_area(f"Purpose {i + 1}", "")
        amount = st.number_input(f"Amount {i + 1}", min_value=0.0, step=0.01, format="%.2f")

        grant_data.append((grant_name, grant_type, organization, purpose, amount))

    deadline = st.date_input("Application Deadline", min_value=datetime.date.today())

    additional_information = st.text_area("Additional Information", "Please provide any additional information here.")

    # Button to generate grant application
    if st.button("Generate Grant Application"):
        if not any(grant_data):
            st.error("Please fill in at least one grant.")
        else:
            for i, (grant_name, grant_type, organization, purpose, amount) in enumerate(grant_data):
                if not grant_name:
                    st.warning(f"Grant Name {i + 1} is required.")
                else:
                    grant_application = generate_content(f"Grant Application: {grant_name}", f"Grant Type: {grant_type}\nOrganization: {organization}\nPurpose: {purpose}\nAmount: ${amount}\nDeadline: {deadline.strftime('%Y-%m-%d')}\nAdditional Information: {additional_information}", [])
                    st.markdown(grant_application)
                    st.markdown("---")


elif page == "SMS Campaign":
    st.title("SMS Campaign Generation")
    st.write("Create customized SMS campaigns.")

    campaign_options = [
        "Promotional Campaign",
        "Transactional Campaign",
        "Reminder Campaign",
        "Event Invitation Campaign",
        "Feedback Campaign",
        "Survey Campaign"
    ]

    campaign_type = st.selectbox("Campaign Type", campaign_options)
    campaign_name = st.text_input("Campaign Name", "")
    sender_name = st.text_input("Sender Name", "")
    message_content = st.text_area("Message Content", "")
    recipients = st.text_area("Recipient Numbers (one per line)", "")
    send_date = st.date_input("Send Date", min_value=datetime.date.today())
    send_time = st.time_input("Send Time", value=datetime.time(9, 0))

    # Button to generate SMS campaign
    if st.button("Generate SMS Campaign"):
        # Generate SMS campaign content based on the selected campaign type
        if campaign_type == "Promotional Campaign":
            sms_campaign_content = generate_promotional_sms(campaign_name, sender_name, message_content, recipients.split("\n"), send_date, send_time)
        elif campaign_type == "Transactional Campaign":
            sms_campaign_content = generate_transactional_sms(campaign_name, sender_name, message_content, recipients.split("\n"), send_date, send_time)
        elif campaign_type == "Reminder Campaign":
            sms_campaign_content = generate_reminder_sms(campaign_name, sender_name, message_content, recipients.split("\n"), send_date, send_time)
        elif campaign_type == "Event Invitation Campaign":
            sms_campaign_content = generate_event_invitation_sms(campaign_name, sender_name, message_content, recipients.split("\n"), send_date, send_time)
        elif campaign_type == "Feedback Campaign":
            sms_campaign_content = generate_feedback_sms(campaign_name, sender_name, message_content, recipients.split("\n"), send_date, send_time)
        elif campaign_type == "Survey Campaign":
            sms_campaign_content = generate_survey_sms(campaign_name, sender_name, message_content, recipients.split("\n"), send_date, send_time)
        else:
            sms_campaign_content = "No campaign content generated. Please select a valid campaign type."

        st.text(sms_campaign_content)

elif page == "Real Estate Letter":
    st.title("Real Estate Letter Generation")
    st.write("Generate customized real estate letters.")

    letter_types = [
        "Purchase Agreement",
        "Sales Contract",
        "Property Offer Letter",
        "Property Acceptance Letter",
        "Property Rejection Letter",
        "Lease Agreement",
        "Rental Application",
        "Notice to Vacate",
        "Property Appraisal Letter",
        "Property Inspection Report",
        "Property Valuation Letter",
        "Property Transfer Letter",
        "Property Closing Letter",
        "Wholesale Agreement",
        "Foreclosure Avoidance Letter"
    ]

    letter_type = st.selectbox("Letter Type", letter_types)

    recipient_name = st.text_input("Recipient Name", "")
    property_address = st.text_input("Property Address", "")
    seller_name = st.text_input("Seller's Name", "")
    buyer_name = st.text_input("Buyer's Name", "")
    purchase_price = st.number_input("Purchase Price ($)", value=0, step=1000)
    closing_date = st.date_input("Closing Date", min_value=datetime.date.today())
    earnest_money_deposit = st.number_input("Earnest Money Deposit ($)", value=0, step=1000)

    # Additional fields for Wholesale Agreement
    if letter_type == "Wholesale Agreement":
        wholesale_buyer_name = st.text_input("Wholesale Buyer's Name", "")
        wholesale_purchase_price = st.number_input("Wholesale Purchase Price ($)", value=0, step=1000)
        wholesale_closing_date = st.date_input("Wholesale Closing Date", min_value=datetime.date.today())
        assignment_fee = st.number_input("Assignment Fee ($)", value=0, step=1000)

    # Additional fields for Foreclosure Avoidance Letter
    if letter_type == "Foreclosure Avoidance Letter":
        lender_name = st.text_input("Lender's Name", "")
        outstanding_loan_amount = st.number_input("Outstanding Loan Amount ($)", value=0, step=1000)
        proposed_solution = st.text_area("Proposed Solution", "")

    # Button to generate real estate letter
    if st.button("Generate Real Estate Letter"):
        # Generate real estate letter content based on the selected type
        if letter_type == "Wholesale Agreement":
            real_estate_letter_content = generate_wholesale_agreement(recipient_name, property_address, seller_name, buyer_name, purchase_price, closing_date, earnest_money_deposit, wholesale_buyer_name, wholesale_purchase_price, wholesale_closing_date, assignment_fee)
        elif letter_type == "Foreclosure Avoidance Letter":
            real_estate_letter_content = generate_foreclosure_avoidance_letter(recipient_name, property_address, lender_name, outstanding_loan_amount, proposed_solution)
        else:
            real_estate_letter_content = generate_real_estate_letter(recipient_name, property_address, seller_name, buyer_name, purchase_price, closing_date, earnest_money_deposit)

        st.markdown(real_estate_letter_content)

        # Add a separator after the real estate letter for better readability
        st.markdown("---")
        

elif page == "Credit Letter":
    st.title("Credit Letter Generation")
    st.write("Generate customized credit letters.")

    credit_letter_type = st.selectbox("Credit Letter Type", ["Credit Limit Increase Request", "Past Due Reminder", "Payment Confirmation", "Account Closure Notification", "Late Payment Forgiveness", "Credit Score Update", "Credit Line Reduction Notice", "Account Termination Letter", "Payment Plan Agreement", "Credit Report Dispute"])

    recipient_name = st.text_input("Recipient Name", "")
    company_name = st.text_input("Company Name", "")
    credit_limit = st.number_input("Credit Limit ($)", value=0, step=1000)
    account_number = st.text_input("Account Number", "")
    current_balance = st.number_input("Current Balance ($)", value=0, step=100)
    past_due_amount = st.number_input("Past Due Amount ($)", value=0, step=100)
    due_date = st.date_input("Due Date", min_value=datetime.date.today())
    late_fee = st.number_input("Late Fee ($)", value=0, step=10)

    # Button to generate credit letter
    if st.button("Generate Credit Letter"):
        # Generate credit letter content based on the selected type
        credit_letter_content = generate_credit_letter(credit_letter_type, recipient_name, company_name, credit_limit, account_number, current_balance, past_due_amount, due_date, late_fee)
        st.markdown(credit_letter_content)

        # Add a separator after the credit letter for better readability
        st.markdown("---")


elif page == "Recipe":
    st.title("Recipe Generation")
    st.write("Generate customized recipes based on ingredients.")

    ingredients = st.text_area("Enter Ingredients (separated by commas)", "")
    cuisine_type = st.selectbox("Cuisine Type", ["Italian", "Mexican", "Indian", "Chinese", "Mediterranean", "Japanese", "French", "Thai", "American", "Greek"])
    diet_type = st.multiselect("Diet Type", ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Low-Carb", "Low-Fat", "Dairy-Free"])
    meal_type = st.multiselect("Meal Type", ["Breakfast", "Brunch", "Lunch", "Dinner", "Appetizer", "Main Course", "Side Dish", "Dessert", "Snack"])

    # Button to generate recipes
    if st.button("Generate Recipes"):
        # Generate recipes based on ingredients
        generated_recipes = generate_recipes(ingredients, cuisine_type, diet_type, meal_type)
        for recipe in generated_recipes:
            st.markdown(recipe)

        # Add a separator after the recipes for better readability
        st.markdown("---")
        

elif page == "Business Contract":
    st.title("Business Contracts Generation")
    st.write("Generate customized business contracts.")

    contract_type = st.selectbox("Contract Type", ["Employment Agreement", "Non-Disclosure Agreement (NDA)", "Service Agreement", "Partnership Agreement", "Sales Agreement", "Consulting Agreement", "Lease Agreement", "Freelance Contract", "Investment Agreement", "Confidentiality Agreement"])
    company_name = st.text_input("Company Name", "")
    counterparty_name = st.text_input("Counterparty Name", "")
    contract_date = st.date_input("Contract Date", min_value=datetime.date.today())

    # Define contract terms based on contract type
    if contract_type == "Employment Agreement":
        job_title = st.text_input("Job Title", "")
        salary = st.number_input("Salary ($)", value=0, step=1000)
        start_date = st.date_input("Start Date", min_value=datetime.date.today())
        end_date = st.date_input("End Date")
        responsibilities = st.text_area("Responsibilities", "")
        benefits = st.text_area("Benefits", "")
    elif contract_type == "Non-Disclosure Agreement (NDA)":
        scope = st.text_area("Scope of Confidentiality", "")
        term = st.text_input("Term (in years)", "")
        disclosure_party = st.text_input("Disclosure Party", "")
        receiving_party = st.text_input("Receiving Party", "")
    elif contract_type == "Service Agreement":
        services_rendered = st.text_area("Services Rendered", "")
        service_provider = st.text_input("Service Provider", "")
        service_recipient = st.text_input("Service Recipient", "")
        payment_terms = st.text_area("Payment Terms", "")
    # Add more contract types as needed...

    # Button to generate contract
    if st.button("Generate Contract"):
        # Generate contract content
        contract_content = generate_contract(contract_type, company_name, counterparty_name, contract_date, job_title, salary, start_date, end_date, responsibilities, benefits, scope, term, disclosure_party, receiving_party, services_rendered, service_provider, service_recipient, payment_terms)
        st.markdown(contract_content)

        # Add a separator after the contract for better readability
        st.markdown("---")
        

elif page == "Blog":
    st.title("Blog Generation")
    st.write("Create engaging blog posts for your website.")

    blog_title = st.text_input("Blog Title", "")
    blog_author = st.text_input("Author", "")
    blog_date = st.date_input("Publish Date", min_value=datetime.date.today())
    blog_category = st.selectbox("Category", ["Technology", "Health", "Travel", "Food", "Fashion", "Finance", "Business", "Lifestyle", "Fitness", "Education"])
    blog_content = st.text_area("Content", "")

    # Button to generate blog post
    if st.button("Blog"):
        # Generate blog content
        blog_post = generate_blog_post(blog_title, blog_author, blog_date, blog_category, blog_content)
        st.markdown(blog_post)

        # Add a separator after the blog post for better readability
        st.markdown("---")


elif page == "Event Details":
    st.title("Event Details Generator")
    st.write("Create event details for your upcoming events.")

    event_title = st.text_input("Event Title", "")
    event_description = st.text_area("Event Description", "")
    event_date = st.date_input("Event Date", min_value=datetime.date.today())
    event_time = st.time_input("Event Time")
    event_location = st.text_input("Event Location", "")
    event_type = st.selectbox("Event Type", ["Conference", "Seminar", "Workshop", "Webinar", "Networking Event", "Trade Show", "Panel Discussion", "Meetup", "Exhibition", "Hackathon"])
    event_topics = st.multiselect("Event Topics", ["Technology", "Business", "Health & Wellness", "Art & Culture", "Science", "Education", "Sports", "Entertainment", "Food & Drink", "Environment"])

    # Speaker details section
    st.subheader("Speaker Details")
    speaker_name = st.text_input("Speaker Name", "")
    speaker_bio = st.text_area("Speaker Bio", "")
    speaker_photo = st.file_uploader("Speaker Photo", type=["jpg", "jpeg", "png"])

    # Button to generate event details
    if st.button("Event Details"):
        # Generate event content
        event_content = generate_event(event_title, event_description, event_date, event_time, event_location, event_type, event_topics)
        st.markdown(event_content)

        # Generate speaker content
        speaker_content = generate_speaker(speaker_name, speaker_bio, speaker_photo)
        st.markdown(speaker_content)

        # Add a separator between event and speaker details for better readability
        st.markdown("---")


elif page == "Course and Quiz":
    st.title("Course and Quiz Generator")
    st.write("Create interactive courses and quizzes for your audience.")

    course_title = st.text_input("Course Title", "")
    course_description = st.text_area("Course Description", "")
    course_duration = st.number_input("Course Duration (hours)", min_value=0, value=1)
    course_difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
    course_topics = st.multiselect("Course Topics", ["Programming", "Data Science", "Machine Learning", "Web Development", "Finance", "Business", "Design", "Language Learning", "Marketing", "Personal Development"])

    # Quiz creation section
    st.subheader("Quiz Creation")
    st.write("Create quizzes to assess knowledge retention.")

    quiz_title = st.text_input("Quiz Title", "")
    quiz_description = st.text_area("Quiz Description", "")
    quiz_questions = st.number_input("Number of Questions", min_value=1, value=5)
    quiz_difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    quiz_topics = st.multiselect("Quiz Topics", ["Programming", "Data Science", "Machine Learning", "Web Development", "Finance", "Business", "Design", "Language Learning", "Marketing", "Personal Development"])

    # Button to generate course and quiz
    if st.button("Generate Course and Quiz"):
        # Generate course content
        course_content = generate_course(course_title, course_description, course_duration, course_difficulty, course_topics)
        st.markdown(course_content)

        # Generate quiz content
        quiz_content = generate_quiz(quiz_title, quiz_description, quiz_questions, quiz_difficulty, quiz_topics)
        st.markdown(quiz_content)

        # Add a separator between course and quiz for better readability
        st.markdown("---")
# Page: Product Page
elif page == "Product Page":
    st.title("Product Page Copy Generator")
    st.write("Generate copy for a product page to showcase features and benefits.")

    product_name = st.text_input("Product Name", "")
    target_audience = st.text_area("Target Audience", "")
    pain_points = st.text_area("Pain Points", "")
    benefits = st.text_area("Benefits", "")
    call_to_action = st.text_input("Call to Action", "")

    # Button to generate product page copy
    if st.button("Generate Product Page Copy"):
        product_page_copy = generate_copy("Product Page", product_name, target_audience, pain_points, benefits, call_to_action)
        st.text(product_page_copy)

# Page: Upsell Page
elif page == "Upsell Page":
    st.title("Upsell Page Copy Generator")
    st.write("Generate copy for an upsell page to encourage additional purchases.")

    product_name = st.text_input("Product Name", "")
    target_audience = st.text_area("Target Audience", "")
    pain_points = st.text_area("Pain Points", "")
    benefits = st.text_area("Benefits", "")
    call_to_action = st.text_input("Call to Action", "")

    # Button to generate upsell page copy
    if st.button("Generate Upsell Page Copy"):
        upsell_page_copy = generate_copy("Upsell Page", product_name, target_audience, pain_points, benefits, call_to_action)
        st.text(upsell_page_copy)

# Page: Downsell Page
elif page == "Downsell Page":
    st.title("Downsell Page Copy Generator")
    st.write("Generate copy for a downsell page to offer alternative options.")

    product_name = st.text_input("Product Name", "")
    target_audience = st.text_area("Target Audience", "")
    pain_points = st.text_area("Pain Points", "")
    benefits = st.text_area("Benefits", "")
    call_to_action = st.text_input("Call to Action", "")

    # Button to generate downsell page copy
    if st.button("Generate Downsell Page Copy"):
        downsell_page_copy = generate_copy("Downsell Page", product_name, target_audience, pain_points, benefits, call_to_action)
        st.text(downsell_page_copy)

# Page: Lesson Plan Generator
elif page == "Lesson Plan":
    st.title("Lesson Plan Generator")
    st.write("Create lesson plans tailored to your teaching needs.")

    num_lessons = st.number_input("Number of Lessons", min_value=1, value=1)

    lesson_data = []
    for i in range(num_lessons):
        st.write(f"Lesson {i + 1}")
        lesson_name = st.text_input(f"Lesson Name {i + 1}", "")
        subject = st.text_input(f"Subject {i + 1}", "")
        grade_level = st.selectbox(f"Grade Level {i + 1}", ["Kindergarten", "Elementary School", "Middle School", "High School"])
        objectives = st.text_area(f"Objectives {i + 1}", "")
        activities = st.text_area(f"Activities {i + 1}", "")
        materials = st.text_area(f"Materials {i + 1}", "")
        assessment = st.text_area(f"Assessment {i + 1}", "")

        lesson_data.append((lesson_name, subject, grade_level, objectives, activities, materials, assessment))

    duration = st.number_input("Duration per Lesson (minutes)", min_value=1, value=60)

    # Button to generate lesson plans
    if st.button("Generate Lesson Plans"):
        if not any(lesson_data):
            st.error("Please fill in at least one lesson.")
        else:
            for i, (lesson_name, subject, grade_level, objectives, activities, materials, assessment) in enumerate(lesson_data):
                if not lesson_name:
                    st.warning(f"Lesson Name {i + 1} is required.")
                else:
                    lesson_plan = generate_content(f"Lesson Plan: {lesson_name}", f"Subject: {subject}\nGrade Level: {grade_level}\nObjectives: {objectives}\nActivities: {activities}\nMaterials: {materials}\nAssessment: {assessment}\nDuration: {duration} minutes", [])
                    st.markdown(lesson_plan)
                    st.markdown("---")

# Page: Website Sections Generator
elif page == "Website Sections":
    st.title("Website Sections Generator")
    st.write("Create various sections for your website.")

    num_sections = st.number_input("Number of Sections", min_value=1, value=1)

    section_data = []
    for i in range(num_sections):
        st.header(f"Section {i + 1}")
        section_name = st.text_input(f"Section Name", f"Section {i + 1} Name")
        content_type = st.radio(f"Content Type", ["Text", "HTML", "Python Code"])
        
        default_content = {
            "Text": "Enter your text content here.",
            "HTML": "<p>This is HTML content.</p>",
            "Python Code": "print('This is Python code.')"
        }

        section_content = st.text_area("Section Content", default_content[content_type])

        section_type = st.selectbox("Section Type", ["Header", "Footer", "About Us", "Contact Us", "Services", "Portfolio", "Testimonials", "FAQ", "Blog", "Gallery"])

        section_data.append((section_name, section_content, section_type))

    # Button to generate website sections
    if st.button("Generate Website Sections"):
        for i, (section_name, section_content, section_type) in enumerate(section_data):
            if not section_name:
                st.warning(f"Section Name {i + 1} is required.")
            else:
                website_section = generate_content(f"Website Section: {section_name}", f"Section Type: {section_type}\nSection Content:\n{section_content}", [])
                st.markdown(website_section)
                st.markdown("---")


elif page == "Marketing Plan":
    st.title("Marketing Plan Generator")
    st.write("Create a customized marketing plan for your business.")

    num_strategies = st.number_input("Number of Marketing Strategies", min_value=1, value=1)

    marketing_data = []
    for i in range(num_strategies):
        st.write(f"Marketing Strategy {i + 1}")
        strategy_name = st.text_input(f"Strategy Name {i + 1}", "")
        target_audience = st.text_input(f"Target Audience {i + 1}", "")
        channels = st.multiselect(f"Marketing Channels {i + 1}", ["Social Media", "Email Marketing", "Content Marketing", "Search Engine Optimization (SEO)", "Pay-Per-Click (PPC) Advertising", "Influencer Marketing", "Events/Sponsorships", "Public Relations", "Direct Mail", "Guerrilla Marketing"], ["Social Media"])
        platforms = st.multiselect(f"Platforms {i + 1}", ["Facebook", "Instagram", "Twitter", "LinkedIn", "Pinterest", "YouTube", "TikTok", "Snapchat", "Reddit", "Tumblr", "Other"], ["Facebook"])
        budget = st.number_input(f"Budget (in USD) {i + 1}", min_value=0.0, step=100.0, format="%.2f")
        timeline = st.text_area(f"Timeline {i + 1}", "")
        success_metrics = st.text_area(f"Success Metrics {i + 1}", "")

        marketing_data.append((strategy_name, target_audience, channels, platforms, budget, timeline, success_metrics))

    # Button to generate marketing plan
    if st.button("Generate Marketing Plan"):
        if not any(marketing_data):
            st.error("Please fill in at least one marketing strategy.")
        else:
            for i, (strategy_name, target_audience, channels, platforms, budget, timeline, success_metrics) in enumerate(marketing_data):
                if not strategy_name:
                    st.warning(f"Strategy Name {i + 1} is required.")
                else:
                    marketing_plan = generate_content(f"Marketing Plan: {strategy_name}", f"Target Audience: {target_audience}\nChannels: {', '.join(channels)}\nPlatforms: {', '.join(platforms)}\nBudget: ${budget}\nTimeline:\n{timeline}\nSuccess Metrics:\n{success_metrics}", [])
                    st.markdown(marketing_plan)
                    st.markdown("---")
                    
# Page: Business Plan
elif page == "Business Plan":
    st.title("Business Plan Generator")
    st.write("Create business plans for your ventures.")

    business_types = st.multiselect("Select Business Types", ["Tech Startup", "Restaurant", "E-commerce", "Consulting Firm", "Healthcare Practice", "Real Estate Agency", "Fitness Center", "Fashion Brand", "Event Planning", "Education Service"])
    target_markets = st.multiselect("Select Target Markets", ["Local", "Regional", "National", "Global", "Niche", "Mass Market", "B2B", "B2C", "Online", "Offline"])
    revenue_models = st.multiselect("Select Revenue Models", ["Subscription", "Freemium", "Pay-Per-Use", "Advertising", "Affiliate Marketing", "Product Sales", "Service Fees", "Licensing", "Rentals", "Donations"])
    marketing_strategies = st.multiselect("Select Marketing Strategies", ["Social Media Marketing", "Content Marketing", "Email Marketing", "Search Engine Optimization", "Pay-Per-Click Advertising", "Influencer Marketing", "Event Sponsorship", "Guerrilla Marketing", "Partnerships", "Referral Programs"])

    # Button to generate business plan
    if st.button("Generate Business Plan"):
        # Generate business plan
        for business_type, target_market, revenue_model, marketing_strategy in zip(business_types, target_markets, revenue_models, marketing_strategies):
            business_plan = generate_content("Business Plan", f"Business Type: {business_type}\nTarget Market: {target_market}\nRevenue Model: {revenue_model}\nMarketing Strategy: {marketing_strategy}", [])
            st.markdown(business_plan)

            # Add a separator between plans for better readability
            st.markdown("---")

# Page: Real Estate
elif page == "Real Estate":
    st.title("Real Estate Page")
    st.write("Explore real estate listings.")

    property_types = st.multiselect("Select Property Types", ["House", "Apartment", "Condo", "Townhouse", "Land", "Commercial Property", "Vacation Rental", "Farm", "Ranch", "Industrial Property"])
    locations = st.multiselect("Select Locations", ["Urban", "Suburban", "Rural", "Waterfront", "Mountain View", "Desert", "Forest", "Island", "Countryside", "City Center"])
    price_ranges = st.multiselect("Select Price Ranges", ["Under $100,000", "$100,000 - $250,000", "$250,000 - $500,000", "$500,000 - $1,000,000", "$1,000,000 - $2,000,000", "$2,000,000 - $5,000,000", "$5,000,000 - $10,000,000", "$10,000,000 - $20,000,000", "$20,000,000 - $50,000,000", "Over $50,000,000"])
    amenities = st.multiselect("Select Amenities", ["Swimming Pool", "Gym", "Garden", "Garage", "Balcony", "Fireplace", "Ocean View", "Mountain View", "Smart Home Technology", "Security System"])

    # Button to generate real estate page
    if st.button("Generate Real Estate Page"):
        # Generate real estate page
        for property_type, location, price_range, amenity in zip(property_types, locations, price_ranges, amenities):
            real_estate_page = generate_content("Real Estate Page", f"Property Type: {property_type}\nLocation: {location}\nPrice Range: {price_range}\nAmenities: {amenity}", [])
            st.markdown(real_estate_page)

            # Add a separator between pages for better readability
            st.markdown("---")
# Page: E-commerce Listing
elif page == "E-commerce Listing":
    st.title("E-commerce Listing Generator")
    st.write("Create listings for your e-commerce products.")

    product_name = st.text_input("Product Name", "")
    brand = st.text_input("Brand", "")
    description = st.text_area("Description", "")
    price = st.number_input("Price", value=0.0, step=0.01)
    quantity = st.number_input("Quantity", value=1, min_value=1)
    categories = st.multiselect("Categories", ["Electronics", "Clothing", "Home & Kitchen", "Beauty & Personal Care", "Sports & Outdoors", "Books", "Toys & Games", "Health & Household", "Automotive", "Tools & Home Improvement"], default=["Electronics"])
    platforms = st.multiselect("Platforms", ["Amazon", "eBay", "Shopify", "Etsy", "Walmart", "Alibaba", "Target", "Best Buy", "Costco", "Home Depot"], default=["Amazon"])
    sku = st.text_input("SKU", "")
    dimensions = st.text_input("Dimensions", "")
    weight = st.number_input("Weight (kg)", value=0.0, step=0.01)
    shipping_options = st.multiselect("Shipping Options", ["Free Shipping", "Express Shipping", "International Shipping"], default=["Free Shipping"])
    images = st.file_uploader("Upload Images", accept_multiple_files=True)

    # Button to generate e-commerce listing
    if st.button("Generate E-commerce Listing"):
        # Generate e-commerce listing
        ecom_listing = generate_content("E-commerce Listing", f"Product Name: {product_name}\nBrand: {brand}\nDescription: {description}\nPrice: ${price}\nQuantity: {quantity}\nCategories: {', '.join(categories)}\nPlatforms: {', '.join(platforms)}\nSKU: {sku}\nDimensions: {dimensions}\nWeight: {weight} kg\nShipping Options: {', '.join(shipping_options)}", [])
        if images:
            for image in images:
                ecom_listing += f"\n![Image](data:{image.type};base64,{image.read().encode('base64').decode()})"
        st.markdown(ecom_listing)

        # Add a separator between listings for better readability
        st.markdown("---")

# Page: Email Sequences
if page == "Email Sequences":
    st.title("Email Sequences Generator")
    st.write("Craft effective email sequences for your marketing campaigns.")

    sequence_name = st.text_input("Sequence Name", "")
    emails = st.text_area("Emails (separated by line breaks)", "")
    email_type = st.selectbox("Email Type", ["Welcome Sequence", "Promotional Sequence", "Follow-up Sequence", "Abandoned Cart Sequence", "Feedback Sequence", "Re-engagement Sequence"])
    email_subject = st.text_input("Email Subject", "")
    send_time = st.time_input("Send Time", value=datetime.time(9, 0))
    send_date = st.date_input("Send Date", value=datetime.date.today())
    sender_name = st.text_input("Sender Name", "")
    sender_email = st.text_input("Sender Email", "")

    # Button to generate email sequences
    if st.button("Generate Email Sequences"):
        # Generate email sequences
        email_sequence = generate_content(sequence_name, emails, [f"Email Type: {email_type}", f"Subject: {email_subject}", f"Send Time: {send_time}", f"Send Date: {send_date}", f"Sender Name: {sender_name}", f"Sender Email: {sender_email}"])
        st.markdown(email_sequence)

        # Add a separator between sequences for better readability
        st.markdown("---")

# Page: Google Listing
elif page == "Google Listing":
    st.title("Google Listing Generator")
    st.write("Generate a Google listing.")

    # Input fields
    name = st.text_input("Name")
    address = st.text_input("Address")
    phone = st.text_input("Phone")
    website = st.text_input("Website")
    categories = st.multiselect("Categories", ["Restaurant", "Hotel", "Cafe", "Bar", "Store", "Service", "Attraction"])

    # Button to generate Google listing
    if st.button("Generate Google Listing"):
        listing_content = generate_google_listing(name, address, phone, website, categories)
        st.text_area("Generated Google Listing", value=listing_content, height=300)# Page: About
elif page == "About":
    st.title("About Content Generator")
    st.write("Welcome to the Content Generator, a tool designed to assist with various content creation needs.")

    # Add your about section content here

# Page: Settings
elif page == "Settings":
    st.title("Settings")
    st.write("We value your feedback and suggestions. Please share your thoughts with us.")

    # Feedback form
    feedback = st.text_area("Your Feedback", "")

    # Button to submit feedback
    if st.button("Submit Feedback"):
        # Store feedback in database or send via email
        st.write("Thank you for your feedback! We'll use it to improve the Content Generator.")

    # Help section
    st.header("Need Help?")
    st.write("If you have any questions or encounter issues, please contact us at support@example.com.")

    # Dark mode toggle
    st.sidebar.markdown("---")
    st.sidebar.title("Display Settings")
    dark_mode = st.sidebar.checkbox("Dark Mode")

    # Apply dark mode if toggled
    if dark_mode:
        st.markdown(
            """
            <style>
            .reportview-container {
                background-color: #1a1a1a;
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
