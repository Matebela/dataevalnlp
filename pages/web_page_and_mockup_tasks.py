import streamlit as st

def display():
    st.title("Web Page and Mockup Tasks")
    st.write("Manage your web page and mockup tasks here.")
    
    # Add input fields, buttons, and other widgets here
    page_title = st.text_input("Page Title")
    page_content = st.text_area("Page Content")
    if st.button("Save Page Content"):
        st.success("Page content saved successfully!")
