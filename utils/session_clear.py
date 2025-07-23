import streamlit as st

CTF_TEMP_KEYS = [
    "edit_mode",
    "is_processing",
    "is_processing_db",
    "submitted_ctf04",
    "submitted_ctf05",
    "submitted_ctf06",
    "submitted_ctf07",
    "submitted_ctf08",
    "submitted_ctf09",
    "submitted_ctf10",
    "ctf04_override",
    "ctf05_admin_cookie",
    "ctf05_stolen_cookie",
    "ctf05_attempt_count",
    "ctf05_memos",
    "ctf06_flag",
    "is_top_admin",
    "counter",
    "ctf07_admin"
]

def clear_temp_ctf_keys(except_keys: list = []):
    for k in CTF_TEMP_KEYS:
        if k not in except_keys and k in st.session_state:
            del st.session_state[k]