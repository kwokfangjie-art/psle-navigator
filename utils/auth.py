import streamlit as st


def require_password():
    """
    Simple password gate for the educational prototype.

    The password must be stored in Streamlit Secrets as:
    APP_PASSWORD = "your_password"
    """

    if st.session_state.get("authenticated"):
        return

    st.title("🔐 PSLE Navigator")

    st.write(
        "This prototype is password-protected for assessment purposes."
    )

    password = st.text_input(
        "Enter app password",
        type="password"
    )

    if st.button(
        "Sign in",
        type="primary",
        use_container_width=True
    ):

        if password == st.secrets["APP_PASSWORD"]:

            st.session_state["authenticated"] = True
            st.rerun()

        else:

            st.error("Incorrect password.")

    st.stop()
