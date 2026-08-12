import streamlit as st
from utils.auth import require_login, logout


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="PSLE Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

require_login()


# ==================================================
# SIDEBAR USER INFO
# ==================================================

with st.sidebar:

    st.write(
        f"👤 **{st.session_state.get('username')}**"
    )

    st.caption(
        f"Role: {st.session_state.get('role')}"
    )

    if st.button(
        "Sign out",
        use_container_width=True
    ):

        logout()

    st.divider()
    

# ==================================================
# DEFINE NAVIGATION
# ==================================================

home_page = st.Page(
    "pages/home_content.py",
    title="Home",
    icon="🏠"
)

school_explorer_page = st.Page(
    "pages/1_🎓_School_Explorer.py",
    title="School Explorer",
    icon="🎓"
)

ai_navigator_page = st.Page(
    "pages/2_🤖_AI_Navigator.py",
    title="AI Navigator",
    icon="🤖"
)

about_page = st.Page(
    "pages/4_ℹ️_About_Us.py",
    title="About Us",
    icon="ℹ️"
)

methodology_page = st.Page(
    "pages/5_🔬_Methodology.py",
    title="Methodology",
    icon="🔬"
)


navigation = st.navigation(
    [
        home_page,
        school_explorer_page,
        ai_navigator_page,
        about_page,
        methodology_page
    ]
)

navigation.run()
