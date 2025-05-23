# --- CTF05 ---
import streamlit as st
from utils.llm_utils import ctf05_LLM_ask
from utils.ui import render_main_header, render_flag_sub
from utils.auth import get_user

user = get_user()

if not user:
    st.error("로그인 후 이용 가능합니다.")
    st.page_link("pages/login.py", label="👉 로그인하기")
    st.stop()
    
render_main_header()

st.header("🔒 [CTF05] AI의 폭주")
st.write("부적절한 출력을 활용해 AI의 정보를 얻어주세요")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션
user_input = st.text_input("LLM에 질문하기")

if user_input:
    response_text = ctf05_LLM_ask(user_input)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf05") 
