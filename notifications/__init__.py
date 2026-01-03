from .email_sender import send_contract_email, send_post_property_email_notification
from .whatsapp_sender import send_whatsapp_message


def send_message(
    name,
    phone_number,
    email,
    card_number,
    contract_type,
    property_id,
    use_whatsapp=False,
    use_email=True,
):
    success_email = False
    success_whatsapp = False

    if use_email:
        success_email = send_contract_email(
            customer_name=name,
            customer_email=email,
            phone_number=phone_number,
            card_number=card_number,
            contract_type=contract_type,
            property_id=property_id,
        )

    if use_whatsapp:
        success_whatsapp = send_whatsapp_message(
            phone_number=phone_number,
            customer_name=name,
            card_number=card_number,
            contract_type=contract_type,
            property_id=property_id,
        )

    result = True
    if use_email and not success_email:
        result = False
    if use_whatsapp and not success_whatsapp:
        result = False

    if not use_email and not use_whatsapp:
        return False

    return result


def send_upload_confirmation(property_data, user_email):
    return send_post_property_email_notification(property_data, user_email)
