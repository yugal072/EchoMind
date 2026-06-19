import streamlit as st
import requests

from api.client import ingest, upload

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