import streamlit as st
import requests
import json

# Load OpenRouter API key from Streamlit secrets
try:
    OPENROUTER_API_KEY = st.secrets["secrets"]["openrouter_api_key"]
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
    provided webinar transcript. The white paper should cover key topics, insights, and actionable recommendations discussed in the webinar.

Webinar Transcript: {webinar_transcript}

Instructions:
1. **Analyze the Transcript**: Identify the main topics, key points, and important insights discussed in the webinar.
2. **Create an Outline**: Organize the content into logical sections and subsections, including:
    - Introduction
    - Background Information
    - Main Sections (3-5 sections covering key topics)
    - Actionable Recommendations
    - Conclusion
3. **Develop Content**: For each section, generate detailed and informative content by:
    - Expanding on key points and insights from the webinar
    - Providing relevant examples, case studies, or statistics
    - Offering practical advice and actionable recommendations
    - Ensuring a clear and logical flow of information
4. **Engaging Introduction**: Write an introduction that captures the reader's attention, highlights the importance of the topic, and provides an overview of the white paper.
5. **Compelling Conclusion**: Summarize the main points, reinforce key takeaways, and encourage the reader to take action based on the recommendations.
6. **Professional Tone**: Maintain a professional and informative tone, using clear and concise language.
7. **Incorporate Visuals**: Suggest relevant visuals (e.g., charts, graphs, diagrams) to support the content and enhance understanding. Provide descriptions or suggestions for visuals.
8. **Proofread and Refine**: Ensure clarity, coherence, and accuracy. Make necessary edits to enhance the overall quality.
9. **Format the White Paper**: Use appropriate headings, subheadings, bullet points, and white space for a visually appealing layout.
10. **Final Version**: Provide a final version of the white paper, approximately 1000-1500 words in length, ready for distribution.

Note: Please generate the white paper based on the provided webinar transcript and instructions.
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

