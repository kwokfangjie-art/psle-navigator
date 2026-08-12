import streamlit as st


# ==================================================
# LOGIN
# ==================================================

def require_login():
    """
    Simple two-user authentication for PathFinder.

    Credentials are stored in Streamlit Secrets.

    Roles:
    - Admin
    - User
    """

    # ----------------------------------------------
    # Already authenticated
    # ----------------------------------------------

    if st.session_state.get("authenticated"):
        return


    # ----------------------------------------------
    # Hide navigation while logged out
    # ----------------------------------------------

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }

            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # Login screen
    # ----------------------------------------------

    st.title("🔐 PathFinder")

    st.write(
        "Sign in to access the educational prototype."
    )

    st.caption(
        "This application is restricted to authorised "
        "users for assessment purposes."
    )

    st.divider()


    # ----------------------------------------------
    # Login form
    # ----------------------------------------------

    with st.form(
        "login_form"
    ):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Sign in",
            type="primary",
            use_container_width=True
        )


    # ----------------------------------------------
    # Validate credentials
    # ----------------------------------------------

    if submitted:

        username = username.strip()

        admin_username = st.secrets[
            "ADMIN_USERNAME"
        ]

        admin_password = st.secrets[
            "ADMIN_PASSWORD"
        ]

        user_username = st.secrets[
            "USER_USERNAME"
        ]

        user_password = st.secrets[
            "USER_PASSWORD"
        ]


        # ------------------------------------------
        # ADMIN
        # ------------------------------------------

        if (
            username == admin_username
            and password == admin_password
        ):

            st.session_state[
                "authenticated"
            ] = True

            st.session_state[
                "username"
            ] = username

            st.session_state[
                "role"
            ] = "Admin"

            st.rerun()


        # ------------------------------------------
        # USER
        # ------------------------------------------

        elif (
            username == user_username
            and password == user_password
        ):

            st.session_state[
                "authenticated"
            ] = True

            st.session_state[
                "username"
            ] = username

            st.session_state[
                "role"
            ] = "User"

            st.rerun()


        # ------------------------------------------
        # INVALID
        # ------------------------------------------

        else:

            st.error(
                "Incorrect username or password."
            )


    # ----------------------------------------------
    # Prevent rest of app from loading
    # ----------------------------------------------

    st.stop()


# ==================================================
# LOGOUT
# ==================================================

def logout():

    keys_to_clear = [
        "authenticated",
        "username",
        "role",
        "student_profile",
        "chat_messages"
    ]

    for key in keys_to_clear:

        if key in st.session_state:

            del st.session_state[
                key
            ]

    st.rerun()


# ==================================================
# ADMIN CHECK
# ==================================================

def require_admin():

    if (
        st.session_state.get(
            "role"
        )
        != "Admin"
    ):

        st.error(
            "This page is available to administrators only."
        )

        st.stop()


# ==================================================
# CURRENT USER
# ==================================================

def get_current_user():

    return {
        "username": st.session_state.get(
            "username"
        ),

        "role": st.session_state.get(
            "role"
        )
    }
