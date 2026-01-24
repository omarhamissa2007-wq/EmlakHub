import streamlit as st
import os
from PIL import Image
from data.properties_data import properties
from utils import get_image_path


st.set_page_config(page_title="EmlakHub - Details", page_icon="🏠", layout="wide")
st.title("🏘️ تفاصيل العقار")

if (
    "selected_property" not in st.session_state
    or st.session_state.selected_property is None
):
    st.warning("⚠️ لم يتم اختيار عقار. يرجى العودة إلى الصفحة الرئيسية واختيار عقار.")
    if st.button("← العودة إلى الصفحة الرئيسية"):
        st.switch_page("pages/gallery.py")


else:
    property_id = st.session_state.selected_property
    property_data = properties[property_id]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("صورة العقار")

        try:
            image_path = get_image_path(property_data["image"])
            img = Image.open(image_path)
            st.image(img, width=600)
        except Exception as e:
            st.error(f"خطأ في تحميل الصورة: {str(e)}")

        if st.button("📄 عرض العقد", use_container_width=True):
            st.session_state.selected_property = property_id
            st.switch_page("pages/contract.py")

    with col2:
        st.subheader("معلومات العقار")
        st.write(f"المعرّف: {property_id}")
        st.write(f"السعر: {property_data['price']}")
        st.write(f"العنوان: {property_data['address']}")
        st.write(f"النوع: {property_data['type']}")

        st.divider()

        st.subheader("المواصفات")
        st.write(f"عدد الغرف: {property_data['rooms']}")
        st.write(f"المساحة: {property_data['space']}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← العودة إلى الصفحة الرئيسية", use_container_width=True):
            st.session_state.selected_property = None
            st.switch_page("pages/gallery.py")

    with col2:
        if st.button("🔄 اختيار عقار آخر", use_container_width=True):
            st.session_state.selected_property = None
            st.rerun()
