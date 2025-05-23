# --- CTF03 ---
import streamlit as st
from utils import mathlib
from utils.ui import render_main_header, render_flag_sub
from utils.llm_utils import ctf03_LLM_ask
from utils.auth import get_user

user = get_user()

if not user:
    st.error("로그인 후 이용 가능합니다.")
    st.page_link("pages/login.py", label="👉 로그인하기")
    st.stop()
    
render_main_header()

st.header("🔒 [CTF03] 회사 내 조작된 계산기")
st.write("조작된 mathlib2을 LLM 계산기에 침투시켜, 그릇된 계산 결과를 그대로 출력하게 만들어보세요.")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

user_input = st.text_input(" 덧셈 / 뺄셈 / 곱하기 / 나누기가 가능한 계산기입니다.")

if user_input:
    response_text = ctf03_LLM_ask(user_input)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf03") 