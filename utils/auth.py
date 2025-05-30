import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_client():
    sb = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=SUPABASE_URL,
        key=SUPABASE_KEY
    )   
    return sb.client                     

def get_admin_client_direct():
    url=SUPABASE_URL
    key=SUPABASE_KEY
    return create_client(url, key)

def get_user():
    return st.session_state.get("user")

def require_login():
    user = st.session_state.get("user")

    if not user: 
        st.error("로그인 후 이용 가능합니다.")
        st.page_link("pages/login.py", label="👉 로그인하기")
        st.stop()
    return user