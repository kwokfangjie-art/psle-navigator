import streamlit as st
import pandas as pd
import re


def normalise_school_name(name):
    """
    Creates a standardised school name used only for matching datasets.
    The original school name is still used for display.
    """

    if pd.isna(name):
        return ""

    name = str(name).strip().lower()

    # Remove common suffixes that may appear in one dataset but not another
    name = re.sub(r"\s*\(secondary\)\s*$", "", name)

    # Standardise apostrophes
    name = name.replace("’", "'")

    # Remove punctuation
    name = re.sub(r"[^a-z0-9\s]", " ", name)

    # Collapse multiple spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name

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

    df = pd.read_csv("data/General information of schools.csv")

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

    gender_map = {
        "CO-ED SCHOOL": "Co-ed",
        "BOYS' SCHOOL": "Boys",
        "GIRLS' SCHOOL": "Girls"
    }

    df["gender"] = df["nature_code"].map(gender_map)
    df["zone"] = df["zone_code"].str.title()

    df = df.rename(
        columns={
            "url_address": "website",
            "sap_ind": "sap",
            "ip_ind": "ip"
        }
    )

    df["school_key"] = df["school_name"].apply(
    normalise_school_name
)

    keep_columns = [
    "school_name",
    "school_key",
    "gender",
    "zone",
    "type_code",
    "mainlevel_code",
    "sap",
    "ip",
    "website"
]

    return df[keep_columns].copy()


@st.cache_data
def load_psle_ranges():

    df = pd.read_csv("data/psle_ranges.csv")

    df["school_key"] = df["school_name"].apply(
        normalise_school_name
    )

    return df

schools = load_school_data()
psle_ranges = load_psle_ranges()


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🎓 School Explorer")

st.write(
    "Tell us about the student to explore secondary school options "
    "that may match their profile."
)

st.info(
    "💡 This prototype uses official MOE school information and "
    "historical PSLE score ranges for educational purposes only. "
    "Results do not predict or guarantee admission."
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
# RESULT TYPE
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
# POSTING PATHWAY
# ==================================================

st.subheader("📘 Posting pathway")

posting_pathway = st.selectbox(
    "Which pathway would you like to explore?",
    options=[
        "Posting Group 3",
        "Posting Group 2",
        "Posting Group 1",
        "Integrated Programme"
    ]
)

st.caption(
    "PSLE score ranges differ by Posting Group and for "
    "Integrated Programme schools."
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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Overall PSLE Score",
            f"AL {overall_al}"
        )

    with col2:
        st.metric(
            "Posting Pathway",
            posting_pathway
        )

    with col3:
        st.metric(
            "Preferred Zone",
            preferred_zone
        )

    with col4:
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
    # Select PSLE ranges for chosen pathway
    # ----------------------------------------------

    selected_ranges = psle_ranges[
        psle_ranges["pathway"] == posting_pathway
    ].copy()


    # ----------------------------------------------
    # Merge school directory with PSLE ranges
    # ----------------------------------------------

    matches = matches.merge(
        selected_ranges,
        on="school_key",
        how="inner",
        suffixes=("", "_psle")
    )


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
    # Match PSLE score
    # ----------------------------------------------

    matches = matches[
        overall_al <= matches["score_high"]
    ].copy()


    # ----------------------------------------------
    # Create match labels
    # ----------------------------------------------

    def classify_match(row):

        midpoint = (
            row["score_low"]
            + row["score_high"]
        ) / 2

        if overall_al <= row["score_low"]:
            return "Strong historical match"

        elif overall_al <= midpoint:
            return "Within indicative range"

        else:
            return "Near upper end"


    if not matches.empty:
        matches["match_label"] = matches.apply(
            classify_match,
            axis=1
        )


    # ----------------------------------------------
    # Preferred-zone ranking
    # ----------------------------------------------

    if preferred_zone != "Any":

        matches["zone_match"] = (
            matches["zone"] == preferred_zone
        )

    else:

        matches["zone_match"] = True


    # ----------------------------------------------
    # IP preference ranking
    # ----------------------------------------------

    matches["ip_match"] = (
        matches["ip"] == "Yes"
    )


    # ----------------------------------------------
    # Sort results
    # ----------------------------------------------

    if ip_priority == "Yes":

        matches = matches.sort_values(
            by=[
                "zone_match",
                "ip_match",
                "score_high",
                "school_name"
            ],
            ascending=[
                False,
                False,
                True,
                True
            ]
        )

    else:

        matches = matches.sort_values(
            by=[
                "zone_match",
                "score_high",
                "school_name"
            ],
            ascending=[
                False,
                True,
                True
            ]
        )


    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    st.divider()

    st.subheader("🎓 Potential school matches")

    st.caption(
        "PSLE score ranges are based on the previous S1 Posting exercise "
        "and are indicative only. They do not guarantee admission."
    )


    if matches.empty:

        st.warning(
            "No potential matches were found for the selected "
            "profile and pathway in the current dataset."
        )

    else:

        st.write(
            f"**{len(matches)} potential match"
            f"{'es' if len(matches) != 1 else ''} found**"
        )


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


        st.write("")


        # ------------------------------------------
        # School cards
        # ------------------------------------------

        for _, school in matches.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns(
                    [
                        4,
                        1
                    ]
                )

                with col1:

                    st.subheader(
                        school["school_name"]
                    )

                    st.write(
                        f"**{school['gender']}** · "
                        f"{school['zone']} · "
                        f"{school['type_code'].title()}"
                    )


                with col2:

                    if school["match_label"] == "Strong historical match":

                        st.success(
                            "Strong match"
                        )

                    elif school["match_label"] == "Within indicative range":

                        st.info(
                            "Within range"
                        )

                    else:

                        st.warning(
                            "Near upper end"
                        )


                # ----------------------------------
                # PSLE RANGE
                # ----------------------------------

                st.write(
                    f"**2025 PSLE range:** "
                    f"{int(school['score_low'])}–"
                    f"{int(school['score_high'])}"
                )

                st.write(
                    f"**Pathway:** "
                    f"{school['pathway']}"
                )


                # ----------------------------------
                # PROGRAMMES
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
                # WHY THIS SCHOOL APPEARS
                # ----------------------------------

                st.write(
                    "**Why this school appears:**"
                )

                st.write(
                    "✓ Student's PSLE score is within or stronger "
                    "than the school's historical indicative range."
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


                st.caption(
                    "Historical PSLE score ranges are for reference only "
                    "and do not predict admission outcomes."
                )


                # ----------------------------------
                # SOURCE / WEBSITE
                # ----------------------------------

                if pd.notna(
                    school.get("source_url")
                ):

                    source_url = str(
                        school["source_url"]
                    ).strip()

                    if source_url:

                        st.link_button(
                            "View MOE source ↗",
                            source_url
                        )


                if (
                    pd.notna(school["website"])
                    and str(school["website"]).strip() != ""
                ):

                    website = str(
                        school["website"]
                    ).strip()

                    if not website.startswith(
                        (
                            "http://",
                            "https://"
                        )
                    ):

                        website = (
                            "https://"
                            + website
                        )

                    st.link_button(
                        "Visit school website ↗",
                        website
                    )
