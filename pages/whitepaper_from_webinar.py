import streamlit as st
import requests
import json

# Load OpenRouter API key from Streamlit secrets
try:
    OPENROUTER_API_KEY = st.secrets["openrouter_api_key"]
except KeyError:
    st.error("OpenRouter API key not found in secrets.toml. Please add it.")
    st.stop()

# Function to display the whitepaper from webinar page
def display():
    st.title("Whitepaper from Webinar")

    # Text input for webinar transcript
    webinar_transcript = st.text_area("Paste Webinar Transcript", height=200)

    # Button to generate whitepaper
    if st.button("Generate Whitepaper"):
        if webinar_transcript:
            # Call OpenRouter API to generate whitepaper
            whitepaper_content = generate_whitepaper(webinar_transcript)
            # Display the generated whitepaper
            st.markdown("## Generated Whitepaper")
            st.markdown(whitepaper_content)
            # Provide a download button for the whitepaper
            st.download_button("Download Whitepaper", whitepaper_content, file_name="whitepaper.txt")
        else:
            st.error("Please paste the webinar transcript.")

# Function to generate whitepaper using OpenRouter API
def generate_whitepaper(webinar_transcript):
    prompt = f"""
    Objective: Generate a comprehensive and informative white paper based on the provided webinar transcript. The white paper should cover the key topics, insights, and actionable recommendations discussed in the webinar.

    Webinar Transcript: {webinar_transcript}

    Instructions:
    1. Analyze the webinar transcript and identify the main topics, key points, and important insights discussed.
    2. Create an outline for the white paper, organizing the content into logical sections and subsections based on the identified topics and key points. The outline should include:
        - Introduction
        - Background information
        - Main sections (3-5 sections covering the key topics)
        - Actionable recommendations
        - Conclusion
    3. For each section in the outline, generate detailed and informative content by:
        - Expanding on the key points and insights from the webinar
        - Providing relevant examples, case studies, or statistics to support the points
        - Offering practical advice and actionable recommendations for the target audience
        - Ensuring a clear and logical flow of information throughout the section
    4. Write an engaging introduction that captures the reader's attention, highlights the importance of the topic, and provides an overview of what the white paper will cover.
    5. Develop a compelling conclusion that summarizes the main points, reinforces the key takeaways, and encourages the reader to take action based on the recommendations provided.
    6. Ensure that the white paper maintains a professional and informative tone throughout, using clear and concise language that is easy to understand for the target audience.
    7. Incorporate relevant visuals, such as charts, graphs, or diagrams, to support the content and enhance the reader's understanding. (Note: Please provide descriptions or suggestions for visuals; I cannot generate actual images.)
    8. Proofread and refine the generated content to ensure clarity, coherence, and accuracy. Make any necessary edits or improvements to enhance the overall quality of the white paper.
    9. Format the white paper in a visually appealing and easy-to-read layout, using appropriate headings, subheadings, bullet points, and white space.
    10. Provide a final version of the white paper, ready for distribution to the target audience.

    Note: The generated white paper should be approximately 1000-1500 words in length. Please generate the white paper based on the provided webinar transcript and instructions.
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
    whitepaper_content = response_json['choices'][0]['message']['content']
    return whitepaper_content
