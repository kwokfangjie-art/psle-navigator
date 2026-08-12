import streamlit as st


# ==================================================
# HERO
# ==================================================

st.markdown(
    """
<div style="text-align: center; padding: 1.2rem 0 1rem 0;">
    <div style="
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: #EAF2F8;
        color: #1F4E79;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
    ">
        🎓 For Singapore parents & students
    </div>

    <h1 style="
        font-size: 3rem;
        line-height: 1.15;
        margin-bottom: 0.9rem;
        color: #1F2937;
    ">
        Navigate your child's secondary school journey with confidence
    </h1>

    <p style="
        font-size: 1.1rem;
        max-width: 780px;
        margin: 0 auto;
        color: #6B7280;
        line-height: 1.6;
    ">
        Explore potential school matches, understand historical cut-off points,
        discover relevant CCAs, and get grounded AI guidance on Singapore's
        PSLE-to-secondary-school transition.
    </p>
</div>
""",
    unsafe_allow_html=True
)

st.write("")


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
    "Why use PSLE Navigator?"
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

- MOE school information;
- MOE co-curricular activity information;
- a curated historical PSLE cut-off point dataset; and
- a small RAG document knowledge base covering PSLE and secondary-school transition topics.
"""
)

st.caption(
    "Historical cut-off points are reference points only "
    "and do not guarantee future admission outcomes."
)


st.divider()


# ==================================================
# DOCUMENTATION
# ==================================================

st.header(
    "📖 Project documentation"
)

doc_col1, doc_col2 = st.columns(2)


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
RAG retrieval also does not guarantee that the most relevant source will
always be selected.

Always verify current PSLE, S1 Posting, DSA-Sec and school information
with the Ministry of Education and the relevant school's official information.
"""
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "PSLE Navigator · AI Bootcamp Capstone Project · Educational prototype"
)
