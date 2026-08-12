import streamlit as st
import pandas as pd
import plotly.express as px
import re
from utils.auth import require_password


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="School Explorer | PSLE Navigator",
    page_icon="🎓",
    layout="wide"
)

require_password()


# ==================================================
# CONSTANTS
# ==================================================

SECONDARY_LEVELS = [
    "SECONDARY (S1-S5)",
    "SECONDARY (S1-S4)",
    "MIXED LEVEL (S1-JC2)",
    "MIXED LEVEL (P1-S4)",
    "MIXED LEVEL (S1-S5, JC1-JC2)"
]


# ==================================================
# NORMALISE SCHOOL NAMES
# ==================================================

def normalise_school_name(name):

    if pd.isna(name):
        return ""

    name = str(name).strip().lower()

    name = re.sub(
        r"\s*\(secondary\)\s*$",
        "",
        name
    )

    name = name.replace("’", "'")

    name = re.sub(
        r"[^a-z0-9\s]",
        " ",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    return name


# ==================================================
# INTEREST → CCA MATCHING RULES
# ==================================================

# IMPORTANT:
# These are CCA matches, NOT DSA guarantees.
#
# The values below are matched against MOE's
# cca_grouping_desc field.

INTEREST_CCA_MAP = {

    "Football": [
        "FOOTBALL"
    ],

    "Basketball": [
        "BASKETBALL"
    ],

    "Swimming": [
        "SWIMMING"
    ],

    "Badminton": [
        "BADMINTON"
    ],

    "Athletics": [
        "TRACK AND FIELD",
        "SP-CCA (ATHLETICS)",
        "CROSS COUNTRY"
    ],

    "Table Tennis": [
        "TABLE TENNIS"
    ],

    "Choir / Singing": [
        "CHOIR"
    ],

    "Band / Orchestra": [
        "CONCERT BAND",
        "STRING ENSEMBLE",
        "SINGAPORE NATIONAL YOUTH ORCHESTRA"
    ],

    "Chinese Orchestra": [
        "CHINESE ORCHESTRA",
        "SINGAPORE NATIONAL YOUTH CHINESE ORCHESTRA"
    ],

    "Dance": [
        "MODERN DANCE",
        "CHINESE DANCE",
        "MALAY DANCE",
        "INDIAN DANCE"
    ],

    "Drama / Theatre": [
        "ENGLISH DRAMA",
        "CHINESE DRAMA",
        "ENGLISH LANGUAGE, DRAMA AND DEBATING"
    ],

    "Mathematics": [
        "MATHEMATICS"
    ],

    "Science": [
        "BIOLOGICAL SCIENCE",
        "PHYSICAL SCIENCE",
        "ENVIRONMENTAL SCIENCE"
    ],

    "Robotics & Coding": [
        "ROBOTICS",
        "INFOCOMM TECHNOLOGY (COMPUTING)"
    ],

    "Engineering": [
        "DESIGN AND INNOVATION",
        "ROBOTICS"
    ],

    "Debate": [
        "DEBATING AND PUBLIC SPEAKING",
        "ENGLISH LANGUAGE, DRAMA AND DEBATING"
    ],

    "Creative Writing": [
        "ENGLISH LANGUAGE, DRAMA AND DEBATING"
    ],

    "Visual Arts": [
        "ART AND CRAFTS",
        "PHOTOGRAPHY",
        "DIGITAL MEDIA",
        "INFOCOMM TECHNOLOGY (MEDIA PRODUCTION)"
    ],

    "Student Leadership": [
        "STUDENT LEADERSHIP (COUNCIL)",
        "STUDENT LEADERSHIP (HOUSE)",
        "STUDENT LEADERSHIP (PEER SUPPORT)",
        "STUDENT LEADERSHIP (PREFECT)"
    ],

    "Community Service": [
        "COMMUNITY SERVICE"
    ],

    "Uniformed Groups": [
        "NATIONAL POLICE CADET CORPS",
        "NATIONAL CADET CORPS (LAND)",
        "NATIONAL CADET CORPS (SEA)",
        "NATIONAL CADET CORPS (AIR)",
        "NATIONAL CIVIL DEFENCE CADET CORPS",
        "RED CROSS YOUTH",
        "ST JOHN BRIGADE",
        "GIRL GUIDES",
        "SCOUTS",
        "BOYS' BRIGADE",
        "GIRLS' BRIGADE"
    ]
}


# ==================================================
# LOAD OFFICIAL MOE SCHOOL DATA
# ==================================================

@st.cache_data
def load_school_data():

    df = pd.read_csv(
        "data/General information of schools.csv"
    )

    df = df[
        df["mainlevel_code"].isin(
            SECONDARY_LEVELS
        )
    ].copy()

    # ----------------------------------------------
    # Gender
    # ----------------------------------------------

    gender_map = {
        "CO-ED SCHOOL": "Co-ed",
        "BOYS' SCHOOL": "Boys",
        "GIRLS' SCHOOL": "Girls"
    }

    df["gender"] = (
        df["nature_code"]
        .map(gender_map)
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
# LOAD HISTORICAL COP DATA
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


# ==================================================
# LOAD OFFICIAL MOE CCA DATA
# ==================================================

@st.cache_data
def load_cca_data():

    df = pd.read_csv(
        "data/CocurricularactivitiesCCAs.csv"
    )

    # Keep only schools with secondary-level sections
    df = df[
        df["school_section"].isin(
            SECONDARY_LEVELS
        )
    ].copy()

    # Create matching key
    df["school_key"] = (
        df["School_name"]
        .apply(normalise_school_name)
    )

    # Clean CCA description
    df["cca_grouping_desc"] = (
        df["cca_grouping_desc"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


schools = load_school_data()
psle_data = load_psle_data()
cca_data = load_cca_data()


# ==================================================
# FIND INTEREST MATCHES FOR A SCHOOL
# ==================================================

def find_interest_matches(
    school_key,
    selected_interests
):

    if not selected_interests:
        return []

    school_ccas = set(
        cca_data.loc[
            cca_data["school_key"] == school_key,
            "cca_grouping_desc"
        ].tolist()
    )

    matched_interests = []

    for interest in selected_interests:

        possible_ccas = (
            INTEREST_CCA_MAP.get(
                interest,
                []
            )
        )

        if any(
            cca in school_ccas
            for cca in possible_ccas
        ):
            matched_interests.append(
                interest
            )

    return matched_interests


# ==================================================
# PAGE HEADER
# ==================================================

st.title(
    "🎓 School Explorer"
)

st.write(
    "Explore secondary schools that may match the student's "
    "PSLE profile, location preferences and interests."
)

st.info(
    "💡 Historical cut-off points are provided for reference only. "
    "Actual admission outcomes vary from year to year and are not guaranteed."
)

st.divider()


# ==================================================
# STUDENT PROFILE
# ==================================================

st.subheader(
    "👤 Student profile"
)

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
# PSLE SUBJECT SCORES
# ==================================================

st.subheader(
    "📊 PSLE Subject AL Scores"
)

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

    scores[subject] = (
        st.segmented_control(
            subject,
            options=list(
                range(1, 9)
            ),
            default=None,
            key=f"score_{subject}"
        )
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
        "Select all 4 subjects to calculate "
        "the overall AL score."
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

st.subheader(
    "📘 Admission pathway"
)

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
    "Only pathways currently available in the "
    "historical cut-off dataset are shown."
)

st.divider()


# ==================================================
# SCHOOL PREFERENCES
# ==================================================

st.subheader(
    "📍 School preferences"
)

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
# INTERESTS & DSA
# ==================================================

st.subheader(
    "🏅 Interests & DSA-Sec"
)

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
    options=list(
        INTEREST_CCA_MAP.keys()
    ),
    placeholder="Select all that apply"
)

st.caption(
    "Selected interests are compared against schools' "
    "published CCA offerings to help identify relevant schools."
)

if interests:

    st.write(
        f"**{len(interests)} selected:** "
        + ", ".join(interests)
    )

st.warning(
    "CCA availability does not mean that the school offers "
    "DSA-Sec for that activity. Always check the school's "
    "official DSA-Sec information separately."
)

st.divider()


# ==================================================
# HIGHER MOTHER TONGUE
# ==================================================

st.subheader(
    "🗣️ Mother Tongue"
)

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
    # SAVE SHARED STUDENT PROFILE
    # ==================================================

    st.session_state["student_profile"] = {
        "name": student_name.strip() if student_name else "Student",
        "gender": gender,
        "overall_al": overall_al,
        "english_al": scores["English Language"],
        "mother_tongue_al": scores["Mother Tongue Language"],
        "maths_al": scores["Mathematics"],
        "science_al": scores["Science"],
        "result_type": result_type,
        "pathway": posting_pathway,
        "preferred_zone": preferred_zone,
        "ip_priority": ip_priority,
        "dsa_interest": dsa_interest,
        "interests": interests,
        "higher_mt": higher_mt
    }
    
    # ==================================================
    # PROFILE SUMMARY
    # ==================================================

    st.success(
        "Student profile created successfully!"
    )

    st.subheader(
        "Profile summary"
    )

    col1, col2, col3 = (
        st.columns(3)
    )

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
        suffixes=(
            "",
            "_cop"
        )
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

    # Lower AL is stronger.
    # Only schools where the student's score is equal
    # to or stronger than the historical COP are shown.

    matches = matches[
        overall_al <= matches["cutoff"]
    ].copy()


    # ==================================================
    # COP MARGIN
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
        matches["ip"]
        .astype(str)
        .str.upper()
        .isin(
            [
                "YES",
                "Y",
                "1"
            ]
        )
    )


    # ==================================================
    # CCA / INTEREST MATCHING
    # ==================================================

    if not matches.empty:

        matches[
            "matched_interests"
        ] = matches[
            "school_key"
        ].apply(
            lambda school_key:
            find_interest_matches(
                school_key,
                interests
            )
        )

        matches[
            "interest_match_count"
        ] = matches[
            "matched_interests"
        ].apply(len)

    else:

        matches[
            "matched_interests"
        ] = pd.Series(
            dtype=object
        )

        matches[
            "interest_match_count"
        ] = pd.Series(
            dtype=int
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


    # If interests are selected,
    # rank schools with more CCA matches higher.

    if interests:

        sort_columns.append(
            "interest_match_count"
        )

        sort_ascending.append(
            False
        )


    # If IP is a priority,
    # rank IP schools higher.

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


    matches = (
        matches
        .sort_values(
            by=sort_columns,
            ascending=sort_ascending
        )
        .reset_index(
            drop=True
        )
    )


    # ==================================================
    # RESULTS
    # ==================================================

    st.divider()

    st.subheader(
        "🎓 Potential school matches"
    )

    st.caption(
        "Matches are based on historical cut-off points, "
        "school profile information and selected preferences. "
        "They do not predict admission."
    )


    if matches.empty:

        st.warning(
            "No potential matches were found in the "
            "current historical cut-off dataset."
        )

    else:

        # ==================================================
        # RESULT FILTERS
        # ==================================================

        st.subheader(
            "🔎 Refine results"
        )

        filter_col1, filter_col2 = (
            st.columns(2)
        )


        with filter_col1:

            selected_match_types = (
                st.multiselect(
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
            )


        with filter_col2:

            preferred_zone_only = (
                st.checkbox(
                    "Show only schools in preferred zone",
                    value=False,
                    disabled=(
                        preferred_zone
                        == "Any"
                    )
                )
            )


        # ----------------------------------------------
        # CCA filter
        # ----------------------------------------------

        interest_matches_only = (
            st.checkbox(
                "Show only schools matching at least one selected interest",
                value=False,
                disabled=not bool(interests)
            )
        )


        # ----------------------------------------------
        # Apply match-category filter
        # ----------------------------------------------

        filtered_matches = matches[
            matches["match_label"]
            .isin(
                selected_match_types
            )
        ].copy()


        # ----------------------------------------------
        # Apply zone filter
        # ----------------------------------------------

        if (
            preferred_zone_only
            and preferred_zone != "Any"
        ):

            filtered_matches = (
                filtered_matches[
                    filtered_matches[
                        "zone"
                    ]
                    == preferred_zone
                ].copy()
            )


        # ----------------------------------------------
        # Apply CCA-interest filter
        # ----------------------------------------------

        if (
            interest_matches_only
            and interests
        ):

            filtered_matches = (
                filtered_matches[
                    filtered_matches[
                        "interest_match_count"
                    ] > 0
                ].copy()
            )


        st.divider()


        # ==================================================
        # RESULT SUMMARY
        # ==================================================

        st.write(
            f"**{len(filtered_matches)} potential match"
            f"{'es' if len(filtered_matches) != 1 else ''} shown**"
        )


        comfortable_count = len(
            filtered_matches[
                filtered_matches[
                    "match_label"
                ] == "Comfortable"
            ]
        )

        competitive_count = len(
            filtered_matches[
                filtered_matches[
                    "match_label"
                ] == "Competitive"
            ]
        )

        borderline_count = len(
            filtered_matches[
                filtered_matches[
                    "match_label"
                ] == "Borderline"
            ]
        )


        summary1, summary2, summary3 = (
            st.columns(3)
        )


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


        # ----------------------------------------------
        # Interest summary
        # ----------------------------------------------

        if interests:

            interest_school_count = len(
                filtered_matches[
                    filtered_matches[
                        "interest_match_count"
                    ] > 0
                ]
            )

            st.info(
                f"⭐ {interest_school_count} of the displayed "
                f"schools offer at least one CCA related to "
                f"the selected interests."
            )


        st.write("")


        # ==================================================
        # COP VISUALISATION
        # ==================================================

        st.subheader(
            "📊 Student score vs historical COP"
        )

        st.caption(
            "Lower AL scores are stronger. Each dot represents "
            "a school's historical cut-off point. The vertical "
            "dashed line shows the student's PSLE score."
        )


        if not filtered_matches.empty:

            chart_data = (
                filtered_matches
                .head(25)
                .copy()
            )

            chart_data[
                "Historical COP"
            ] = chart_data[
                "cutoff"
            ]

            chart_data[
                "School"
            ] = chart_data[
                "school_name"
            ]

            chart_data[
                "Match"
            ] = chart_data[
                "match_label"
            ]

            chart_data[
                "Interest matches"
            ] = chart_data[
                "interest_match_count"
            ]


            fig = px.scatter(
                chart_data,
                x="Historical COP",
                y="School",
                symbol="Match",
                hover_data={
                    "zone": True,
                    "gender": True,
                    "pathway": True,
                    "Interest matches": True,
                    "Historical COP": True,
                    "School": False
                },
                title=(
                    "Historical COP of potential "
                    "school matches"
                )
            )


            fig.add_vline(
                x=overall_al,
                line_dash="dash",
                annotation_text=(
                    f"Student AL {overall_al}"
                ),
                annotation_position="top"
            )


            fig.update_xaxes(
                range=[
                    3.5,
                    32.5
                ],
                dtick=1,
                title=(
                    "PSLE Achievement Level"
                )
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


            if len(
                filtered_matches
            ) > 25:

                st.caption(
                    "The chart shows the first 25 ranked "
                    "matches. All matching schools remain "
                    "listed below."
                )

        else:

            st.info(
                "No schools match the selected filters."
            )


        st.divider()


        # ==================================================
        # SCHOOL DETAILS
        # ==================================================

        st.subheader(
            "🏫 School details"
        )


        if filtered_matches.empty:

            st.warning(
                "No schools match the selected result "
                "filters. Try broadening the filters."
            )


        # ==================================================
        # SCHOOL CARDS
        # ==================================================

        for _, school in (
            filtered_matches.iterrows()
        ):

            with st.container(
                border=True
            ):

                col1, col2 = (
                    st.columns(
                        [
                            4,
                            1
                        ]
                    )
                )


                # ------------------------------------------
                # SCHOOL NAME
                # ------------------------------------------

                with col1:

                    st.subheader(
                        school[
                            "school_name"
                        ]
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

                    if (
                        school[
                            "match_label"
                        ]
                        == "Comfortable"
                    ):

                        st.success(
                            "Comfortable"
                        )

                    elif (
                        school[
                            "match_label"
                        ]
                        == "Competitive"
                    ):

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
                    f"**Historical COP "
                    f"({int(school['year'])}):** "
                    f"AL {int(school['cutoff'])}"
                )

                st.write(
                    f"**Student score:** "
                    f"AL {overall_al}"
                )


                margin = int(
                    school[
                        "cop_margin"
                    ]
                )


                if margin > 0:

                    st.write(
                        f"**Difference:** Student's score "
                        f"is {margin} AL point"
                        f"{'s' if margin != 1 else ''} "
                        f"stronger than the historical COP."
                    )

                else:

                    st.write(
                        "**Difference:** Student's score "
                        "is exactly at the historical COP."
                    )


                # ------------------------------------------
                # PROGRAMMES
                # ------------------------------------------

                programme_badges = []


                if school[
                    "ip_match"
                ]:

                    programme_badges.append(
                        "🎓 IP"
                    )


                sap_value = str(
                    school[
                        "sap"
                    ]
                ).upper()


                if sap_value in [
                    "YES",
                    "Y",
                    "1"
                ]:

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
                # INTEREST / CCA MATCHES
                # ------------------------------------------

                matched_interests = (
                    school[
                        "matched_interests"
                    ]
                )


                if matched_interests:

                    st.success(
                        "⭐ "
                        + str(
                            len(
                                matched_interests
                            )
                        )
                        + " interest match"
                        + (
                            "es"
                            if len(
                                matched_interests
                            ) != 1
                            else ""
                        )
                    )

                    st.write(
                        "**Related CCA offerings:** "
                        + " · ".join(
                            matched_interests
                        )
                    )

                elif interests:

                    st.caption(
                        "No direct CCA match was found "
                        "for the selected interests."
                    )


                # ------------------------------------------
                # WHY THIS SCHOOL APPEARS
                # ------------------------------------------

                st.write(
                    "**Why this school appears:**"
                )

                st.write(
                    "✓ Student's score is equal to or "
                    "stronger than the historical COP."
                )

                st.write(
                    "✓ School gender matches the "
                    "student's profile."
                )


                if (
                    preferred_zone
                    != "Any"
                ):

                    if (
                        school[
                            "zone"
                        ]
                        == preferred_zone
                    ):

                        st.write(
                            "✓ Matches preferred "
                            "school zone."
                        )

                    else:

                        st.write(
                            "• Outside the preferred "
                            "zone, but shown as another "
                            "possible option."
                        )


                if matched_interests:

                    st.write(
                        "✓ Offers CCA activities related "
                        "to the student's selected interests."
                    )


                if (
                    ip_priority == "Yes"
                    and school[
                        "ip_match"
                    ]
                ):

                    st.write(
                        "✓ Offers the Integrated Programme, "
                        "matching the stated preference."
                    )


                # ------------------------------------------
                # DISCLAIMERS
                # ------------------------------------------

                st.caption(
                    "Historical COPs are reference points only. "
                    "Actual posting outcomes may vary each year."
                )

                if matched_interests:

                    st.caption(
                        "CCA matches indicate related activities "
                        "listed in the MOE CCA dataset. They do "
                        "not indicate DSA-Sec availability or "
                        "eligibility."
                    )


                # ------------------------------------------
                # LINKS
                # ------------------------------------------

                link_col1, link_col2 = (
                    st.columns(2)
                )


                with link_col1:

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
                                source_url,
                                use_container_width=True
                            )


                with link_col2:

                    if (
                        pd.notna(
                            school[
                                "website"
                            ]
                        )
                        and str(
                            school[
                                "website"
                            ]
                        ).strip()
                        != ""
                    ):

                        website = str(
                            school[
                                "website"
                            ]
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
                            website,
                            use_container_width=True
                        )
