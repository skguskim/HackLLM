import os
from dotenv import load_dotenv
import streamlit as st
from utils.auth import get_client, require_login
from cryptography.fernet import Fernet

load_dotenv()

fernet_key = os.getenv("FERNET_KEY") # 암호화에 사용할 대칭키

cipher = Fernet(fernet_key.encode()) 

# 10분 정도 캐시 유지, uid마다 분리됨
@st.cache_data(ttl=600)  
def get_decrypted_api_key(uid: str) -> str | None:
    sb = get_client()
    try:
        res = sb.table("profiles").select("api_key").eq("id", uid).single().execute()
        encrypted_api_key = res.data.get("api_key")
        if not encrypted_api_key:
            return None
        return cipher.decrypt(encrypted_api_key.encode()).decode()
    except:
        return None
    
def require_api_key():
    # 먼저 사용자 로그인 확인
    user = require_login() 
    user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
    
    if "api_key" not in st.session_state:
        decrypted_api_key = get_decrypted_api_key(user_id)

        if not decrypted_api_key:
            st.error("API 키를 제출한 뒤 이용해주세요.")
            st.page_link("pages/mypage.py", label="👉 API키 제출하러 가기")
            st.stop()

        st.session_state["api_key"] = decrypted_api_key

    return st.session_state["api_key"]