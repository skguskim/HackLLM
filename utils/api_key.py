import os
from dotenv import load_dotenv
import streamlit as st
from utils.auth import get_client, require_login
from cryptography.fernet import Fernet

load_dotenv()

fernet_key = os.getenv("FERNET_KEY") # 암호화에 사용할 대칭키

cipher = Fernet(fernet_key.encode()) 

# 이부분 코드 리팩토링 필요
user = require_login() 
supabase = get_client() 

def require_api_key():
    user = require_login() # st 세션상태 user만 가져옴 

    if not st.session_state.get("api_key"):
        st.error("API 키를 제출한 뒤 이용해주세요.")
        st.page_link("pages/mypage.py", label="👉 API키 제출하러 가기")
        st.stop()
    else:
        res = supabase.table("profiles").select("api_key").eq("id", user["id"]).single().execute()
        encrypted_api_key = res.data["api_key"]
        decrypted_api_key = cipher.decrypt(encrypted_api_key.encode()).decode()
    return decrypted_api_key #ctf01~10에서 require_api_key()로 받은 값을 LLM 호출 함수로 전달