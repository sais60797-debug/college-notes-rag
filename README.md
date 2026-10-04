# College Notes RAG Assistant

A Windows-friendly College Notes RAG chatbot built with Streamlit, ChromaDB,
Sentence Transformers, PyPDF, and Groq Llama 3.3 70B.

## Run

1. Install Python 3.10+ if it is not already installed.
2. Put PDF notes inside `data/`.
3. Double-click `START.bat`.
4. On the first run, paste your Groq API key when asked.
5. The browser opens the application.
6. Click **Rebuild Knowledge Base** after adding or changing PDFs.

The application stores the API key in `.env`. Never upload `.env` to GitHub.

## Architecture

PDF -> text extraction -> chunking -> Sentence Transformer embeddings -> ChromaDB
-> similarity retrieval -> Groq Llama 3.3 70B -> answer + source pages

## Notes

This package is a clean, simplified Windows-ready implementation inspired by the
referenced College_RAG_Chatbot repository. It is intentionally easier to run and
understand than the original multi-component version.
