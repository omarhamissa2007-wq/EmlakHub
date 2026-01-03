import streamlit as st
import os
from PIL import Image
from data.properties_data import properties


st.set_page_config(page_title="EmlakHub - Home", page_icon="🏠", layout="wide")


st.title("Gallery")
st.write("---")


def get_image_path(image_rel_path):
    root_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root_dir, image_rel_path)


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
