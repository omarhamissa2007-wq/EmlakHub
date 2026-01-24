import streamlit as st
from PIL import Image
from data.properties_data import properties
from utils import get_image_path

st.markdown(
    """
    <style>
        .stButton > button {
            color: #ffd700 !important;
            font-weight: bold !important;
            background-color: transparent !important;
            border: 1px solid #ffd700 !important;
            border-radius: 5px !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.set_page_config(page_title="EmlakHub - Home", page_icon="🏠", layout="wide")


st.title("Gallery")
st.write("---")


if properties:
    cols = st.columns(4)

    for index, (property_id, property_data) in enumerate(properties.items()):
        try:
            image_path = get_image_path(property_data["image"])
            img = Image.open(image_path)

            col_index = index % 4
            with cols[col_index]:
                with st.form(key=f"buy_{index}"):
                    st.image(
                        img,
                        output_format="auto",
                        caption=property_id,
                        use_container_width=True,
                    )
                    st.write(f"**السعر:** {property_data['price']}")
                    st.write(f"**العنوان:** {property_data['address']}")
                    st.write(f"**الغرف:** {property_data['rooms']}")
                    st.write(f"**المساحة:** {property_data['space']}")

                    if st.form_submit_button("عرض التفاصيل"):
                        st.session_state.selected_property = property_id
                        st.switch_page("pages/property_details.py")

        except Exception as e:
            st.error(f"خطأ في تحميل العقار {property_id}: {str(e)}")

else:
    st.warning("لم يتم العثور على أي عقارات")
