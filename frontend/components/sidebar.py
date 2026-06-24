import streamlit as st
import requests
import os
from pathlib import Path

main_path = Path(__file__).resolve().parents[2]
backend_path = main_path/ "backend"

from api.client import ingest, upload, ingest_audio
BASE_URL = "http://localhost:8000"

def render_sidebar():
    with st.sidebar:
        st.header("Controls")
        files = st.file_uploader("upload file", accept_multiple_files=True, type=['pdf','txt'])
        
        if st.button("Upload and ingest"):
            if not files:
                st.warning("Please upload the files first.")
                return
            
            with st.spinner("Uploadint to vectorstore..."):
                result = upload(files)
                
            st.write(f"Added Uploaded files to vectorstore {result}")
            
    
        if st.button("Ingest Data"):
            with st.spinner("Ingesting data..."):
                result = ingest()
            st.success("Completed")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
            
            
        ### Audio Upload section
        ### Audio Upload Section
        uploaded_audios = st.sidebar.file_uploader(
            "Upload Voice Note / Audio",
            type=["mp3", "wav", "m4a", "ogg"],
            accept_multiple_files=True
        )

        if uploaded_audios:
            for uploaded_audio in uploaded_audios:
                if uploaded_audio is not None:
                    with st.spinner(f"Transcribing {uploaded_audio.name}..."):
                        # Create directory
                        temp_dir = backend_path/"data/uploads/audio"
                        os.makedirs(temp_dir, exist_ok=True)
                        
                        temp_path = os.path.join(temp_dir, uploaded_audio.name)
                        
                        # Save file
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_audio.getbuffer())
                        
                        # Call backend with correct JSON
                        response = requests.post(
                            f"{BASE_URL}/ingest/audio",
                            json={"file_path": temp_path}
                        )
                        
                        if response.status_code == 200:
                            st.success(f"✅ {uploaded_audio.name} added successfully!")
                        else:
                            st.error(f"Failed {uploaded_audio.name}: {response.text}")
        
        ## Session HIstory view
        st.divider()
        st.subheader("History")
        
        if st.button("Show Full History"):
            if "messages" in st.session_state and st.session_state.messages:
                with st.expander("Raw Chat History", expanded= True):
                    st.json(st.session_state.messages)
            else:
                st.info("No messages yet")
                
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun
        
        if "session_id" in st.session_state:
            st.caption(f"Session ID: {st.session_state.session_id}")