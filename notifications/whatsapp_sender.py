import pywhatkit as kit
import streamlit as st
import time
from data.properties_data import properties


# --- WHATSAPP MESSAGES ---

CUSTOMER_MESSAGE_TEMPLATE = """🏠 *تأكيد العقد*

مرحباً *{customer_name}*،

تم استلام بيانات عقدك بنجاح! ✅

━━━━━━━━━━━━━━━━━━━━
📋 *تفاصيل العقد:*
━━━━━━━━━━━━━━━━━━━━

👤 الاسم: {customer_name}
📞 الهاتف: {phone_number}
💳 البطاقة: {card_number}
📑 نوع العقد: {contract_type}
🏠 نوع العقار: {property_type}
💰 السعر: {price}
📍 العنوان: {address}

━━━━━━━━━━━━━━━━━━━━

سيتم التواصل معك خلال 24 ساعة ✨

_تم الإرسال تلقائياً عبر نظام إدارة العقارات_"""

ADMIN_MESSAGE_TEMPLATE = """📋 *إشعار جديد - عقد*

تم إرسال عقد جديد من:

👤 الاسم: {customer_name}
📞 الهاتف: {phone_number}
🏠 نوع العقار: {property_type}
📑 نوع العقد: {contract_type}

يرجى مراجعة النظام لمزيد من التفاصيل."""


def send_whatsapp_message(
    phone_number,
    customer_name,
    card_number,
    contract_type,
    property_id,
    admin_phone="+201008526422",
):
    try:
        # Format customer phone number
        customer_phone = str(phone_number).strip()
        if not customer_phone.startswith("+"):
            customer_phone = "+" + customer_phone

        property_data = properties[property_id]

        # Customer message
        customer_message = CUSTOMER_MESSAGE_TEMPLATE.format(
            customer_name=customer_name,
            phone_number=phone_number,
            card_number=card_number,
            contract_type=contract_type,
            property_type=property_data["type"],
            price=property_data.get("price", "غير محدد"),
            address=property_data.get("address", "غير محدد"),
        )

        # Admin notification
        admin_message = ADMIN_MESSAGE_TEMPLATE.format(
            customer_name=customer_name,
            phone_number=phone_number,
            property_type=property_data["type"],
            contract_type=contract_type,
        )

        # Send to customer
        kit.sendwhatmsg_instantly(
            phone_no=customer_phone,
            message=customer_message,
            wait_time=15,
            tab_close=True,
            close_time=3,
        )

        # Send to admin
        kit.sendwhatmsg_instantly(
            phone_no=admin_phone,
            message=admin_message,
            wait_time=15,
            tab_close=True,
            close_time=3,
        )

        time.sleep(2)  # Small delay for UI feedback
        st.success(f"✅ تم إرسال رسالة WhatsApp إلى {customer_phone}")
        return True

    except Exception as e:
        st.error(f"❌ خطأ في إرسال WhatsApp: {e}")
        st.warning("""
        ⚠️ تأكد من:
        1. WhatsApp Web مفتوح ومسجل دخول
        2. رقم الهاتف صحيح ويبدأ بـ + ورمز الدولة
        3. مثال صحيح: +201001234567
        """)
        return False
