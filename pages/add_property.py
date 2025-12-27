import streamlit as st
import os
from datetime import datetime
from data.properties_data import properties

# تكوين الصفحة
st.set_page_config(
    page_title="إضافة عقار جديد",
    page_icon="🏠",
    layout="centered"
)

# عنوان الصفحة
st.title("إضافة عقار جديد")
st.markdown("---")

# المسارات
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create uploads directory

# دالة لحفظ البيانات
def save_property(property_data, image_file=None):
    try:
        # إنشاء معرف فريد للعقار
        property_id = f"property_{int(datetime.now().timestamp())}"
        
        # حفظ الصورة إذا وجدت
        if image_file is not None:
            image_ext = os.path.splitext(image_file.name)[1]
            image_filename = f"{property_id}{image_ext}"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            
            # حفظ الصورة
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())
            
            # حفظ مسار الصورة
            property_data["صورة_العقار"] = f"uploads/{image_filename}"
        
        # إضافة العقار للقائمة
        properties[property_id] = property_data
        
        # حفظ البيانات في الملف
        with open("data/properties_data.py", "w", encoding="utf-8") as f:
            f.write("properties = " + str(properties))
        
        return True
    except Exception as e:
        st.error(f"حدث خطأ أثناء حفظ البيانات: {e}")
        return False

# نموذج إضافة عقار
with st.form("property_form"):
    st.subheader("معلومات العقار")
    
    # معلومات أساسية
    name = st.text_input("اسم العقار", placeholder="أدخل اسم العقار")
    price = st.number_input("السعر (جنيه مصري)", min_value=0, step=1000, value=0)
    address = st.text_area("عنوان العقار", placeholder="أدخل العنوان")
    rooms = st.number_input("عدد الغرف", min_value=0, step=1, value=1)
    
    # رفع صورة
    uploaded_image = st.file_uploader("صورة العقار", type=["jpg", "jpeg", "png"])
    
    submit_button = st.form_submit_button("حفظ العقار", use_container_width=True)
    
    if submit_button:
        if not all([name, address, price > 0]):
            st.error("الرجاء إدخال جميع الحقول المطلوبة")
        else:
            # تجميع البيانات
            property_data = {
                "اسم العقار": name,
                "السعر": f"{price:,} جنيه مصري",
                "العنوان": address,
                "عدد الغرف": rooms
            }
            
            # حفظ البيانات
            if save_property(property_data, uploaded_image):
                st.success("تم إضافة العقار بنجاح!")
                st.balloons()

# رابط للعودة للصفحة الرئيسية
st.markdown("---")
if st.button("العودة للصفحة الرئيسية", use_container_width=True):
    st.switch_page("pages/home.py")