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
    You are a marketing assistant tasked with drafting a compelling email promoting a company's attendance at an upcoming conference. The email should have a dual focus:

    1. **General Promotion:** Briefly introduce the company and highlight its presence at the event. Showcase key products or services.
    2. **Featured Presentation Promotion:**  Dedicate a section to specifically promoting a presentation being given by a company representative.

    Here is the information provided to you:

    **Objective:** {objective}
    **Event Details:** {event_details}
    **Products to Promote:** {products_to_promote}
    **Copy and Trademark Usage:** {copy_and_trademark_usage}
    **Marketing Objective:** {marketing_objective}
    **Call to Action:** {cta}
    **Target Audience:** {audience}
    **Destination URL:** {destination_url}

    **Instructions:** 
    Using the information provided, craft a single, well-structured email that incorporates both the general promotion and the featured presentation promotion. Ensure the email is informative, engaging, and adheres to the specified copy and trademark guidelines. 
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
