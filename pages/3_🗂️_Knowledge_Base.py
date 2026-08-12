import streamlit as st
import os
import shutil
from pathlib import Path

from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from utils.auth import require_admin


# ==================================================
# ADMIN ONLY
# ==================================================

require_admin()


# ==================================================
# PATHS
# ==================================================

UPLOAD_DIR = Path("rag_documents")
VECTOR_DIR = Path("vector_store")

UPLOAD_DIR.mkdir(
    exist_ok=True
)

VECTOR_DIR.mkdir(
    exist_ok=True
)


# ==================================================
# PAGE HEADER
# ==================================================

st.title("🗂️ Knowledge Base")

st.write(
    "Upload reference documents used by the AI Navigator's "
    "Retrieval-Augmented Generation (RAG) pipeline."
)

st.info(
    "This page is available to Admin users only."
)

st.divider()


# ==================================================
# SUPPORTED FILE TYPES
# ==================================================

st.subheader("📄 Upload documents")

st.write(
    "Supported formats: PDF and TXT."
)

uploaded_files = st.file_uploader(
    "Choose reference documents",
    type=[
        "pdf",
        "txt"
    ],
    accept_multiple_files=True
)


# ==================================================
# TEXT EXTRACTION
# ==================================================

def extract_text_from_pdf(
    file_path
):

    reader = PdfReader(
        str(file_path)
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = (
            page.extract_text()
            or ""
        )

        if text.strip():

            pages.append(
                {
                    "page": page_number,
                    "text": text
                }
            )

    return pages


def extract_text_from_txt(
    file_path
):

    text = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    return [
        {
            "page": None,
            "text": text
        }
    ]


# ==================================================
# LOAD DOCUMENTS
# ==================================================

def load_documents_from_folder():

    documents = []

    for file_path in sorted(
        UPLOAD_DIR.iterdir()
    ):

        if not file_path.is_file():
            continue

        suffix = (
            file_path.suffix
            .lower()
        )

        if suffix == ".pdf":

            extracted_pages = (
                extract_text_from_pdf(
                    file_path
                )
            )

        elif suffix == ".txt":

            extracted_pages = (
                extract_text_from_txt(
                    file_path
                )
            )

        else:

            continue


        for item in extracted_pages:

            documents.append(
                Document(
                    page_content=(
                        item[
                            "text"
                        ]
                    ),
                    metadata={
                        "source": (
                            file_path.name
                        ),
                        "page": (
                            item[
                                "page"
                            ]
                        )
                    }
                )
            )

    return documents


# ==================================================
# BUILD VECTOR STORE
# ==================================================

def build_vector_store():

    documents = (
        load_documents_from_folder()
    )

    if not documents:

        raise ValueError(
            "No readable PDF or TXT documents were found."
        )


    # ----------------------------------------------
    # Text chunking
    # ----------------------------------------------

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=150
        )
    )

    chunks = (
        splitter.split_documents(
            documents
        )
    )


    # ----------------------------------------------
    # Embeddings
    # ----------------------------------------------

    embeddings = (
        OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=st.secrets[
                "OPENAI_API_KEY"
            ]
        )
    )


    # ----------------------------------------------
    # FAISS vector store
    # ----------------------------------------------

    vector_store = (
        FAISS.from_documents(
            chunks,
            embeddings
        )
    )


    vector_store.save_local(
        str(
            VECTOR_DIR
        )
    )


    return (
        len(documents),
        len(chunks)
    )


# ==================================================
# SAVE UPLOADS
# ==================================================

if uploaded_files:

    if st.button(
        "Save uploaded documents",
        type="primary",
        use_container_width=True
    ):

        saved_count = 0

        for uploaded_file in (
            uploaded_files
        ):

            file_path = (
                UPLOAD_DIR
                / uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as output_file:

                output_file.write(
                    uploaded_file.getbuffer()
                )

            saved_count += 1


        st.success(
            f"{saved_count} document"
            f"{'s' if saved_count != 1 else ''} saved."
        )

        st.rerun()


st.divider()


# ==================================================
# CURRENT DOCUMENTS
# ==================================================

st.subheader(
    "📚 Current knowledge-base documents"
)

current_files = [
    file_path.name
    for file_path in sorted(
        UPLOAD_DIR.iterdir()
    )
    if file_path.is_file()
]


if current_files:

    for filename in current_files:

        st.write(
            f"• {filename}"
        )

else:

    st.warning(
        "No documents have been uploaded yet."
    )


st.divider()


# ==================================================
# BUILD / REBUILD INDEX
# ==================================================

st.subheader(
    "🧠 Build RAG index"
)

st.write(
    """
When the index is built, documents are:

1. read from the knowledge-base folder;
2. converted to text;
3. split into overlapping chunks;
4. converted into embeddings; and
5. stored in a FAISS vector index.
"""
)


if st.button(
    "Build / rebuild FAISS index",
    type="primary",
    use_container_width=True,
    disabled=not bool(
        current_files
    )
):

    with st.spinner(
        "Building vector store..."
    ):

        try:

            document_count, chunk_count = (
                build_vector_store()
            )

            st.success(
                f"FAISS index built successfully from "
                f"{document_count} document section"
                f"{'s' if document_count != 1 else ''} "
                f"and {chunk_count} text chunks."
            )

        except Exception as error:

            st.error(
                f"Could not build the vector store: {error}"
            )


# ==================================================
# VECTOR STORE STATUS
# ==================================================

st.divider()

st.subheader(
    "📦 Vector store status"
)

index_file = (
    VECTOR_DIR
    / "index.faiss"
)

pickle_file = (
    VECTOR_DIR
    / "index.pkl"
)


if (
    index_file.exists()
    and pickle_file.exists()
):

    st.success(
        "FAISS vector store is available."
    )

else:

    st.warning(
        "FAISS vector store has not been built yet."
    )


# ==================================================
# REMOVE ALL DOCUMENTS
# ==================================================

st.divider()

st.subheader(
    "🗑️ Reset knowledge base"
)

st.warning(
    "This removes uploaded documents and the current FAISS index."
)


if st.button(
    "Delete all knowledge-base data"
):

    if UPLOAD_DIR.exists():

        shutil.rmtree(
            UPLOAD_DIR
        )

    if VECTOR_DIR.exists():

        shutil.rmtree(
            VECTOR_DIR
        )

    UPLOAD_DIR.mkdir(
        exist_ok=True
    )

    VECTOR_DIR.mkdir(
        exist_ok=True
    )

    st.success(
        "Knowledge base cleared."
    )

    st.rerun()


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Admin Knowledge Base · PDF/TXT → chunks → embeddings → FAISS"
)
