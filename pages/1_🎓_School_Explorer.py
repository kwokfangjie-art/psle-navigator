import streamlit as st
import pandas as pd
import plotly.express as px
import re


# ==================================================
# NORMALISE SCHOOL NAMES FOR DATASET MATCHING
# ==================================================

def normalise_school_name(name):
    """
    Creates a standardised school name used only for matching datasets.
    The original MOE school name is preserved for display.
    """

    if pd.isna(name):
        return ""

    name = str(name).strip().lower()

    # Remove "(Secondary)" if it appears at the end
    name = re.sub(r"\s*\(secondary\)\s*$", "", name)

    # Standardise apostrophes
    name = name.replace("’", "'")

    # Remove punctuation
    name = re.sub(r"[^a-z0-9\s]", " ", name)

    # Collapse repeated spaces
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

    df = pd.read_csv(
        "data/General information of schools.csv"
    )

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
    # Gender
    # ----------------------------------------------

    gender_map = {
        "CO-ED SCHOOL": "Co-ed",
        "BOYS' SCHOOL": "Boys",
        "GIRLS' SCHOOL": "Girls"
    }

    df["gender"] = df["nature_code"].map(
        gender_map
    )

    # ----------------------------------------------
    # Zone
    # ----------------------------------------------

    df["zone"] = (
        df["zone_code"]
        .astype(str)
        .str.title()
    )

    # ----------------------------------------------
    # Rename fields
    # ----------------------------------------------

    df = df.rename(
        columns={
            "url_address": "website",
            "sap_ind": "sap",
            "ip_ind": "ip"
        }
    )

    # ----------------------------------------------
    # Matching key
    # ----------------------------------------------

    df["school_key"] = (
        df["school_name"]
        .apply(normalise_school_name)
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


# ==================================================
# LOAD HISTORICAL PSLE COP DATA
# ==================================================

@st.cache_data
def load_psle_data():

    df = pd.read_csv(
        "data/psle_ranges.csv"
    )

    df["school_key"] = (
        df["school_name"]
        .apply(normalise_school_name)
    )

    return df


schools = load_school_data()
psle_data = load_psle_data()


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🎓 School Explorer")

st.write(
    "Explore secondary schools that may match the student's "
    "PSLE profile and preferences."
)

st.info(
    "💡 Historical cut-off points are provided for reference only. "
    "Actual admission outcomes vary from year to year and are not guaranteed."
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

    overall_al = sum(
        scores.values()
    )

    st.metric(
        "Overall PSLE Score",
        f"AL {overall_al}"
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
# ADMISSION PATHWAY
# ==================================================

st.subheader("📘 Admission pathway")

available_pathways = (
    psle_data["pathway"]
    .dropna()
    .drop_duplicates()
    .tolist()
)

preferred_order = [
    "Posting Group 3",
    "Posting Group 2",
    "Posting Group 1",
    "Integrated Programme"
]

available_pathways = [
    pathway
    for pathway in preferred_order
    if pathway in available_pathways
]


posting_pathway = st.selectbox(
    "Which pathway would you like to explore?",
    options=available_pathways
)

st.caption(
    "Only pathways currently available in the historical "
    "cut-off dataset are shown."
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
    "Schools in the preferred zone will be ranked first. "
    "Schools outside the zone may still be shown."
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
    "IP schools offer a 6-year programme leading towards "
    "qualifications such as the A-Levels or IB Diploma."
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
    "DSA-Sec allows students to apply based on talents "
    "and achievements before the S1 Posting exercise."
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
# PROFILE VALIDATION
# ==================================================

profile_complete = (
    gender is not None
    and all_scores_selected
    and posting_pathway is not None
)


# ==================================================
# SUBMIT
# ==================================================

if st.button(
    "Find potential school matches →",
    type="primary",
    use_container_width=True,
    disabled=not profile_complete
):

    # ==================================================
    # PROFILE SUMMARY
    # ==================================================

    st.success(
        "Student profile created successfully!"
    )

    st.subheader(
        "Profile summary"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall PSLE Score",
            f"AL {overall_al}"
        )

    with col2:
        st.metric(
            "Pathway",
            posting_pathway
        )

    with col3:
        st.metric(
            "Preferred Zone",
            preferred_zone
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
    # FILTER COP DATA BY PATHWAY
    # ==================================================

    selected_cop = psle_data[
        psle_data["pathway"]
        == posting_pathway
    ].copy()


    # ==================================================
    # MERGE WITH OFFICIAL MOE DIRECTORY
    # ==================================================

    matches = schools.merge(
        selected_cop,
        on="school_key",
        how="inner",
        suffixes=("", "_cop")
    )


    # ==================================================
    # GENDER FILTER
    # ==================================================

    if gender == "Male":

        matches = matches[
            matches["gender"].isin(
                [
                    "Boys",
                    "Co-ed"
                ]
            )
        ].copy()

    elif gender == "Female":

        matches = matches[
            matches["gender"].isin(
                [
                    "Girls",
                    "Co-ed"
                ]
            )
        ].copy()


    # ==================================================
    # HISTORICAL COP FILTER
    # ==================================================

    # Lower AL scores are stronger.
    # Only show schools where the student's score is
    # equal to or stronger than the historical COP.

    matches = matches[
        overall_al <= matches["cutoff"]
    ].copy()


    # ==================================================
    # CALCULATE COP MARGIN
    # ==================================================

    if not matches.empty:

        matches["cop_margin"] = (
            matches["cutoff"]
            - overall_al
        )


    # ==================================================
    # MATCH CLASSIFICATION
    # ==================================================

    def classify_match(margin):

        if margin >= 3:
            return "Comfortable"

        elif margin >= 1:
            return "Competitive"

        else:
            return "Borderline"


    if not matches.empty:

        matches["match_label"] = (
            matches["cop_margin"]
            .apply(classify_match)
        )


    # ==================================================
    # ZONE MATCH
    # ==================================================

    if preferred_zone != "Any":

        matches["zone_match"] = (
            matches["zone"]
            == preferred_zone
        )

    else:

        matches["zone_match"] = True


    # ==================================================
    # IP MATCH
    # ==================================================

    matches["ip_match"] = (
        matches["ip"] == "Yes"
    )


    # ==================================================
    # SORT RESULTS
    # ==================================================

    sort_columns = [
        "zone_match"
    ]

    sort_ascending = [
        False
    ]


    if ip_priority == "Yes":

        sort_columns.append(
            "ip_match"
        )

        sort_ascending.append(
            False
        )


    sort_columns.extend(
        [
            "cutoff",
            "school_name"
        ]
    )

    sort_ascending.extend(
        [
            True,
            True
        ]
    )


    matches = matches.sort_values(
        by=sort_columns,
        ascending=sort_ascending
    )


    # ==================================================
    # RESULTS
    # ==================================================

    st.divider()

    st.subheader(
        "🎓 Potential school matches"
    )

    st.caption(
        "Matches are based on historical cut-off points and "
        "basic profile criteria. They do not predict admission."
    )


    if matches.empty:

        st.warning(
            "No potential matches were found in the current "
            "historical cut-off dataset."
        )

    else:

        # ==================================================
        # RESULT FILTERS
        # ==================================================

        st.subheader(
            "🔎 Refine results"
        )

        filter_col1, filter_col2 = st.columns(2)


        with filter_col1:

            selected_match_types = st.multiselect(
                "Match category",
                options=[
                    "Comfortable",
                    "Competitive",
                    "Borderline"
                ],
                default=[
                    "Comfortable",
                    "Competitive",
                    "Borderline"
                ]
            )


        with filter_col2:

            preferred_zone_only = st.checkbox(
                "Show only schools in preferred zone",
                value=False,
                disabled=preferred_zone == "Any"
            )


        # ----------------------------------------------
        # Apply match-category filter
        # ----------------------------------------------

        filtered_matches = matches[
            matches["match_label"].isin(
                selected_match_types
            )
        ].copy()


        # ----------------------------------------------
        # Apply zone-only filter
        # ----------------------------------------------

        if (
            preferred_zone_only
            and preferred_zone != "Any"
        ):

            filtered_matches = filtered_matches[
                filtered_matches["zone"]
                == preferred_zone
            ].copy()


        st.divider()


        # ==================================================
        # RESULT SUMMARY
        # ==================================================

        st.write(
            f"**{len(filtered_matches)} potential match"
            f"{'es' if len(filtered_matches) != 1 else ''} shown**"
        )


        if preferred_zone != "Any":

            zone_count = len(
                filtered_matches[
                    filtered_matches["zone"]
                    == preferred_zone
                ]
            )

            st.write(
                f"📍 **{zone_count}** match"
                f"{'es' if zone_count != 1 else ''} "
                f"in the **{preferred_zone}** zone."
            )


        comfortable_count = len(
            filtered_matches[
                filtered_matches["match_label"]
                == "Comfortable"
            ]
        )

        competitive_count = len(
            filtered_matches[
                filtered_matches["match_label"]
                == "Competitive"
            ]
        )

        borderline_count = len(
            filtered_matches[
                filtered_matches["match_label"]
                == "Borderline"
            ]
        )


        summary1, summary2, summary3 = st.columns(3)


        with summary1:
            st.metric(
                "Comfortable",
                comfortable_count
            )

        with summary2:
            st.metric(
                "Competitive",
                competitive_count
            )

        with summary3:
            st.metric(
                "Borderline",
                borderline_count
            )


        st.write("")


        # ==================================================
        # COP VISUALISATION
        # ==================================================

        st.subheader(
            "📊 Student score vs historical COP"
        )

        st.caption(
            "Lower AL scores are stronger. Each dot represents a school's "
            "historical cut-off point. The vertical dashed line shows "
            "the student's PSLE score."
        )


        if not filtered_matches.empty:

            chart_data = (
                filtered_matches
                .head(25)
                .copy()
            )

            chart_data["Historical COP"] = (
                chart_data["cutoff"]
            )

            chart_data["School"] = (
                chart_data["school_name"]
            )

            chart_data["Match"] = (
                chart_data["match_label"]
            )


            fig = px.scatter(
                chart_data,
                x="Historical COP",
                y="School",
                symbol="Match",
                hover_data={
                    "zone": True,
                    "gender": True,
                    "pathway": True,
                    "Historical COP": True,
                    "School": False
                },
                title="Historical COP of potential school matches"
            )


            fig.add_vline(
                x=overall_al,
                line_dash="dash",
                annotation_text=f"Student AL {overall_al}",
                annotation_position="top"
            )


            fig.update_xaxes(
                range=[3.5, 32.5],
                dtick=1,
                title="PSLE Achievement Level"
            )


            fig.update_yaxes(
                title=""
            )


            fig.update_layout(
                height=max(
                    450,
                    len(chart_data) * 32
                )
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


            if len(filtered_matches) > 25:

                st.caption(
                    "The chart shows the first 25 ranked matches. "
                    "All matching schools remain listed below."
                )

        else:

            st.info(
                "No schools match the selected filters."
            )


        st.divider()


        # ==================================================
        # SCHOOL CARDS
        # ==================================================

        st.subheader(
            "🏫 School details"
        )


        if filtered_matches.empty:

            st.warning(
                "No schools match the selected result filters. "
                "Try selecting additional match categories or removing "
                "the preferred-zone filter."
            )


        for _, school in filtered_matches.iterrows():

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [
                        4,
                        1
                    ]
                )


                # ------------------------------------------
                # SCHOOL NAME AND DETAILS
                # ------------------------------------------

                with col1:

                    st.subheader(
                        school["school_name"]
                    )

                    st.write(
                        f"**{school['gender']}** · "
                        f"{school['zone']} · "
                        f"{str(school['type_code']).title()}"
                    )


                # ------------------------------------------
                # MATCH LABEL
                # ------------------------------------------

                with col2:

                    if school["match_label"] == "Comfortable":

                        st.success(
                            "Comfortable"
                        )

                    elif school["match_label"] == "Competitive":

                        st.info(
                            "Competitive"
                        )

                    else:

                        st.warning(
                            "Borderline"
                        )


                # ------------------------------------------
                # HISTORICAL COP
                # ------------------------------------------

                st.write(
                    f"**Historical COP ({int(school['year'])}):** "
                    f"AL {int(school['cutoff'])}"
                )

                st.write(
                    f"**Student score:** AL {overall_al}"
                )


                margin = int(
                    school["cop_margin"]
                )


                if margin > 0:

                    st.write(
                        f"**Difference:** Student's score is "
                        f"{margin} AL point"
                        f"{'s' if margin != 1 else ''} "
                        f"stronger than the historical COP."
                    )

                else:

                    st.write(
                        "**Difference:** Student's score is exactly "
                        "at the historical COP."
                    )


                # ------------------------------------------
                # PROGRAMMES
                # ------------------------------------------

                programme_badges = []


                if school["ip"] == "Yes":

                    programme_badges.append(
                        "🎓 IP"
                    )


                if school["sap"] == "Yes":

                    programme_badges.append(
                        "🏮 SAP"
                    )


                if programme_badges:

                    st.write(
                        "**Programmes:** "
                        + " · ".join(
                            programme_badges
                        )
                    )


                # ------------------------------------------
                # WHY THIS SCHOOL APPEARS
                # ------------------------------------------

                st.write(
                    "**Why this school appears:**"
                )

                st.write(
                    "✓ Student's score is equal to or stronger "
                    "than the historical COP."
                )

                st.write(
                    "✓ School gender matches the student's profile."
                )


                if preferred_zone != "Any":

                    if (
                        school["zone"]
                        == preferred_zone
                    ):

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
                        "which matches the stated preference."
                    )


                # ------------------------------------------
                # DISCLAIMER
                # ------------------------------------------

                st.caption(
                    "Historical COPs are reference points only. "
                    "Actual posting outcomes may vary each year."
                )


                # ------------------------------------------
                # COP SOURCE
                # ------------------------------------------

                if pd.notna(
                    school.get(
                        "source_url"
                    )
                ):

                    source_url = str(
                        school[
                            "source_url"
                        ]
                    ).strip()


                    if source_url:

                        st.link_button(
                            "View COP data source ↗",
                            source_url
                        )


                # ------------------------------------------
                # SCHOOL WEBSITE
                # ------------------------------------------

                if (
                    pd.notna(
                        school["website"]
                    )
                    and
                    str(
                        school["website"]
                    ).strip() != ""
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
