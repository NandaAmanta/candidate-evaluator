import os
import fitz  
import chromadb
from chromadb.utils import embedding_functions
import requests
from config import settings

# === Setup Chroma Client ===
CHROMA_PATH = os.getenv("CHROMA_PERSIST_PATH", "./chroma_data")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_func = embedding_functions.CohereEmbeddingFunction(
    api_key=settings.COHERE_API_KEY,
    model_name="embed-multilingual-v3.0"
)

collection = chroma_client.get_or_create_collection(
    name="reference_docs",
    embedding_function=embedding_func
)

# === Helper: Extract text from PDF ===
def extract_text_from_pdf(path: str) -> str:
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

# === List dokumen acuan ===
REFERENCE_DOCS = {
    "job_description": "docs/job_description.pdf",
    "case_study_brief": "docs/case_study_brief.pdf",
    "cv_scoring_rubric": "docs/cv_scoring_rubric.pdf",
    "project_scoring_rubric": "docs/project_scoring_rubric.pdf"
}

# === Ingest each document ===
for name, path in REFERENCE_DOCS.items():
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        continue
    print(f"📄 Ingesting {name} ...")
    text = extract_text_from_pdf(path)
    collection.add(
        documents=[text],
        ids=[name],
        metadatas=[{"type": name}]
    )
    print(f"✅ Added {name} ({len(text)} chars)")

print("\n🎉 All reference documents ingested successfully into ChromaDB.")
