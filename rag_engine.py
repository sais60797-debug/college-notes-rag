import os
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.utils import embedding_functions
from groq import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    Groq,
    NotFoundError,
    RateLimitError,
)
from pypdf import PdfReader

DATA_DIR = Path("data")
DB_DIR = Path("vector_db")
COLLECTION_NAME = "college_notes"
MODEL = "openai/gpt-oss-120b"


class GroqRequestError(Exception):
    """A safe, user-facing error from a Groq API request."""


class RAGEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(DB_DIR))
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn,
        )
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq = Groq(api_key=groq_api_key) if groq_api_key else None

    def has_documents(self):
        return self.collection.count() > 0

    def list_pdfs(self) -> List[str]:
        DATA_DIR.mkdir(exist_ok=True)
        return sorted(pdf.name for pdf in DATA_DIR.glob("*.pdf"))

    def get_stats(self):
        pdf_count = len(self.list_pdfs())
        chunk_count = self.collection.count()
        return {
            "pdf_count": pdf_count,
            "chunk_count": chunk_count,
            "indexed": chunk_count > 0,
        }

    def _create_completion(self, **kwargs):
        if not self.groq:
            raise GroqRequestError(
                "Configure a Groq API key in the sidebar to use AI features."
            )

        try:
            return self.groq.chat.completions.create(**kwargs)
        except AuthenticationError as exc:
            raise GroqRequestError(
                "Groq rejected the saved API key. Replace it in the sidebar under "
                "\"Configure Groq API key\" with a valid key from console.groq.com."
            ) from exc
        except RateLimitError as exc:
            raise GroqRequestError(
                "Groq's request limit or available quota has been reached. "
                "Check your Groq account and try again later."
            ) from exc
        except NotFoundError as exc:
            raise GroqRequestError(
                "Groq could not find the configured model. The model may have been "
                "retired; update the model ID in rag_engine.py and try again."
            ) from exc
        except APIConnectionError as exc:
            raise GroqRequestError(
                "Could not connect to Groq. Check your internet connection and try again."
            ) from exc
        except APIStatusError as exc:
            raise GroqRequestError(
                f"Groq could not complete the request (HTTP {exc.status_code}). "
                "Please try again later."
            ) from exc

    def _extract(self, pdf_path: Path):
        reader = PdfReader(str(pdf_path))
        pages = []
        for page_no, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append((page_no, text))
        return pages

    def _chunks(self, text, size=1200, overlap=200):
        text = " ".join(text.split())
        if not text:
            return []
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            chunk = text[start:end]
            if len(chunk.strip()) > 40:
                chunks.append(chunk.strip())
            if end == len(text):
                break
            start = end - overlap
        return chunks

    def ingest_documents(self):
        DATA_DIR.mkdir(exist_ok=True)
        pdfs = sorted(DATA_DIR.glob("*.pdf"))
        if not pdfs:
            return 0

        try:
            self.client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn,
        )

        ids, docs, metas = [], [], []
        n = 0
        for pdf in pdfs:
            for page_no, text in self._extract(pdf):
                for idx, chunk in enumerate(self._chunks(text)):
                    ids.append(f"{pdf.name}-{page_no}-{idx}-{n}")
                    docs.append(chunk)
                    metas.append({"source": pdf.name, "page": page_no})
                    n += 1

        if docs:
            self.collection.add(ids=ids, documents=docs, metadatas=metas)
        return len(docs)

    def summarize_notes(self) -> str:
        if not self.groq:
            return "Add your Groq API key to generate a study summary."

        if not self.has_documents():
            return "Upload and index at least one PDF before generating a summary."

        result = self.collection.get(include=["documents"], limit=20)
        documents = result.get("documents", [])
        if not documents:
            return "No indexed notes are available for a summary yet."

        context = "\n\n".join(doc for doc in documents if doc and isinstance(doc, str))
        context = context[:8000]

        response = self._create_completion(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a study assistant. Create a concise but useful summary "
                        "of the notes in bullet points. Focus on the main topics, important "
                        "concepts, and exam-ready highlights. Avoid speculation and only "
                        "use the provided notes."
                    ),
                },
                {"role": "user", "content": f"Summarize the following notes:\n\n{context}"},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    def answer(self, question: str) -> Tuple[str, List[str]]:
        if not self.groq:
            return "Please configure your Groq API key before asking questions.", []

        result = self.collection.query(query_texts=[question], n_results=5)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]

        if not documents:
            return "I couldn't find relevant information in your uploaded notes.", []

        context_parts = []
        sources = []
        for doc, meta in zip(documents, metadatas):
            source = f"{meta.get('source', 'Unknown')} — page {meta.get('page', '?')}"
            sources.append(source)
            context_parts.append(f"[Source: {source}]\n{doc}")

        context = "\n\n".join(context_parts)

        system = """You are a college study assistant using Retrieval-Augmented Generation.
Answer ONLY from the provided notes. If the notes do not contain enough information,
say that the answer is not available in the uploaded notes. Do not invent facts.
Explain clearly and in student-friendly language. You may structure answers with headings
and bullet points. Do not mention that you are an AI unless necessary."""

        response = self._create_completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"COLLEGE NOTES:\n{context}\n\nSTUDENT QUESTION:\n{question}\n\nAnswer using only the college notes above."},
            ],
            temperature=0.2,
        )
        answer = response.choices[0].message.content
        return answer, list(dict.fromkeys(sources))
