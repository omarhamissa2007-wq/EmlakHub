import streamlit as st
import os
from datetime import datetime
from data.properties_data import properties
from notifications import send_upload_confirmation

# تكوين الصفحة
st.set_page_config(page_title="نشر عقار جديد", page_icon="🏠", layout="wide")

# التحقق من تسجيل الدخول
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ يجب عليك تسجيل الدخول أولاً لنشر عقار.")
    st.info("سيتم تحويلك لصفحة تسجيل الدخول...")
    if st.button("تسجيل الدخول"):
        st.switch_page("pages/login.py")
    st.stop()

# عنوان الصفحة
st.title("نشر عقار جديد")
st.markdown("---")

# المسارات
UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_property(property_data, image_file=None):
    try:
        property_id = f"property_{int(datetime.now().timestamp())}"

        if image_file is not None:
            image_ext = os.path.splitext(image_file.name)[1]
            image_filename = f"{property_id}{image_ext}"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

            property_data["image"] = f"data/uploads/{image_filename}"
        properties[property_id] = property_data

        with open("data/properties_data.py", "w", encoding="utf-8") as f:
            f.write("properties = " + repr(properties))

        return True
    except Exception as e:
        st.error(f"حدث خطأ أثناء حفظ البيانات: {e}")
        return False


with st.form("property_form"):
    st.subheader("معلومات العقار")

    name = st.text_input("اسم العقار", placeholder="أدخل اسم العقار")
    price = st.number_input("السعر (جنيه مصري)", min_value=0, step=1000, value=0)
    address = st.text_area("عنوان العقار", placeholder="أدخل العنوان")
    with st.expander("تفاصيل إضافية", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            rooms = st.number_input("عدد الغرف", min_value=0, step=1, value=1)
            space = st.text_input("المساحة (مثال: 150 م²)", placeholder="أدخل المساحة")
        with col2:
            property_type = st.selectbox(
                "نوع العقار",
                ["apartment", "villa"],
                format_func=lambda x: "شقة" if x == "apartment" else "فيلا",
            )
            # البريد الإلكتروني للتواصل (تلقائي من تسجيل الدخول)
            default_email = st.session_state.get("email", "")
            contact_email = st.text_input(
                "البريد الإلكتروني للتواصل", value=default_email
            )

    uploaded_image = st.file_uploader("صورة العقار", type=["jpg", "jpeg", "png"])

    submit_button = st.form_submit_button("حفظ العقار", use_container_width=True)

    if submit_button:
        if not all([name, address, price > 0, space]):
            st.error("الرجاء إدخال جميع الحقول المطلوبة")
        elif not uploaded_image:
            st.error("الرجاء رفع صورة للعقار")
        else:
            property_data = {
                "name": name,
                "price": f"{price:,} جنيه",
                "address": address,
                "rooms": rooms,
                "space": space,
                "type": property_type,
            }

            if save_property(property_data, uploaded_image):
                # إرسال بريد تأكيد
                if contact_email:
                    send_upload_confirmation(property_data, contact_email)
                else:
                    st.warning(
                        "⚠️ لم يتم إدخال بريد إلكتروني، لن يتم إرسال رسالة تأكيد."
                    )

                st.success("تم نشر العقار بنجاح!")
                st.balloons()

st.markdown("---")
if st.button("العودة للصفحة الرئيسية", use_container_width=True):
    st.switch_page("pages/gallery.py")
