import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from data.properties_data import properties


SENDER_EMAIL = "omarhamissa2007@gmail.com"
SENDER_PASSWORD = "qiqe tssr sqmk tlzr"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# --- EMAIL TEMPLATES ---

CUSTOMER_EMAIL_TEMPLATE = """
مرحباً {customer_name}،

تم استلام بيانات العقد الخاص بك بنجاح! ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 تفاصيل العقد:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 الاسم الكامل: {customer_name}
📞 رقم الهاتف: {phone_number}
💳 رقم البطاقة: {card_number}
📑 نوع العقد: {contract_type}
🏠 نوع العقار: {property_type}
💰 السعر: {price}
📍 العنوان: {address}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

سيتم مراجعة بياناتك والتواصل معك خلال 24 ساعة.

مع أطيب التحيات،
فريق إدارة العقارات
"""

ADMIN_NOTIFICATION_TEMPLATE = """
📋 *إشعار جديد - عقد*

تم إرسال عقد جديد من:

👤 الاسم: {customer_name}
📧 الإيميل: {customer_email}
📞 الهاتف: {phone_number}
🏠 نوع العقار: {property_type}
💰 السعر: {price}
📍 العنوان: {address}
📑 نوع العقد: {contract_type}

يرجى مراجعة النظام لمزيد من التفاصيل.
"""

POST_PROPERTY_TEMPLATE = """
مرحباً،

تم نشر عقارك الجديد بنجاح على منصة EmlakHub! 🏡

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 تفاصيل العقار:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏠 اسم العقار: {name}
💰 السعر: {price}
📍 العنوان: {address}
🛏️ الغرف: {rooms}
📐 المساحة: {space}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

شكراً لاستخدامك منصتنا.

مع أطيب التحيات،
فريق إدارة العقارات
"""


def create_customer_email(
    customer_name,
    customer_email,
    phone_number,
    card_number,
    contract_type,
    property_data,
):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = customer_email
    msg["Subject"] = f"✅ تأكيد العقد - {customer_name}"

    body = CUSTOMER_EMAIL_TEMPLATE.format(
        customer_name=customer_name,
        phone_number=phone_number,
        card_number=card_number,
        contract_type=contract_type,
        property_type=property_data["type"],
        price=property_data.get("price", "غير محدد"),
        address=property_data.get("address", "غير محدد"),
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def create_admin_notification(
    customer_name,
    customer_email,
    phone_number,
    contract_type,
    property_data,
    admin_email,
):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = admin_email
    msg["Subject"] = f"📋 إشعار عقد جديد - {customer_name}"

    body = ADMIN_NOTIFICATION_TEMPLATE.format(
        customer_name=customer_name,
        customer_email=customer_email,
        phone_number=phone_number,
        property_type=property_data["type"],
        price=property_data.get("price", "غير محدد"),
        address=property_data.get("address", "غير محدد"),
        contract_type=contract_type,
    )

    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def create_post_property_email(property_data, user_email):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = user_email
    msg["Subject"] = f"✅ تم نشر عقارك بنجاح - {property_data.get('name', '')}"

    body = POST_PROPERTY_TEMPLATE.format(
        name=property_data.get("name", ""),
        price=property_data.get("price", ""),
        address=property_data.get("address", ""),
        rooms=property_data.get("rooms", ""),
        space=property_data.get("space", ""),
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def send_email(message, recipient_email):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        return True
    except smtplib.SMTPAuthenticationError:
        st.error(
            "❌ خطأ في المصادقة: كلمة مرور التطبيق (App Password) غير صحيحة أو منتهية الصلاحية."
        )
        st.warning("""
        ⚠️ **مطلوب إجراء من المشرف**:
        يرجى تحديث `SENDER_PASSWORD` في ملف `notifications/email_sender.py` بكلمة مرور تطبيق جديدة صالحة من Google.
        """)
        return False
    except Exception as e:
        st.error(f"❌ خطأ غير متوقع في إرسال البريد: {e}")
        return False


def is_valid_email(email):
    return email and "@" in email


def send_contract_email(
    customer_name,
    customer_email,
    phone_number,
    card_number,
    contract_type,
    property_id,
    admin_email="omarhamissa2007@gmail.com",
):
    try:
        property_data = properties[property_id]

        customer_success = False
        if is_valid_email(customer_email):
            customer_msg = create_customer_email(
                customer_name,
                customer_email,
                phone_number,
                card_number,
                contract_type,
                property_data,
            )
            if send_email(customer_msg, customer_email):
                st.success(f"✅ تم إرسال البريد إلى {customer_email}")
                customer_success = True
        else:
            st.error("❌ البريد الإلكتروني غير صحيح")

        admin_msg = create_admin_notification(
            customer_name,
            customer_email,
            phone_number,
            contract_type,
            property_data,
            admin_email,
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


def send_post_property_email_notification(property_data, user_email):
    if not is_valid_email(user_email):
        st.warning("⚠️ لم يتم العثور على بريد إلكتروني صالح لإرسال التأكيد.")
        return False

    try:
        msg = create_post_property_email(property_data, user_email)
        if send_email(msg, user_email):
            st.success(f"✅ تم إرسال رسالة تأكيد النشر إلى {user_email}")
            return True
        return False
    except Exception as e:
        st.error(f"❌ خطأ في إرسال تأكيد النشر: {e}")
        return False
