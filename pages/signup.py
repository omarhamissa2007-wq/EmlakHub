import streamlit as st


st.set_page_config(
    page_title="EmlakHub - SignUp",
    page_icon="📝",
    layout="centered"
    )

st.title("إنشاء حساب جديد")


with st.form("signup_form"):
    name = st.text_input("الاسم الكامل")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
    submit_button = st.form_submit_button("إنشاء الحساب", use_container_width=True)


if submit_button:
    if not all([name, email, password, confirm_password]):
        st.error("الرجاء ملء جميع الحقول المطلوبة")
    elif password != confirm_password:
        st.error("كلمتا المرور غير متطابقتين")
    else:
        st.success("تم إنشاء الحساب بنجاح!")
        st.session_state.logged_in = True
        st.switch_page("pages/home.py")

if st.button("لديك حساب بالفعل؟ تسجيل الدخول"):
    st.switch_page("pages/login.py")
