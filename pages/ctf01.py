# --- CTF01 ---
import streamlit as st
from utils.llm_utils import ctf01_LLM_ask, ctf01_LLM_ask2
from utils.ui import render_main_header, render_flag_sub
import csv
import json

def render():
    render_main_header()

    st.markdown("# 🔒 [CTF01] 취약한 고객상담 챗봇 ")
    st.write("LLL 컴퍼니의 고객상담을 위한 AI챗봇 Ll는 언제나 정책을 준수합니다!")
    st.write("Ll의 취약점을 이용해 flag을 획득해보세요!")
    st.write()
    st.write("현재 로그인된 계정 : user1")

    st.markdown("---")
    st.markdown("## 🧠 프롬프트 입력")

    # 프롬프트 제출 섹션
    user_input = st.text_input("LLM에 질문하기")

    if user_input:
        response1_text = ctf01_LLM_ask(user_input)
        response2_text = ctf01_LLM_ask2(response1_text)

        st.write("🗣️ LLM1 응답:")
        st.code(response1_text)

        st.markdown("---")

        st.write("🗣️ LLM2 응답:")
        st.code(response2_text)

    st.markdown("---")

    # 플래그 제출 섹션
    flag = "flag{prompt_injection_detected}" 
    render_flag_sub(flag)