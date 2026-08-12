import streamlit as st


# ==================================================
# HERO
# ==================================================

st.markdown(
    """
    <div style="
        text-align: center;
        margin-bottom: 1rem;
    ">
        <span style="
            display: inline-block;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background-color: #EAF2F8;
            color: #1F4E79;
            font-size: 0.9rem;
            font-weight: 600;
        ">
            🎓 For Singapore parents & students
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style="
        text-align: center;
        max-width: 900px;
        margin: 0 auto 1rem auto;
    ">
        Navigate your child's secondary school journey with confidence
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align: center;
        max-width: 780px;
        margin: 0 auto 2rem auto;
        font-size: 1.1rem;
        color: #6B7280;
        line-height: 1.6;
    ">
        Explore potential school matches, understand historical cut-off points,
        discover relevant CCAs, and get grounded AI guidance on Singapore's
        PSLE-to-secondary-school transition.
    </p>
    """,
    unsafe_allow_html=True
)


# ==================================================
# PRIMARY ACTIONS
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
Create a student profile and explore potential school matches using:

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
Ask questions about:

- S1 Posting;
- DSA-Sec;
- Integrated Programme;
- SAP and Higher Mother Tongue;
- school CCAs; and
- individual secondary schools.

The AI can use the student profile and retrieved school or RAG data to personalise its answers.
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
# VALUE PROPOSITION
# ==================================================

st.header(
    "Why use PathFinder?"
)

value1, value2, value3 = st.columns(3)


with value1:

    st.markdown(
        """
### 📊 Personalised

Uses the student's PSLE profile, preferences and interests to tailor school exploration and AI guidance.
"""
    )


with value2:

    st.markdown(
        """
### 🧠 Grounded

Combines structured school data with a FAISS RAG knowledge base instead of relying only on the language model.
"""
    )


with value3:

    st.markdown(
        """
### 🔎 Explainable

Shows why schools appear, historical COP context and retrieved RAG sources where relevant.
"""
    )


st.divider()


# ==================================================
# HOW IT WORKS
# ==================================================

st.header(
    "How it works"
)

step1, step2, step3 = st.columns(3)


with step1:

    st.markdown(
        """
### 1️⃣ Create a profile

Enter non-sensitive details such as PSLE AL scores, gender, preferred zone and interests.
"""
    )


with step2:

    st.markdown(
        """
### 2️⃣ Explore schools

Python filters and ranks potential matches using structured school, COP and CCA data.
"""
    )


with step3:

    st.markdown(
        """
### 3️⃣ Ask questions

The AI Navigator uses structured retrieval and RAG to provide grounded explanations.
"""
    )


# ==================================================
# COMPACT FOOTER AREA
# ==================================================

st.divider()

footer_left, footer_right = st.columns(
    [2, 1]
)


with footer_left:

    st.caption(
        "PathFinder is an educational prototype. "
        "Historical cut-off points are reference points only "
        "and do not guarantee future admission outcomes."
    )


with footer_right:

    about_col, method_col = st.columns(2)

    with about_col:

        if st.button(
            "ℹ️ About",
            use_container_width=True
        ):

            st.switch_page(
                "pages/4_ℹ️_About_Us.py"
            )

    with method_col:

        if st.button(
            "🔬 Methodology",
            use_container_width=True
        ):

            st.switch_page(
                "pages/5_🔬_Methodology.py"
            )


# ==================================================
# IMPORTANT NOTICE
# ==================================================

with st.expander(
    "⚠️ Important notice"
):

    st.warning(
        """
This web application is a prototype developed for **educational purposes only**.

The information provided here is **not intended for real-world usage**
and should not be relied upon for making decisions.

The language model may generate inaccurate or incorrect information.
RAG retrieval does not guarantee that the most relevant source will
always be selected.

Always verify current PSLE, S1 Posting, DSA-Sec and school information
with the Ministry of Education and the relevant school's official information.
"""
    )


# ==================================================
# FOOTER
# ==================================================

st.caption(
    "PathFinder · AI Bootcamp Capstone Project"
)
