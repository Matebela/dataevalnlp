import streamlit as st
import hashlib
import time
from pages import main_page, whitepaper_from_webinar

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
            page = st.sidebar.selectbox("Go to", ["Main Page", "Whitepaper from Webinar"])
            st.sidebar.button("Logout", on_click=logout)

            # Display the selected page
            if page == "Main Page":
                main_page.display()
            elif page == "Whitepaper from Webinar":
                whitepaper_from_webinar.display()

if __name__ == "__main__":
    main()
