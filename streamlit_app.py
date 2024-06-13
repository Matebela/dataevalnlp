import streamlit as st
import hashlib
import time
from pages import (
    main_page,
    email_copy_tasks,
    advertising_copy_tasks,
    web_page_and_mockup_tasks,
    press_release_tasks,
    social_media_tasks,
    blog_write_task,
    strategy_competitor_tasks,
    whitepaper_from_webinar,
)

# Function to create the login form
def login_form():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    return username, password

# Function to authenticate the user
def authenticate(username, password):
    try:
        authorized_users = st.secrets["credentials"]
        
        if username in authorized_users:
            hashed_password = authorized_users[username]
            if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
                return True
    except Exception as e:
        st.error(f"Error during authentication: {e}")
    return False

# Function to handle logout
def logout():
    st.session_state.authenticated = False
    st.experimental_rerun()

# Main function to handle the login flow and page navigation
def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if 'last_active' not in st.session_state:
        st.session_state.last_active = time.time()

    if not st.session_state.authenticated:
        username, password = login_form()
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.last_active = time.time()
                st.experimental_rerun() 
            else:
                st.error("Invalid username or password")
    else:
        # Check for session timeout (e.g., 30 minutes)
        if time.time() - st.session_state.last_active > 1800:
            st.warning("Session timed out. Please log in again.")
            logout()
        else:
            st.session_state.last_active = time.time()
            # Display the selected page dynamically
            st.title("Select a Page")
            page = st.selectbox(
                "Choose a Page",
                [
                    "Main Page",
                    "Email Copy Tasks",
                    "Advertising Copy Tasks",
                    "Web Page and Mockup Tasks",
                    "Press Release Tasks",
                    "Social Media Tasks",
                    "Blog Write Task",
                    "Strategy Competitor Tasks",
                    "Whitepaper from Webinar",
                ],
            )
            st.button("Logout", on_click=logout)

            if page == "Main Page":
                main_page.display()
            elif page == "Email Copy Tasks":
                email_copy_tasks.display()
            elif page == "Advertising Copy Tasks":
                advertising_copy_tasks.display()
            elif page == "Web Page and Mockup Tasks":
                web_page_and_mockup_tasks.display()
            elif page == "Press Release Tasks":
                press_release_tasks.display()
            elif page == "Social Media Tasks":
                social_media_tasks.display()
            elif page == "Blog Write Task":
                blog_write_task.display()
            elif page == "Strategy Competitor Tasks":
                strategy_competitor_tasks.display()
            elif page == "Whitepaper from Webinar":
                whitepaper_from_webinar.display()

if __name__ == "__main__":
    main()
