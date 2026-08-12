import streamlit as st
import pandas as pd
import plotly.express as px
import re


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

    name = name.replace(
        "’",
        "'"
    )

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
# INTEREST → CCA MAPPING
# ==================================================

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
# LOAD SCHOOL DATA
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

    gender_map = {
        "CO-ED SCHOOL": "Co-ed",
        "BOYS' SCHOOL": "Boys",
        "GIRLS' SCHOOL": "Girls"
    }

    df["gender"] = (
        df["nature_code"]
        .map(gender_map)
    )

    df["zone"] = (
        df["zone_code"]
        .astype(str)
        .str.title()
    )

    df = df.rename(
        columns={
            "url_address": "website",
            "sap_ind": "sap",
            "ip_ind": "ip"
        }
    )

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

    return df[
        keep_columns
    ].copy()


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
# LOAD CCA DATA
# ==================================================

@st.cache_data
def load_cca_data():

    df = pd.read_csv(
        "data/CocurricularactivitiesCCAs.csv"
    )

    df = df[
        df["school_section"].isin(
            SECONDARY_LEVELS
        )
    ].copy()

    df["school_key"] = (
        df["School_name"]
        .apply(normalise_school_name)
    )

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
# INTEREST MATCHING
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

    matched = []

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

            matched.append(
                interest
            )

    return matched


# ==================================================
# MATCH CATEGORY
# ==================================================

def classify_match(
    margin
):

    if margin >= 3:

        return "Comfortable"

    elif margin >= 1:

        return "Competitive"

    else:

        return "At historical COP"


# ==================================================
# BUILD SCHOOL MATCHES
# ==================================================

def build_school_matches(
    overall_al,
    gender,
    posting_pathway,
    preferred_zone,
    ip_priority,
    interests
):

    # ----------------------------------------------
    # Select pathway
    # ----------------------------------------------

    selected_cop = psle_data[
        psle_data["pathway"]
        == posting_pathway
    ].copy()


    # ----------------------------------------------
    # Join school information
    # ----------------------------------------------

    matches = schools.merge(
        selected_cop,
        on="school_key",
        how="inner",
        suffixes=(
            "",
            "_cop"
        )
    )


    # ----------------------------------------------
    # Gender filter
    # ----------------------------------------------

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


    # ----------------------------------------------
    # Historical COP filter
    # ----------------------------------------------

    matches = matches[
        overall_al
        <= matches["cutoff"]
    ].copy()


    if matches.empty:

        return matches


    matches["cop_margin"] = (
        matches["cutoff"]
        - overall_al
    )


    matches["match_label"] = (
        matches["cop_margin"]
        .apply(
            classify_match
        )
    )


    # ----------------------------------------------
    # Zone
    # ----------------------------------------------

    if preferred_zone != "Any":

        matches["zone_match"] = (
            matches["zone"]
            == preferred_zone
        )

    else:

        matches["zone_match"] = True


    # ----------------------------------------------
    # IP
    # ----------------------------------------------

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


    # ----------------------------------------------
    # Interests
    # ----------------------------------------------

    matches["matched_interests"] = (
        matches["school_key"]
        .apply(
            lambda key:
            find_interest_matches(
                key,
                interests
            )
        )
    )


    matches["interest_match_count"] = (
        matches["matched_interests"]
        .apply(len)
    )


    # ----------------------------------------------
    # Preserve existing ranking logic
    # ----------------------------------------------

    sort_columns = [
        "zone_match"
    ]

    sort_ascending = [
        False
    ]


    if interests:

        sort_columns.append(
            "interest_match_count"
        )

        sort_ascending.append(
            False
        )


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

    return matches


# ==================================================
# PAGE HEADER
# ==================================================

st.title(
    "🎓 School Explorer"
)

st.write(
    "Build a student profile and explore secondary schools "
    "that may fit their PSLE results, preferences and interests."
)

st.info(
    "💡 Historical cut-off points are reference points only. "
    "They do not predict or guarantee future admission outcomes."
)


# ==================================================
# 1. STUDENT & PSLE
# ==================================================

st.header(
    "1️⃣ Student & PSLE"
)

st.caption(
    "Start with the student's basic profile and PSLE results."
)


with st.container(
    border=True
):

    profile_col1, profile_col2 = (
        st.columns(
            [
                2,
                1
            ]
        )
    )


    with profile_col1:

        student_name = st.text_input(
            "Student's name",
            placeholder="e.g. Alex",
            help=(
                "Optional. Used only to personalise "
                "the current session."
            )
        )


    with profile_col2:

        gender = st.segmented_control(
            "Gender",
            options=[
                "Male",
                "Female"
            ],
            default=None
        )


    st.write("")

    st.subheader(
        "📊 PSLE Subject AL Scores"
    )

    st.caption(
        "AL1 is the strongest grade and AL8 is the weakest. "
        "Select one Achievement Level for each subject."
    )


    score_col1, score_col2 = (
        st.columns(2)
    )

    scores = {}


    with score_col1:

        scores[
            "English Language"
        ] = st.segmented_control(
            "English Language",
            options=list(
                range(1, 9)
            ),
            default=None,
            key="score_English Language"
        )


        scores[
            "Mother Tongue Language"
        ] = st.segmented_control(
            "Mother Tongue Language",
            options=list(
                range(1, 9)
            ),
            default=None,
            key="score_Mother Tongue Language"
        )


    with score_col2:

        scores[
            "Mathematics"
        ] = st.segmented_control(
            "Mathematics",
            options=list(
                range(1, 9)
            ),
            default=None,
            key="score_Mathematics"
        )


        scores[
            "Science"
        ] = st.segmented_control(
            "Science",
            options=list(
                range(1, 9)
            ),
            default=None,
            key="score_Science"
        )


    all_scores_selected = all(
        score is not None
        for score in scores.values()
    )


    if all_scores_selected:

        overall_al = sum(
            scores.values()
        )

        st.write("")

        score_summary_col1, score_summary_col2 = (
            st.columns(
                [
                    1,
                    2
                ]
            )
        )


        with score_summary_col1:

            st.metric(
                "Overall PSLE Score",
                f"AL {overall_al}"
            )


        with score_summary_col2:

            st.success(
                "✓ All four subject scores are complete."
            )

            st.caption(
                "Lower overall AL scores indicate "
                "stronger PSLE performance."
            )


    else:

        overall_al = None

        st.caption(
            "Complete all four subject scores to calculate "
            "the overall PSLE score."
        )


    st.write("")

    result_type = st.radio(
        "These scores are:",
        options=[
            "Predicted / estimated",
            "Actual PSLE results"
        ],
        horizontal=True
    )


# ==================================================
# 2. SCHOOL PREFERENCES
# ==================================================

st.header(
    "2️⃣ School preferences"
)

st.caption(
    "Tell us what matters when exploring possible school options."
)


with st.container(
    border=True
):

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


    preference_col1, preference_col2 = (
        st.columns(2)
    )


    with preference_col1:

        posting_pathway = st.selectbox(
            "Admission pathway to explore",
            options=available_pathways,
            help=(
                "The available choices reflect the "
                "historical COP data currently loaded "
                "into the prototype."
            )
        )

        st.caption(
            "Not sure about Posting Groups? "
            "Ask AI Navigator for an explanation."
        )


    with preference_col2:

        preferred_zone = (
            st.segmented_control(
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
        )

        st.caption(
            "Schools in the preferred zone are ranked first. "
            "Other suitable options can still appear."
        )


    st.write("")

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
        "Choose Yes if you particularly want IP schools "
        "to be prioritised in the results."
    )


# ==================================================
# 3. INTERESTS & PROGRAMMES
# ==================================================

st.header(
    "3️⃣ Interests & programmes"
)

st.caption(
    "Add interests and programme preferences to make "
    "the results more relevant."
)


with st.container(
    border=True
):

    interests = st.multiselect(
        "Interests and talents",
        options=list(
            INTEREST_CCA_MAP.keys()
        ),
        placeholder="Select all that apply"
    )

    st.caption(
        "We'll highlight schools with published CCAs "
        "related to the selected interests."
    )


    if interests:

        st.write(
            f"**{len(interests)} selected:** "
            + ", ".join(
                interests
            )
        )


    st.write("")

    programme_col1, programme_col2 = (
        st.columns(2)
    )


    with programme_col1:

        dsa_interest = st.radio(
            "Considering DSA-Sec?",
            options=[
                "Yes, actively",
                "Maybe / not sure",
                "No"
            ],
            index=1
        )

        st.caption(
            "Used to personalise guidance. "
            "CCA availability is not treated as evidence "
            "that the school offers DSA-Sec in that area."
        )


    with programme_col2:

        higher_mt = st.radio(
            "Higher Mother Tongue at PSLE",
            options=[
                "Higher Chinese",
                "Higher Malay",
                "Higher Tamil",
                "No"
            ],
            index=3
        )


    st.warning(
        "CCA matches show related school activities only. "
        "They do not indicate DSA-Sec availability or eligibility."
    )


# ==================================================
# VALIDATION
# ==================================================

profile_complete = (
    gender is not None
    and all_scores_selected
    and posting_pathway is not None
)


missing_items = []


if gender is None:

    missing_items.append(
        "student gender"
    )


if not all_scores_selected:

    missing_items.append(
        "all four PSLE subject scores"
    )


if posting_pathway is None:

    missing_items.append(
        "admission pathway"
    )


# ==================================================
# READY TO EXPLORE
# ==================================================

st.header(
    "🔎 Ready to explore?"
)


with st.container(
    border=True
):

    if profile_complete:

        st.write(
            "We'll compare this profile against the "
            "school information and historical COP data."
        )


    else:

        st.write(
            "Complete the required information before "
            "searching for school matches."
        )

        st.caption(
            "Still needed: "
            + ", ".join(
                missing_items
            )
            + "."
        )


    find_matches = st.button(
        "Find school matches →",
        type="primary",
        use_container_width=True,
        disabled=not profile_complete
    )


# ==================================================
# FIND SCHOOL MATCHES
# ==================================================

if find_matches:

    student_profile = {

        "name": (
            student_name.strip()
            if student_name
            else "Student"
        ),

        "gender": gender,

        "overall_al": overall_al,

        "english_al": (
            scores[
                "English Language"
            ]
        ),

        "mother_tongue_al": (
            scores[
                "Mother Tongue Language"
            ]
        ),

        "maths_al": (
            scores[
                "Mathematics"
            ]
        ),

        "science_al": (
            scores[
                "Science"
            ]
        ),

        "result_type": result_type,

        "pathway": posting_pathway,

        "preferred_zone": preferred_zone,

        "ip_priority": ip_priority,

        "dsa_interest": dsa_interest,

        "interests": interests,

        "higher_mt": higher_mt
    }


    st.session_state[
        "student_profile"
    ] = student_profile


    st.session_state[
        "school_matches"
    ] = build_school_matches(
        overall_al=overall_al,
        gender=gender,
        posting_pathway=posting_pathway,
        preferred_zone=preferred_zone,
        ip_priority=ip_priority,
        interests=interests
    )


# ==================================================
# RESULTS
# ==================================================

if (
    "school_matches"
    in st.session_state
    and "student_profile"
    in st.session_state
):

    matches = (
        st.session_state[
            "school_matches"
        ].copy()
    )

    searched_profile = (
        st.session_state[
            "student_profile"
        ]
    )


    st.divider()

    st.header(
        "🎓 Potential school matches"
    )

    st.caption(
        "Results use historical COPs and the selected profile. "
        "They do not predict admission outcomes."
    )


    # ==================================================
    # SEARCH SUMMARY
    # ==================================================

    with st.container(
        border=True
    ):

        st.subheader(
            "Your search"
        )

        search_col1, search_col2, search_col3, search_col4 = (
            st.columns(4)
        )


        with search_col1:

            st.metric(
                "PSLE Score",
                f"AL {searched_profile['overall_al']}"
            )


        with search_col2:

            st.metric(
                "Pathway",
                searched_profile[
                    "pathway"
                ]
            )


        with search_col3:

            st.metric(
                "Zone",
                searched_profile[
                    "preferred_zone"
                ]
            )


        with search_col4:

            interest_count = len(
                searched_profile.get(
                    "interests",
                    []
                )
            )

            st.metric(
                "Interests",
                interest_count
            )


        if searched_profile.get(
            "interests"
        ):

            st.caption(
                "Selected interests: "
                + ", ".join(
                    searched_profile[
                        "interests"
                    ]
                )
            )


    # ==================================================
    # EMPTY RESULTS
    # ==================================================

    if matches.empty:

        st.warning(
            "No potential matches were found in the current "
            "historical COP dataset."
        )

        st.write(
            "Try another pathway or adjust the student's preferences."
        )


    else:

        # ==================================================
        # RESULT FILTERS
        # ==================================================

        with st.expander(
            "🔎 Refine results"
        ):

            filter_col1, filter_col2 = (
                st.columns(2)
            )


            with filter_col1:

                selected_match_types = (
                    st.multiselect(
                        "Historical COP position",
                        options=[
                            "Comfortable",
                            "Competitive",
                            "At historical COP"
                        ],
                        default=[
                            "Comfortable",
                            "Competitive",
                            "At historical COP"
                        ]
                    )
                )


            with filter_col2:

                preferred_zone_only = (
                    st.checkbox(
                        "Only show preferred zone",
                        value=False,
                        disabled=(
                            searched_profile[
                                "preferred_zone"
                            ]
                            == "Any"
                        )
                    )
                )


            interest_matches_only = (
                st.checkbox(
                    "Only show schools matching at least one interest",
                    value=False,
                    disabled=not bool(
                        searched_profile.get(
                            "interests",
                            []
                        )
                    )
                )
            )


        # ==================================================
        # APPLY FILTERS
        # ==================================================

        filtered_matches = matches[
            matches["match_label"]
            .isin(
                selected_match_types
            )
        ].copy()


        if (
            preferred_zone_only
            and searched_profile[
                "preferred_zone"
            ] != "Any"
        ):

            filtered_matches = (
                filtered_matches[
                    filtered_matches["zone"]
                    == searched_profile[
                        "preferred_zone"
                    ]
                ]
                .copy()
            )


        if (
            interest_matches_only
            and searched_profile.get(
                "interests"
            )
        ):

            filtered_matches = (
                filtered_matches[
                    filtered_matches[
                        "interest_match_count"
                    ] > 0
                ]
                .copy()
            )


        # ==================================================
        # RESULT SUMMARY
        # ==================================================

        match_count = len(
            filtered_matches
        )


        st.subheader(
            f"{match_count} potential "
            f"{'matches' if match_count != 1 else 'match'}"
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


        at_cop_count = len(
            filtered_matches[
                filtered_matches[
                    "match_label"
                ] == "At historical COP"
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
                "At historical COP",
                at_cop_count
            )


        if searched_profile.get(
            "interests"
        ):

            interest_school_count = len(
                filtered_matches[
                    filtered_matches[
                        "interest_match_count"
                    ] > 0
                ]
            )

            st.info(
                f"⭐ {interest_school_count} displayed "
                f"{'schools' if interest_school_count != 1 else 'school'} "
                f"have at least one CCA related to the selected interests."
            )


        # ==================================================
        # CHART
        # ==================================================

        st.subheader(
            "📊 Historical COP comparison"
        )

        st.caption(
            "Lower AL scores are stronger. "
            "The dashed line represents the student's PSLE score."
        )


        if not filtered_matches.empty:

            chart_data = (
                filtered_matches
                .head(25)
                .copy()
            )


            chart_data[
                "Historical COP"
            ] = (
                chart_data[
                    "cutoff"
                ]
            )


            chart_data[
                "School"
            ] = (
                chart_data[
                    "school_name"
                ]
            )


            chart_data[
                "Match"
            ] = (
                chart_data[
                    "match_label"
                ]
            )


            chart_data[
                "Interest matches"
            ] = (
                chart_data[
                    "interest_match_count"
                ]
            )


            fig = px.scatter(
                chart_data,
                x="Historical COP",
                y="School",
                symbol="Match",
                hover_data={
                    "zone": True,
                    "gender": True,
                    "Interest matches": True,
                    "Historical COP": True,
                    "School": False
                }
            )


            fig.add_vline(
                x=searched_profile[
                    "overall_al"
                ],
                line_dash="dash",
                annotation_text=(
                    f"Student AL "
                    f"{searched_profile['overall_al']}"
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
                    len(chart_data)
                    * 32
                ),
                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10
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
                    "The chart displays the first 25 ranked schools. "
                    "All matching schools remain listed below."
                )


        # ==================================================
        # SCHOOL CARDS
        # ==================================================

        st.divider()

        st.subheader(
            "🏫 Explore the schools"
        )


        if filtered_matches.empty:

            st.warning(
                "No schools match the selected filters. "
                "Try broadening your criteria."
            )


        for _, school in (
            filtered_matches.iterrows()
        ):

            with st.container(
                border=True
            ):

                heading_col, status_col = (
                    st.columns(
                        [
                            4,
                            1.4
                        ]
                    )
                )


                # ------------------------------------------
                # SCHOOL HEADER
                # ------------------------------------------

                with heading_col:

                    st.subheader(
                        school[
                            "school_name"
                        ]
                    )

                    st.caption(
                        f"{school['gender']} · "
                        f"{school['zone']} · "
                        f"{str(school['type_code']).title()}"
                    )


                with status_col:

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
                            "At historical COP"
                        )


                # ------------------------------------------
                # KEY NUMBERS
                # ------------------------------------------

                metric_col1, metric_col2, metric_col3 = (
                    st.columns(3)
                )


                with metric_col1:

                    st.metric(
                        "Student AL",
                        searched_profile[
                            "overall_al"
                        ]
                    )


                with metric_col2:

                    st.metric(
                        f"Historical COP ({int(school['year'])})",
                        int(
                            school[
                                "cutoff"
                            ]
                        )
                    )


                with metric_col3:

                    margin = int(
                        school[
                            "cop_margin"
                        ]
                    )

                    st.metric(
                        "AL difference",
                        margin
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
                # INTEREST MATCHES
                # ------------------------------------------

                matched_interests = (
                    school[
                        "matched_interests"
                    ]
                )


                if matched_interests:

                    st.write(
                        "⭐ **Interest matches:** "
                        + " · ".join(
                            matched_interests
                        )
                    )


                elif searched_profile.get(
                    "interests"
                ):

                    st.caption(
                        "No direct CCA match was found "
                        "for the selected interests."
                    )


                # ------------------------------------------
                # WHY THIS SCHOOL
                # ------------------------------------------

                st.markdown(
                    "**Why this school appears**"
                )


                reasons = [
                    "✓ Student's score is equal to or stronger "
                    "than the historical COP.",
                    "✓ School gender matches the student's profile."
                ]


                if (
                    searched_profile[
                        "preferred_zone"
                    ] != "Any"
                ):

                    if (
                        school[
                            "zone"
                        ]
                        == searched_profile[
                            "preferred_zone"
                        ]
                    ):

                        reasons.append(
                            "✓ Matches the preferred school zone."
                        )

                    else:

                        reasons.append(
                            "• Outside the preferred zone, but still "
                            "meets the core school-match criteria."
                        )


                if matched_interests:

                    reasons.append(
                        "✓ Offers CCA activities related "
                        "to selected interests."
                    )


                if (
                    searched_profile[
                        "ip_priority"
                    ] == "Yes"
                    and school[
                        "ip_match"
                    ]
                ):

                    reasons.append(
                        "✓ Offers the Integrated Programme."
                    )


                for reason in reasons:

                    st.write(
                        reason
                    )


                # ------------------------------------------
                # MORE DETAILS
                # ------------------------------------------

                with st.expander(
                    "More details"
                ):

                    margin = int(
                        school[
                            "cop_margin"
                        ]
                    )


                    if margin > 0:

                        st.write(
                            f"The student's score is **{margin} AL "
                            f"point{'s' if margin != 1 else ''} stronger** "
                            f"than the historical COP."
                        )

                    else:

                        st.write(
                            "The student's score is exactly at "
                            "the historical COP."
                        )


                    st.caption(
                        "Historical COPs are reference points only "
                        "and actual posting outcomes may vary."
                    )


                    if matched_interests:

                        st.caption(
                            "CCA matches do not indicate DSA-Sec "
                            "availability or eligibility."
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
                                "View COP source ↗",
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


        # ==================================================
        # NEXT STEP
        # ==================================================

        st.divider()

        with st.container(
            border=True
        ):

            next_col1, next_col2 = (
                st.columns(
                    [
                        3,
                        1
                    ]
                )
            )


            with next_col1:

                st.subheader(
                    "🤖 Have questions about these schools?"
                )

                st.write(
                    "AI Navigator can use the same student profile "
                    "to explain school options, admissions pathways "
                    "and other considerations."
                )


            with next_col2:

                if st.button(
                    "Ask AI Navigator →",
                    type="primary",
                    use_container_width=True
                ):

                    st.switch_page(
                        "pages/2_🤖_AI_Navigator.py"
                    )
