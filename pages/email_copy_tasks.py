import streamlit as st

def display():
    st.title("Email Copy Tasks")
    st.write("Manage your email copy tasks here.")
    
    # Add input fields, buttons, and other widgets here
    email_subject = st.text_input("Email Subject")
    email_body = st.text_area("Email Body")
    if st.button("Save Email Copy"):
        st.success("Email copy saved successfully!")
