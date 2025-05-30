# --- CTF06 ---
# 06: 과도한 위임
import streamlit as st
from utils.llm_utils import ctf06_LLM_ask
from utils.ui import render_main_header, render_flag_sub
from utils.auth import require_login
from utils.api_key import require_api_key

user = require_login()
user_api_key = require_api_key()

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
    response_text = ctf06_LLM_ask(user_input, user)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf06") 