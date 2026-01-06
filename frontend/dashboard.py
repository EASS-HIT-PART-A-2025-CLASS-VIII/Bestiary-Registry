import streamlit as st
import requests
import datetime
import realm_map
import sidebar
import settings
from st_keyup import st_keyup
import streamlit.components.v1 as components
import os
import api_utils
import api_client


st.set_page_config(
    page_title="Mythical Creature Dashboard",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
)




def load_css():
    # Inject Fonts (Material Symbols etc.)
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
    """,
        unsafe_allow_html=True,
    )

    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


def format_time_ago(iso_str):
    try:
        # Handle "Just now" or "Unknown" legacy data
        if not iso_str or "T" not in str(iso_str):
            return iso_str or "Unknown"

        dt = datetime.datetime.fromisoformat(str(iso_str))
        now = datetime.datetime.now(datetime.timezone.utc)

        # Ensure dt is aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)

        diff = now - dt
        seconds = diff.total_seconds()

        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            return f"{int(seconds // 60)} min ago"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} hours ago"
        else:
            return f"{int(seconds // 86400)} days ago"
    except Exception:
        return iso_str


def get_creatures():
    return api_utils.get_creatures()


def get_classes():
    return api_utils.get_classes()


def delete_creature(id):
    try:
        api_client.delete_creature(id)
        api_utils.clear_cache()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False


def update_creature(id, payload):
    try:
        api_client.update_creature(id, payload)
        api_utils.clear_cache()
    except Exception as e:
        st.error(f"Error: {e}")


@st.dialog("Summon New Creature")
def summon_dialog():
    classes_data = get_classes()

    # ... (skipping unchanged lines) ...

    # Extract just names for dropdown
    std_names = [c["name"] for c in classes_data]

    # Ensure "Other" is available for creating new ones
    if "Other" not in std_names:
        std_names.append("Other")

    # Force "Other" to be first
    if "Other" in std_names:
        std_names.remove("Other")
        std_names.insert(0, "Other")

    all_classes = std_names

    # Remove st.form to allow dynamic "Other" field
    st.markdown("### Entity Details")
    name = st.text_input("Name", placeholder="e.g. Phoenix", key="summon_name")

    # Dynamic Layout: Check session state for current class to decide layout
    # Default to first class if not in state
    if all_classes:
        current_val = st.session_state.get("summon_class", all_classes[0])
    else:
        current_val = "Other"  # Fallback if no classes

    new_class = ""
    selected_class = current_val

    if current_val == "Other":
        # Two columns if "Other" is selected (to show New Class input side-by-side)
        c1, c2 = st.columns(2)
        with c1:
            selected_class = st.selectbox(
                "Class",
                all_classes,
                key="summon_class",
                format_func=lambda x: "𝗢𝘁𝗵𝗲𝗿" if x == "Other" else x,
            )
        with c2:
            new_class = st.text_input("New Class (Optional)", key="summon_new_class")
    else:
        # Full width otherwise
        selected_class = st.selectbox(
            "Class",
            all_classes,
            key="summon_class",
            format_func=lambda x: "𝗢𝘁𝗵𝗲𝗿" if x == "Other" else x,
        )

    myth = st.text_input("Mythology", placeholder="e.g. Greek", key="summon_myth")
    habitat = st.text_input(
        "Habitat", placeholder="e.g. Volcanic Peaks", key="summon_habitat"
    )
    danger = st.slider("Danger Level", 1, 10, 5, key="summon_danger")

    if st.button(
        "Summon Entity", type="primary", use_container_width=True, key="summon_submit"
    ):
        # Validation
        errors = []
        if not name.strip():
            errors.append("Name is required.")
        if not myth.strip():
            errors.append("Mythology is required.")
        if not habitat.strip():
            errors.append("Habitat is required.")
        if selected_class == "Other" and not new_class.strip():
            errors.append("New Class is required when 'Other' is selected.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            final_class = new_class if selected_class == "Other" else selected_class

            payload = {
                "name": name,
                "creature_type": final_class,
                "mythology": myth,
                "danger_level": danger,
                "habitat": habitat,
                # last_modify auto-set by backend
            }
            try:
                api_client.create_creature(payload)
                api_utils.clear_cache()
                st.success("Entity Summoned!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {e}")


@st.dialog("Edit Creature")
def edit_dialog(c):
    # ... (skipping lines) ...
    st.markdown(f"### Edit {c['name']}")
    classes_data = get_classes()
    std_names = [x["name"] for x in classes_data] or ["Other"]

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=c["name"])
        myth = st.text_input("Mythology", value=c["mythology"])
    with col2:
        # Default to current class if in list, else "Other"
        curr_type = c["creature_type"]
        default_idx = std_names.index(curr_type) if curr_type in std_names else 0
        new_type = st.selectbox("Class", std_names, index=default_idx)
        danger = st.slider("Danger Level", 1, 10, value=c["danger_level"])

    habitat = st.text_input("Habitat", value=c.get("habitat", "Unknown"))

    if st.button("Save Changes", type="primary", use_container_width=True):
        payload = {
            "name": name,
            "creature_type": new_type,
            "mythology": myth,
            "danger_level": danger,
            "habitat": habitat,
            # last_modify auto-updated by backend
        }
        update_creature(c["id"], payload)
        # update_creature calls api_utils.clear_cache() now so we don't need to add it here explicitly if we modify update_creature
        st.success("Updated!")
        st.rerun()


@st.dialog("Banish Entity?")
def banish_dialog(c):
    st.markdown(f"**Are you sure you want to banish {c['name']} to eternity?**")
    st.markdown("This action cannot be undone.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Yes, Banish", type="primary", use_container_width=True):
            if delete_creature(c["id"]):
                st.rerun()


# --- Navigation State ---
view = st.query_params.get("view", "registry")

# --- Layout: Sidebar ---
sidebar.render_sidebar(view)  # <--- Delegated implementation

# --- Routing ---
if view == "map":
    realm_map.show_map()
    st.stop()

if view == "settings":
    settings.render_settings()
    st.stop()

# --- Layout: Main Dashboard ---
col_h, col_b = st.columns([3, 1])
with col_h:
    st.markdown(
        '<h1 style="font-size: 36px; font-weight: 800; margin: 0; padding: 0;">Bestiary Registry</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color: #ad92c9; margin-top: 6px;">Manage and monitor all mythical entities across the known realms.</p>',
        unsafe_allow_html=True,
    )
with col_b:
    st.write("")  # Spacer
    if st.button("＋ Summon New Creature", type="primary", use_container_width=True):
        summon_dialog()

st.write("")

# Metrics Logic
creatures = get_creatures()
total = len(creatures)
critical = sum(1 for c in creatures if c["danger_level"] >= 9)

# Calculate monthly activity
now = datetime.datetime.now(datetime.timezone.utc)
start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
month_name = start_of_month.strftime("%B")

added_this_month = 0
added_last_24h = 0
one_day_ago = now - datetime.timedelta(days=1)

for c in creatures:
    try:
        lm = c.get("last_modify")
        if lm and lm != "Unknown":
            dt = datetime.datetime.fromisoformat(str(lm))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)

            # Monthly Check
            if dt >= start_of_month:
                added_this_month += 1

            # 24h Check
            if dt >= one_day_ago:
                added_last_24h += 1
    except Exception:
        pass

# Metrics UI
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Total Creatures</span>
            <span class="material-symbols-outlined" style="color: #7f13ec;">pets</span>
        </div>
        <div>
            <div class="metric-value">{total:,.0f}</div>
            <div class="metric-trend" style="color: #4ade80;">
                <span class="material-symbols-outlined" style="font-size: 16px;">trending_up</span>
                <span>+{added_this_month} from last moon</span>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Recent Activity</span>
            <span class="material-symbols-outlined" style="color: #7f13ec;">history</span>
        </div>
        <div>
            <div class="metric-value">{added_last_24h}</div>
            <div class="metric-trend" style="color: #4ade80;">
                <span class="material-symbols-outlined" style="font-size: 16px;">trending_up</span>
                <span>Last 24 Hours</span>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Danger Alerts</span>
            <span class="material-symbols-outlined" style="color: #ef4444;">warning</span>
        </div>
        <div>
            <div class="metric-value">{critical} Critical</div>
            <div class="metric-trend" style="color: #ef4444;">
                <span class="material-symbols-outlined" style="font-size: 16px;">trending_up</span>
                <span>Requires attention</span>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.write("")

# Search & Filter
# Using columns with manual markdown icons not perfect, sticking to input with placeholders as cleaner in Python
s_col, f_col = st.columns([2, 1])
with s_col:
    # Custom search icon styling
    # We inject a manual icon overlay and use dynamic styles into the iframe
    st.markdown(
        """
<div style="
    font-family: 'Material Symbols Outlined';
    position: absolute;
    z-index: 9999;
    top: -5px;
    margin-top: 10px;
    left: 10px;
    color: #ad92c9;
    pointer-events: none;
    font-size: 20px;
">search</div>
""",
        unsafe_allow_html=True,
    )

    components.html(
        """
<script>
(function () {
  function inject() {
    const iframes = parent.document.querySelectorAll(
      'iframe[title*="st_keyup"], iframe[title*="keyup"], iframe[src*="st_keyup"]'
    );

    for (const iframe of iframes) {
      try {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        if (!doc || !doc.head) continue;

        if (doc.getElementById("keyup-custom-style")) return;

        const style = doc.createElement("style");
        style.id = "keyup-custom-style";
        style.textContent = `
          /* UNIVERSAL RESET */
          body { margin: 0; padding: 0; background: transparent !important; }

          /* Force Input Styles - restoring WHITE background */
          input, textarea, [contenteditable] {
            background-color: #ffffff !important; 
            color: #261933 !important; /* Dark text for white background */
            border: 1px solid #4d3267 !important;
            border-radius: 8px !important;
            padding-left: 40px !important;
            outline: none !important;
            box-shadow: none !important;
            font-family: 'Inter', sans-serif !important;
          }

          /* FORCE PURPLE FOCUS */
          input:focus, textarea:focus, 
          input:active, textarea:active,
          input:focus-visible, textarea:focus-visible {
            border-color: #7f13ec !important;
            box-shadow: 0 0 0 2px #7f13ec !important; /* 2px Purple Ring */
            outline: none !important;
          }

          input::placeholder {
            color: #ad92c9 !important;
            opacity: 0.8 !important;
            font-weight: 400 !important;
          }
        `;
        doc.head.appendChild(style);
        return;
      } catch (e) {}
    }
  }

  setInterval(inject, 200);
})();
</script>
""",
        height=0,
    )

    search_q = st_keyup(
        "Search",
        placeholder="Search creatures by name...",
        label_visibility="collapsed",
    )
with f_col:
    # Advanced Filters Popover
    with st.popover("Filter Options", use_container_width=True):
        st.markdown("### Filter Entities")

        # 1. Extract Unique Values
        all_types = sorted(list({c["creature_type"] for c in creatures}))
        all_myths = sorted(list({c["mythology"] for c in creatures}))
        all_habitats = sorted(list({c.get("habitat", "Unknown") for c in creatures}))

        # 2. Controls
        sel_types = st.multiselect("Class", all_types)
        sel_myths = st.multiselect("Mythology", all_myths)
        sel_habitats = st.multiselect("Habitat", all_habitats)
        sel_danger = st.slider("Danger Level", 1, 10, (1, 10))

# Apply Filters
filtered = creatures

# Initial Search Filter
if search_q:
    filtered = [c for c in filtered if search_q.lower() in c["name"].lower()]

# Advanced Filters
if sel_types:
    filtered = [c for c in filtered if c["creature_type"] in sel_types]
if sel_myths:
    filtered = [c for c in filtered if c["mythology"] in sel_myths]
if sel_habitats:
    filtered = [c for c in filtered if c.get("habitat", "Unknown") in sel_habitats]

# Danger Range
min_d, max_d = sel_danger
filtered = [c for c in filtered if min_d <= c["danger_level"] <= max_d]

# --- Table ---
st.markdown('<div class="table-container">', unsafe_allow_html=True)

# Header Row
cols = st.columns([1.8, 1, 1.5, 2, 1.4, 1.2, 1])
headers = [
    "Creature Name",
    "Class",
    "Mythology",
    "Danger Level",
    "Habitat",
    "Last Modify",
    "Actions",
]
with st.container():
    st.markdown('<div class="table-header">', unsafe_allow_html=True)

    # We construct the header HTML manually to ensure it sits in the container
    # But to align with Streamlit columns, we actually need to render standard columns
    # and just style them.
    # The container wrapper ".table-header" gives the BG.

    for col, h in zip(cols, headers):
        with col:
            st.markdown(f'<div class="col-header">{h}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Data Rows
for c in filtered:
    st.markdown('<div class="table-row">', unsafe_allow_html=True)

    c1, c2, c3, c4, c5, c6, c7 = st.columns([1.8, 1, 1.5, 2, 1.4, 1.2, 1])

    # 1. Name
    with c1:
        img_url = (
            c.get("image_url")
            or f"https://api.dicebear.com/7.x/identicon/svg?seed={c['name']}"
        )
        st.markdown(
            f"""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="{img_url}" class="avatar-img">
            <span class="text-white font-bold table-text">{c["name"]}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 2. Class
    with c2:
        ctype = c["creature_type"]
        # Dynamic Color Lookup
        classes_data = get_classes()  # Cached

        # Default
        bg, text, border = "rgba(127,19,236,0.1)", "#ad92c9", "rgba(127,19,236,0.2)"

        # Find matching class
        match = next((x for x in classes_data if x["name"] == ctype), None)
        if match:
            bg, text, border = (
                match["color"],
                match["text_color"],
                match["border_color"],
            )

        st.markdown(
            f'<span class="badge" style="background:{bg}; color:{text}; border-color:{border};">{ctype}</span>',
            unsafe_allow_html=True,
        )

    # 3. Myth
    with c3:
        st.markdown(
            f'<span class="text-muted table-text">{c["mythology"]}</span>',
            unsafe_allow_html=True,
        )

    # 4. Danger Level (1-10)
    with c4:
        val = c["danger_level"]

        # 1-3 Low (Green), 4-6 Moderate (Yellow), 7-8 High (Purple), 9-10 Critical (Red)
        if val <= 3:
            label, color = "Low", "#4ade80"
        elif val <= 6:
            label, color = "Moderate", "#FFD700"
        elif val <= 8:
            label, color = "High", "#FFA500"
        else:
            label, color = "Critical", "#EF6F44"

        # Width: val * 10 percent
        width = val * 10

        st.markdown(
            f"""
        <div class="col-danger">
            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px;">
                <span style="color: {color}; font-weight: 700;">{label}</span>
                <span style="color: {color}; font-weight: 600;">{val}/10</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {width}%; background-color: {color};"></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # 5. Habitat
    with c5:
        st.markdown(
            f'<span class="text-muted table-text">{c.get("habitat", "Unknown")}</span>',
            unsafe_allow_html=True,
        )

    # 6. Last Modify
    with c6:
        # relative_time = format_time_ago(c.get("last_modify"))
        relative_time = format_time_ago(c.get("last_modify"))
        st.markdown(
            f'<span class="text-muted table-text">{relative_time}</span>',
            unsafe_allow_html=True,
        )

    # 7. Actions
    with c7:
        ac1, ac2 = st.columns(2)
        with ac1:
            if st.button("✎", key=f"e{c['id']}", help="Edit"):
                edit_dialog(c)
        with ac2:
            if st.button("✖", key=f"d{c['id']}", help="Delete"):
                banish_dialog(c)

    st.markdown("</div>", unsafe_allow_html=True)

# Close container
st.markdown("</div>", unsafe_allow_html=True)
