import streamlit as st
import os
from datetime import datetime

# تكوين الصفحة
st.set_page_config(
    page_title="إضافة عقار جديد",
    page_icon="🏠",
    layout="wide"
)

# عنوان الصفحة
st.title("إضافة عقار جديد للبيع")
st.markdown("---")

# دالة لحفظ البيانات
UPLOAD_FOLDER = "property_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_property(data, files):
    try:
        # حفظ البيانات في ملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(UPLOAD_FOLDER, f"property_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
        
        # حفظ الملفات المرفوعة
        if files:
            for i, file in enumerate(files):
                file_ext = os.path.splitext(file.name)[1]
                file_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}_image_{i}{file_ext}")
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
        
        return True
    except Exception as e:
        st.error(f"حدث خطأ أثناء حفظ البيانات: {e}")
        return False

# نموذج إضافة عقار
with st.form("property_form"):
    st.subheader("معلومات العقار")
    
    # معلومات أساسية
    col1, col2 = st.columns(2)
    with col1:
        property_type = st.selectbox("نوع العقار", ["شقة", "فيلا", "عمارة", "أرض", "محل تجاري"])
    with col2:
        property_status = st.selectbox("حالة العقار", ["جديد", "مستعمل", "تحت الإنشاء"])
    
    # السعر والمساحة
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("السعر (جنيه مصري)", min_value=0, step=1000)
    with col2:
        area = st.number_input("المساحة (متر مربع)", min_value=0)
    
    # الموقع
    st.subheader("الموقع")
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox("المحافظة", ["القاهرة", "الجيزة", "الإسكندرية", "المنصورة", "أسيوط"])
    with col2:
        district = st.text_input("الحي/المنطقة")
    
    address = st.text_area("العنوان بالتفصيل")
    
    # مواصفات إضافية
    st.subheader("مواصفات إضافية")
    col1, col2, col3 = st.columns(3)
    with col1:
        rooms = st.number_input("عدد الغرف", min_value=0, step=1)
    with col2:
        bathrooms = st.number_input("عدد الحمامات", min_value=0, step=1)
    with col3:
        floor = st.number_input("الدور", min_value=-2)
    
    # وصف العقار
    st.subheader("وصف العقار")
    description = st.text_area("أضف وصفًا تفصيليًا للعقار")
    
    # رفع الصور
    st.subheader("صور العقار")
    uploaded_files = st.file_uploader("اختر صور العقار (الحد الأقصى 10 صور)", 
                                    type=["jpg", "jpeg", "png"], 
                                    accept_multiple_files=True)
    
    # معلومات المعلن
    st.subheader("معلومات الاتصال")
    col1, col2 = st.columns(2)
    with col1:
        contact_name = st.text_input("الاسم بالكامل")
    with col2:
        contact_phone = st.text_input("رقم الهاتف")
    
    contact_email = st.text_input("البريد الإلكتروني (اختياري)", "")
    
    # شروط وأحكام
    st.markdown("### الشروط والأحكام")
    agree = st.checkbox("أوافق على الشروط والأحكام")
    
    # زر الإرسال
    submit_button = st.form_submit_button("إضافة العقار")
    
    if submit_button:
        if not all([contact_name, contact_phone]):
            st.error("الرجاء إدخال جميع الحقول المطلوبة")
        elif not agree:
            st.error("يجب الموافقة على الشروط والأحكام")
        else:
            # تجميع البيانات
            property_data = {
                "نوع العقار": property_type,
                "الحالة": property_status,
                "السعر": f"{price:,} جنيه مصري",
                "المساحة": f"{area} متر مربع",
                "المحافظة": city,
                "المنطقة": district,
                "العنوان": address,
                "عدد الغرف": rooms,
                "عدد الحمامات": bathrooms,
                "الدور": floor,
                "الوصف": description,
                "اسم المعلن": contact_name,
                "هاتف المعلن": contact_phone,
                "البريد الإلكتروني": contact_email if contact_email else "غير مدخل",
                "تاريخ الإضافة": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # حفظ البيانات
            if save_property(property_data, uploaded_files):
                st.success("تم إضافة العقار بنجاح! سنقوم بمراجعته والاتصال بك قريبًا.")
                st.balloons()

# رابط للعودة للصفحة الرئيسية
st.markdown("---")
if st.button("العودة للصفحة الرئيسية"):
    st.switch_page("pages/home.py")
