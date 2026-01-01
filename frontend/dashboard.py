import streamlit as st
import requests

# --- Configuration ---
st.set_page_config(
    page_title="Mythical Creature Dashboard",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"

# --- Pixel-Perfect CSS (Extracted from User HTML) ---
st.markdown(
    """
<style>
    /* VARIABLES (Tailwind Config) */
    :root {
        --color-primary: #7f13ec;
        --color-bg-dark: #191022;
        --color-surface-dark: #261933;
        --color-border-dark: #4d3267;
        --color-text-muted: #ad92c9;
        --color-white: #ffffff;
        --color-success: #4ade80; /* emerald-400 */
        --color-danger: #ef4444; /* red-500 */
        --color-warning: #eab308; /* yellow-500 */
    }

    /* GLOBAL RESET & FONTS */
    .stApp {
        background-color: var(--color-bg-dark);
        color: var(--color-white);
        font-family: 'Space Grotesk', 'Noto Sans', sans-serif;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: var(--color-bg-dark);
        border-right: 1px solid var(--color-border-dark);
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px;
        margin-bottom: 24px;
    }
    .user-avatar {
        width: 48px;
        height: 48px;
        border-radius: 9999px;
        border: 2px solid var(--color-primary);
        background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuDJ04_kiv_eXMKK7q6dBDpl0GbckGVvqgDlx7Scg_WIDxfhuMVHZrJ-OPOZM2dTsS9SSf3Le6HrGacvT9SvvQuCOV8IKZfA6MXE45D4E67k1Pyo1N2dyqQm0SamvPybuJS-K79_ZQCwEOURuwaEWXXr5demS0gEi6qLkMFAbMLBL_cZIsknSrxe84Znlk_TqUn4bZ1HOtb_yoIi5vt5CJc7Mo-mxmHh_KAPoT4ITi8a_SB6cCfjhobTn7DNpbNDog01W1aKRusnDoo");
        background-size: cover;
    }
    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        border-radius: 8px;
        color: var(--color-text-muted);
        text-decoration: none;
        transition: all 0.2s;
        cursor: pointer;
    }
    .nav-item.active {
        background-color: var(--color-primary);
        color: white;
        box-shadow: 0 4px 10px rgba(127, 19, 236, 0.25);
    }
    .nav-item:hover:not(.active) {
        background-color: var(--color-surface-dark);
        color: white;
    }

    /* METRIC CARDS */
    .metric-card {
        background-color: var(--color-surface-dark);
        border: 1px solid var(--color-border-dark);
        border-radius: 12px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .metric-label {
        font-size: 14px;
        font-weight: 500;
        color: var(--color-text-muted);
    }
    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: white;
    }
    .metric-trend {
        font-size: 12px;
        font-weight: 500;
        display: flex;
        align-items: center;
        margin-top: 4px;
    }
    
    /* TABLE HEADER STYLING */
    .table-header {
        background-color: rgba(25, 16, 34, 0.5);
        border-bottom: 1px solid var(--color-border-dark);
        padding: 16px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--color-text-muted);
        margin-bottom: 8px;
    }

    /* TABLE ROW STYLING (For Streamlit Columns) */
    .table-row {
        padding: 12px 0;
        border-bottom: 1px solid var(--color-border-dark);
        align-items: center;
        transition: background-color 0.2s;
    }
    .table-row:hover {
        background-color: rgba(25, 16, 34, 0.3);
    }

    /* BADGES */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        border: 1px solid;
    }
    
    /* PROGRESS BAR */
    .progress-bg {
        width: 100%;
        height: 6px;
        background-color: var(--color-bg-dark);
        border-radius: 9999px;
        margin-top: 6px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 9999px;
    }

    /* FORM STYLING */
    div[data-testid="stDialog"] {
        background-color: var(--color-surface-dark);
        color: white;
    }

    /* HIDE STREAMLIT CHROME */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
</style>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
""",
    unsafe_allow_html=True,
)


# --- Helper Functions ---
def get_creatures():
    try:
        response = requests.get(f"{API_URL}/creatures/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def add_creature(payload):
    try:
        requests.post(f"{API_URL}/creatures/", json=payload)
    except Exception as e:
        st.error(f"Failed to summon: {e}")


def update_creature(id, payload):
    try:
        requests.put(f"{API_URL}/creatures/{id}", json=payload)
    except Exception as e:
        st.error(f"Failed to update: {e}")


def delete_creature(id):
    try:
        requests.delete(f"{API_URL}/creatures/{id}")
    except Exception as e:
        st.toast(f"Registry Error: Could not banish entity. {e}")


# List of standard classes
STD_CLASSES = ["Avian", "Reptilian", "Aquatic", "Equine", "Hybrid", "Other"]

# --- Sidebar Content ---
with st.sidebar:
    st.markdown(
        """
    <div class="user-profile">
        <div class="user-avatar"></div>
        <div>
            <div style="font-weight: 700; font-size: 16px;">Merlin's Admin</div>
            <div style="color: var(--color-text-muted); font-size: 14px;">High Summoner</div>
        </div>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 8px;">
        <div class="nav-item active">
            <span class="material-symbols-outlined">menu_book</span>
            Bestiary Registry
        </div>
        <div class="nav-item">
            <span class="material-symbols-outlined">map</span>
            Realm Map
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="nav-item">
            <span class="material-symbols-outlined">settings</span>
            Settings
        </div>
        <div class="nav-item" style="color: #ef4444;">
            <span class="material-symbols-outlined">logout</span>
            Log Out
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- Main Content ---

# Header Section
col_head, col_btn = st.columns([3, 1])
with col_head:
    st.markdown(
        """
    <h1 style="font-size: 36px; font-weight: 900; margin-bottom: 8px;">Bestiary Registry</h1>
    <p style="color: var(--color-text-muted);">Manage and monitor all mythical entities across the known realms.</p>
    """,
        unsafe_allow_html=True,
    )


# Dialog for creation
@st.dialog("Summon New Creature")
def summon_dialog():
    st.write("Enter details for the new entity.")

    # Dynamic Class Logic (fetch inside dialog)
    creatures = get_creatures()
    existing_types = {c["creature_type"] for c in creatures}
    all_classes = sorted(list(set(STD_CLASSES) | existing_types))

    with st.form("summon_form", clear_on_submit=True):
        name = st.text_input("Creature Name", placeholder="e.g. Phoenix")

        # Class logic
        selected_class = st.selectbox("Class", all_classes)
        c_type = selected_class

        # Text input for custom class
        new_class_input = st.text_input(
            "Or type a new Class (leave empty to use dropdown):"
        )

        myth = st.text_input("Mythology", placeholder="e.g. Greek")
        danger = st.slider("Danger Level", 1, 10, 5)
        habitat = st.text_input("Habitat", placeholder="e.g. Volcanic Peaks")

        # Submit Button inside the form
        submitted = st.form_submit_button(
            "Summon Entity", type="primary", use_container_width=True
        )

        if submitted:
            final_class = new_class_input if new_class_input.strip() else c_type

            if name and final_class:
                payload = {
                    "name": name,
                    "creature_type": final_class,
                    "mythology": myth,
                    "danger_level": danger,
                    "habitat": habitat or "Unknown",
                }

                try:
                    st.toast("Summoning entity...", icon="⏳")
                    response = requests.post(f"{API_URL}/creatures/", json=payload)

                    if response.status_code == 200:
                        st.success("Summoned successfully!")
                        import time

                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Failed to summon: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
            else:
                st.error("Name and Class are required.")


# Dialog for Editing
@st.dialog("Edit Creature")
def edit_dialog(creature):
    st.write(f"Editing {creature['name']}")
    name = st.text_input("Creature Name", value=creature["name"])

    # Avatar Preview
    st.write("Avatar Preview:")
    current_image = creature.get("image_url")
    if current_image:
        st.image(current_image, width=100, caption="Current Avatar")
    else:
        st.info("No custom avatar (using default)")

    # Pre-select class logic
    current_class = creature["creature_type"]
    idx = 0
    if current_class in STD_CLASSES:
        idx = STD_CLASSES.index(current_class)
    else:
        idx = STD_CLASSES.index("Other")

    selected_class = st.selectbox("Class", STD_CLASSES, index=idx)
    c_type = selected_class

    if selected_class == "Other":
        # If it was already a custom class, show that value default, otherwise empty
        default_custom = current_class if current_class not in STD_CLASSES else ""
        c_type = st.text_input("Enter new Class type:", value=default_custom)

    myth = st.text_input("Mythology", value=creature["mythology"])
    danger = st.slider("Danger Level", 1, 10, value=creature["danger_level"])

    habitat = st.text_input("Habitat", value=creature.get("habitat", "Unknown"))

    if st.button("Update Entity", type="primary", use_container_width=True):
        if name and c_type:
            payload = {
                "name": name,
                "creature_type": c_type,
                "mythology": myth,
                "danger_level": danger,
                "habitat": habitat,
            }
            update_creature(creature["id"], payload)


with col_btn:
    st.write("")
    if st.button("＋ Summon New Creature", type="primary", use_container_width=True):
        summon_dialog()

st.write("")  # Spacer

# Metrics Section
creatures = get_creatures()
total = len(creatures)
critical_count = sum(1 for c in creatures if c["danger_level"] >= 8)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-label">Total Creatures</span>
            <span class="material-symbols-outlined" style="color: var(--color-primary);">pets</span>
        </div>
        <div>
            <div class="metric-value">{total:,.0f}</div>
            <div class="metric-trend" style="color: var(--color-success);">
                <span class="material-symbols-outlined" style="font-size: 16px; margin-right: 4px;">trending_up</span>
                +5% from last moon
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
            <span class="metric-label">Recently Added</span>
            <span class="material-symbols-outlined" style="color: var(--color-primary);">history</span>
        </div>
        <div>
            <div class="metric-value">{min(total, 12)}</div>
            <div class="metric-trend" style="color: var(--color-success);">
                <span class="material-symbols-outlined" style="font-size: 16px; margin-right: 4px;">trending_up</span>
                +2% this week
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
            <span class="material-symbols-outlined" style="color: var(--color-danger);">warning</span>
        </div>
        <div>
            <div class="metric-value">{critical_count} Critical</div>
            <div class="metric-trend" style="color: var(--color-danger);">
                <span class="material-symbols-outlined" style="font-size: 16px; margin-right: 4px;">trending_up</span>
                Requires attention
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# Table Header (Custom HTML) - Removed Last Sighting
st.markdown(
    """
<div class="table-header" style="display: flex;">
    <div style="flex: 2;">Creature Name</div>
    <div style="flex: 1;">Class</div>
    <div style="flex: 2;">Danger Level</div>
    <div style="flex: 1.5;">Habitat</div>
    <div style="flex: 1; text-align: right;">Actions</div>
</div>
""",
    unsafe_allow_html=True,
)

# Table Rows (Streamlit Iteration for Interactivity)
for c in creatures:
    with st.container():
        # CSS Styling wrapper for the row
        st.markdown('<div class="table-row">', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns([2, 1, 2, 1.5, 1])

        # 1. Name & Avatar
        with c1:
            avatar_url = (
                c.get("image_url")
                or f"https://api.dicebear.com/7.x/identicon/svg?seed={c['name']}"
            )

            # Use native st.image for better reliability than CSS background-image
            # We use a nested column layout here to control size
            sub_c1, sub_c2 = st.columns([1, 3])
            with sub_c1:
                st.image(avatar_url, width=40)
                st.caption(f"[Link]({avatar_url})")  # Debug link
            with sub_c2:
                st.markdown(
                    f"<div style='margin-top: 8px; font-weight: 700;'>{c['name']}</div>",
                    unsafe_allow_html=True,
                )

        # 2. Class Badge
        with c2:
            ctype = c["creature_type"].lower()
            badge_style = (
                "background: rgba(45, 43, 59, 0.5); color: white; border-color: #555;"
            )
            if "avian" in ctype:
                badge_style = "background: rgba(249, 115, 22, 0.1); color: #fb923c; border-color: rgba(249, 115, 22, 0.2);"
            elif "reptile" in ctype or "reptilian" in ctype:
                badge_style = "background: rgba(34, 197, 94, 0.1); color: #4ade80; border-color: rgba(34, 197, 94, 0.2);"
            elif "water" in ctype or "aquatic" in ctype:
                badge_style = "background: rgba(6, 182, 212, 0.1); color: #22d3ee; border-color: rgba(6, 182, 212, 0.2);"
            elif "equine" in ctype:
                badge_style = "background: rgba(59, 130, 246, 0.1); color: #60a5fa; border-color: rgba(59, 130, 246, 0.2);"
            elif "hybrid" in ctype:
                badge_style = "background: rgba(168, 85, 247, 0.1); color: #c084fc; border-color: rgba(168, 85, 247, 0.2);"

            st.markdown(
                f"<div class='badge' style='{badge_style} border: 1px solid;'>{c['creature_type']}</div>",
                unsafe_allow_html=True,
            )

        # 3. Danger Level
        with c3:
            danger_val = c["danger_level"] * 10
            danger_color = "var(--color-primary)"
            if danger_val >= 80:
                danger_color = "var(--color-danger)"
            elif danger_val >= 50:
                danger_color = "#eab308"
            elif danger_val <= 30:
                danger_color = "var(--color-success)"

            st.markdown(
                f"""
            <div style="display: flex; flex-direction: column; gap: 4px;">
                <div style="display: flex; justify-content: space-between; font-size: 12px; color: var(--color-text-muted);">
                    <span style="color: {danger_color}; font-weight: 600;">Level {c["danger_level"]}</span>
                    <span>{danger_val}/100</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {danger_val}%; background-color: {danger_color};"></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # 4. Habitat
        with c4:
            st.markdown(
                f"<span style='color: var(--color-text-muted);'>{c.get('habitat', 'Unknown')}</span>",
                unsafe_allow_html=True,
            )

        # 5. Actions (Buttons!)
        with c5:
            # We use small columns for icons to keep them tight
            ac1, ac2 = st.columns(2)
            with ac1:
                if st.button("✏️", key=f"edit_{c['id']}", help="Edit Creature"):
                    edit_dialog(c)
            with ac2:
                st.button(
                    "🗑️",
                    key=f"del_{c['id']}",
                    help="Banish Entity",
                    on_click=delete_creature,
                    args=(c["id"],),
                )

        st.markdown("</div>", unsafe_allow_html=True)  # End row wrapper
