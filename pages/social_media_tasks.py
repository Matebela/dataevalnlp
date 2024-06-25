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
    st.title("Social Media Post Generation")

    # User Input Fields
    topic = st.text_input("What is the main topic or key message you want to promote?")
    target_audience = st.text_input("Who is the target audience for this article?")
    article_link = st.text_input("Paste the link to your article:")
    article_content = st.text_area("Paste the content of your article:", height=300)
    additional_context = st.text_area("Any additional context or key points to emphasize? (Optional)", height=100)

    # Button to generate social media posts
    if st.button("Generate Posts"):
        if all([topic, target_audience, article_link, article_content]):
            posts = generate_social_media_posts(topic, target_audience, article_link, article_content, additional_context)
            if posts:
                st.markdown("## Generated Social Media Posts")

                st.markdown("**LinkedIn Posts:**")
                for i, post in enumerate(posts['linkedin']):
                    st.write(f"**Post {i+1}:** {post}")

                st.markdown("**Twitter Posts:**")
                for i, post in enumerate(posts['twitter']):
                    st.write(f"**Post {i+1}:** {post}")

            else:
                st.error("Failed to generate posts. Please try again.")
        else:
            st.error("Please fill in all required fields.")

# Function to generate social media posts using OpenRouter API
def generate_social_media_posts(topic, target_audience, article_link, article_content, additional_context):
    prompt = f"""
    LinkedIn and Twitter Post Prompt
    Topic to Promote: {topic}
    Target Audience: {target_audience}
    Additional Context: {additional_context}
    Goal: Generate 6 social media posts: 3 for LinkedIn and 3 for Twitter, promoting the provided article about {topic} in the life science and biotech industry.
    Instructions:
    For each post:
    1. Identify Key Points: Analyze the article and extract the main topic, key challenges addressed, solutions offered, and desired outcomes.
    2. Craft a Compelling Hook: Start with a question, statement, or statistic that captures attention and relates to the article's central theme.
    3. Summarize the Problem/Challenge: Briefly describe the pain points or challenges faced by the target audience ({target_audience}) that the blog article addresses.
    4. Present the Solution/Expertise: Highlight the expertise and solutions presented in the article as they relate to the identified challenges.
    5. Emphasize Benefits/Results: Focus on the positive outcomes and results that the target audience can achieve by applying the insights from the article.
    6. Include a Call to Action: Encourage readers to learn more by visiting the blog.
    7. Add Relevant Hashtags: Use industry-specific hashtags to increase reach and visibility within the life science and biotech community.
    Output:
    LinkedIn Posts:
    Post 1: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] ... [Benefits/Results] [Call to Action] #[Relevant Hashtags]
    Post 2: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] ... [Benefits/Results] [Call to Action] #[Relevant Hashtags]
    Post 3: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] ... [Benefits/Results] [Call to Action] #[Relevant Hashtags]
    Twitter Posts:
    Post 1: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] [Benefits/Results] [Call to Action] #[Relevant Hashtags] ({article_link})
    Post 2: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] [Benefits/Results] [Call to Action] #[Relevant Hashtags] ({article_link})
    Post 3: [Compelling Hook] ... [Problem/Challenge] [Solution/Expertise] [Benefits/Results] [Call to Action] #[Relevant Hashtags] ({article_link})
    Important Considerations:
    - Length: Keep LinkedIn posts concise (around 300 words) and Twitter posts even shorter (under 280 characters).
    - Visuals: Consider suggesting relevant images or videos to accompany the posts to increase engagement.
    - Formatting: Use bullet points, bold text, and line breaks to make your posts easy to read.
    - Target Audience: Tailor your language and messaging to the specific target audience ({target_audience}) of the blog article.
    - Additional Context: Incorporate the provided additional context where relevant.
    """

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        },
        data=json.dumps({
            "model": "openrouter/auto",
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "user", "content": article_content}
            ]
        })
    )

    response_json = response.json()

    try:
        posts_content = response_json['choices'][0]['message']['content']
        linkedin_posts = posts_content.split("LinkedIn Posts:")[1].split("Twitter Posts:")[0].strip().split("\n\n")
        twitter_posts = posts_content.split("Twitter Posts:")[1].strip().split("\n\n")
        linkedin_posts = [post.strip() for post in linkedin_posts if post.strip()]
        twitter_posts = [post.strip() for post in twitter_posts if post.strip()]
        return {"linkedin": linkedin_posts, "twitter": twitter_posts}
    except (IndexError, KeyError, ValueError) as e:
        st.error(f"Error processing response: {e}")
        return None

# Run the display function to start the Streamlit app
if __name__ == "__main__":
    display()
