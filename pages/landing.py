import streamlit as st
st.set_page_config(page_title="Real Estate Landing Page", page_icon="🏠", layout="wide")
st.subheader("welcome to EmlakHub landing page")


st.markdown("---")



st.subheader("Why Choose Us?")
st.write("""
    ✅ Trusted real estate company  
    ✅ Best prices in the market  
    ✅ Fast and safe transactions  
    ✅ Wide selection of properties  
    """)

st.markdown("---")


st.subheader("🔥 Our Main Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(" 🏘️ Buy Properties")
    st.write("Find the best properties for sale at affordable prices.")

with col2:
    st.write("🏡 Rent Homes")
    st.write("Browse a wide variety of rental homes and apartments.")

with col3:
    st.write(" 🛠️ Property Management")
    st.write("Professional management for your real estate investments.")

st.markdown("---")
if st.button("🔍 Explore Properties"):
    st.success("Redirecting to the properties page... (You can link it later)")

