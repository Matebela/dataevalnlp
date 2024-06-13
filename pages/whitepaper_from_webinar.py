import streamlit as st
import datetime

def display():
    st.title("Whitepaper from Webinar")

    # Input fields for webinar details
    webinar_title = st.text_input("Webinar Title")
    webinar_date = st.date_input("Webinar Date", datetime.date.today())
    key_points = st.text_area("Key Points", "Enter the key points discussed in the webinar...")

    # File upload for webinar transcript
    uploaded_file = st.file_uploader("Upload Webinar Transcript", type=["txt", "pdf"])

    # Button to generate whitepaper
    if st.button("Generate Whitepaper"):
        if webinar_title and key_points and uploaded_file:
            # Process the uploaded file and generate the whitepaper
            whitepaper_content = generate_whitepaper(webinar_title, webinar_date, key_points, uploaded_file)
            st.success("Whitepaper generated successfully!")
            st.download_button("Download Whitepaper", whitepaper_content, file_name="whitepaper.txt")
        else:
            st.error("Please fill in all the details and upload the transcript.")

def generate_whitepaper(title, date, key_points, file):
    # Read the uploaded file
    if file.type == "text/plain":
        transcript = file.read().decode("utf-8")
    elif file.type == "application/pdf":
        # You can use a library like PyPDF2 to read PDF files
        import PyPDF2
        reader = PyPDF2.PdfFileReader(file)
        transcript = ""
        for page in range(reader.numPages):
            transcript += reader.getPage(page).extract_text()
    
    # Generate the whitepaper content
    whitepaper_content = f"Title: {title}\n"
    whitepaper_content += f"Date: {date}\n\n"
    whitepaper_content += f"Key Points:\n{key_points}\n\n"
    whitepaper_content += f"Transcript:\n{transcript}\n"
    
    return whitepaper_content
