import streamlit as st
import hashlib
import time

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

# Function to display the main page
def main_page():
    st.title("Main Page")
    st.write("Welcome to the app! This app helps you manage various tasks.")
    st.write("Use the sidebar to navigate to different task pages.")

# Function to display the subpages with placeholders
def email_copy_tasks():
    st.title("Email Copy Tasks")
    st.write("Placeholder for Email Copy Tasks content.")

def advertising_copy_tasks():
    st.title("Advertising Copy Tasks")
    st.write("Placeholder for Advertising Copy Tasks content.")

def web_page_and_mockup_tasks():
    st.title("Web Page and Mockup Tasks")
    st.write("Placeholder for Web Page and Mockup Tasks content.")

def press_release_tasks():
    st.title("Press Release Tasks")
    st.write("Placeholder for Press Release Tasks content.")

def social_media_tasks():
    st.title("Social Media Tasks")
    st.write("Placeholder for Social Media Tasks content.")

def blog_write_task():
    st.title("Blog Write Task")
    st.write("Placeholder for Blog Write Task content.")

def strategy_competitor_tasks():
    st.title("Strategy Competitor Tasks")
    st.write("Placeholder for Strategy Competitor Tasks content.")

def whitepaper_from_webinar():
    st.title("Whitepaper from Webinar")
    st.write("Placeholder for Whitepaper from Webinar content.")

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
                st.experimental_rerun()  # Rerun the script to show the main content
            else:
                st.error("Invalid username or password")
    else:
        # Check for session timeout (e.g., 30 minutes)
        if time.time() - st.session_state.last_active > 1800:
            st.warning("Session timed out. Please log in again.")
            logout()
        else:
            st.session_state.last_active = time.time()

            # Sidebar for navigation
            st.sidebar.title("Navigation")
            page = st.sidebar.selectbox("Go to", ["Main Page", "Email Copy Tasks", "Advertising Copy Tasks", "Web Page and Mockup Tasks", "Press Release Tasks", "Social Media Tasks", "Blog Write Task", "Strategy Competitor Tasks", "Whitepaper from Webinar"])
            st.sidebar.button("Logout", on_click=logout)

            # Display the selected page
            if page == "Main Page":
                main_page()
            elif page == "Email Copy Tasks":
                email_copy_tasks()
            elif page == "Advertising Copy Tasks":
                advertising_copy_tasks()
            elif page == "Web Page and Mockup Tasks":
                web_page_and_mockup_tasks()
            elif page == "Press Release Tasks":
                press_release_tasks()
            elif page == "Social Media Tasks":
                social_media_tasks()
            elif page == "Blog Write Task":
                blog_write_task()
            elif page == "Strategy Competitor Tasks":
                strategy_competitor_tasks()
            elif page == "Whitepaper from Webinar":
                whitepaper_from_webinar()

if __name__ == "__main__":
    main()
