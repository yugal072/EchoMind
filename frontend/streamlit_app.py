
import streamlit as st

from components.sidebar import render_sidebar
from components.chat import render_chat
from utils.session import initialize_session

st.set_page_config(
    page_title="EchoMind",
    page_icon=":brain:",
    layout="wide",
)

initialize_session()

st.title("EchoMind :brain:")

render_sidebar()
render_chat()