import requests
import api_utils
import streamlit as st

API_URL = "http://localhost:8000"


@st.dialog("Edit Class")
def edit_class_dialog(c):
    st.markdown(f"**Edit {c['name']}**")

    # Pre-fill simple color if possible (this is tricky from rgba, so we default to black if parsing fails, user picks new)
    # Attempt to parse hex from text_color which is what we used for storing exact color
    default_color = c.get("text_color", "#9333ea")

    e_name = st.text_input("Name", value=c["name"])
    e_color = st.color_picker("Color", value=default_color)

    if st.button("Save Changes", type="primary", use_container_width=True):
        # Convert Hex to RGBA
        h = e_color.lstrip("#")
        rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

        payload = {
            "name": e_name,
            "color": f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.1)",
            "border_color": f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.2)",
            "text_color": e_color,
        }
        try:
            res = requests.put(f"{API_URL}/classes/{c['id']}", json=payload)
            if res.status_code == 200:
                api_utils.clear_cache()
                st.success("Updated!")
                st.rerun()
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(f"Error: {e}")


@st.dialog("Delete Class?")
def delete_class_dialog(c):
    st.markdown(f"**Are you sure you want to delete {c['name']}?**")
    st.markdown(
        "This will remove it from filters and usage options. Existing creatures will remain but may lose custom styling."
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Yes, Delete", type="primary", use_container_width=True):
            try:
                requests.delete(f"{API_URL}/classes/{c['id']}")
                api_utils.clear_cache()
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


def render_settings():
    st.markdown("## ⚙️ Settings")

    tab1, tab2 = st.tabs(["Class Management", "General"])

    with tab1:
        st.markdown("### Creature Classes")
        st.markdown("Manage the classes available for summoning and filtering.")

        # Fetch existing classes
        try:
            res = requests.get(f"{API_URL}/classes/")
            if res.status_code == 200:
                classes = res.json()
            else:
                st.error("Failed to fetch classes.")
                classes = []
        except Exception:
            st.error("Backend offline.")
            classes = []

        col_new, col_list = st.columns([1, 2])

        # --- Create New Class ---
        with col_new:
            st.markdown("#### Add New Class")
            with st.form("new_class_form"):
                new_name = st.text_input("Class Name", placeholder="e.g. Celestial")
                new_color = st.color_picker("Badge Color", "#9333ea")

                submitted = st.form_submit_button("Create Class", type="primary")
                if submitted:
                    if not new_name.strip():
                        st.warning("Name cannot be empty.")
                    else:
                        # Hex to RGB conversion
                        h = new_color.lstrip("#")
                        rgb = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))

                        payload = {
                            "name": new_name,
                            "color": f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.1)",
                            "border_color": f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.2)",
                            "text_color": new_color,
                        }

                        try:
                            r = requests.post(f"{API_URL}/classes/", json=payload)
                            if r.status_code == 200:
                                api_utils.clear_cache()
                                st.success(f"Added {new_name}!")
                                st.rerun()
                            else:
                                st.error(r.text)
                        except Exception as e:
                            st.error(f"Error: {e}")

        # --- List Existing with Edit ---
        with col_list:
            st.markdown("#### Existing Classes")
            for c in classes:
                with st.container():
                    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                    with c1:
                        # Preview Badge
                        st.markdown(
                            f'<span class="badge" style="background:{c["color"]}; color:{c["text_color"]}; border-color:{c["border_color"]};">{c["name"]}</span>',
                            unsafe_allow_html=True,
                        )

                    with c2:
                        st.caption(f"ID: {c['id']}")

                    with c3:
                        if c["name"] != "Other":
                            if st.button(
                                "✎", key=f"edit_cls_{c['id']}", help="Edit Class"
                            ):
                                edit_class_dialog(c)

                    with c4:
                        if c["name"] != "Other":
                            if st.button(
                                "✖", key=f"del_{c['id']}", help=f"Delete {c['name']}"
                            ):
                                delete_class_dialog(c)
