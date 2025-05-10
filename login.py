import streamlit as st
from auth import login

st.set_page_config(page_title="Login", layout="centered", page_icon="🔑")
login()