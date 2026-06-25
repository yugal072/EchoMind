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
        
        uploaded_files = st.file_uploader("upload file", accept_multiple_files=True, type=['pdf','txt'])
        
        if st.button("Upload and ingest"):
            if not uploaded_files:
                st.warning("Please upload the files first.")
                return
            
            file_dir = backend_path/"data/uploads/files"
            os.makedirs(file_dir, exist_ok=True)
            
            saved_paths = []
            for uploaded_file in uploaded_files:
                file_path = file_dir/ uploaded_file.name

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    
                saved_paths.append(str(file_path))
                st.success(f"Saved: {uploaded_file.name}")
            
            with st.spinner("Uploading  to vectorstore..."):
                result = upload(saved_paths)    # List of paths
    
            st.write(f"Added Uploaded files to vectorstore {result}")
            
    
        ### Audio Upload Section
        uploaded_audios = st.file_uploader(
            "Upload Voice Note / Audio",
            type=["mp3", "wav", "m4a", "ogg"],
            accept_multiple_files=True
        )

        if uploaded_audios and st.button("Process audio files"):
            # Create directory
            temp_dir = backend_path/"data/uploads/audio"
            os.makedirs(temp_dir, exist_ok=True)
            
            for audio_file in uploaded_audios:
                temp_path = temp_dir/ audio_file.name
                
                with open(temp_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                
                with st.spinner(f"Transcribing {audio_file.name}..."):
                    response = requests.post(
                        f"{BASE_URL}/ingest/audio",
                        json={"file_path": str(temp_path)}
                    )
                    if response.status_code==200:
                        st.success(f"✅ {audio_file.name} processed successfully!")
                    else:
                        st.error(f"❌ Failed {audio_file.name}: {response.text}")
                    
                                    
        # Manual Ingest
        if st.button("Ingest Data"):
            with st.spinner("Ingesting data..."):
                result = ingest()
            st.success("Ingestion Completed")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
            
            
       # === History Debug ===
        st.divider()
        st.subheader("Debug")
        if st.button("Show Raw History"):
            if st.session_state.get("messages"):
                with st.expander("Chat History (JSON)", expanded=False):
                    st.json(st.session_state.messages)
            else:
                st.info("No messages yet.")