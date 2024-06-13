import streamlit as st

def display():
    st.title("Strategy Competitor Tasks")
    st.write("Manage your strategy and competitor analysis tasks here.")
    
    # Add input fields, buttons, and other widgets here
    competitor_name = st.text_input("Competitor Name")
    analysis_content = st.text_area("Analysis Content")
    if st.button("Save Analysis"):
        st.success("Analysis saved successfully!")
