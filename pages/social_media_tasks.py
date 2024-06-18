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
    context = st.text_area("Provide some context about your company/product:", height=100)
    topic = st.text_input("What is the main topic of the article you want to promote?")
    article_link = st.text_input("Paste the link to your article:")

    # Button to generate social media posts
    if st.button("Generate Posts"):
        if all([context, topic, article_link]):
            posts = generate_social_media_posts(context, topic, article_link)
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
            st.error("Please fill in all the fields.")

# Function to generate social media posts using OpenRouter API
def generate_social_media_posts(context, topic, article_link):
    prompt = f"""
    LinkedIn and Twitter Post Prompt
    Context: {context}
    Goal: Generate 6 social media posts: 3 for LinkedIn and 3 for Twitter, promoting the provided article about {topic} in the life science and biotech industry.
    Instructions:
    For each post:
    1. Craft a Compelling Hook: Start with a question, statement, or statistic that captures attention and relates to the article's central theme.
    2. Summarize the Problem/Challenge: Briefly describe the pain points or challenges faced by the target audience that the blog article addresses.
    3. Present the Solution/Expertise: Highlight Samba Scientific's expertise and services as the solution to the identified challenges. Briefly mention the blog article as a source of valuable information.
    4. Emphasize Benefits/Results: Focus on the positive outcomes and results companies can achieve by reading the blog article and utilizing Samba Scientific's services.
    5. Include a Call to Action: Encourage readers to learn more by visiting the blog, downloading resources, or contacting Samba Scientific.
    6. Add Relevant Hashtags: Use industry-specific hashtags to increase reach and visibility within the life science and biotech community.
    7. Include the article link: {article_link} in each post.
    Output:
    Separate the output into two sections: "LinkedIn Posts:" and "Twitter Posts:". Under each section, list the three posts.
    Important Considerations:
    * Length: Keep LinkedIn posts concise (around 300 words) and Twitter posts even shorter (under 280 characters).
    * Visuals: Consider adding relevant images or videos to your posts to increase engagement.
    * Formatting: Use bullet points, bold text, and line breaks to make your posts easy to read.
    * Target Audience: Tailor your language and messaging to the specific target audience of the blog article.
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
        posts_content = response_json['choices'][0]['message']['content']
        linkedin_posts, twitter_posts = posts_content.split("Twitter Posts:")
        linkedin_posts = [post.strip() for post in linkedin_posts.split("LinkedIn Posts:")[1].strip().split("\n") if post.strip()]
        twitter_posts = [post.strip() for post in twitter_posts.strip().split("\n") if post.strip()]
        return {"linkedin": linkedin_posts, "twitter": twitter_posts}
    except (IndexError, KeyError, ValueError) as e:
        st.error(f"Error processing response: {e}")
        return None

# Run the display function to start the Streamlit app
if __name__ == "__main__":
    display()
