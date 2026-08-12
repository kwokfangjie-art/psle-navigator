import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="School Explorer | PSLE Navigator",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# Load school data
# --------------------------------------------------

@st.cache_data
def load_school_data():
    return pd.read_csv("data/schools.csv")

schools = load_school_data()

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

    # --------------------------------------------------
    # Find potential school matches
    # --------------------------------------------------

    matches = schools.copy()

    # Match by gender
    if gender == "Male":
        matches = matches[
            matches["gender"].isin(["Male", "Co-ed"])
        ]
    elif gender == "Female":
        matches = matches[
            matches["gender"].isin(["Female", "Co-ed"])
        ]

    # Match by indicative PSLE score range
    matches = matches[
        overall_al <= matches["score_high"]
    ]

    # Preferred zone is used for ranking, not exclusion
    if preferred_zone != "Any":
        matches["zone_match"] = (
            matches["zone"] == preferred_zone
        )
        matches = matches.sort_values(
            by=["zone_match", "score_high"],
            ascending=[False, True]
        )
    else:
        matches = matches.sort_values(
            by="score_high",
            ascending=True
        )

    st.divider()

    st.subheader("🎓 Potential school matches")

    st.caption(
        "These results are based on indicative score ranges and "
        "basic profile matching. They do not predict or guarantee admission."
    )

    if matches.empty:
        st.warning(
            "No potential matches were found in the current school dataset."
        )

    else:
        st.write(
            f"**{len(matches)} potential match"
            f"{'es' if len(matches) != 1 else ''} found**"
        )

        for _, school in matches.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.subheader(school["school_name"])

                    st.write(
                        f"**{school['gender']}** · "
                        f"{school['zone']} · "
                        f"Indicative AL {school['score_low']}–{school['score_high']}"
                    )

                with col2:

                    if overall_al <= school["score_low"]:
                        st.success("Strong match")

                    elif overall_al <= school["score_high"]:
                        st.info("Within range")

                st.write("**Why this school appears:**")

                st.write(
                    "✓ Student's AL score is within or stronger than "
                    "the school's indicative range."
                )

                st.write(
                    "✓ School gender matches the student's profile."
                )

                if preferred_zone != "Any":

                    if school["zone"] == preferred_zone:
                        st.write("✓ Matches preferred school zone.")

                    else:
                        st.write(
                            "• Outside preferred zone, but shown as "
                            "another potential option."
                        )

                programme_badges = []

                if school["ip"] == "Yes":
                    programme_badges.append("IP")

                if school["sap"] == "Yes":
                    programme_badges.append("SAP")

                if programme_badges:
                    st.write(
                        "**Programmes:** "
                        + " · ".join(programme_badges)
                    )

                if pd.notna(school["website"]):
                    st.link_button(
                        "Visit school website ↗",
                        school["website"]
                    )
