# utils/rag_utils.py
from utils.rag_utils_supabase import SupabaseRAG
_rag = None

def get_rag_manager() -> SupabaseRAG:
    global _rag
    if _rag is None:
        _rag = SupabaseRAG(table="rag_docs_ctf04") 
    return _rag