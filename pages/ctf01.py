# --- CTF01 ---
# 01: 시스템 프롬프트 인젝션
import streamlit as st
from utils.llm_utils import ctf01_llm_ask, ctf01_llm_flag
from utils.ui import render_main_header, render_flag_sub
from utils.auth import require_login
from utils.api_key import require_api_key 

user = require_login()
user_api_key = require_api_key()


render_main_header()

st.header("🔐 [CTF01] 취약한 고객상담 챗봇")
st.write("LLL 컴퍼니의 고객상담을 위한 AI챗봇 Ll는 언제나 정책을 준수합니다!")
st.write("Ll의 취약점을 이용해 flag을 획득해보세요!")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션``
user_input = st.text_input("LLM에 질문하기")

if user_input:
    response1_text = ctf01_llm_ask(user_input)
    response2_text = ctf01_llm_flag(user_api_key, response1_text)

    if response2_text != None:
        st.write("🗣️ LLM1 응답:")
        st.code(response1_text)

        st.markdown("---")

        st.write("🗣️ LLM2 응답:")
        st.code(response2_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf01") 
