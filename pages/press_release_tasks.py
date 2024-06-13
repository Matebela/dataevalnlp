import streamlit as st

def display():
    st.title("Press Release Tasks")
    st.write("Manage your press release tasks here.")
    
    # Add input fields, buttons, and other widgets here
    release_title = st.text_input("Release Title")
    release_content = st.text_area("Release Content")
    if st.button("Save Press Release"):
        st.success("Press release saved successfully!")
