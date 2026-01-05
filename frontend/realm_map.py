import streamlit as st

import os


def show_map():
    st.markdown(
        '<h1 style="font-size: 36px; font-weight: 800; margin: 0; padding: 0;">Realm Map</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color: #ad92c9; margin-top: 6px;">Explore the territories of known mythical entities.</p>',
        unsafe_allow_html=True,
    )

    st.write("")

    try:
        img_path = os.path.join(os.path.dirname(__file__), "pictures/creatureMap.jpg")
        st.image(img_path, use_container_width=True)
    except Exception as e:
        st.error(f"Map image not found: {e}")
