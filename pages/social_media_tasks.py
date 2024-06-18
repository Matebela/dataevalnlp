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
    Generate 3 LinkedIn posts and 3 Twitter posts promoting the provided article about {topic} in the life science and biotech industry.
    Context: {context}
    Article Link: {article_link}
    
    Instructions:
    - Each LinkedIn post should be around 300 words.
    - Each Twitter post should be under 280 characters.
    - Include the article link in each post.
    - Use relevant hashtags for the life science and biotech industry.
    
    LinkedIn Posts:
    1.
    2.
    3.
    
    Twitter Posts:
    1.
    2.
    3.
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
