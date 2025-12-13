import streamlit as st
import os
from PIL import Image
from data.properties_data import properties


st.set_page_config(
    page_title="EmlakHub - Home",
    page_icon="🏠",
    layout="wide"
)


st.title('Gallery')
st.write('---')


if properties:
    cols = st.columns(4)
    
    for idx, (property_id, property_data) in enumerate(properties.items()):
        try:
            image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), property_data['image'])
            img = Image.open(image_path)
            
            with cols[idx % 4]:
                # card_container = st.container(border=True)
                # with card_container:
                    with st.form(key=f'buy_{idx}'):
                        st.image(img, output_format='auto', caption=property_id, use_container_width=True)
                        st.write(f"**السعر:** {property_data['price']}")
                        st.write(f"**العنوان:** {property_data['address']}")
                        st.write(f"**الغرف:** {property_data['rooms']}")
                        st.write(f"**المساحة:** {property_data['space']}")
                        
                        if st.form_submit_button('عرض التفاصيل'):
                            st.session_state.selected_property = property_id
                            # st.session_state.selected_image = image_path  
                            st.switch_page("pages/poperty_details.py")
                
        except Exception as e:
            st.error(f'خطأ في تحميل العقار {property_id}: {str(e)}')

else:
    st.warning('لم يتم العثور على أي عقارات')