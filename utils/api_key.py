import os
from dotenv import load_dotenv
import streamlit as st
from utils.auth import get_client, require_login
from cryptography.fernet import Fernet

load_dotenv()

fernet_key = os.getenv("FERNET_KEY") #암호화에 사용할 대칭키

cipher = Fernet(fernet_key.encode())

user = require_login() #로그인 된 유저 정보 가져옴 -> res.user
supabase = get_client() #슈퍼베이스 연결객체

def require_api_key():
    if not st.session_state["api_key"]:
        st.switch_page("pages/mypage.py")
    else:
        #api키 정보가 존재하므로 DB에서 빼와서 복호화
        res = supabase.table("profiles").select("api_key").eq("id", user.id).single().execute()
        encrypted_api_key = res.data["api_key"]
        decrypted_api_key = cipher.decrypt(encrypted_api_key.encode()).decode()
    return decrypted_api_key #이제 llm한테 전달할 때 require_api_key()로 전달해야함

#여기가 mypage라고 가정하고

if st.session_state["api_key"]:
    st.text_input("-API key-", value="[API key 제출 완료]", disabled=True)
else:
    api_key = st.text_input("-API key-", value="openAI API key를 입력하세요")
    #여기에서 인풋 암호화
    encrypted_api_key = cipher.encrypt(api_key.encode())
    res = supabase.table("profiles").update({
        "api_key": encrypted_api_key
        }).eq("UID", user.id).execute()
    if res.data:
        st.success("✅ API 키가 성공적으로 저장되었습니다.")
    else:
        st.error("❌ API 키 저장에 실패했습니다. 다시 시도해주세요.")
#마이페이지에서는 DB에 저장만 









 

# #api 키 없을 경우 요구하는 함수
# def require_api_key():
#     api_key = st.text_input("openAI API key", type="password")
#     #암호화해서 최초로 db에 저장하는 함수
    # encrypted_api_key = cipher.encrypt(api_key.encode())
    # response = supabase.table("profiles").update({
    #     "api_key": encrypted_api_key
    #     }).eq("UID", user.id).execute() #response.date = T/F 반환
    
    


# #api키 정보 존재하는지 검사하는 함수
# def check_api_key():
#     if not user.api_key:
#         #api_key 정보가 존재하지 않을 때
#         require_api_key() 
#         #이후 세션에 저장



# row = (
#             supabase
#             .table("flags")
#             .select("points, challenge_id")
#             .eq("flag_hash", hashed)
#             .single()
#             .execute()
#             .data
#         )