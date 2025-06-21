# --- CTF06 ---
# 06: 과도한 위임
import streamlit as st
from utils.llm_utils import ctf06_check_admin, ctf06_LLM_ask_json, ctf06_send_emil
from utils.ui import render_main_header, render_flag_sub
from utils.auth import require_login, get_client
from utils.api_key import require_api_key
import json
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key() 

sb_client = get_client()
res = sb_client.table("profiles").select("username").eq("id", user.id).single().execute()
nickname = res.data["username"]
user_email_for_resend = f'{nickname}@ctf06.store'

# 권한 검증을 위해 사용할 키 생성
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

render_main_header()

st.header("🔒 [CTF06] 수상한 이메일 전송 시스템")
st.write("""
        LLM 컴퍼니는 사내 업무를 자동화를 위한 AI 비서를 도입했습니다!  
        AI 비서는 이메일 전송 요청을 스스로 해석하여 해당 작업을 수행할 수 있습니다.

        AI 비서가 어떤 요청까지 처리할 수 있는지 테스트해보고, 위험한 명령을 통해 flag를 획득하세요!   
""")

if st.button("힌트 보기", key="hint"):
    st.write("AI 비서는 관리자 계정의 이메일 주소를 알고 있습니다!")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션
user_input = st.text_input("LLM에 질문하기")

if user_input:
    ctf06_check_admin(user_input, user_api_key) #입력에 따라서 세션 상태 변경
    st.write(st.session_state["is_admin"])
    
    response1 = ctf06_LLM_ask_json(user_input, user, user_email_for_resend, user_api_key) # 응답으로 json 또는 일반 응답
    response2 = ctf06_send_emil(response1, user, user_email_for_resend) # 이메일 전송 담당
    st.write("🗣️ LLM 응답:")
    st.code(response2)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf06") 