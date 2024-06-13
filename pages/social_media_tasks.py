import streamlit as st

def display():
    st.title("Social Media Tasks")
    st.write("Manage your social media tasks here.")
    
    # Add input fields, buttons, and other widgets here
    post_title = st.text_input("Post Title")
    post_content = st.text_area("Post Content")
    if st.button("Save Social Media Post"):
        st.success("Social media post saved successfully!")
