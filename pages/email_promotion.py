import streamlit as st
import requests
import json

# Load OpenRouter API key from Streamlit secrets
try:
    OPENROUTER_API_KEY = st.secrets["secrets"]["openrouter_api_key"]
except KeyError:
    st.error("OpenRouter API key not found in secrets.toml. Please add it.")
    st.stop()

# Function to display the email promotion page
def display():
    st.title("Email Promotion")

    # User Input Fields
    objective = st.text_area("Objective", height=50)
    event_details = st.text_area("Event Details", height=150)
    products_to_promote = st.text_area("Products to Promote", height=100)
    copy_and_trademark_usage = st.text_area("Copy and Trademark Usage", height=100)
    marketing_objective = st.text_input("Marketing Objective")
    cta = st.text_input("Call to Action")
    audience = st.text_input("Target Audience")
    destination_url = st.text_input("Destination URL")

    # Button to generate email
    if st.button("Generate Email"):
        if all([objective, event_details, products_to_promote,
                copy_and_trademark_usage, marketing_objective,
                cta, audience, destination_url]):

            email_content = generate_email(objective, event_details,
                                          products_to_promote,
                                          copy_and_trademark_usage,
                                          marketing_objective, cta,
                                          audience, destination_url)
            if email_content:
                st.markdown("## Generated Email")
                st.markdown(email_content, unsafe_allow_html=True)
            else:
                st.error("Failed to generate email. Please try again.")
        else:
            st.error("Please fill in all the fields.")


# Function to generate email using OpenRouter API
def generate_email(objective, event_details, products_to_promote,
                   copy_and_trademark_usage, marketing_objective,
                   cta, audience, destination_url):

    prompt = f"""
    You are a marketing assistant tasked with drafting a compelling email promoting a company's attendance at an upcoming conference. 
    The email should follow the structure and style of the example provided below. 

    **Example Email Structure:**

    **Subject Line Option A:** [Engaging subject line related to the event and company]
    **Subject Line Option B:** [Alternative engaging subject line]
    **Preview Text Option A:** [Concise and enticing preview text]
    **Preview Text Option B:** [Alternative preview text]

    **Title:** [Compelling title for the email body]

    **Body:**
    [Engaging introduction and company/product overview]
    [Information about the featured presentation, including speaker, title, date, time, location]
    [Call to action to visit the booth or attend the presentation]

    **CTA:** [Clear call to action with a link to the destination URL]

    **Here is the information for this email:**

    **Objective:** {objective}
    **Event Details:** {event_details}
    **Products to Promote:** {products_to_promote}
    **Copy and Trademark Usage:** {copy_and_trademark_usage}
    **Marketing Objective:** {marketing_objective}
    **Call to Action:** {cta}
    **Target Audience:** {audience}
    **Destination URL:** {destination_url}

    **Instructions:** 
    Using the information and example structure provided, craft a single, well-structured email. 
    Ensure the email is informative, engaging, and adheres to the specified copy and trademark guidelines. 
    Provide two options each for the subject line and preview text.
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data=json.dumps({
            "model": "openrouter/auto",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    response_json = response.json()

    try:
        email_content = response_json['choices'][0]['message']['content']
        return email_content
    except (IndexError, KeyError) as e:
        st.error(f"Error processing response: {e}")
        return None
