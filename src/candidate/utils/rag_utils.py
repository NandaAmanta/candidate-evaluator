
from chromadb.api.models.Collection import Collection

def retrieve_context(collection : Collection , query: str, n: int = 3) -> str:
        try:
            results = collection.query(query_texts=[query], n_results=n)
            # results["documents"] shape: [[doc1, doc2,...]]
            docs = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            # join with small separators
            combined = []
            for i, d in enumerate(docs):
                header = ""
                md = metadatas[i] if i < len(metadatas) else {}
                if md.get("type"):
                    header = f"[{md.get('type')}]"
                combined.append(f"{header}\n{d}")
            return "\n\n---\n\n".join(combined).strip()
        except Exception:
            return ""