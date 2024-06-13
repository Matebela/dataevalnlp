import streamlit as st

def display():
    st.title("Advertising Copy Tasks")
    st.write("Manage your advertising copy tasks here.")
    
    # Add input fields, buttons, and other widgets here
    ad_title = st.text_input("Ad Title")
    ad_content = st.text_area("Ad Content")
    if st.button("Save Ad Copy"):
        st.success("Ad copy saved successfully!")
