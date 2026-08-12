import streamlit as st

st.set_page_config(
    page_title="PSLE Navigator",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 PSLE Navigator")

st.subheader(
    "Navigate your child's secondary school journey with confidence"
)

st.write(
    "An AI-powered prototype that helps parents and students "
    "explore secondary school options and understand admission pathways."
)

with st.expander("⚠️ Important Notice"):
    st.warning(
        """
        This web application is a prototype developed for educational purposes only.
        The information provided here is NOT intended for real-world usage and should
        not be relied upon for making any decisions, especially those related to
        financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect
        information. You assume full responsibility for how you use any generated output.

        Always consult official MOE information and qualified professionals for accurate
        and personalised advice.
        """
    )
