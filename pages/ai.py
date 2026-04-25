import streamlit as st

st.set_page_config(page_title="EmlakHub - مساعد AI", page_icon="🤖", layout="wide")

st.title("🤖 مساعد الموقع")
st.write("اسألني أي شيء عن العقارات أو خدمات الموقع، وسأساعدك بسرعة.")
st.markdown("---")

# Simple navigation
st.sidebar.title("🏠 EmlakHub")
st.sidebar.write("منصة العقارات الشاملة")
if st.sidebar.button("المعرض"):
    st.switch_page("pages/gallery.py")
if st.sidebar.button("من نحن"):
    st.switch_page("pages/about.py")
if st.sidebar.button("نشر عقار"):
    st.switch_page("pages/post_property.py")

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []

st.info("جرّب أسئلة مثل: كيف أبحث عن شقة؟ كيف أنشر عقار؟ ما هي خطوات تسجيل الدخول؟")

with st.form("ai_form"):
    question = st.text_input("اكتب سؤالك هنا", placeholder="مثال: كيف أجد شقة للإيجار؟")
    submit = st.form_submit_button("إرسال")

if submit:
    if question.strip():
        st.session_state.ai_chat_history.append({"user": question})
        q = question.lower()
        if any(k in q for k in ["بيع", "شراء", "شراء عقار", "عقارات للبيع", "عقار للبيع", "بيع عقار"]):
            answer = "يمكنك البحث عن عقارات للبيع في صفحة المعرض، وتحسين النتائج باستخدام مرشح النوع والسعر."
        elif any(k in q for k in ["إيجار", "ايجار", "شقة للإيجار", "منزل للإيجار", "عقارات للإيجار", "الإيجار"]):
            answer = "في المعرض يمكنك استخدام البحث المرن للعثور على العقارات المتاحة للإيجار حسب العنوان أو المنطقة."
        elif any(k in q for k in ["سعر", "ميزانية", "تكلفة", "ثمن"]):
            answer = "الأسعار تظهر في كل بطاقة عقار. يمكنك تعديل نطاق السعر في معرض العقارات للعثور على الخيارات المناسبة."
        elif any(k in q for k in ["تسجيل", "حساب", "دخول", "إنشاء حساب", "signup", "login"]):
            answer = "أنشئ حسابك من صفحة التسجيل ثم سجل الدخول لبدء نشر العقار أو متابعة العروض."
        elif any(k in q for k in ["تواصل", "مساعدة", "استفسار", "خدمة العملاء"]):
            answer = "يمكنك إرسال رسالة من صفحة من نحن، أو طرح سؤالك هنا وسيصلك رد مساعد الموقع."
        elif any(k in q for k in ["تفاصيل", "عرض التفاصيل", "description"]):
            answer = "اضغط على أي عقار في معرض العقارات للدخول إلى صفحة التفاصيل ثم عرض العقد."
        else:
            answer = "أنا مساعد افتراضي مرتبط بالموقع لمساعدتك في البحث عن عقارات وخدمات المنصة. اطرح سؤالك وسأجاوبك."
        st.session_state.ai_chat_history.append({"bot": answer})
    else:
        st.warning("من فضلك اكتب سؤالاً قبل الإرسال.")

if st.session_state.ai_chat_history:
    st.markdown("---")
    for message in st.session_state.ai_chat_history:
        if "user" in message:
            st.markdown(f"**سؤال العميل:** {message['user']}")
        if "bot" in message:
            st.markdown(f"**الرد:** {message['bot']}")

st.markdown("---")
if st.button("الذهاب إلى المعرض", use_container_width=True):
    st.switch_page("pages/gallery.py")
