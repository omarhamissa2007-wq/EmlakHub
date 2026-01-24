import streamlit as st
import os
from data.properties_data import properties
from PIL import Image
from notifications import send_message
from utils import get_image_path


st.set_page_config(page_title="EmlakHub - Contract", page_icon="📝", layout="wide")
st.title("📄 Contract")
st.divider()


if (
    "selected_property" not in st.session_state
    or not st.session_state.selected_property
):
    st.warning("⚠️ لم يتم اختيار عقار. يرجى العودة إلى الصفحة الرئيسية واختيار عقار.")
    st.stop()

property_id = st.session_state.selected_property
property_data = properties[property_id]


col1, col2 = st.columns(2)

with col1:
    st.subheader("بيانات العميل")

    col1_form, col2_form = st.columns(2)

    with col1_form:
        name = st.text_input("👤 الاسم الكامل")
        phone_input = st.text_input("📞 رقم الهاتف (ابدأ بـ +20 لمصر)")
        email = st.text_input("📧 البريد الإلكتروني")

    with col2_form:
        card_number = st.text_input("💳 رقم البطاقة")
        contract_type = st.selectbox(
            "📑 اختر نوع العقد:", ["ownership", "tenant"], index=0
        )

    st.info("📢 سيتم إرسال تأكيد العقد عبر البريد الإلكتروني")


with col2:
    st.subheader("معلومات العقار")
    property_type = property_data["type"]
    st.write(f"النوع: {property_type}")
    st.write(f"السعر: {property_data['price']}")
    st.write(f"العنوان: {property_data['address']}")
    st.divider()

    try:
        image_path = get_image_path(property_data["image"])
        img = Image.open(image_path)
        st.image(img, width=600)
    except Exception as e:
        st.error(f"خطأ في تحميل الصورة: {str(e)}")


st.divider()


def load_contract_file(contract_type):
    if contract_type == "ownership":
        filename = "ownership_contract.pdf"
        label = "📃 تحميل عقد البيع"
    else:
        filename = "tenant_contract.pdf"
        label = "🏠 تحميل عقد الإيجار"

    try:
        path = f"assets/documents/{filename}"
        with open(path, "rb") as f:
            return f.read(), filename, label
    except FileNotFoundError:
        st.error(f"ملف {filename} غير موجود في المجلد assets/documents.")
        return None, None, None


contract_data, contract_filename, contract_label = load_contract_file(contract_type)

if contract_data:
    st.download_button(
        label=contract_label,
        data=contract_data,
        file_name=contract_filename,
        mime="application/pdf",
        use_container_width=True,
    )


uploaded_file = st.file_uploader("📤 ارفع العقد بعد التوقيع (PDF فقط)", type=["pdf"])

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    expected_file = (
        "ownership_contract.pdf"
        if contract_type == "ownership"
        else "tenant_contract.pdf"
    )

    if uploaded_file.name == expected_file:
        with open(f"data/uploads/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ تم رفع العقد بنجاح!")

    else:
        st.error(f"❌ خطأ! الرجاء رفع الملف الصحيح: {expected_file}")


if st.button("إرسال تفاصيل العقد", use_container_width=True):
    if not all([name, phone_input, card_number, email]):
        st.error("الرجاء ملء جميع الحقول المطلوبة")

    elif not phone_input.startswith("+"):
        st.error("الرجاء إدخال رقم الهاتف بالصيغة الصحيحة (ابدأ برمز الدولة)")

    elif "@" not in email:
        st.error("الرجاء إدخال بريد إلكتروني صحيح")

    else:
        success = send_message(
            name=name,
            phone_number=phone_input,
            email=email,
            card_number=card_number,
            contract_type="ملكية" if contract_type == "ownership" else "إيجار",
            property_id=property_id,
            use_whatsapp=False,  # WhatsApp disabled
            use_email=True,
        )

        if success:
            st.balloons()
            st.success("✅ تم إرسال تفاصيل العقد بنجاح!")
