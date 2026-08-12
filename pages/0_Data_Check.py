import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MOE Data Check",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 MOE Data Check")

# IMPORTANT:
# Replace the filename below with the EXACT filename
# of the MOE CSV you uploaded into the data folder.

FILE_PATH = "data/General information of schools.csv"

try:
    df = pd.read_csv(FILE_PATH)

    st.success(f"Loaded {len(df)} rows successfully.")

    st.subheader("Column names")
    st.write(df.columns.tolist())

    st.subheader("Main level codes")
    st.write(
        df["mainlevel_code"]
        .dropna()
        .value_counts()
    )

    st.subheader("Nature codes")
    st.write(
        df["nature_code"]
        .dropna()
        .value_counts()
    )

    st.subheader("Zone codes")
    st.write(
        df["zone_code"]
        .dropna()
        .value_counts()
    )

    st.subheader("SAP values")
    st.write(
        df["sap_ind"]
        .dropna()
        .value_counts()
    )

    st.subheader("IP values")
    st.write(
        df["ip_ind"]
        .dropna()
        .value_counts()
    )

    st.subheader("Sample records")

    st.dataframe(
        df[
            [
                "school_name",
                "mainlevel_code",
                "nature_code",
                "zone_code",
                "type_code",
                "sap_ind",
                "ip_ind",
                "url_address"
            ]
        ].head(20),
        use_container_width=True
    )

except FileNotFoundError:
    st.error(
        f"Could not find {FILE_PATH}. "
        "Check that the filename exactly matches the CSV in your data folder."
    )
