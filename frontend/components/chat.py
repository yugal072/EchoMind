import streamlit as st
from api.client import chat

def render_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    question = st.chat_input("What do you want to know?")
    
    if not question:
        return
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.spinner("Assistant"):
        with st.spinner("Thinking..."):
            response = chat(question, st.session_state.session_id)
            answer = response.get("answer", "Sorry, I couldn't find an answer.")
            st.markdown(answer)
            
            sources = response.get("sources", [])
            if sources:
               with st.expander("Sources"):
                   st.json(sources)
                   
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})