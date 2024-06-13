import streamlit as st
import assemblyai as aai
import requests

# Function to display the whitepaper from webinar page
def display():
    st.title("Whitepaper from Webinar")

    # File upload for webinar transcript
    uploaded_file = st.file_uploader("Upload Webinar Transcript", type=["txt", "pdf", "mp3", "wav", "mp4"])

    # URL input for webinar transcript
    file_url = st.text_input("Or enter the URL of the file to transcribe")

    # Button to generate whitepaper
    if st.button("Generate Whitepaper"):
        if uploaded_file or file_url:
            if uploaded_file:
                # Save the uploaded file to a temporary location
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_path = uploaded_file.name
            else:
                file_path = file_url

            # Transcribe the file
            transcript = transcribe_file(file_path)

            # Display the transcript in a fixed-width box
            st.text_area("Transcript", transcript, height=300)

            # Provide a download button for the transcript
            st.download_button("Download Transcript", transcript, file_name="transcript.txt")
        else:
            st.error("Please upload the transcript or provide a URL.")

# Function to transcribe the file using AssemblyAI
def transcribe_file(file_path):
    aai.settings.api_key = st.secrets["credentials"]["assemblyai_api_key"]
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)

    if file_path.startswith("http"):
        # If the file is a URL, transcribe it directly
        transcript = transcriber.transcribe(file_path, config=config)
    else:
        # If the file is local, check if it's an audio file
        if file_path.endswith(('.mp3', '.mp4', '.wav')):
            # If it's an audio file, upload it to AssemblyAI's servers first
            file_url = transcriber.upload(file_path)
            # Then transcribe the uploaded file
            transcript = transcriber.transcribe(file_url, config=config)
        else:
            # If it's not an audio file, transcribe it directly
            with open(file_path, "rb") as f:
                transcript = transcriber.transcribe(f, config=config)

    transcript_text = "\n".join([f"Speaker {utterance.speaker}: {utterance.text}" for utterance in transcript.utterances])
    return transcript_text
