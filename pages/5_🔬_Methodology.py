import streamlit as st


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🔬 Methodology")

st.write(
    "This page explains how PSLE Navigator processes user inputs, "
    "integrates structured datasets, builds a FAISS vector store, "
    "retrieves relevant information, performs document summarisation, "
    "and uses a large language model to generate grounded responses."
)

st.info(
    "The application is an educational prototype developed by a team of two. "
    "Its outputs are not official MOE advice and should be verified independently."
)

st.divider()


# ==================================================
# 1. SYSTEM OVERVIEW
# ==================================================

st.header("1. System overview")

st.write(
    """
PSLE Navigator combines deterministic Python logic with a
Retrieval-Augmented Generation (RAG) pipeline and a document summarisation
workflow.

The application separates tasks that are better handled by conventional
code from tasks that benefit from a language model.

**Python is used for:**
- PSLE AL calculation;
- school filtering and ranking;
- historical COP comparison;
- gender matching;
- zone matching;
- CCA-interest matching;
- structured data joins;
- named-school lookup;
- document text extraction; and
- selection of relevant school records.

**The RAG / LLM pipeline is used for:**
- semantic retrieval from custom reference documents;
- policy and process explanations;
- personalised follow-up questions;
- conversational responses;
- grounded natural-language generation; and
- AI-assisted document summarisation.
"""
)

st.code(
    """
User
  |
  v
Streamlit Interface
  |
  +-------------------------------------+
  |                                     |
  v                                     v
School Explorer                    AI Navigator
  |                                     |
  v                                     v
Structured datasets                Intent classification
  |                                     |
  v                                     v
Python matching                Structured retrieval
                                        +
                                 FAISS RAG retrieval
                                        |
                                        v
                                 Combined context
                                        |
                                        v
                                       LLM
                                        |
                                        v
                                 Grounded response

Admin
  |
  v
Knowledge Base
  |
  +---------------------------+
  |                           |
  v                           v
RAG indexing            Document summarisation
""",
    language="text"
)


# ==================================================
# 2. USER ROLES AND LOGIN
# ==================================================

st.header("2. User roles and login")

st.write(
    """
The application includes a simple two-user authentication system.

Credentials are stored using Streamlit Secrets rather than in public
source code.
"""
)

st.markdown(
    """
**Admin role**
- access to School Explorer;
- access to AI Navigator;
- access to Knowledge Base document upload and FAISS index management;
- access to AI Document Summariser;
- access to About Us and Methodology.

**User role**
- access to School Explorer;
- access to AI Navigator;
- access to About Us and Methodology;
- no access to Knowledge Base administration.
"""
)

st.write(
    """
Authentication status and role information are stored in Streamlit
`session_state` for the active session.
"""
)


# ==================================================
# 3. DATA SOURCES
# ==================================================

st.header("3. Data sources")

st.write(
    """
The prototype uses both structured data and unstructured reference
documents.
"""
)

st.subheader("Structured datasets")

st.markdown(
    """
**A. General information of schools**

Used for:
- school name;
- school type;
- gender profile;
- geographical zone;
- Integrated Programme indicator;
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
- comparison with the student's overall AL score.
"""
)

st.warning(
    "The historical COP dataset is curated for the prototype and "
    "does not represent a real-time official admissions database."
)


st.subheader("RAG document corpus")

st.write(
    """
The custom knowledge base contains a small set of documents covering:

- PSLE scoring;
- Secondary 1 Posting;
- Full Subject-Based Banding and Posting Groups;
- DSA-Sec;
- Integrated Programme;
- Higher Mother Tongue and SAP schools; and
- considerations when choosing a secondary school.
"""
)


# ==================================================
# 4. STRUCTURED DATA PREPARATION
# ==================================================

st.header("4. Structured data preparation")

st.write(
    """
The structured datasets use different naming conventions for schools.

For example:

`RIVER VALLEY HIGH SCHOOL`

and:

`River Valley High School (Secondary)`

may refer to the same school.

To join these records, the application creates a normalised school key.
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
    "The original school name is retained for display."
)


# ==================================================
# 5. STUDENT PROFILE
# ==================================================

st.header("5. Student profile")

st.write(
    """
The School Explorer collects non-sensitive information to personalise the
experience.

Inputs include:

- student name or nickname;
- gender;
- four subject AL scores;
- predicted or actual result status;
- selected pathway;
- preferred school zone;
- IP preference;
- DSA-Sec interest;
- interests and talents; and
- Higher Mother Tongue status.
"""
)

st.write(
    """
The four subject AL scores are summed using deterministic Python logic.

The resulting profile is stored in Streamlit `session_state`, allowing
the AI Navigator to reuse the same profile without asking the user to
enter the information again.
"""
)


# ==================================================
# 6. USE CASE 1
# ==================================================

st.header("6. Use Case 1 — School Explorer")

st.subheader("Objective")

st.write(
    """
The School Explorer helps users explore potential secondary school
matches using structured school information and the student's profile.
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
Select COP records for chosen pathway
        |
        v
Join COP records with school directory
        |
        v
Filter by gender
        |
        v
Compare AL with historical COP
        |
        v
Calculate preferred-zone match
        |
        v
Match interests against school CCA records
        |
        v
Rank potential schools
        |
        v
Display filters, metrics,
visualisation and school cards
""",
    language="text"
)


# ==================================================
# 7. SCHOOL MATCHING LOGIC
# ==================================================

st.header("7. School matching logic")

st.write(
    """
Lower PSLE AL scores represent stronger results.

A school is retained where the student's overall AL is equal to or
stronger than the historical COP stored in the prototype dataset.
"""
)

st.subheader("Prototype match categories")

st.markdown(
    """
- **Comfortable** — student is at least 3 AL points stronger than the historical COP.
- **Competitive** — student is 1–2 AL points stronger than the historical COP.
- **Borderline** — student is exactly at the historical COP.
"""
)

st.warning(
    "These labels are explanatory prototype categories only. "
    "They are not probabilities and do not predict admission."
)


# ==================================================
# 8. CCA-INTEREST MATCHING
# ==================================================

st.header("8. CCA-interest matching")

st.write(
    """
Selected interests are mapped to related CCA descriptions in the
structured CCA dataset.

Examples include:

- Football → FOOTBALL
- Robotics & Coding → ROBOTICS / INFOCOMM TECHNOLOGY (COMPUTING)
- Debate → DEBATING AND PUBLIC SPEAKING
- Student Leadership → STUDENT LEADERSHIP-related records
"""
)

st.code(
    """
Selected interest
        |
        v
Interest-to-CCA mapping
        |
        v
Retrieve school's CCA records
        |
        v
Compare mapped activity names
        |
        v
Count matched interests
        |
        v
Use match count in ranking
""",
    language="text"
)

st.warning(
    "CCA availability does not mean the same activity is offered through DSA-Sec."
)


# ==================================================
# 9. DATA VISUALISATION
# ==================================================

st.header("9. Data visualisation")

st.write(
    """
The School Explorer uses Plotly to visualise each shortlisted school's
historical COP against the student's overall AL.

The student's score is shown as a vertical reference line.

This gives users a visual representation of relative position instead of
relying only on text labels.
"""
)


# ==================================================
# 10. ADMIN KNOWLEDGE BASE
# ==================================================

st.header("10. Admin Knowledge Base")

st.write(
    """
The Admin role includes a Knowledge Base page where reference documents
can be uploaded and managed.

Supported formats are PDF and TXT.
"""
)

st.code(
    """
Admin uploads document
        |
        v
Save document
        |
        v
Extract text
        |
        v
Create LangChain Documents
        |
        v
Split into text chunks
        |
        v
Generate embeddings
        |
        v
Store in FAISS
""",
    language="text"
)


# ==================================================
# 11. DOCUMENT TEXT EXTRACTION
# ==================================================

st.header("11. Document processing")

st.write(
    """
TXT files are read directly as text.

PDF files are processed using PyPDF. Text is extracted page by page so
page information can be retained as metadata.
"""
)

st.write(
    """
Each extracted section is represented as a LangChain `Document` with
metadata such as:

- source filename; and
- page number, where available.
"""
)


# ==================================================
# 12. TEXT CHUNKING
# ==================================================

st.header("12. Text chunking")

st.write(
    """
Documents are split using LangChain's
`RecursiveCharacterTextSplitter`.

The current prototype uses:

- chunk size: approximately 900 characters;
- chunk overlap: approximately 150 characters.
"""
)

st.write(
    """
Overlap is used so that important context near a chunk boundary is less
likely to be lost during retrieval.
"""
)


# ==================================================
# 13. EMBEDDINGS
# ==================================================

st.header("13. Embeddings")

st.write(
    """
Each text chunk is converted into an embedding using the OpenAI embedding
model:

`text-embedding-3-small`

An embedding represents the semantic meaning of a text chunk as a numeric
vector.

This allows the system to compare a user's question with document chunks
based on semantic similarity rather than exact keyword matching.
"""
)


# ==================================================
# 14. FAISS VECTOR STORE
# ==================================================

st.header("14. FAISS vector store")

st.write(
    """
The document embeddings are stored using FAISS.

FAISS enables efficient vector similarity search over the custom
knowledge base.

The vector store is built through LangChain's FAISS integration and saved
locally as:

- `index.faiss`
- `index.pkl`
"""
)


# ==================================================
# 15. USE CASE 2
# ==================================================

st.header("15. Use Case 2 — AI Navigator")

st.subheader("Objective")

st.write(
    """
The AI Navigator provides conversational guidance using both structured
school data and a RAG document knowledge base.
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
Named-school detection
        |
        +------------------------------+
        |                              |
        v                              v
Structured retrieval              FAISS retrieval
        |                              |
        v                              v
School / COP / CCA              Relevant document
records                          chunks
        |                              |
        +---------------+--------------+
                        |
                        v
              Combine retrieved context
                        |
                        v
             Add student profile context
                        |
                        v
                 Final LLM call
                        |
                        v
             Grounded personalised answer
                        |
                        v
              Display retrieved sources
""",
    language="text"
)


# ==================================================
# 16. PROMPT CHAINING
# ==================================================

st.header("16. Prompt chaining")

st.write(
    """
The AI Navigator uses multiple stages rather than relying on one large
prompt.
"""
)

st.subheader("Stage 1 — Intent classification")

st.write(
    """
The first model call classifies the user's question into a category such as:

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
The application then performs two types of retrieval:

**Structured retrieval**

Used for:
- school details;
- historical COP records;
- CCA records; and
- profile-based school recommendations.

**FAISS semantic retrieval**

Used for:
- PSLE policy information;
- S1 Posting explanations;
- Full SBB / Posting Groups;
- DSA-Sec guidance;
- IP;
- HMT / SAP; and
- school-choice guidance.
"""
)

st.subheader("Stage 3 — Response generation")

st.write(
    """
The final LLM call receives:

- system instructions;
- student profile;
- classified intent;
- structured records;
- retrieved RAG chunks; and
- recent conversation history.

The model then generates the final grounded response.
"""
)


# ==================================================
# 17. HYBRID RETRIEVAL
# ==================================================

st.header("17. Hybrid retrieval architecture")

st.write(
    """
The prototype uses hybrid retrieval because structured and unstructured
information require different retrieval techniques.
"""
)

st.code(
    """
               User Question
                    |
                    v
             Intent Classification
                    |
          +---------+---------+
          |                   |
          v                   v
Structured Retrieval      FAISS Retrieval
          |                   |
School/COP/CCA data        Document chunks
          |                   |
          +---------+---------+
                    |
                    v
              Combined Context
                    |
                    v
                   LLM
""",
    language="text"
)

st.write(
    """
For example:

- "Does Anderson offer Robotics?" is answered primarily using structured
  CCA data.

- "How does DSA-Sec work?" is answered primarily using the FAISS document
  knowledge base.

- A complex school-choice question may use both.
"""
)


# ==================================================
# 18. RAG RETRIEVAL
# ==================================================

st.header("18. RAG retrieval")

st.write(
    """
For each question, the user's query is converted into an embedding using
the same embedding model used when building the FAISS index.

FAISS performs semantic similarity search and currently retrieves up to
four relevant chunks.

The retrieved chunks are then included in the final model context.
"""
)

st.code(
    """
Question
   |
   v
Question embedding
   |
   v
FAISS similarity search
   |
   v
Top relevant chunks
   |
   v
Add chunks to prompt
   |
   v
LLM answer
""",
    language="text"
)


# ==================================================
# 19. RAG SOURCE VISIBILITY
# ==================================================

st.header("19. RAG source visibility")

st.write(
    """
When RAG chunks are retrieved, the AI Navigator provides expandable
sections that allow the user to inspect the retrieval results.

These can show:

- source filename;
- page number, where available; and
- the retrieved passage itself.

This helps make the RAG process visible and auditable during the
prototype demonstration.
"""
)


# ==================================================
# 20. DOCUMENT SUMMARISATION
# ==================================================

st.header("20. AI Document Summarisation")

st.write(
    """
The Admin Knowledge Base also includes a Generative AI document
summarisation feature.

An administrator selects one document from the knowledge base and chooses
a summary style.
"""
)

st.markdown(
    """
Available summary styles include:

- **Executive summary**
- **Key points**
- **Parent-friendly explanation**
"""
)

st.subheader("Summarisation process flow")

st.code(
    """
Admin selects document
        |
        v
Extract full document text
        |
        v
Select summary style
        |
        v
Build grounded summarisation prompt
        |
        v
Send document text to LLM
        |
        v
Generate document summary
        |
        v
Display summary to Admin
""",
    language="text"
)

st.write(
    """
The summarisation prompt instructs the language model to:

- use only information contained in the selected document;
- avoid adding unsupported facts;
- use British English;
- follow the selected summary style; and
- treat document content as reference material rather than system
  instructions.
"""
)


# ==================================================
# 21. SUMMARISATION INPUT LIMIT
# ==================================================

st.header("21. Summarisation input handling")

st.write(
    """
For this prototype, very large documents are limited to approximately
50,000 characters before being sent for summarisation.

If a document exceeds that limit, the application informs the Admin that
the summary was generated from only the first portion of the document.

This keeps the prototype simple and prevents excessively large single
model requests.
"""
)


# ==================================================
# 22. NAMED-SCHOOL DETECTION
# ==================================================

st.header("22. Named-school detection")

st.write(
    """
Users may refer to schools using shortened names rather than their full
official names.

For example:

`Anderson`

instead of:

`ANDERSON SECONDARY SCHOOL`

The application generates possible aliases from official school names.
"""
)

st.write(
    """
Only aliases that uniquely identify one school are retained.

This reduces the risk of resolving an ambiguous shortened name to the
wrong school.
"""
)


# ==================================================
# 23. PROMPT ENGINEERING
# ==================================================

st.header("23. Prompt engineering")

st.write(
    """
The application uses different prompts for different stages.
"""
)

st.markdown(
    """
**Intent-classification prompt**

Classifies user questions into predefined categories.

**Final-answer system prompt**

Defines:
- role;
- grounding requirements;
- source priority;
- personalisation;
- uncertainty handling;
- prompt-injection safeguards; and
- response style.

**Document-summarisation prompt**

Defines:
- selected summary style;
- source-only summarisation;
- prohibition on unsupported facts; and
- treatment of document text as reference content only.
"""
)


# ==================================================
# 24. PROMPT-INJECTION SAFEGUARDS
# ==================================================

st.header("24. Prompt-injection safeguards")

st.write(
    """
PSLE Navigator applies several prompt-injection safeguards.
"""
)

st.markdown(
    """
**1. System instruction priority**

User instructions cannot override the system rules.

**2. Secret protection**

The model is instructed not to reveal:

- API keys;
- Streamlit Secrets;
- hidden prompts; or
- internal configuration.

**3. Retrieved-document isolation**

RAG chunks are wrapped inside a reference-data section.

The model is explicitly instructed that retrieved content is factual
reference material rather than instructions.

**4. Structured-data isolation**

Structured school records are also provided as reference information
rather than executable instructions.

**5. Grounded answers**

The assistant is instructed not to invent school-specific or policy facts
that are not supported by retrieved evidence.

**6. CCA / DSA distinction**

The model must not infer that a school offers DSA-Sec simply because a
related CCA exists.

**7. Summarisation isolation**

The summariser is told to treat document text as reference content rather
than instructions and to use only the supplied document as its factual
basis.
"""
)


# ==================================================
# 25. API SECURITY
# ==================================================

st.header("25. API and credential security")

st.write(
    """
API keys and login credentials are stored using Streamlit Secrets.

They are not hard-coded into the public GitHub repository.

The application accesses the OpenAI API key through:

`st.secrets["OPENAI_API_KEY"]`
"""
)


# ==================================================
# 26. CONVERSATION MEMORY
# ==================================================

st.header("26. Conversation history")

st.write(
    """
Chat history is stored in Streamlit `session_state`.

Recent messages are included in subsequent model calls so that follow-up
questions can retain conversational context.

The user can clear the conversation at any time.
"""
)


# ==================================================
# 27. ERROR HANDLING
# ==================================================

st.header("27. Error handling")

st.markdown(
    """
The prototype includes basic error handling for:

- incomplete student profiles;
- empty school-search results;
- unavailable FAISS indexes;
- intent-classification failures;
- failed LLM API calls;
- missing school-specific information;
- missing RAG results;
- unreadable PDF or TXT documents; and
- failed document-summarisation requests.
"""
)


# ==================================================
# 28. LLM DATA HANDLING
# ==================================================

st.header("28. LLM data handling")

st.write(
    """
Relevant user questions, recent conversation content, student profile
context and retrieved evidence are sent to the LLM API when generating a
response.

For document summarisation, the selected document's extracted text is
sent to the LLM API.

The prototype intentionally avoids collecting sensitive personal
information.

LLM response and summarisation calls are configured with `store=False`.
"""
)


# ==================================================
# 29. DESIGN PRINCIPLES
# ==================================================

st.header("29. Design principles")

st.markdown(
    """
**Deterministic logic for calculations**

The LLM is not used to calculate PSLE totals or compare scores against
historical COP thresholds.

**RAG for policy information**

Policy and process questions are grounded in a custom knowledge base.

**Structured retrieval for school facts**

School, COP and CCA information is retrieved directly from structured
datasets.

**GenAI for summarisation**

The language model is used to transform document text into concise,
user-friendly summaries.

**Explainability**

The School Explorer explains why each school appears.

**Source transparency**

RAG sources and retrieved passages can be displayed to the user.

**Role separation**

Knowledge-base management and document summarisation are restricted to
the Admin role.
"""
)


# ==================================================
# 30. LIMITATIONS
# ==================================================

st.header("30. Limitations")

st.markdown(
    """
- Historical COPs may change from year to year.
- The COP dataset is curated and incomplete.
- Affiliated-school priority is outside current scope.
- CCA availability does not establish DSA-Sec availability.
- The RAG corpus is intentionally small.
- FAISS may retrieve a chunk that is only partially relevant.
- The LLM may still generate inaccurate information.
- Policies may change after the knowledge-base documents are created.
- AI summaries may omit details from the original document.
- Large documents may be truncated before summarisation.
- Uploaded files and the local FAISS index are not production-grade
  persistent storage.
- Student profiles and conversations are session-based.
"""
)


# ==================================================
# 31. FUTURE ENHANCEMENTS
# ==================================================

st.header("31. Possible future enhancements")

st.markdown(
    """
Potential enhancements include:

- persistent cloud document storage;
- automatic knowledge-base updates;
- larger RAG corpus;
- document versioning;
- metadata-based filtering;
- relevance-score thresholds;
- multi-stage document summarisation for large files;
- more complete historical COP coverage;
- official DSA-Sec talent-area data;
- persistent student profiles;
- saved school shortlists; and
- multi-year COP trend analysis.
"""
)


# ==================================================
# 32. EDUCATIONAL DISCLAIMER
# ==================================================

st.header("32. Educational disclaimer")

st.warning(
    """
This web application is a prototype developed for **educational purposes
only**.

The information provided here is **NOT intended for real-world usage**
and should not be relied upon for making decisions.

The language model may generate inaccurate or incorrect information.
RAG retrieval does not guarantee that the most relevant document chunk
will always be selected, and AI-generated summaries may omit relevant
details from the original source.

Always verify current PSLE, S1 Posting, DSA-Sec and school information
with the Ministry of Education and the relevant school's official
information.
"""
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "PSLE Navigator · AI Bootcamp Capstone · "
    "LangChain + FAISS RAG + GenAI document summarisation"
)
