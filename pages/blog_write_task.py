import streamlit as st

def display():
    st.title("Blog Write Task")
    st.write("Manage your blog writing tasks here.")
    
    # Add input fields, buttons, and other widgets here
    blog_title = st.text_input("Blog Title")
    blog_content = st.text_area("Blog Content")
    if st.button("Save Blog Post"):
        st.success("Blog post saved successfully!")
