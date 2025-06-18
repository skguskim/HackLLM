import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client
import os
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

COOKIE_NAME = "llm_user_id"

RemoveEmptyElementContainer()

def get_client():
    sb = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=SUPABASE_URL,
        key=SUPABASE_KEY
    )   
    return sb.client                    

def get_admin_client_direct():
    url = SUPABASE_URL
    key = SUPABASE_KEY
    return create_client(url, key)

def get_user():
    user = st.session_state.get("user")
    if user:
        return user

    cookie = CookieController()
    user_id = cookie.get(COOKIE_NAME)
    
    if user_id:
        st.session_state["user"] = {
            "id": user_id
        }
        return st.session_state["user"]
    return None

def require_login():
    user = st.session_state.get("user") 

    if not user: 
        st.error("로그인 후 이용 가능합니다.")
        st.page_link("pages/login.py", label="👉 로그인하기")
        st.stop()
    return user
