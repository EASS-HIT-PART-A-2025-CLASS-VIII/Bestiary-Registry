import api_utils
import streamlit as st
import api_client


# --- Flash Message Check ---
if "toast_msg" in st.session_state:
    msg, icon = st.session_state.pop("toast_msg")
    st.toast(msg, icon=icon)


@st.dialog("Edit Class")
def edit_class_dialog(c):
    st.markdown(f"**Edit {c['name']}**")

    # Pre-fill color
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
            api_client.update_class(c["id"], payload)
            api_utils.clear_cache()
            st.session_state["toast_msg"] = ("Class Updated!", "✅")
            st.rerun()
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
                api_client.delete_class(c["id"])
                api_utils.clear_cache()
                st.session_state["toast_msg"] = ("Class Deleted!", "🗑️")
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
        # Fetch existing classes
        classes = api_utils.get_classes()
        if not classes:
            st.warning("Backend offline or no classes found.")

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
                            api_client.create_class(payload)
                            api_utils.clear_cache()
                            st.session_state["toast_msg"] = (
                                f"Class '{new_name}' added!",
                                "✨",
                            )
                            st.rerun()
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
