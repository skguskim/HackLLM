import os
from dotenv import load_dotenv
import streamlit as st
from utils.auth import get_client, require_login
from cryptography.fernet import Fernet

load_dotenv()

fernet_key = os.getenv("FERNET_KEY") # 암호화에 사용할 대칭키

cipher = Fernet(fernet_key.encode()) # Fernet 객체가 byte 타입의 키를 요구 + .env에서 str형태로 가져오기 때문에 .encode()

user = require_login() # 로그인 된 유저 정보 가져옴 -> res.user
supabase = get_client() # 슈퍼베이스 연결객체

def require_api_key():
    user = require_login() # 슈퍼베이스에서 유저 정보 받아옴 res.user
    if not st.session_state.get("api_key"):
        st.error("API 키를 제출한 뒤 이용해주세요.")
        st.page_link("pages/mypage.py", label="👉 API키 제출하러 가기")
        st.stop()
    else:
        # api키 정보가 존재하므로 DB에서 빼와서 복호화한 뒤 반환
        res = supabase.table("profiles").select("api_key").eq("id", user.id).single().execute()
        encrypted_api_key = res.data["api_key"]
        decrypted_api_key = cipher.decrypt(encrypted_api_key.encode()).decode()
    return decrypted_api_key # 이제 llm한테 전달할 때 require_api_key()로 전달해야함
