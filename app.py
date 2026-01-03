import streamlit as st


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


st.set_page_config(page_title="EmlakHub - init", page_icon="🏠", layout="wide")


if st.session_state.logged_in:
    st.switch_page("pages/gallery.py")
else:
    st.switch_page("pages/login.py")
