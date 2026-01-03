import streamlit as st


st.set_page_config(page_title="EmlakHub - Login", page_icon="🔑", layout="centered")
st.title("EmlakHub - تسجيل الدخول")

with st.form("login_form"):
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    submit_button = st.form_submit_button("تسجيل الدخول", use_container_width=True)


if submit_button:
    if email and password:
        st.session_state.logged_in = True
        st.session_state.email = email
        st.success("تم تسجيل الدخول بنجاح!")
        st.switch_page("pages/gallery.py")
    else:
        st.error("الرجاء إدخال البريد الإلكتروني وكلمة المرور")


if st.button("إنشاء حساب جديد"):
    st.switch_page("pages/signup.py")
