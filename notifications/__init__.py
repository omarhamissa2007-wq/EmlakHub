from .email_sender import send_contract_email
import streamlit as st

def send_message(name, phone_number, card_number, contract_type, property_id, use_whatsapp=False, use_email=True, email=None):
    
    success = False
    
    # Only send email for now (WhatsApp disabled)
    if use_email and email:
        email_sent = send_contract_email(
            customer_name=name,
            customer_email=email,
            phone_number=phone_number,
            card_number=card_number,
            contract_type=contract_type,
            property_id=property_id
        )
        success = email_sent
    
    if not success:
        st.warning("⚠️ لم يتم إرسال الإشعار. يرجى التأكد من صحة البريد الإلكتروني.")

    return success
