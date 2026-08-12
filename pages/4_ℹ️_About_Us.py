import streamlit as st
from utils.auth import require_password


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="About Us | PSLE Navigator",
    page_icon="ℹ️",
    layout="wide"
)

require_password()


# ==================================================
# PAGE HEADER
# ==================================================

st.title("ℹ️ About PSLE Navigator")

st.write(
    "PSLE Navigator is an educational prototype designed to help "
    "Singapore parents and Primary 6 students better understand the "
    "transition from PSLE to secondary school."
)

st.info(
    "This application was developed as part of an AI Bootcamp capstone "
    "project and is intended for educational and demonstration purposes only."
)

st.divider()


# ==================================================
# PROJECT OVERVIEW
# ==================================================

st.header("🎯 Project overview")

st.write(
    """
The secondary school admission journey can involve many different pieces
of information — PSLE Achievement Levels, Posting Groups, historical
school cut-off points, Integrated Programme options, school location,
CCAs, Direct School Admission and other pathways.

PSLE Navigator brings selected information together into one interactive
application so that users can explore how different factors may relate
to a student's profile.
"""
)


# ==================================================
# PROBLEM STATEMENT
# ==================================================

st.header("❓ Problem statement")

st.write(
    """
Parents and students may need to consult multiple websites and information
sources when considering secondary school options.

It can also be difficult to understand how general information relates
to an individual student's situation.

PSLE Navigator therefore aims to:

- consolidate selected school and admission information;
- present the information in a more accessible format;
- personalise the experience using non-sensitive profile inputs;
- provide interactive explanations through an AI assistant; and
- help users understand the factors they may wish to consider when
  researching secondary schools.
"""
)


# ==================================================
# TARGET USERS
# ==================================================

st.header("👨‍👩‍👧 Target users")

st.write(
    """
The prototype is designed primarily for:

- parents of Primary 6 students;
- Primary 6 students exploring secondary school options; and
- users who want a simpler explanation of Singapore's secondary school
  admission pathways.
"""
)


# ==================================================
# OBJECTIVES
# ==================================================

st.header("✅ Project objectives")

st.write(
    """
The project has four main objectives:

1. **Consolidate information**  
   Bring together selected school profile, historical cut-off point and
   CCA information in one interface.

2. **Personalise guidance**  
   Use non-sensitive inputs such as PSLE AL score, gender, preferred zone
   and interests to tailor results.

3. **Improve understanding**  
   Use an AI assistant to explain concepts such as S1 Posting, DSA-Sec,
   Integrated Programme and school selection considerations.

4. **Present information effectively**  
   Use forms, filters, school cards and visualisations to make the
   information easier to explore.
"""
)


# ==================================================
# CORE USE CASES
# ==================================================

st.header("🧩 Core use cases")

use_case_1, use_case_2 = st.columns(2)


with use_case_1:

    st.subheader("🎓 Use Case 1 — School Explorer")

    st.write(
        """
The School Explorer allows users to enter a student profile and view
potential school matches based on selected criteria.

Key features include:

- PSLE subject AL inputs;
- automatic overall AL calculation;
- gender matching;
- pathway selection;
- preferred school zone;
- historical COP comparison;
- IP and SAP indicators;
- CCA interest matching;
- result filters;
- match categories; and
- an interactive historical COP visualisation.
"""
    )


with use_case_2:

    st.subheader("🤖 Use Case 2 — AI Navigator")

    st.write(
        """
The AI Navigator provides conversational guidance about PSLE and
secondary school admission.

Key features include:

- shared student profile context;
- personalised answers;
- prompt chaining;
- question intent classification;
- retrieval from local school, COP and CCA datasets;
- named-school lookup;
- grounded school-specific responses;
- conversation memory; and
- prompt-injection safeguards.
"""
    )


# ==================================================
# DATA SOURCES
# ==================================================

st.header("📚 Data sources")

st.write(
    """
The prototype uses a combination of official and supplementary
publicly available information.
"""
)


st.subheader("Official MOE / Government data")

st.write(
    """
**1. MOE School Directory and Information — General information of schools**

Used for:
- school name;
- school type;
- gender profile;
- geographical zone;
- Integrated Programme indicator;
- SAP indicator; and
- school website.

**2. MOE School Directory and Information — Co-curricular activities**

Used for:
- school-level CCA offerings;
- CCA category information; and
- matching selected student interests with related school activities.
"""
)


st.subheader("Historical cut-off point data")

st.write(
    """
The prototype also contains a curated dataset of historical PSLE cut-off
points for selected schools.

These values are used only as historical reference points for the
prototype's matching logic.

Historical cut-off points may change from year to year and must not be
interpreted as guaranteed admission thresholds.
"""
)


# ==================================================
# PERSONALISATION
# ==================================================

st.header("👤 Personalisation")

st.write(
    """
The application uses generic, non-sensitive profile information to
personalise results.

The profile may contain:

- predicted or actual subject AL scores;
- overall PSLE score;
- gender;
- preferred school zone;
- pathway being explored;
- IP preference;
- DSA-Sec interest;
- selected interests and talents; and
- Higher Mother Tongue status.

The prototype does not require NRIC numbers, residential addresses,
telephone numbers or other sensitive personal information.
"""
)


# ==================================================
# HOW SCHOOL MATCHING WORKS
# ==================================================

st.header("🔎 How school matching works")

st.write(
    """
The School Explorer uses deterministic Python logic rather than asking
the language model to calculate school matches.

The current matching process considers:

1. the selected admission pathway;
2. student gender and school gender profile;
3. the student's overall AL relative to the historical COP;
4. preferred geographical zone;
5. selected interests relative to published school CCA offerings; and
6. selected programme preferences.

Schools are then ranked and presented with an explanation of why they
appear in the results.
"""
)


# ==================================================
# MATCH CATEGORIES
# ==================================================

st.subheader("Historical COP match categories")

st.write(
    """
For the purposes of this educational prototype, schools may be labelled:

- **Comfortable** — student's AL is at least 3 points stronger than the
  historical COP;
- **Competitive** — student's AL is 1–2 points stronger than the
  historical COP; or
- **Borderline** — student's AL is exactly at the historical COP.

These labels describe the student's position relative to a historical
reference point only. They are not probabilities and do not predict
admission outcomes.
"""
)


# ==================================================
# CCA MATCHING
# ==================================================

st.header("🏅 Interest and CCA matching")

st.write(
    """
Selected student interests are mapped to related CCA descriptions in
the MOE CCA dataset.

For example, a Robotics & Coding interest may be matched with activities
such as Robotics or Infocomm Technology (Computing), where those
activities are listed for a school.

An interest match means only that a related CCA is present in the
dataset.

**It does not mean that the school offers Direct School Admission
(DSA-Sec) for that activity.**
"""
)


# ==================================================
# AI NAVIGATOR
# ==================================================

st.header("🤖 AI Navigator")

st.write(
    """
The AI Navigator uses a large language model to explain information and
respond to follow-up questions.

For school-related questions, the application first retrieves relevant
records from the local datasets before providing them to the language
model as reference information.

The AI is instructed not to invent school-specific details that are
missing from the retrieved records.
"""
)


# ==================================================
# SCOPE
# ==================================================

st.header("📌 Project scope")

st.write(
    """
PSLE Navigator focuses on selected aspects of the Singapore
PSLE-to-secondary-school transition.

The prototype currently covers:

- PSLE AL scoring;
- historical school COP comparisons;
- school profile information;
- school zone information;
- selected IP and SAP indicators;
- school CCA information;
- S1 Posting explanations;
- DSA-Sec explanations;
- Integrated Programme explanations;
- Higher Mother Tongue discussions; and
- personalised school exploration.
"""
)


# ==================================================
# OUT OF SCOPE
# ==================================================

st.header("🚫 Out of scope")

st.write(
    """
The prototype does not attempt to provide:

- guaranteed admission predictions;
- real-time S1 Posting results;
- complete modelling of affiliated-school priority;
- complete DSA-Sec talent-area data for every school;
- real-time school vacancies;
- personalised professional advice; or
- official decisions on behalf of MOE or any school.
"""
)


# ==================================================
# LIMITATIONS
# ==================================================

st.header("⚠️ Limitations")

st.write(
    """
Users should be aware of several important limitations:

- Historical COPs may change from year to year.
- The historical COP dataset is curated and does not necessarily include
  every Singapore secondary school or pathway.
- Affiliation priority is outside the current prototype scope.
- CCA availability does not establish DSA-Sec availability.
- School programmes and policies may change.
- The AI model may generate inaccurate, incomplete or outdated answers.
- The AI assistant cannot replace official MOE guidance.
"""
)


# ==================================================
# PRIVACY
# ==================================================

st.header("🔐 Privacy and data handling")

st.write(
    """
The prototype is designed to avoid collecting sensitive personal
information.

Student profile information is used within the Streamlit session to
personalise the School Explorer and AI Navigator.

The application does not require users to provide NRIC numbers, home
addresses or other sensitive identifying information.

The OpenAI API key is stored separately using Streamlit Secrets and is
not stored in the public GitHub source code.
"""
)


# ==================================================
# EDUCATIONAL DISCLAIMER
# ==================================================

st.header("⚠️ Important notice")

st.warning(
    """
This web application is a prototype developed for **educational purposes
only.**

The information provided here is **NOT intended for real-world usage**
and should not be relied upon for making decisions.

Furthermore, please be aware that the language model may generate
inaccurate or incorrect information. You assume full responsibility for
how you use any generated output.

Always verify current PSLE, S1 Posting, DSA-Sec and school information
with the Ministry of Education and the relevant school's official
website.
"""
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "PSLE Navigator · AI Bootcamp Capstone Project · Educational prototype"
)
