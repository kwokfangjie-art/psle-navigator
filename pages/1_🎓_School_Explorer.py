import streamlit as st
import pandas as pd


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="School Explorer | PSLE Navigator",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# LOAD OFFICIAL MOE SCHOOL DATA
# ==================================================

@st.cache_data
def load_school_data():

    # IMPORTANT:
    # This filename must exactly match the file in your GitHub data folder.
    df = pd.read_csv("data/General information of schools.csv")

    # Keep schools that provide secondary-level education
    secondary_levels = [
        "SECONDARY (S1-S5)",
        "SECONDARY (S1-S4)",
        "MIXED LEVEL (S1-JC2)",
        "MIXED LEVEL (P1-S4)",
        "MIXED LEVEL (S1-S5, JC1-JC2)"
    ]

    df = df[
        df["mainlevel_code"].isin(secondary_levels)
    ].copy()

    # ----------------------------------------------
    # Clean gender
    # ----------------------------------------------

    gender_map = {
        "CO-ED SCHOOL": "Co-ed",
        "BOYS' SCHOOL": "Boys",
        "GIRLS' SCHOOL": "Girls"
    }

    df["gender"] = df["nature_code"].map(gender_map)

    # ----------------------------------------------
    # Clean zone
    # ----------------------------------------------

    df["zone"] = df["zone_code"].str.title()

    # ----------------------------------------------
    # Rename useful fields
    # ----------------------------------------------

    df = df.rename(
        columns={
            "url_address": "website",
            "sap_ind": "sap",
            "ip_ind": "ip"
        }
    )

    # ----------------------------------------------
    # Make school names easier to read
    # ----------------------------------------------

    df["school_name"] = df["school_name"].str.title()

    # ----------------------------------------------
    # Keep only fields required by the app
    # ----------------------------------------------

    keep_columns = [
        "school_name",
        "gender",
        "zone",
        "type_code",
        "mainlevel_code",
        "sap",
        "ip",
        "website"
    ]

    df = df[keep_columns].copy()

    return df


schools = load_school_data()


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🎓 School Explorer")

st.write(
    "Tell us about the student to explore secondary school options "
    "that may match their profile."
)

st.info(
    "💡 This prototype currently uses official MOE school information "
    "for gender, location and programme matching. "
    "PSLE score-range matching will be added in the next stage."
)

st.divider()


# ==================================================
# STUDENT PROFILE
# ==================================================

st.subheader("👤 Student profile")

student_name = st.text_input(
    "Student's name (optional)",
    placeholder="e.g. Alex"
)

gender = st.segmented_control(
    "Gender",
    options=[
        "Male",
        "Female"
    ],
    default=None
)

st.divider()


# ==================================================
# PSLE SCORES
# ==================================================

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
    score is not None
    for score in scores.values()
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

    st.caption(
        "Select all 4 subjects to calculate the overall AL score."
    )


# ==================================================
# PREDICTED / ACTUAL
# ==================================================

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


# ==================================================
# SCHOOL PREFERENCES
# ==================================================

st.subheader("📍 School preferences")

preferred_zone = st.segmented_control(
    "Preferred school zone",
    options=[
        "Any",
        "North",
        "South",
        "East",
        "West"
    ],
    default="Any"
)

st.caption(
    "Select 'Any' to see potential matches regardless of location."
)


ip_priority = st.radio(
    "Is the Integrated Programme (IP) a priority?",
    options=[
        "Yes",
        "Maybe",
        "No"
    ],
    index=1,
    horizontal=True
)

st.caption(
    "The Integrated Programme is a 6-year pathway that generally "
    "allows students to progress towards qualifications such as "
    "the A-Levels or IB Diploma without taking the national "
    "Secondary 4 examination route."
)

st.divider()


# ==================================================
# DSA
# ==================================================

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


# ==================================================
# HIGHER MOTHER TONGUE
# ==================================================

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


# ==================================================
# SUBMIT
# ==================================================

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

    # ----------------------------------------------
    # PROFILE SUMMARY
    # ----------------------------------------------

    st.success("Student profile created successfully!")

    st.subheader("Profile summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall PSLE Score",
            f"AL {overall_al}"
        )

    with col2:
        st.metric(
            "Preferred Zone",
            preferred_zone
        )

    with col3:
        st.metric(
            "IP Priority",
            ip_priority
        )

    st.write(
        "**Gender:**",
        gender
    )

    st.write(
        "**Result type:**",
        result_type
    )

    if interests:

        st.write(
            "**Interests:**",
            ", ".join(interests)
        )

    else:

        st.write(
            "**Interests:** Not specified"
        )


    # ==================================================
    # SCHOOL MATCHING
    # ==================================================

    matches = schools.copy()


    # ----------------------------------------------
    # Match gender
    # ----------------------------------------------

    if gender == "Male":

        matches = matches[
            matches["gender"].isin(
                [
                    "Boys",
                    "Co-ed"
                ]
            )
        ]

    elif gender == "Female":

        matches = matches[
            matches["gender"].isin(
                [
                    "Girls",
                    "Co-ed"
                ]
            )
        ]


    # ----------------------------------------------
    # Rank by preferred zone
    #
    # IMPORTANT:
    # Zone does NOT exclude schools.
    # Preferred-zone schools simply appear first.
    # ----------------------------------------------

    if preferred_zone != "Any":

        matches["zone_match"] = (
            matches["zone"] == preferred_zone
        )

        matches = matches.sort_values(
            by=[
                "zone_match",
                "school_name"
            ],
            ascending=[
                False,
                True
            ]
        )

    else:

        matches = matches.sort_values(
            by="school_name",
            ascending=True
        )


    # ----------------------------------------------
    # Optional IP preference ranking
    # ----------------------------------------------

    if ip_priority == "Yes":

        matches["ip_match"] = (
            matches["ip"] == "Yes"
        )

        if preferred_zone != "Any":

            matches = matches.sort_values(
                by=[
                    "zone_match",
                    "ip_match",
                    "school_name"
                ],
                ascending=[
                    False,
                    False,
                    True
                ]
            )

        else:

            matches = matches.sort_values(
                by=[
                    "ip_match",
                    "school_name"
                ],
                ascending=[
                    False,
                    True
                ]
            )


    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    st.divider()

    st.subheader("🎓 Potential school matches")

    st.caption(
        "These results currently use school gender, zone and programme "
        "information from the MOE school directory. "
        "PSLE score-range matching will be added separately."
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


        # ------------------------------------------
        # Results summary
        # ------------------------------------------

        if preferred_zone != "Any":

            zone_count = len(
                matches[
                    matches["zone"] == preferred_zone
                ]
            )

            st.write(
                f"📍 **{zone_count}** of these schools are in "
                f"the **{preferred_zone}** zone."
            )


        if ip_priority == "Yes":

            ip_count = len(
                matches[
                    matches["ip"] == "Yes"
                ]
            )

            st.write(
                f"🎓 **{ip_count}** schools in the results "
                f"offer the Integrated Programme."
            )


        st.write("")


        # ------------------------------------------
        # School cards
        # ------------------------------------------

        for _, school in matches.iterrows():

            with st.container(border=True):

                st.subheader(
                    school["school_name"]
                )


                # ----------------------------------
                # Basic school details
                # ----------------------------------

                st.write(
                    f"**{school['gender']}** · "
                    f"{school['zone']} · "
                    f"{school['type_code'].title()}"
                )


                # ----------------------------------
                # Programme badges
                # ----------------------------------

                programme_badges = []

                if school["ip"] == "Yes":
                    programme_badges.append("🎓 IP")

                if school["sap"] == "Yes":
                    programme_badges.append("🏮 SAP")


                if programme_badges:

                    st.write(
                        "**Programmes:** "
                        + " · ".join(programme_badges)
                    )


                # ----------------------------------
                # Why this school appears
                # ----------------------------------

                st.write(
                    "**Why this school appears:**"
                )

                st.write(
                    "✓ School gender matches the student's profile."
                )


                if preferred_zone != "Any":

                    if school["zone"] == preferred_zone:

                        st.write(
                            "✓ Matches preferred school zone."
                        )

                    else:

                        st.write(
                            "• Outside the preferred zone, "
                            "but shown as another possible option."
                        )


                if (
                    ip_priority == "Yes"
                    and school["ip"] == "Yes"
                ):

                    st.write(
                        "✓ Offers the Integrated Programme, "
                        "which matches the student's stated preference."
                    )


                # ----------------------------------
                # Website
                # ----------------------------------

                if (
                    pd.notna(school["website"])
                    and str(school["website"]).strip() != ""
                ):

                    website = str(
                        school["website"]
                    ).strip()

                    # Add https:// if dataset does not include it
                    if not website.startswith(
                        ("http://", "https://")
                    ):

                        website = (
                            "https://" + website
                        )


                    st.link_button(
                        "Visit school website ↗",
                        website
                    )
