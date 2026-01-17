import streamlit as st

st.set_page_config(page_title="About Us - Real Estate", page_icon="🏠", layout="wide")
st.subheader("About Us")
st.markdown("---")
st.markdown("""
    <style>
    .stButton> button{
    color: #ffd700 !important;
    font-weight: bold !important;
    background-color: transparent !important;
    border: 1px solid #ffd700 !important;
    border-radius: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("Who We Are")
st.write("""
احنا شركه عقارات  شقق وفلل للبيع والتأجير في مصر وحلمنا نطلع الاول في عقارات  
""")

st.markdown("---")

st.subheader("🎯 Our misson")
st.write("""
 توفير أفضل العقارات بأسعار تنافسيه  
-ضمان الشفافية في جميع المعاملات العقارية  
- مساعدة العملاء على اتخاذ القرار المناسب بسهولة  
| تقديم دعم مستمر قبل وبعد الشراء  
""")

st.subheader("👁‍🗨 رؤيتنا")
st.write("""
أن نكون المنصة العقارية الرائدة في العالم العربي من خلال تقديم تجربة مستخدم سلسة وآمنة وموثوقة.
""")

st.markdown("---")

st.subheader("👨‍💼 Our Team")

st.write("Mr Omar Hossam Hamissa")

st.markdown("---")

st.subheader("📞 Contact Us")
st.write("We are happy to hear from you anytime:")

st.write("📍 Address: kafr el-shiek, Egypt")
st.write("📱 Phone: 01015013337")
st.write("✉️ Email: emlakhub46@gmail.com")

st.markdown("---")

# Contact form
st.subheader("ارسال الرساله")

with st.form("contact_form"):
    name = st.text_input("الاسم")
    phone = st.text_input("التلفون")
    massage = st.text_area("الرسالة", height=150)

    send = st.form_submit_button("إرسال ")

    if send:
        if name and massage:
            st.success("✅ تم إرسال رسالتك! سنقوم بالاتصال بك في أقرب وقت.")
        else:
            st.error("❌ يرجى إدخال اسمك ورسالتك.")

st.markdown("---")
st.caption("© 2025 EmlakHUB Real Estate Website — جميع الحقوق محفوظة.")
