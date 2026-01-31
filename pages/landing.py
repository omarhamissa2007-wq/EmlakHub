import streamlit as st
st.set_page_config(page_title="Real Estate ", page_icon="🏠", layout="wide")




st.markdown("""
    <style>
    .stButton> button{
    color: red !important;
    font-weight: bold !important;
    background-color: transparent !important;
    border: 1px solid red !important;
    border-radius: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)


st.subheader("welcome to EmlakHub ")


st.markdown("---")

st.subheader("لماذا تختارنا؟")
st.write("""
     ✅ مُوثوق ومحترف في مجال العقارات  
    ✅ أفضل الأسعار في السوق  
    ✅ معاملات سريعة وأمانية  
    ✅ مجموعة واسعة من العقارات 
    """)



st.markdown("---")


st.subheader("🔥 الخدمه الرائسيه")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(" 🏘️ بيع العقارات")
    st.write("ابحث عن أفضل العقارات للبيع بأسعار مناسبة.")

with col2:
    st.write("🏡 منازل للإيجار")
    st.write("تصفح مجموعة واسعة من المنازل والشقق للإيجار.")

with col3:
  st.write(" 🛠️ إدارة العقارات")
st.write("إدارة احترافية لاستثماراتك العقارية.")

st.markdown("---")
if st.button("🔍 استكشف العقارات"):
    st.success("جارٍ التوجيه إلى صفحة العقارات... (يمكنك ربطها لاحقاً)")
    st.switch_page("pages/gallery.py")




