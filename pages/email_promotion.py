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

    # Text inputs for event details, email type, and target audience
    event_details = st.text_area("Event Details", height=100)
    email_type = st.text_input("Email Type")
    target_audience = st.text_input("Target Audience")

    # Button to generate email
    if st.button("Generate Email"):
        if event_details and email_type and target_audience:
            # Call OpenRouter API to generate email
            email_content, explanation = generate_email(event_details, email_type, target_audience)
            if email_content and explanation:
                # Display the generated email
                st.markdown("## Generated Email")
                st.markdown(email_content, unsafe_allow_html=True)
                # Display the explanation
                st.markdown("## Explanation")
                st.markdown(explanation)
                # Provide a download button for the email
                st.download_button("Download Email", email_content, file_name="email.txt")
            else:
                st.error("Failed to generate email. Please try again.")
        else:
            st.error("Please fill in all the fields.")

# Function to generate email using OpenRouter API
def generate_email(event_details, email_type, target_audience):
    prompt = f"""
    <Inputs> {event_details} {email_type} {target_audience} </Inputs>
    Here are the instructions for the AI assistant:

    <Instructions> You will be drafting an email to promote an upcoming event. I will provide the key details about the event inside <event></event> tags, the type of email to write inside <emailtype></emailtype> tags, and information about the target audience inside <audience></audience> tags.
    <event>{event_details}</event>
    <emailtype>{email_type}</emailtype>
    <audience>{target_audience}</audience>

    First, carefully review the event details, email type, and target audience information.

    Then, draft the email while following these guidelines:

    Open the email with an attention-grabbing subject line that concisely conveys the event's value proposition to the target audience
    In the email body, expand on the key event details in an engaging way that will resonate with the target audience
    Highlight the benefits of attending the event and how it addresses the audience's interests, needs or pain points
    Include a clear call-to-action with details on how to RSVP, register or get tickets
    Close the email in a way that creates a sense of urgency and excitement
    Use a tone and style appropriate for the email type and target audience
    Keep the email concise - no more than 200 words
    Write your draft inside <email></email> tags. After drafting the email, provide a short explanation inside <explanation></explanation> tags on how your email draft is designed to effectively promote the event to the target audience.
    </Instructions>
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
    
    # Log the response for debugging
    st.write("API Response:", response_json)
    
    try:
        email_content = response_json['choices'][0]['message']['content']
        explanation = response_json['choices'][0]['message']['content']  # Assuming the explanation is also in the first choice
        return email_content, explanation
    except (IndexError, KeyError) as e:
        st.error(f"Error processing response: {e}")
        return None, None
