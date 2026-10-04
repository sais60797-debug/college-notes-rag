import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="College Notes | Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --ink: #17243b;
            --muted: #718096;
            --blue: #4169e1;
            --line: #e8edf5;
            --paper: #ffffff;
        }
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background: #f5f7fb;
            color: var(--ink);
        }
        [data-testid="stHeader"] {
            background: rgba(245, 247, 251, 0.88);
        }
        [data-testid="stSidebar"] {
            background: #fff;
            border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.25rem;
        }
        .block-container {
            max-width: 1220px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3, h4 {
            color: var(--ink);
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: -0.035em;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.25rem 0 1.5rem;
        }
        .brand-mark {
            display: grid;
            width: 42px;
            height: 42px;
            place-items: center;
            border-radius: 14px;
            background: #eaf0ff;
            font-size: 1.35rem;
        }
        .brand-name {
            color: var(--ink);
            font: 800 1rem 'Segoe UI', sans-serif;
            letter-spacing: -0.04em;
        }
        .brand-caption {
            color: var(--muted);
            font-size: 0.72rem;
            margin-top: 0.1rem;
        }
        .section-label {
            color: #8a96a9;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin: 1.2rem 0 0.65rem;
            text-transform: uppercase;
        }
        .hero {
            position: relative;
            overflow: hidden;
            padding: 2rem 2.1rem;
            border-radius: 24px;
            background: linear-gradient(115deg, #17243b 0%, #243f77 60%, #4169e1 100%);
            box-shadow: 0 16px 36px rgba(30, 55, 105, 0.16);
            color: #fff;
        }
        .hero:after {
            position: absolute;
            top: -100px;
            right: -45px;
            width: 310px;
            height: 310px;
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 50%;
            box-shadow: 0 0 0 35px rgba(255,255,255,0.035), 0 0 0 75px rgba(255,255,255,0.025);
            content: "";
        }
        .hero-kicker {
            color: #b8c9ff;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        .hero h1 {
            position: relative;
            z-index: 1;
            margin: 0.55rem 0 0.5rem;
            color: #fff !important;
            font-size: clamp(1.8rem, 3vw, 2.5rem);
            line-height: 1.15;
        }
        .hero p {
            position: relative;
            z-index: 1;
            max-width: 620px;
            margin: 0;
            color: #d9e2fb;
            font-size: 0.98rem;
            line-height: 1.65;
        }
        .metric-card {
            min-height: 108px;
            padding: 1rem 1.1rem;
            border: 1px solid var(--line);
            border-radius: 17px;
            background: var(--paper);
            box-shadow: 0 4px 14px rgba(25, 45, 80, 0.035);
        }
        .metric-label {
            color: var(--muted);
            font-size: 0.79rem;
            font-weight: 600;
        }
        .metric-value {
            margin-top: 0.35rem;
            color: var(--ink);
            font: 800 1.55rem 'Segoe UI', sans-serif;
            letter-spacing: -0.05em;
        }
        .metric-foot {
            color: #8c98aa;
            font-size: 0.72rem;
            margin-top: 0.15rem;
        }
        .content-card {
            padding: 1.45rem 1.55rem;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: var(--paper);
            box-shadow: 0 5px 18px rgba(25, 45, 80, 0.035);
        }
        .empty-icon {
            display: grid;
            width: 54px;
            height: 54px;
            place-items: center;
            border-radius: 17px;
            background: #edf2ff;
            font-size: 1.55rem;
        }
        .empty-title {
            margin: 0.9rem 0 0.35rem;
            color: var(--ink);
            font: 800 1.2rem 'Segoe UI', sans-serif;
        }
        .empty-copy {
            max-width: 660px;
            color: var(--muted);
            line-height: 1.65;
        }
        .status-pill {
            display: inline-block;
            padding: 0.32rem 0.65rem;
            border: 1px solid #ccebd9;
            border-radius: 999px;
            background: #effaf4;
            color: #23834f;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .status-pill.pending {
            border-color: #f0dfb4;
            background: #fff9e9;
            color: #9b6b09;
        }
        .stButton > button {
            min-height: 2.65rem;
            border-radius: 11px;
            font-weight: 650;
            transition: all 150ms ease;
        }
        .stButton > button[kind="primary"] {
            border: 0;
            background: var(--blue);
            box-shadow: 0 5px 12px rgba(65, 105, 225, 0.18);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: #b6c7fb;
        }
        [data-testid="stFileUploader"] {
            padding: 0.45rem;
            border: 1px dashed #cbd5e5;
            border-radius: 14px;
            background: #fafbfe;
        }
        [data-testid="stChatMessage"] {
            border: 1px solid var(--line);
            border-radius: 16px;
            background: #fff;
            box-shadow: 0 3px 12px rgba(25, 45, 80, 0.035);
        }
        [data-testid="stChatInput"] {
            border-color: #dce3ef;
            border-radius: 15px;
        }
        [data-testid="stExpander"] {
            border-color: var(--line);
            border-radius: 13px;
            background: #fff;
        }
        .sidebar-note {
            color: var(--muted);
            font-size: 0.76rem;
            line-height: 1.55;
        }
        @media (max-width: 700px) {
            .block-container { padding: 1rem 1rem 2rem; }
            .hero { padding: 1.5rem; }
            .content-card { padding: 1.15rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

import hmac

# Optional password gate: set APP_PASSWORD in .env or Streamlit secrets to enable it.
_app_password = os.getenv("APP_PASSWORD")
if _app_password and not st.session_state.get("authed"):
    st.title("College Notes Study Assistant")
    _pw = st.text_input("Password", type="password")
    if _pw:
        if hmac.compare_digest(_pw, _app_password):
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

from rag_engine import GroqRequestError, RAGEngine


@st.cache_resource
def get_engine():
    return RAGEngine()


engine = get_engine()


@st.cache_resource(show_spinner="Indexing the notes in the data folder (first start only)...")
def auto_build(_engine):
    # Cloud disks are wiped on restart, so rebuild the index from the PDFs in data/.
    if not _engine.has_documents() and _engine.list_pdfs():
        _engine.ingest_documents()
    return True


auto_build(engine)
stats = engine.get_stats()
has_documents = engine.has_documents()
has_api_key = bool(os.getenv("GROQ_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []
if "notes_summary" not in st.session_state:
    st.session_state.notes_summary = ""


def handle_question(question: str):
    if not question or not question.strip():
        return

    clean_question = question.strip()
    st.session_state.messages.append({"role": "user", "content": clean_question})
    with st.chat_message("user"):
        st.markdown(clean_question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your notes..."):
            try:
                answer, sources = engine.answer(clean_question)
            except GroqRequestError as exc:
                answer, sources = str(exc), []
                st.error(answer)
            else:
                st.markdown(answer)
                if sources:
                    st.caption("Sources: " + " · ".join(sources))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">🎓</div>
            <div>
                <div class="brand-name">Study Companion</div>
                <div class="brand-caption">Your notes, made searchable</div>
            </div>
        </div>
        <div class="section-label">Workspace</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">Knowledge base</div>',
        unsafe_allow_html=True,
    )
    metric_left, metric_right = st.columns(2)
    with metric_left:
        st.metric("PDFs", stats["pdf_count"])
    with metric_right:
        st.metric("Chunks", stats["chunk_count"])

    uploaded_file = st.file_uploader(
        "Add study material",
        type=["pdf"],
        help="Upload a PDF to add it to your local notes library.",
    )
    if uploaded_file:
        target = DATA_DIR / Path(uploaded_file.name).name
        file_id = f"{uploaded_file.name}-{uploaded_file.size}"
        if st.session_state.get("last_upload") != file_id:
            target.write_bytes(uploaded_file.getvalue())
            st.session_state["last_upload"] = file_id
            st.rerun()
        st.success(f"Added {target.name} - now click Build knowledge base")

    if st.button(
        "Build knowledge base",
        type="primary",
        use_container_width=True,
        help="Read the PDFs in your data folder and prepare them for search.",
    ):
        with st.spinner("Reading and indexing your PDFs (first run downloads the embedding model)..."):
            count = engine.ingest_documents()
        if count:
            st.session_state["build_msg"] = f"Indexed {count} text chunks."
            st.rerun()
        else:
            st.warning("No readable PDF text was found in the data folder.")
    if st.session_state.get("build_msg"):
        st.success(st.session_state.pop("build_msg"))

    if engine.list_pdfs():
        with st.expander("Files in your library", expanded=False):
            for pdf_name in engine.list_pdfs():
                st.caption(f"📄 {pdf_name}")
    else:
        st.caption("Your uploaded PDFs will appear here.")

    st.markdown('<div class="section-label">Study tools</div>', unsafe_allow_html=True)
    if st.button(
        "Generate study summary",
        use_container_width=True,
        disabled=not has_documents or not has_api_key,
        help="Requires indexed PDFs and a Groq API key.",
    ):
        with st.spinner("Creating a focused summary..."):
            try:
                st.session_state["notes_summary"] = engine.summarize_notes()
            except GroqRequestError as exc:
                st.error(str(exc))
            else:
                st.rerun()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="section-label">About</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-note">Answers are grounded in your indexed PDFs. '
        'AI responses use Groq; document storage stays on this machine.</p>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Your personal study workspace</div>
        <h1>Make your notes work harder.</h1>
        <p>Find clear answers in your course material, understand tricky concepts, and keep every response connected to its source.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

metric_columns = st.columns(3)
metrics = [
    ("Study documents", stats["pdf_count"], "PDFs in your library"),
    ("Knowledge indexed", stats["chunk_count"], "searchable note passages"),
    (
        "Assistant",
        "Key saved" if has_api_key else "Setup",
        "API key is checked when used" if has_api_key else "Groq connection",
    ),
]
for column, (label, value, footnote) in zip(metric_columns, metrics):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-foot">{footnote}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
if not has_documents:
    st.markdown(
        """
        <div class="content-card">
            <div class="empty-icon">📚</div>
            <div class="empty-title">Start with your course notes</div>
            <div class="empty-copy">Upload one or more PDFs using the panel on the left, then select <b>Build knowledge base</b>. Your files will be prepared for searching locally. You can set up the AI key later.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    if not has_api_key:
        st.info(
            "Your notes are indexed and ready. Add a Groq API key in the sidebar "
            "to enable AI chat and study summaries."
        )
    else:
        st.markdown(
            '<span class="status-pill">● API key saved · not yet verified</span>',
            unsafe_allow_html=True,
        )

    if st.session_state.notes_summary:
        with st.expander("Your study summary", expanded=False):
            st.markdown(st.session_state.notes_summary)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                st.caption("Sources: " + " · ".join(message["sources"]))

    if not st.session_state.messages and has_api_key:
        st.markdown(
            """
            <div class="content-card">
                <div class="empty-title" style="margin-top:0;">What would you like to learn?</div>
                <div class="empty-copy">Ask a question about your indexed notes. Answers include references to the PDF pages they came from.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        prompt_columns = st.columns(3)
        suggestions = [
            "Summarize the key concepts",
            "Explain the main differences",
            "What should I remember for an exam?",
        ]
        for column, suggestion in zip(prompt_columns, suggestions):
            with column:
                if st.button(suggestion, use_container_width=True):
                    st.session_state["quick_question"] = suggestion
                    st.rerun()

    if has_documents and has_api_key:
        st.markdown('<div class="section-label">Ask about your PDF</div>', unsafe_allow_html=True)
        with st.form("pdf_question_form", clear_on_submit=True):
            question = st.text_area(
                "Question",
                placeholder="Ask a question about the uploaded PDF, e.g. 'What are the key concepts in chapter 3?'",
                height=120,
                disabled=not has_api_key,
            )
            submitted = st.form_submit_button("Ask question", use_container_width=True)
            if submitted and question:
                handle_question(question)

    if "quick_question" in st.session_state:
        quick_question = st.session_state.pop("quick_question")
        handle_question(quick_question)
    else:
        question = st.chat_input(
            "Ask a question about your notes...",
            disabled=not has_api_key,
        )
        if question:
            handle_question(question)
