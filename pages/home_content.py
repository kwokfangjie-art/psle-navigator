import streamlit as st


# ==================================================
# HERO
# ==================================================

st.markdown(
    """
<div style="text-align: center; padding: 2rem 0 1rem 0;">
    <div style="display: inline-block; padding: 0.35rem 0.75rem; border-radius: 999px; background: rgba(49, 130, 206, 0.10); font-size: 0.9rem; margin-bottom: 1rem;">
        🎓 For Singapore parents & students
    </div>
    <h1 style="font-size: 3rem; margin-bottom: 0.75rem;">
        Navigate your child's secondary school journey with confidence
    </h1>
    <p style="font-size: 1.15rem; max-width: 800px; margin: 0 auto 1.5rem auto; color: #888;">
        Explore potential secondary school matches, understand historical
        cut-off points, discover relevant CCAs, and ask an AI assistant
        about Singapore's PSLE-to-secondary-school transition.
    </p>
</div>
""",
    unsafe_allow_html=True
)


# ==================================================
# MAIN ACTIONS
# ==================================================

col1, col2 = st.columns(2)


with col1:

    with st.container(
        border=True
    ):

        st.subheader(
            "🎓 Explore school options"
        )

        st.write(
            """
Enter a student profile and explore potential school matches based on:

- overall PSLE AL score;
- historical school COPs;
- gender;
- preferred zone;
- pathway;
- IP preference; and
- selected interests and CCA offerings.
"""
        )

        if st.button(
            "Open School Explorer →",
            type="primary",
            use_container_width=True
        ):

            st.switch_page(
                "pages/1_🎓_School_Explorer.py"
            )


with col2:

    with st.container(
        border=True
    ):

        st.subheader(
            "🤖 Ask the AI Navigator"
        )

        st.write(
            """
Ask follow-up questions about:

- S1 Posting;
- DSA-Sec;
- Integrated Programme;
- SAP schools;
- Higher Mother Tongue;
- school CCAs; and
- individual secondary schools.

The AI can use the student profile and retrieved school data to personalise its answers.
"""
        )

        if st.button(
            "Open AI Navigator →",
            use_container_width=True
        ):

            st.switch_page(
                "pages/2_🤖_AI_Navigator.py"
            )


st.divider()


# ==================================================
# FEATURE OVERVIEW
# ==================================================

st.header(
    "What can PSLE Navigator do?"
)

feature1, feature2 = st.columns(2)


with feature1:

    with st.container(
        border=True
    ):

        st.subheader(
            "📊 Personalised school matching"
        )

        st.write(
            "Compare the student's PSLE score against historical "
            "cut-off points and view potential school matches."
        )


    with st.container(
        border=True
    ):

        st.subheader(
            "🏅 Interest & CCA matching"
        )

        st.write(
            "Match selected interests with related CCA offerings "
            "from the MOE school dataset."
        )


with feature2:

    with st.container(
        border=True
    ):

        st.subheader(
            "💬 Grounded AI guidance"
        )

        st.write(
            "Ask school-specific questions using retrieved school, "
            "historical COP and CCA information."
        )


    with st.container(
        border=True
    ):

        st.subheader(
            "📈 Interactive visualisation"
        )

        st.write(
            "Visualise the student's AL score against historical "
            "school cut-off points."
        )


st.divider()


# ==================================================
# HOW IT WORKS
# ==================================================

st.header(
    "How it works"
)

step1, step2, step3 = (
    st.columns(3)
)


with step1:

    st.subheader(
        "1️⃣ Create a profile"
    )

    st.write(
        "Enter generic, non-sensitive details such as "
        "PSLE AL scores, gender, zone and interests."
    )


with step2:

    st.subheader(
        "2️⃣ Explore schools"
    )

    st.write(
        "The application uses deterministic Python logic "
        "to filter and rank potential school matches."
    )


with step3:

    st.subheader(
        "3️⃣ Ask follow-up questions"
    )

    st.write(
        "The AI Navigator uses the profile and retrieved "
        "reference data to provide personalised explanations."
    )


st.divider()


# ==================================================
# DATA SOURCES
# ==================================================

st.header(
    "📚 Information used by this prototype"
)

st.write(
    """
PSLE Navigator consolidates selected information from:

- MOE School Directory and Information — General information of schools;
- MOE School Directory and Information — Co-curricular activities;
- a curated historical PSLE cut-off point dataset; and
- the application's student profile and matching logic.
"""
)

st.caption(
    "Historical cut-off points are used as reference points only "
    "and may not represent future admission outcomes."
)


st.divider()


# ==================================================
# DOCUMENTATION
# ==================================================

st.header(
    "📖 Project documentation"
)

doc_col1, doc_col2 = (
    st.columns(2)
)


with doc_col1:

    if st.button(
        "ℹ️ About PSLE Navigator",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_ℹ️_About_Us.py"
        )


with doc_col2:

    if st.button(
        "🔬 View Methodology",
        use_container_width=True
    ):

        st.switch_page(
            "pages/5_🔬_Methodology.py"
        )


st.divider()


# ==================================================
# REQUIRED ASSIGNMENT DISCLAIMER
# ==================================================

with st.expander(
    "⚠️ IMPORTANT NOTICE — Please read"
):

    st.warning(
        """
**IMPORTANT NOTICE:** This web application is a prototype developed for
**educational purposes only.** The information provided here is
**NOT intended for real-world usage** and should not be relied upon for
making any decisions, especially those related to financial, legal, or
healthcare matters.

**Furthermore, please be aware that the LLM may generate inaccurate or
incorrect information. You assume full responsibility for how you use any
generated output.**

Always consult with qualified professionals for accurate and personalised
advice.
"""
    )

    st.write(
        """
For PSLE and secondary-school admission matters, always verify current
information with the Ministry of Education and the relevant school's
official website.
"""
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "PSLE Navigator · AI Bootcamp Capstone Project · Educational prototype"
)

