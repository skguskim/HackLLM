# ✅ utils/rag_utils.py
import os
import uuid
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Callable

class RAGManager:
    def __init__(self, base_path: str = "./chroma_db"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        os.makedirs(base_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=base_path)
        self.collections = {}

    def create_or_reset_collection(self, name: str) -> chromadb.api.models.Collection:
        try:
            existing = [col.name for col in self.client.list_collections()]
            if name in existing:
                self.client.delete_collection(name)
        except Exception as e:
            print(f"[RAG] 컬렉션 삭제 실패: {e}")

        collection = self.client.create_collection(name)
        self.collections[name] = collection
        return collection

    def add_documents(self, collection_name: str, documents: List[str], metadatas: List[dict] = None) -> None:
        if collection_name not in self.collections:
            raise ValueError(f"[RAG] 컬렉션 '{collection_name}'이 존재하지 않습니다.")

        collection = self.collections[collection_name]
        embeddings = [self.model.encode(doc).tolist() for doc in documents]
        ids = [f"{collection_name}_{uuid.uuid4()}" for _ in documents]
        if metadatas is None:
            metadatas = [{} for _ in documents]

        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

    def query_collection(self, name: str, query_text: str, top_k: int = 3):
        if name not in self.collections:
            raise ValueError(f"컬렉션 '{name}'이 존재하지 않습니다.")
        collection = self.collections[name]
        query_vec = self.model.encode(query_text).tolist()
        return collection.query(
            query_embeddings=[query_vec],
            n_results=top_k,
            include=["documents", "metadatas"]
        )

rag_instance = None

def get_rag_manager() -> RAGManager:
    global rag_instance
    if rag_instance is None:
        rag_instance = RAGManager(base_path="./chroma_db")
    return rag_instance
