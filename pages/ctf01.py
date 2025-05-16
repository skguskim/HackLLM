# --- CTF01 ---
import streamlit as st
from utils.llm_utils import ctf01_LLM_ask
from utils.ui import render_main_header

def render():
    st.markdown("# 🤖 [CTF01] D차장의 실수")
    st.write("여기는 CTF 문제 설명 칸입니다")

    user_input = st.text_input("질문을 입력하세요")
    if user_input:
        response_text = ctf01_LLM_ask(user_input)
        st.write(response_text)