import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="School Explorer | PSLE Navigator",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 School Explorer")
st.write(
    "Tell us about the student to explore secondary school options "
    "that may match their profile."
)

st.info(
    "💡 This tool uses indicative information for educational purposes only. "
    "It does not predict or guarantee admission to any school."
)

st.divider()

# --------------------------------------------------
# Student Profile
# --------------------------------------------------

st.subheader("👤 Student profile")

student_name = st.text_input(
    "Student's name (optional)",
    placeholder="e.g. Alex"
)

gender = st.segmented_control(
    "Gender",
    options=["Male", "Female"],
    default=None
)

st.divider()

# --------------------------------------------------
# PSLE Scores
# --------------------------------------------------

st.subheader("📊 PSLE Subject AL Scores")

st.caption(
    "AL1 is the strongest grade and AL8 is the weakest. "
    "Select a score for each subject."
)

subjects = [
    "English Language",
    "Mother Tongue Language",
    "Mathematics",
    "Science"
]

scores = {}

for subject in subjects:
    scores[subject] = st.segmented_control(
        subject,
        options=list(range(1, 9)),
        default=None,
        key=f"score_{subject}"
    )

# Check whether all four scores have been selected
all_scores_selected = all(
    score is not None for score in scores.values()
)

if all_scores_selected:
    overall_al = sum(scores.values())

    st.metric(
        label="Overall PSLE Score",
        value=f"AL {overall_al}"
    )

    st.caption(
        f"{scores['English Language']} + "
        f"{scores['Mother Tongue Language']} + "
        f"{scores['Mathematics']} + "
        f"{scores['Science']} = {overall_al}"
    )

else:
    overall_al = None
    st.caption("Select all 4 subjects to calculate the overall AL score.")

# --------------------------------------------------
# Predicted / Actual
# --------------------------------------------------

st.write("")

result_type = st.radio(
    "Are these scores:",
    options=[
        "Predicted / estimated",
        "Actual PSLE results"
    ],
    horizontal=True
)

st.divider()

# --------------------------------------------------
# School Preferences
# --------------------------------------------------

st.subheader("📍 School preferences")

preferred_zone = st.segmented_control(
    "Preferred school zone",
    options=[
        "Any",
        "North",
        "South",
        "East",
        "West",
        "Central"
    ],
    default="Any"
)

st.caption(
    "Select 'Any' to see potential matches regardless of location."
)

ip_priority = st.radio(
    "Is the Integrated Programme (IP) a priority?",
    options=["Yes", "Maybe", "No"],
    index=1,
    horizontal=True
)

st.caption(
    "The Integrated Programme is a 6-year pathway that generally "
    "leads directly to A-Levels, the IB Diploma or another qualification "
    "without taking the Singapore-Cambridge Secondary Education Certificate "
    "examinations at the end of Secondary 4."
)

st.divider()

# --------------------------------------------------
# DSA
# --------------------------------------------------

st.subheader("🏅 Interests & DSA-Sec")

dsa_interest = st.radio(
    "Are you considering Direct School Admission (DSA-Sec)?",
    options=[
        "Yes, actively",
        "Maybe / not sure",
        "No"
    ],
    index=1,
    horizontal=True
)

st.caption(
    "DSA-Sec allows students to apply to secondary schools based on "
    "talents and achievements before the S1 Posting exercise."
)

interests = st.multiselect(
    "Interests and talents",
    options=[
        "Football",
        "Basketball",
        "Swimming",
        "Badminton",
        "Athletics",
        "Table Tennis",
        "Choir / Singing",
        "Band / Orchestra",
        "Chinese Orchestra",
        "Dance",
        "Drama / Theatre",
        "Mathematics",
        "Science",
        "Robotics & Coding",
        "Engineering",
        "Debate",
        "Creative Writing",
        "Visual Arts",
        "Student Leadership",
        "Community Service",
        "Uniformed Groups"
    ],
    placeholder="Select all that apply"
)

st.divider()

# --------------------------------------------------
# Higher Mother Tongue
# --------------------------------------------------

st.subheader("🗣️ Mother Tongue")

higher_mt = st.radio(
    "Is the student taking Higher Mother Tongue at PSLE?",
    options=[
        "Higher Chinese",
        "Higher Malay",
        "Higher Tamil",
        "No"
    ],
    index=3,
    horizontal=True
)

st.divider()

# --------------------------------------------------
# Submit
# --------------------------------------------------

profile_complete = (
    gender is not None
    and all_scores_selected
)

if st.button(
    "Find potential school matches →",
    type="primary",
    use_container_width=True,
    disabled=not profile_complete
):

    st.success("Student profile created successfully!")

    st.subheader("Profile summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Overall PSLE Score", f"AL {overall_al}")

    with col2:
        st.metric("Preferred Zone", preferred_zone)

    with col3:
        st.metric("IP Priority", ip_priority)

    st.write("**Gender:**", gender)
    st.write("**Result type:**", result_type)

    if interests:
        st.write("**Interests:**", ", ".join(interests))
    else:
        st.write("**Interests:** Not specified")

    st.info(
        "School matching will be added in the next stage."
    )
