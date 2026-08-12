import streamlit as st


# ==================================================
# PAGE HEADER
# ==================================================

st.title("ℹ️ About PathFinder")

st.write(
    "PathFinder is an educational GenAI prototype designed to help "
    "Singapore parents and Primary 6 students better understand the "
    "transition from PSLE to secondary school."
)

st.info(
    "This application was developed as an AI Bootcamp capstone project "
    "by a team of two and is intended for educational and demonstration "
    "purposes only."
)

st.divider()


# ==================================================
# PROJECT OVERVIEW
# ==================================================

st.header("🎯 Project overview")

st.write(
    """
Choosing a secondary school can involve many different pieces of
information — PSLE Achievement Levels, Posting Groups, historical
cut-off points, school programmes, CCAs, DSA-Sec and other pathways.

PathFinder brings selected information together into one interactive
application and combines conventional data processing with Generative AI
and Retrieval-Augmented Generation (RAG).

The application contains two main user-facing features:

1. **School Explorer** — personalised exploration of potential secondary
   school options using structured school, historical COP and CCA data.

2. **AI Navigator** — a conversational assistant that combines structured
   school-data retrieval with a FAISS document knowledge base to provide
   grounded explanations and personalised guidance.

The Admin Knowledge Base additionally provides document management and
AI-assisted document summarisation capabilities.
"""
)


# ==================================================
# PROBLEM STATEMENT
# ==================================================

st.header("❓ Problem statement")

st.write(
    """
Parents and students may need to consult multiple websites, documents and
school information sources when considering secondary school options.

It can also be difficult to understand how general policies and school
information relate to an individual student's circumstances.

PathFinder therefore aims to:

- consolidate selected school and admission information;
- make the information easier to explore;
- personalise the experience using non-sensitive student inputs;
- provide conversational explanations through Generative AI;
- use RAG to ground policy and process explanations in a custom
  knowledge base;
- provide AI-assisted summaries of reference documents; and
- help users identify factors they may wish to consider when researching
  secondary schools.
"""
)


# ==================================================
# TARGET USERS
# ==================================================

st.header("👨‍👩‍👧 Target users")

st.write(
    """
The prototype is designed primarily for:

- parents of Primary 6 students;
- Primary 6 students exploring secondary school options; and
- users who want a simpler explanation of Singapore's secondary school
  admission pathways.
"""
)


# ==================================================
# CORE FEATURES
# ==================================================

st.header("🧩 Core features")

feature_1, feature_2 = st.columns(2)


with feature_1:

    st.subheader("🎓 1. School Explorer")

    st.write(
        """
The School Explorer uses deterministic Python logic to compare a student
profile against selected school information.

Features include:

- PSLE subject AL inputs;
- automatic overall AL calculation;
- gender matching;
- pathway selection;
- preferred geographical zone;
- historical COP comparison;
- IP and SAP indicators;
- CCA-interest matching;
- result filters;
- explanatory match categories; and
- historical COP visualisation.
"""
    )


with feature_2:

    st.subheader("🤖 2. AI Navigator")

    st.write(
        """
The AI Navigator provides conversational guidance using a hybrid
retrieval architecture.

Features include:

- student-profile context;
- question intent classification;
- structured school/COP/CCA retrieval;
- FAISS semantic document retrieval;
- Retrieval-Augmented Generation;
- grounded responses;
- source-document display;
- retrieved-passage display;
- conversation history; and
- prompt-injection safeguards.
"""
    )


# ==================================================
# RAG KNOWLEDGE BASE
# ==================================================

st.header("🧠 RAG knowledge base")

st.write(
    """
PathFinder includes a custom document knowledge base for
Retrieval-Augmented Generation (RAG).

Reference documents are processed using the following pipeline:
"""
)

st.code(
    """
Reference documents
        ↓
PDF / TXT text extraction
        ↓
LangChain text splitting
        ↓
Overlapping text chunks
        ↓
OpenAI embeddings
        ↓
FAISS vector store
        ↓
Semantic similarity search
        ↓
Relevant document chunks
        ↓
Grounded LLM response
""",
    language="text"
)

st.write(
    """
The knowledge base contains a small curated corpus covering topics such
as:

- PSLE scoring;
- Secondary 1 Posting;
- Full Subject-Based Banding and Posting Groups;
- DSA-Sec;
- Integrated Programme;
- Higher Mother Tongue and SAP schools; and
- considerations when choosing a secondary school.

This document knowledge base complements, rather than replaces, the
structured school datasets used elsewhere in the application.
"""
)


# ==================================================
# DOCUMENT MANAGEMENT
# ==================================================

st.header("🗂️ Document management & summarisation")

st.write(
    """
The application includes an Admin-only Knowledge Base page for managing
the custom RAG document collection.

Administrators can:

- upload PDF and TXT reference documents;
- view the current document collection;
- build or rebuild the FAISS vector index;
- generate AI-assisted summaries of individual documents; and
- reset the knowledge base.

Uploaded documents are extracted, split into overlapping chunks and
converted into embeddings before being stored in FAISS for semantic
retrieval.
"""
)


# ==================================================
# DOCUMENT SUMMARISER
# ==================================================

st.subheader("✨ AI Document Summariser")

st.write(
    """
The Knowledge Base also includes a Generative AI document summarisation
feature.

An administrator can select a document and generate one of several
summary styles:

- **Executive summary** — highlights the purpose, key information,
  requirements, dates and caveats;
- **Key points** — produces a concise bullet-point summary; or
- **Parent-friendly explanation** — explains the document using simpler
  language.

The summariser uses the extracted text from the selected document as its
source material and instructs the language model not to introduce facts
that are absent from the document.
"""
)

st.code(
    """
Selected document
        ↓
PDF / TXT text extraction
        ↓
Select summary style
        ↓
Grounded summarisation prompt
        ↓
Large Language Model
        ↓
AI-assisted document summary
""",
    language="text"
)


# ==================================================
# USER ROLES
# ==================================================

st.header("🔐 User roles")

st.write(
    """
The prototype includes a simple two-user login system to demonstrate
role-based access.
"""
)

role_1, role_2 = st.columns(2)


with role_1:

    st.subheader("👨‍💼 Admin")

    st.write(
        """
Admin users can access:

- School Explorer;
- AI Navigator;
- Knowledge Base document management;
- AI Document Summariser;
- About Us; and
- Methodology.
"""
    )


with role_2:

    st.subheader("👤 User")

    st.write(
        """
Standard users can access:

- School Explorer;
- AI Navigator;
- About Us; and
- Methodology.

Knowledge Base administration and document summarisation are hidden
from this role.
"""
    )


# ==================================================
# DATA SOURCES
# ==================================================

st.header("📚 Data sources")

st.write(
    """
PathFinder uses two main categories of information.
"""
)


st.subheader("1. Structured datasets")

st.write(
    """
Structured data is used for deterministic school matching and
school-specific retrieval.

The prototype contains:

**General school information**

Used for information such as:

- school name;
- gender profile;
- geographical zone;
- school type;
- Integrated Programme indicator;
- SAP indicator; and
- school website.

**Co-Curricular Activities**

Used for:

- school-level CCA offerings;
- CCA categories; and
- matching selected student interests with related activities.

**Historical PSLE COP data**

Used for:

- historical cut-off points;
- pathway-specific comparisons; and
- school exploration.

Historical COPs are reference points only and do not guarantee admission.
"""
)


st.subheader("2. RAG reference documents")

st.write(
    """
A small document corpus provides explanatory information about PSLE and
secondary-school transition topics.

The documents are converted into embeddings and stored in FAISS.

When a question is asked, semantic similarity search retrieves relevant
chunks before the final language-model response is generated.

The same document collection can also be used by the Admin Document
Summariser.
"""
)


# ==================================================
# HYBRID RETRIEVAL
# ==================================================

st.header("🔀 Hybrid retrieval")

st.write(
    """
The AI Navigator uses two retrieval approaches because different types
of information are better represented in different ways.
"""
)

st.code(
    """
User question
      ↓
Intent classification
      ↓
      ├───────────────┐
      ↓               ↓
Structured        FAISS RAG
retrieval         retrieval
      ↓               ↓
School / COP /    Policy and
CCA records       guidance documents
      │               │
      └───────┬───────┘
              ↓
       Combined context
              ↓
             LLM
              ↓
      Grounded response
""",
    language="text"
)

st.write(
    """
For example, a question about whether a particular school offers
Robotics is better answered using the structured CCA dataset.

A question about how DSA-Sec works is better suited to semantic retrieval
from the document knowledge base.

Questions can also use both sources where appropriate.
"""
)


# ==================================================
# PERSONALISATION
# ==================================================

st.header("👤 Personalisation")

st.write(
    """
The application uses non-sensitive student profile information to
personalise results and explanations.

The profile may include:

- predicted or actual subject AL scores;
- overall PSLE score;
- gender;
- preferred school zone;
- pathway being explored;
- IP preference;
- DSA-Sec interest;
- selected interests and talents; and
- Higher Mother Tongue status.

The same session-based profile can be used by both the School Explorer
and AI Navigator.
"""
)


# ==================================================
# SCHOOL MATCHING
# ==================================================

st.header("🔎 School matching")

st.write(
    """
The School Explorer uses deterministic Python logic rather than asking
the language model to calculate school matches.

The matching process considers factors such as:

1. selected admission pathway;
2. student gender and school gender profile;
3. overall AL relative to the historical COP;
4. preferred geographical zone;
5. selected interests relative to school CCA offerings; and
6. selected programme preferences.

This separation reduces the risk of asking the LLM to perform
calculations that can be handled more reliably using conventional code.
"""
)


# ==================================================
# MATCH CATEGORIES
# ==================================================

st.subheader("Historical COP match categories")

st.write(
    """
For this educational prototype, school matches may be labelled:

- **Comfortable** — student's AL is at least 3 points stronger than the
  historical COP;
- **Competitive** — student's AL is 1–2 points stronger than the
  historical COP; or
- **Borderline** — student's AL is exactly at the historical COP.

These labels describe the student's position relative to a historical
reference point only.

They are not probabilities and do not predict admission outcomes.
"""
)


# ==================================================
# CCA MATCHING
# ==================================================

st.header("🏅 Interest and CCA matching")

st.write(
    """
Selected student interests are mapped to related descriptions in the
CCA dataset.

For example, a Robotics & Coding interest may be matched with activities
such as Robotics or Infocomm Technology (Computing), where those
activities are listed for a school.

An interest match means only that a related CCA is present in the
prototype dataset.

**It does not mean that the school offers DSA-Sec for that activity.**
"""
)


# ==================================================
# AI GROUNDING
# ==================================================

st.header("🛡️ AI grounding and safeguards")

st.write(
    """
The AI Navigator is instructed to use retrieved evidence when answering
factual questions.

The prototype applies several safeguards:

- school-specific claims should rely on retrieved structured records;
- policy explanations should use relevant RAG documents where available;
- missing information should not be invented;
- historical COPs must not be presented as admission guarantees;
- CCA availability must not be treated as proof of DSA-Sec availability;
- retrieved documents are treated as reference material rather than
  executable instructions;
- document summaries should be based only on the selected document; and
- requests to reveal system prompts, API keys or hidden configuration
  are rejected.
"""
)


# ==================================================
# TECHNOLOGY
# ==================================================

st.header("⚙️ Technology used")

st.write(
    """
The prototype uses:

- **Streamlit** — web application interface;
- **Python / pandas** — structured data processing and matching;
- **Plotly** — interactive visualisation;
- **OpenAI API** — intent classification, embeddings, response generation
  and document summarisation;
- **LangChain** — document representation, text splitting and vector-store
  integration;
- **FAISS** — vector storage and semantic similarity search; and
- **PyPDF** — PDF text extraction.
"""
)


# ==================================================
# SCOPE
# ==================================================

st.header("📌 Project scope")

st.write(
    """
PathFinder focuses on selected aspects of the Singapore
PSLE-to-secondary-school transition.

The prototype covers:

- PSLE AL scoring;
- historical COP comparisons;
- selected school information;
- school zone information;
- IP and SAP indicators;
- CCA information;
- S1 Posting explanations;
- DSA-Sec explanations;
- Full Subject-Based Banding and Posting Groups;
- Integrated Programme;
- Higher Mother Tongue;
- personalised school exploration;
- RAG-based question answering;
- visible RAG retrieval results; and
- AI-assisted document summarisation.
"""
)


# ==================================================
# LIMITATIONS
# ==================================================

st.header("⚠️ Limitations")

st.write(
    """
Users should be aware of several limitations:

- Historical COPs may change from year to year.
- The historical COP dataset is curated rather than a real-time national
  admissions database.
- Affiliated-school priority is outside the current prototype scope.
- CCA availability does not establish DSA-Sec availability.
- School programmes and policies may change.
- The RAG system can retrieve an irrelevant or incomplete text chunk.
- The language model can still generate inaccurate information despite
  grounding.
- AI-generated summaries may omit details from the original document.
- Very large documents may be truncated before summarisation in this
  prototype.
- The document corpus is intentionally small.
- Uploaded documents and session information are not intended to provide
  production-grade persistent storage.
- The application cannot replace official MOE or school guidance.
"""
)


# ==================================================
# PRIVACY
# ==================================================

st.header("🔐 Privacy and data handling")

st.write(
    """
The prototype is designed to avoid collecting sensitive personal
information.

Student profile information and chat history are held within the
Streamlit session for personalisation.

The application does not require NRIC numbers, residential addresses or
telephone numbers.

API credentials and login credentials are stored using Streamlit Secrets
rather than being hard-coded into the public source repository.

LLM response and document-summarisation calls are configured with
`store=False`.
"""
)


# ==================================================
# EDUCATIONAL DISCLAIMER
# ==================================================

st.header("⚠️ Important notice")

st.warning(
    """
This web application is a prototype developed for **educational purposes
only**.

The information provided here is **NOT intended for real-world usage**
and should not be relied upon for making decisions.

The language model may generate inaccurate or incorrect information.
RAG retrieval does not guarantee that the most relevant source will
always be selected, and AI-generated summaries should not replace
reading the original source document.

Users assume responsibility for how generated output is used.

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
    "PathFinder · AI Bootcamp Capstone Project · "
    "Structured retrieval + FAISS RAG + GenAI summarisation"
)
