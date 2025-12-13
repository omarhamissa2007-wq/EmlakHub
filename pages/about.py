import streamlit as st

st.set_page_config(page_title="About Us - Real Estate", page_icon="🏠", layout="wide")
st.subheader("About Us")
st.markdown("---")


st.subheader("Who We Are")
st.write("""
We are a leading real estate company with long experience in selling, buying, and renting apartments and villas.
We focus on providing the best real estate solutions to our clients with the highest level of professionalism and safety.
Our goal is to help you find your dream home easily and at affordable prices.
""")

st.markdown("---")

st.subheader("🎯 Our Mission")
st.write("""
- Provide the best properties at competitive prices.  
- Ensure transparency in all real estate transactions.  
- Help clients make the right decision easily.  
- Offer continuous support before and after purchase.  
""")

st.subheader("👁‍🗨 Our Vision")
st.write("""
To become the No.1 real estate platform in the Arab world by offering a smooth, safe, and trusted user experience.
""")

st.markdown("---")

st.subheader("👨‍💼 Our Team")

st.write("Mr. Omar Hossam Hamissa")
st.write("12 years of experience in the real estate field.")

st.markdown("---")

st.subheader("📞 Contact Us")
st.write("We are happy to hear from you anytime:")

st.write("📍 Address: Cairo, Egypt")
st.write("📱 Phone: 01015013337")
st.write("✉️ Email: omr.hosam2002@gmail.com")

st.markdown("---")

# Contact form
st.subheader("📬 Send a Message")

with st.form("contact_form"):
    name = st.text_input("Your Name")
    phone = st.text_input("Phone Number")
    massage = st.text_input("Your Message")

    send = st.form_submit_button("Send")

    if send:
        if name and massage:
            st.success("✅ Your message has been sent! We will contact you soon.")
        else:
            st.error("❌ Please enter your name and message.")

st.markdown("---")
st.caption("© 2025 EmlakHUB Real Estate Website — All Rights Reserved.")
