import streamlit as st

from api.client import ingest

def render_sidebar():
    with st.sidebar:
        st.header("Controls")
        if st.button("Ingest Data"):
            with st.spinner("Ingesting data..."):
                result = ingest()
            st.success("Completed")
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()