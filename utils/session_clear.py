import streamlit as st
CTF_TEMP_KEYS = [
    "payment_message",
    "order_info_message",
    "show_game",
    "show_main",
    "is_processing_payment",
    "submitted_ctf01_payment",
    "submitted_ctf01_main",
    "messages",
    "is_processing",
    "submitted_ctf02",
    "last_processed_input",
    "ctf02_input",
    "edit_mode",
    "submitted_ctf03",
    "ctf03_last_response",
    "ctf03_input",
    "ctf04_override",
    "submitted_ctf04",
    "ctf04_input",
    "admin_level",
    "is_top_admin",
    "submitted_ctf06",
    "ctf06_text_input",
    "is_processing_db",
    "submitted_ctf06_db",
    "counter",
    "ctf07_admin",
    "submitted_ctf07",
    "ctf07_input",
    "submitted_ctf08",
    "submitted_ctf09",
    "ctf09_input",
    "submitted_ctf10",
    "ctf10_input"
]
def clear_temp_ctf_keys(except_keys: list = []):
    for k in CTF_TEMP_KEYS:
        if k not in except_keys and k in st.session_state:
            del st.session_state[k]