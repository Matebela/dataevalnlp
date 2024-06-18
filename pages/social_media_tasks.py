import streamlit as st
import requests
import json

# Load OpenRouter API key from Streamlit secrets
try:
    OPENROUTER_API_KEY = st.secrets["secrets"]["openrouter_api_key"]
except KeyError:
    st.error("OpenRouter API key not found in secrets.toml. Please add it.")
    st.stop()

# Function to display the social media tasks page
def display():
    st.title("Social Media Tasks")

    # User Input Fields
    context = st.text_area("Context", height=100)
    topic = st.text_input("Topic")

    # Button to generate social media posts
    if st.button("Generate Social Media Posts"):
        if context and topic:
            social_media_content = generate_social_media_posts(context, topic)
            if social_media_content:
                st.markdown("## Generated Social Media Posts")
                st.markdown(social_media_content, unsafe_allow_html=True)
            else:
                st.error("Failed to generate social media posts. Please try again.")
        else:
            st.error("Please fill in all the fields.")

# Function to generate social media posts using OpenRouter API
def generate_social_media_posts(context, topic):
    prompt = f"""
    LinkedIn and Twitter Post Prompt
    Context: {context}
    Goal: Generate 6 social media posts: 3 for LinkedIn and 3 for Twitter, promoting the provided article about {topic} in the life science and biotech industry.
    Instructions:
    For each post:
    1. Identify Key Points: Analyze the article and extract the main topic, target audience, key challenges addressed, solutions offered, and desired outcomes.
    2. Craft a Compelling Hook: Start with a question, statement, or statistic that captures attention and relates to the article's central theme.
    3. Summarize the Problem/Challenge: Briefly describe the pain points or challenges faced by the target audience that the blog article addresses.
    4. Present the Solution/Expertise: Highlight Samba Scientific's expertise and services as the solution to the identified challenges. Briefly mention the blog article as a source of valuable information.
    5. Emphasize Benefits/Results: Focus on the positive outcomes and results companies can achieve by reading the blog article and utilizing Samba Scientific's services.
    6. Include a Call to Action: Encourage readers to learn more by visiting the blog, downloading resources, or contacting Samba Scientific.
    7. Add Relevant Hashtags: Use industry-specific hashtags to increase reach and visibility within the life science and biotech community.
    Output:
    LinkedIn Posts:
    * Post 1: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] ... [Benefits/Results] [Call to Action] #[Relevant Hashtags]
    * Post 2: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] ... [Benefits/Results] [Call to Action] #[Relevant Hashtags]
    * Post 3: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] ... [Benefits/Results] [Call to Action] #[Relevant Hashtags]
    Twitter Posts:
    * Post 1: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] [Benefits/Results] [Call to Action] #[Relevant Hashtags] (link to blog article)
    * Post 2: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] [Benefits/Results] [Call to Action] #[Relevant Hashtags] (link to blog article)
    * Post 3: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] [Benefits/Results] [Call to Action] #[Relevant Hashtags] (link to blog article)
    Important Considerations:
    * Length: Keep LinkedIn posts concise (around 300 words) and Twitter posts even shorter (under 280 characters).
    * Visuals: Consider adding relevant images or videos to your posts to increase engagement.
    * Formatting: Use bullet points, bold text, and line breaks to make your posts easy to read.
    * Target Audience: Tailor your language and messaging to the specific target audience of the blog article.
    Example Output (for a fictional article about data management):
    LinkedIn Post 1:
    Tired of data silos and inefficient workflows? Many life science companies struggle with managing their growing data sets. Samba Scientific offers comprehensive data management solutions to streamline your operations, improve decision-making, and unlock valuable insights. Our blog article, "Data Management for Life Sciences: A Comprehensive Guide," provides valuable insights and best practices. Learn how to:
    * Develop a robust data management strategy.
    * Implement data governance policies.
    * Optimize data storage and retrieval.
    * Leverage data analytics for strategic insights.
    Contact us today to discover how Samba Scientific can help you optimize your data management processes! #DataManagement #LifeSciences #Biotech #DataGovernance #DataAnalytics
    Twitter Post 1:
    Data management woes? Samba Scientific has the solution! Our latest blog explores data management strategies for life science companies. Get your copy here: [link to article] #DataManagement #LifeScience #Biotech #DataAnalytics
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
        social_media_content = response_json['choices'][0]['message']['content']
        return social_media_content
    except (IndexError, KeyError) as e:
        st.error(f"Error processing response: {e}")
        return None

if __name__ == "__main__":
    display()
