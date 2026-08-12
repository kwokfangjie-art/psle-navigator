import streamlit as st


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🔬 Methodology")

st.write(
    "This page explains how PSLE Navigator processes user inputs, "
    "integrates multiple datasets, retrieves relevant information, "
    "and uses a large language model to generate grounded responses."
)

st.info(
    "The application is an educational prototype. "
    "Its outputs are not official MOE advice and must be verified independently."
)

st.divider()


# ==================================================
# 1. SYSTEM OVERVIEW
# ==================================================

st.header("1. System overview")

st.write(
    """
PSLE Navigator combines deterministic Python logic with an LLM-powered
assistant.

The application deliberately separates tasks that are better handled by
code from tasks that are better handled by a language model.

**Python is used for:**
- PSLE AL calculation;
- filtering and ranking schools;
- comparing student scores against historical COPs;
- school gender matching;
- zone matching;
- CCA-interest matching;
- dataset joins; and
- retrieving school-specific records.

**The LLM is used for:**
- explaining policies and pathways;
- answering follow-up questions;
- personalising explanations;
- interpreting retrieved school information; and
- presenting information in plain language.
"""
)

st.code(
    """
User
  |
  v
Streamlit Interface
  |
  +----------------------------+
  |                            |
  v                            v
School Explorer            AI Navigator
  |                            |
  v                            v
Python matching          Intent classification
  |                            |
  v                            v
Local datasets           Relevant data retrieval
  |                            |
  v                            v
Ranked results           Context construction
                               |
                               v
                              LLM
                               |
                               v
                        Grounded response
""",
    language="text"
)


# ==================================================
# 2. DATA SOURCES
# ==================================================

st.header("2. Data sources")

st.write(
    """
The prototype consolidates information from multiple sources.

The main local datasets are:
"""
)

st.markdown(
    """
**A. General information of schools**

Used for:
- school name;
- school type;
- gender profile;
- geographical zone;
- IP indicator;
- SAP indicator; and
- school website.

**B. Co-curricular activities dataset**

Used for:
- school-level CCA offerings;
- CCA grouping descriptions; and
- matching student interests to school activities.

**C. Historical PSLE COP dataset**

Used for:
- historical cut-off points;
- pathway-specific school matching; and
- comparison against the student's overall AL score.
"""
)

st.warning(
    "The historical COP dataset is curated for this prototype and "
    "does not represent an official real-time admissions database."
)


# ==================================================
# 3. DATA PREPARATION
# ==================================================

st.header("3. Data preparation")

st.write(
    """
The raw datasets use slightly different school naming conventions.

For example, one source may use:

`RIVER VALLEY HIGH SCHOOL`

while another may use:

`River Valley High School (Secondary)`

To join these records reliably, PSLE Navigator creates a normalised
school key.
"""
)

st.code(
    """
Original school name
        |
        v
Convert to lowercase
        |
        v
Standardise apostrophes
        |
        v
Remove selected suffixes
        |
        v
Remove punctuation
        |
        v
Collapse repeated spaces
        |
        v
Normalised school key
""",
    language="text"
)

st.write(
    """
The normalised key is used only for dataset matching.

The original school name from the main school directory is retained for
display to the user.
"""
)


# ==================================================
# 4. STUDENT PROFILE
# ==================================================

st.header("4. Student profile")

st.write(
    """
The School Explorer collects a set of non-sensitive inputs to personalise
the experience.

These may include:

- student name or nickname;
- gender;
- four PSLE subject AL scores;
- predicted or actual result status;
- pathway being explored;
- preferred school zone;
- IP preference;
- DSA-Sec interest;
- selected interests and talents; and
- Higher Mother Tongue status.
"""
)

st.write(
    """
The four subject AL scores are added using deterministic Python logic to
produce the overall PSLE score.

The profile is then stored in Streamlit `session_state`, allowing the
School Explorer and AI Navigator to share the same profile during the
active session.
"""
)


# ==================================================
# 5. USE CASE 1
# ==================================================

st.header("5. Use Case 1 — School Explorer")

st.subheader("Objective")

st.write(
    """
The School Explorer helps users identify potential school matches based on
the student profile and historical school information.
"""
)

st.subheader("Process flow")

st.code(
    """
Student enters profile
        |
        v
Validate required inputs
        |
        v
Calculate overall PSLE AL
        |
        v
Select historical COP records
for chosen pathway
        |
        v
Join COP data with MOE school directory
        |
        v
Filter by school gender
        |
        v
Compare student AL with historical COP
        |
        v
Calculate zone match
        |
        v
Match interests against MOE CCA data
        |
        v
Rank potential school matches
        |
        v
Display filters, metrics,
visualisation and school cards
""",
    language="text"
)


# ==================================================
# 6. SCHOOL MATCHING LOGIC
# ==================================================

st.header("6. School matching logic")

st.write(
    """
For the historical COP comparison, lower PSLE AL scores are treated as
stronger results.

A school remains in the candidate set where the student's score is equal
to or stronger than the historical COP recorded in the prototype dataset.
"""
)

st.subheader("Match categories")

st.markdown(
    """
The application uses three simple explanatory categories:

- **Comfortable** — student is at least 3 AL points stronger than the historical COP.
- **Competitive** — student is 1–2 AL points stronger than the historical COP.
- **Borderline** — student is exactly at the historical COP.
"""
)

st.warning(
    "These categories are prototype labels only. "
    "They are not probabilities and do not predict admission."
)


# ==================================================
# 7. CCA-INTEREST MATCHING
# ==================================================

st.header("7. CCA-interest matching")

st.write(
    """
Selected student interests are mapped to related descriptions in the MOE
CCA dataset.

Examples include:

- Football → FOOTBALL
- Robotics & Coding → ROBOTICS / INFOCOMM TECHNOLOGY (COMPUTING)
- Debate → DEBATING AND PUBLIC SPEAKING
- Student Leadership → STUDENT LEADERSHIP-related entries
"""
)

st.code(
    """
Selected student interest
        |
        v
Interest-to-CCA mapping
        |
        v
Retrieve school's listed CCAs
        |
        v
Check for matching CCA descriptions
        |
        v
Count matched interests
        |
        v
Use match count as a ranking factor
""",
    language="text"
)

st.warning(
    "A CCA match does not mean that the school offers DSA-Sec "
    "for the same activity."
)


# ==================================================
# 8. DATA VISUALISATION
# ==================================================

st.header("8. Data visualisation")

st.write(
    """
The School Explorer uses a Plotly scatter visualisation to compare the
student's overall AL score with the historical COPs of shortlisted schools.

A vertical reference line represents the student's score, while each
school is plotted using its historical COP.

This allows users to see the student's relative position across multiple
schools rather than relying only on text labels.
"""
)


# ==================================================
# 9. USE CASE 2
# ==================================================

st.header("9. Use Case 2 — AI Navigator")

st.subheader("Objective")

st.write(
    """
The AI Navigator provides conversational explanations of PSLE and
secondary-school admission topics while using the student's shared profile
and retrieved dataset records where relevant.
"""
)

st.subheader("Process flow")

st.code(
    """
User asks question
        |
        v
Prompt Chain Step 1:
Intent classification
        |
        v
Detect named schools / question type
        |
        v
Prompt Chain Step 2:
Retrieve relevant data
        |
        +-----------------------------+
        |                             |
        v                             v
Student-profile matches        Named-school records
        |                             |
        +-------------+---------------+
                      |
                      v
Build grounded reference context
                      |
                      v
Combine with system instructions
and student profile
                      |
                      v
Final LLM call
                      |
                      v
Grounded personalised response
""",
    language="text"
)


# ==================================================
# 10. PROMPT CHAINING
# ==================================================

st.header("10. Prompt chaining")

st.write(
    """
The AI Navigator uses more than one model call instead of relying on a
single large prompt.
"""
)

st.subheader("Stage 1 — Intent classification")

st.write(
    """
The first model call classifies the question into a category such as:

- school recommendation;
- school-specific question;
- CCA / interest question;
- DSA-Sec;
- S1 Posting;
- IP / SAP / HMT;
- general PSLE question; or
- off-topic.
"""
)

st.subheader("Stage 2 — Retrieval")

st.write(
    """
Based on the identified intent, Python retrieves relevant local records.

For example:

- a school recommendation request retrieves profile-compatible schools;
- a named-school question retrieves school details, historical COP records
  and CCA offerings; and
- an interest-related request retrieves schools that match the student's
  selected interests.
"""
)

st.subheader("Stage 3 — Response generation")

st.write(
    """
The retrieved records are inserted into a separate reference-data section.

The final LLM call receives:

- system instructions;
- the student's profile;
- the classified question intent;
- retrieved reference records; and
- recent conversation history.
"""
)


# ==================================================
# 11. RETRIEVAL AND GROUNDING
# ==================================================

st.header("11. Retrieval and grounding")

st.write(
    """
For school-specific questions, the AI is not expected to rely solely on
its pre-trained knowledge.

Relevant records are retrieved from the local datasets and supplied to the
model as reference information.
"""
)

st.code(
    """
Question:
"Does Anderson offer Robotics as a CCA?"

        |
        v

Named-school detection:
"Anderson"
        |
        v
Resolve to:
ANDERSON SECONDARY SCHOOL
        |
        v
Retrieve CCA records
        |
        v
ROBOTICS found in dataset
        |
        v
Send retrieved record to LLM
        |
        v
Answer based on supplied evidence
""",
    language="text"
)

st.write(
    """
If a school-specific fact is not found in the retrieved records, the model
is instructed to say that the prototype does not contain enough
information rather than inventing the answer.
"""
)


# ==================================================
# 12. NAMED-SCHOOL DETECTION
# ==================================================

st.header("12. Named-school detection")

st.write(
    """
Users may refer to schools using shortened names rather than their full
official names.

For example:

`Anderson`

instead of:

`ANDERSON SECONDARY SCHOOL`

The application therefore generates possible school aliases.
"""
)

st.write(
    """
Only aliases that uniquely identify a single school are retained.

This helps reduce the risk of incorrectly resolving an ambiguous short
school name.
"""
)


# ==================================================
# 13. PROMPT ENGINEERING
# ==================================================

st.header("13. Prompt engineering")

st.write(
    """
The AI system prompt contains several groups of instructions.
"""
)

st.markdown(
    """
**Role instructions**

Define PSLE Navigator as an educational assistant focused on Singapore's
PSLE-to-secondary-school transition.

**Scope instructions**

Limit the assistant to relevant topics such as PSLE, S1 Posting, DSA-Sec,
IP, SAP, Higher Mother Tongue, secondary schools and CCAs.

**Grounding instructions**

Require school-specific answers to rely on retrieved reference data.

**Personalisation instructions**

Tell the model to use the student profile only where relevant.

**Uncertainty instructions**

Require the model to state when information cannot be confirmed.

**Response-style instructions**

Use British English, clear headings, short paragraphs and concise
explanations.
"""
)


# ==================================================
# 14. PROMPT-INJECTION SAFEGUARDS
# ==================================================

st.header("14. Prompt-injection safeguards")

st.write(
    """
The assignment requires consideration of prompt-injection risks.

PSLE Navigator applies several controls.
"""
)

st.markdown(
    """
**1. System instruction priority**

The model is told not to follow user instructions that conflict with the
application's system rules.

**2. Secret protection**

The model is explicitly instructed never to reveal API keys, Streamlit
Secrets, hidden prompts or internal configuration.

**3. Reference-data isolation**

Retrieved records are placed inside a clearly marked reference-data
section.

The model is explicitly told that reference data is factual information,
not executable instructions.

**4. Limited topic scope**

Clearly off-topic requests are declined.

**5. Grounded school answers**

The model is instructed not to invent school-specific information that is
missing from the retrieved data.
"""
)


# ==================================================
# 15. API KEY SECURITY
# ==================================================

st.header("15. API key security")

st.write(
    """
The OpenAI API key is not hard-coded into the source code.

It is stored using Streamlit Community Cloud's Secrets feature and
accessed by the application using:

`st.secrets["OPENAI_API_KEY"]`

This prevents the API key from being exposed in the public GitHub
repository.
"""
)


# ==================================================
# 16. LLM DATA HANDLING
# ==================================================

st.header("16. LLM data handling")

st.write(
    """
The application sends relevant conversation content, student profile
context and retrieved reference information to the LLM API when generating
a response.

The prototype deliberately avoids collecting sensitive information such
as NRIC numbers, home addresses or telephone numbers.

The Responses API calls in the AI Navigator are configured with
`store=False`.
"""
)


# ==================================================
# 17. CONVERSATION MEMORY
# ==================================================

st.header("17. Conversation memory")

st.write(
    """
Chat messages are stored in Streamlit `session_state` during the current
application session.

Recent conversation messages are included in subsequent model calls so
that the assistant can understand follow-up questions.

The user can clear the conversation using the Clear button.
"""
)


# ==================================================
# 18. PASSWORD PROTECTION
# ==================================================

st.header("18. Password protection")

st.write(
    """
The deployed prototype is protected by a simple password gate.

The application password is stored using Streamlit Secrets rather than
inside the public source code.

Authentication status is stored in Streamlit `session_state` for the
active session.
"""
)


# ==================================================
# 19. ERROR HANDLING
# ==================================================

st.header("19. Error handling")

st.write(
    """
The prototype includes basic error-handling mechanisms.

Examples include:

- disabling the school-search button until required profile fields are
  completed;
- returning an empty-result message where no school matches are found;
- falling back to a general question category if intent classification
  fails;
- returning a user-friendly error message if an LLM API call fails; and
- stating when school-specific information is unavailable in the local
  datasets.
"""
)


# ==================================================
# 20. DESIGN PRINCIPLES
# ==================================================

st.header("20. Design principles")

st.markdown(
    """
**Deterministic logic for calculations**

The LLM is not used to calculate PSLE totals or determine whether a score
passes a historical COP threshold.

**LLM for explanation**

The language model is used where natural-language interpretation and
explanation provide value.

**Explainability**

School cards explain why each school appears.

**Source awareness**

The application distinguishes between school-directory information,
historical COP data and CCA information.

**Shared context**

The School Explorer and AI Navigator use the same session-based student
profile to reduce repeated user input.
"""
)


# ==================================================
# 21. APPLICATION NAVIGATION
# ==================================================

st.header("21. Application navigation")

st.write(
    """
The application uses Streamlit's explicit multipage navigation.

The top-level `app.py` file is responsible for:

- page configuration;
- password protection; and
- defining the available navigation pages.

The individual pages contain only their own page-specific logic.

The main navigation contains:

- Home;
- School Explorer;
- AI Navigator;
- About Us; and
- Methodology.
"""
)


# ==================================================
# 22. LIMITATIONS
# ==================================================

st.header("22. Limitations")

st.markdown(
    """
- Historical COPs are not current-year guarantees.
- The COP dataset is curated rather than a complete real-time national
  dataset.
- Affiliated-school priority is outside the current scope.
- CCA information does not represent DSA-Sec talent-area information.
- The AI may still generate incorrect or incomplete information.
- Some policy explanations may become outdated as MOE policies change.
- Student profile and chat history are currently session-based rather
  than permanently stored.
- The prototype does not provide real-time school vacancies or posting
  results.
"""
)


# ==================================================
# 23. POSSIBLE FUTURE ENHANCEMENTS
# ==================================================

st.header("23. Possible future enhancements")

st.markdown(
    """
Potential future improvements include:

- official DSA-Sec talent-area data;
- more complete historical COP coverage;
- multiple-year COP trend visualisation;
- school comparison tools;
- persistent user profiles;
- saved school shortlists;
- more comprehensive policy retrieval;
- current-year policy update mechanisms; and
- richer school programme information.
"""
)


# ==================================================
# 24. EDUCATIONAL DISCLAIMER
# ==================================================

st.header("24. Educational disclaimer")

st.warning(
    """
This web application is a prototype developed for **educational purposes
only**.

The information provided here is **NOT intended for real-world usage**
and should not be relied upon for making decisions.

The language model may generate inaccurate or incorrect information.

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
    "PSLE Navigator · AI Bootcamp Capstone · Methodology"
)
