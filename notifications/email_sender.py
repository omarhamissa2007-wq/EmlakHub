import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from data.properties_data import properties


SENDER_EMAIL = "omarhamissa2007@gmail.com"
SENDER_PASSWORD = "pfkdbfcoyeluvjif"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def create_customer_email(customer_name, customer_email, phone_number, card_number, 
                         contract_type, property_data):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = customer_email
    msg['Subject'] = f"✅ تأكيد العقد - {customer_name}"
    body = f"""
مرحباً {customer_name}،

تم استلام بيانات العقد الخاص بك بنجاح! ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 تفاصيل العقد:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 الاسم الكامل: {customer_name}
📞 رقم الهاتف: {phone_number}
💳 رقم البطاقة: {card_number}
📑 نوع العقد: {contract_type}
🏠 نوع العقار: {property_data['type']}
💰 السعر: {property_data.get('price', 'غير محدد')}
📍 العنوان: {property_data.get('address', 'غير محدد')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

سيتم مراجعة بياناتك والتواصل معك خلال 24 ساعة.

مع أطيب التحيات،
فريق إدارة العقارات
""".format(
        customer_name=customer_name,
        phone_number=phone_number,
        card_number=card_number,
        contract_type=contract_type,
        price=property_data.get('price', 'غير محدد'),
        address=property_data.get('address', 'غير محدد')
    )
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg


def create_admin_notification(customer_name, customer_email, phone_number, 
                            contract_type, property_data, admin_email):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = admin_email
    msg['Subject'] = f"📋 إشعار عقد جديد - {customer_name}"
    body = f"""
📋 *إشعار جديد - عقد*

تم إرسال عقد جديد من:

👤 الاسم: {customer_name}
📧 الإيميل: {customer_email}
📞 الهاتف: {phone_number}
🏠 نوع العقار: {property_data['type']}
💰 السعر: {property_data.get('price', 'غير محدد')}
📍 العنوان: {property_data.get('address', 'غير محدد')}
📑 نوع العقد: {contract_type}

يرجى مراجعة النظام لمزيد من التفاصيل.
""".format(
        customer_name=customer_name,
        customer_email=customer_email,
        phone_number=phone_number,
        price=property_data.get('price', 'غير محدد'),
        address=property_data.get('address', 'غير محدد'),
        contract_type=contract_type
    )
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg


def send_email(message, recipient_email):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        return True
    except Exception as e:
        st.error(f"❌ خطأ في إرسال البريد إلى {recipient_email}: {e}")
        return False


def is_valid_email(email):
    return email and "@" in email


def send_contract_email(customer_name, customer_email, phone_number, 
                      card_number, contract_type, property_id, admin_email="omarhamissa2007@gmail.com"):
    try:
        property_data = properties[property_id]
        
        customer_success = False
        if is_valid_email(customer_email):
            customer_msg = create_customer_email(
                customer_name, customer_email, phone_number, 
                card_number, contract_type, property_data
            )
            if send_email(customer_msg, customer_email):
                st.success(f"✅ تم إرسال البريد إلى {customer_email}")
                customer_success = True
        else:
            st.error("❌ البريد الإلكتروني غير صحيح")
        
        admin_msg = create_admin_notification(
            customer_name, customer_email, phone_number, 
            contract_type, property_data, admin_email
        )
        admin_success = send_email(admin_msg, admin_email)
        if admin_success:
            st.success("✅ تم إرسال إشعار للمشرف")
        
        return customer_success or admin_success
        
    except smtplib.SMTPAuthenticationError:
        st.error("❌ خطأ في تسجيل الدخول! تحقق من صحة الإيميل وكلمة المرور")
        return False
    except Exception as e:
        st.error(f"❌ خطأ غير متوقع: {e}")
        return False
