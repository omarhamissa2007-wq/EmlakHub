import streamlit as st
import os
from data.properties_data import properties
from PIL import Image

from notifications import send_message


# إعداد الصفحة
st.set_page_config(
    page_title="EmlakHub - Contract", 
    page_icon="📝", 
    layout="wide"
)
st.title("📄 Contract")
st.divider()



# التحقق من اختيار العقار
if "selected_property" not in st.session_state or not st.session_state.selected_property:
    st.warning("⚠️ لم يتم اختيار عقار. يرجى العودة إلى الصفحة الرئيسية واختيار عقار.")
    st.stop()

property_id = st.session_state.selected_property
property_data = properties[property_id]




# عرض بيانات العقار
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
        contract_type = st.selectbox("📑 اختر نوع العقد:", ["ownership", "tenant"], index=0)
    
        
    st.info("📢 سيتم إرسال تأكيد العقد عبر البريد الإلكتروني")




with col2:
    st.subheader("معلومات العقار")
    property_type = property_data["type"]
    st.write(f"النوع: {property_type}")
    st.write(f"السعر: {property_data['price']}")
    st.write(f"العنوان: {property_data['address']}")
    st.divider()

    try:
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), property_data['image'])
        img = Image.open(image_path)
        st.image(img, width=600)
    except Exception as e:
        st.error(f"خطأ في تحميل الصورة: {str(e)}")




# تحميل ملفات العقود
owner_data = None
lease_data = None

st.divider()

if contract_type == "ownership":
    try:
        with open("PDFs/ownership_contract.pdf", "rb") as f:
            owner_data = f.read()
    except FileNotFoundError:
        st.error("ملف ownership_contract.pdf غير موجود في المجلد PDFs.")
else:
    try:
        with open("PDFs/tenant_contract.pdf", "rb") as f:
            lease_data = f.read()
    except FileNotFoundError:
        st.error("ملف tenant_contract.pdf غير موجود في المجلد PDFs.")

# أزرار تحميل العقود
if contract_type == "ownership" and owner_data is not None:
    st.download_button(
        label="📃 تحميل عقد البيع",
        data=owner_data,
        file_name="ownership_contract.pdf",
        mime="application/pdf",
        use_container_width=True
    )
elif contract_type == "tenant" and lease_data is not None:
    st.download_button(
        label="🏠 تحميل عقد الإيجار",
        data=lease_data,
        file_name="tenant_contract.pdf",
        mime="application/pdf",
        use_container_width=True
    )



# رفع العقد بعد التوقيع
uploaded_file = st.file_uploader("📤 ارفع العقد بعد التوقيع (PDF فقط)", type=["pdf"])

if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    expected_file = "ownership_contract.pdf" if contract_type == "ownership" else "tenant_contract.pdf"

    if uploaded_file.name == expected_file:
        with open(f"uploads/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ تم رفع العقد بنجاح!")

    else:
        st.error(f"❌ خطأ! الرجاء رفع الملف الصحيح: {expected_file}")




# زر إرسال البيانات
if st.button("إرسال تفاصيل العقد", use_container_width=True):

    if not all([name, phone_input, card_number, email]):
        st.error("الرجاء ملء جميع الحقول المطلوبة")
    
    elif not phone_input.startswith('+'):
        st.error("الرجاء إدخال رقم الهاتف بالصيغة الصحيحة (ابدأ برمز الدولة)")
    
    elif '@' not in email:
        st.error("الرجاء إدخال بريد إلكتروني صحيح")
    
    else:
        # Only send email (WhatsApp disabled for now)
        success = send_message(
            name=name,
            phone_number=phone_input,
            email=email,
            card_number=card_number,
            contract_type="ملكية" if contract_type == "ownership" else "إيجار",
            property_id=property_id,
            use_whatsapp=False,  # WhatsApp disabled
            use_email=True
        )
        
        if success:
            st.balloons()
            st.success("✅ تم إرسال تفاصيل العقد بنجاح!")