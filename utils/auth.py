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

def get_cookie_controller():
    if "cookie_controller" not in st.session_state:
        st.session_state["cookie_controller"] = CookieController()
    return st.session_state["cookie_controller"]

def get_client():
    sb = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=SUPABASE_URL,
        key=SUPABASE_KEY,
        ttl=0
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

    cookie = get_cookie_controller()
    uid = cookie.get(COOKIE_NAME)
    
    if uid:
        st.session_state["user"] = {
            "id": uid
        }
        return st.session_state["user"]

    return None

def require_login():
    user = st.session_state.get("user") 

    if not user: 
        st.error("로그인 후 이용 가능합니다.")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.page_link("pages/login.py", label="👉 로그인하기")
        with col2:
            st.page_link("app.py", label="🏠 메인 페이지", use_container_width=True)
        st.stop()
    return user
