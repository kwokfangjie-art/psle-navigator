import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import quote_plus


# ==================================================
# SETTINGS
# ==================================================

INPUT_FILE = "data/General information of schools.csv"
OUTPUT_FILE = "data/psle_ranges.csv"

REQUEST_DELAY = 1.0

BASE_URL = (
    "https://www.moe.gov.sg/schoolfinder/"
    "schooldetail?schoolname={school_slug}"
)


# ==================================================
# NORMALISE SCHOOL NAME
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
# CREATE SCHOOLFINDER SLUG
# ==================================================

def create_school_slug(school_name):

    name = school_name.lower().strip()

    name = name.replace("&", "and")
    name = name.replace("’", "")
    name = name.replace("'", "")
    name = name.replace(".", "")
    name = name.replace(",", "")
    name = name.replace("(", "")
    name = name.replace(")", "")

    name = re.sub(
        r"[^a-z0-9]+",
        "-",
        name
    )

    return name.strip("-")


# ==================================================
# EXTRACT SCORE YEAR
# ==================================================

def extract_score_year(text):

    match = re.search(
        r"PSLE score range of\s+(\d{4})",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


# ==================================================
# EXTRACT SCORE RANGE
# ==================================================

def parse_score_range(text):

    if text is None:
        return None, None

    text = str(text).strip()

    match = re.search(
        r"(\d+)\s*(?:\([A-Z]\))?\s*[-–]\s*"
        r"(\d+)\s*(?:\([A-Z]\))?",
        text
    )

    if not match:
        return None, None

    low = int(match.group(1))
    high = int(match.group(2))

    return low, high


# ==================================================
# EXTRACT HCL / SPECIAL LETTERS
# ==================================================

def extract_score_letters(text):

    if text is None:
        return None, None

    letters = re.findall(
        r"\(([A-Z])\)",
        str(text)
    )

    if len(letters) >= 2:
        return letters[0], letters[1]

    if len(letters) == 1:
        return letters[0], letters[0]

    return None, None


# ==================================================
# DETECT PATHWAY
# ==================================================

def standardise_pathway(text):

    text = str(text).strip().lower()

    if "posting group 3" in text:
        return "Posting Group 3"

    if "posting group 2" in text:
        return "Posting Group 2"

    if "posting group 1" in text:
        return "Posting Group 1"

    if "integrated programme" in text:
        return "Integrated Programme"

    if text == "ip":
        return "Integrated Programme"

    return None


# ==================================================
# GET SCHOOL PAGE
# ==================================================

def get_school_page(school_name):

    slug = create_school_slug(school_name)

    url = BASE_URL.format(
        school_slug=quote_plus(slug)
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(compatible; PSLE-Navigator-Educational-Prototype/1.0)"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return response.text, url


# ==================================================
# PARSE SCHOOL PAGE
# ==================================================

def parse_school_page(
    school_name,
    html,
    source_url
):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    page_text = soup.get_text(
        " ",
        strip=True
    )

    year = extract_score_year(
        page_text
    )

    records = []


    # ----------------------------------------------
    # Find all tables
    # ----------------------------------------------

    tables = soup.find_all("table")


    for table in tables:

        table_text = table.get_text(
            " ",
            strip=True
        )

        if (
            "Posting Group" not in table_text
            and
            "Integrated Programme" not in table_text
        ):
            continue


        rows = table.find_all("tr")


        # ------------------------------------------
        # Determine whether table contains
        # affiliated / non-affiliated columns
        # ------------------------------------------

        header_text = ""

        if rows:
            header_text = rows[0].get_text(
                " ",
                strip=True
            ).lower()

        has_non_affiliated = (
            "non-affiliated" in header_text
            or
            "non affiliated" in header_text
        )


        for row in rows:

            cells = row.find_all(
                ["th", "td"]
            )

            cell_text = [
                cell.get_text(
                    " ",
                    strip=True
                )
                for cell in cells
            ]


            if not cell_text:
                continue


            pathway = standardise_pathway(
                cell_text[0]
            )

            if pathway is None:
                continue


            # --------------------------------------
            # Decide which range to use
            # --------------------------------------

            range_text = None


            if has_non_affiliated:

                # Expected structure:
                # pathway | affiliated | non-affiliated

                if len(cell_text) >= 3:
                    range_text = cell_text[-1]


            else:

                # Expected structure:
                # pathway | score range

                if len(cell_text) >= 2:
                    range_text = cell_text[-1]


            if not range_text:
                continue


            score_low, score_high = (
                parse_score_range(
                    range_text
                )
            )


            if (
                score_low is None
                or
                score_high is None
            ):
                continue


            hcl_low, hcl_high = (
                extract_score_letters(
                    range_text
                )
            )


            records.append(
                {
                    "school_name": school_name,
                    "school_key": normalise_school_name(
                        school_name
                    ),
                    "year": year,
                    "pathway": pathway,
                    "score_low": score_low,
                    "score_high": score_high,
                    "hcl_low": hcl_low,
                    "hcl_high": hcl_high,
                    "source_url": source_url
                }
            )


    return records


# ==================================================
# LOAD SECONDARY SCHOOLS
# ==================================================

def load_secondary_schools():

    df = pd.read_csv(
        INPUT_FILE
    )

    secondary_levels = [
        "SECONDARY (S1-S5)",
        "SECONDARY (S1-S4)",
        "MIXED LEVEL (S1-JC2)",
        "MIXED LEVEL (P1-S4)",
        "MIXED LEVEL (S1-S5, JC1-JC2)"
    ]

    df = df[
        df["mainlevel_code"].isin(
            secondary_levels
        )
    ].copy()

    return (
        df["school_name"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


# ==================================================
# MAIN
# ==================================================

def main():

    schools = load_secondary_schools()

    print(
        f"Found {len(schools)} secondary-level schools."
    )

    all_records = []
    failed_schools = []


    for index, school_name in enumerate(
        schools,
        start=1
    ):

        print(
            f"[{index}/{len(schools)}] "
            f"{school_name}"
        )

        try:

            html, source_url = (
                get_school_page(
                    school_name
                )
            )

            records = parse_school_page(
                school_name,
                html,
                source_url
            )


            if records:

                all_records.extend(
                    records
                )

                print(
                    f"  → {len(records)} "
                    f"score range(s) found"
                )

            else:

                print(
                    "  → No PSLE score ranges found"
                )

                failed_schools.append(
                    school_name
                )


        except Exception as error:

            print(
                f"  → ERROR: {error}"
            )

            failed_schools.append(
                school_name
            )


        time.sleep(
            REQUEST_DELAY
        )


    # ----------------------------------------------
    # Save output
    # ----------------------------------------------

    results = pd.DataFrame(
        all_records
    )


    if not results.empty:

        results = results.sort_values(
            by=[
                "school_name",
                "pathway"
            ]
        )

        results.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print()
        print(
            f"Saved {len(results)} rows "
            f"to {OUTPUT_FILE}"
        )

    else:

        print(
            "No PSLE range data was extracted."
        )


    # ----------------------------------------------
    # Show failures
    # ----------------------------------------------

    if failed_schools:

        print()
        print(
            "Schools requiring manual review:"
        )

        for school in failed_schools:
            print(
                f" - {school}"
            )


if __name__ == "__main__":
    main()
