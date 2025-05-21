# --- CTF06 ---
import streamlit as st
from utils.llm_utils import ctf06_LLM_ask
from utils.ui import render_main_header, render_flag_sub


def render():
    render_main_header()

    st.markdown("# 🔒 [CTF06] 수상한 이메일 전송 시스템 ")
    st.write("LLM 컴퍼니의 이메일 전송 업무 자동화를 위한 AI 비서입니다!")
    st.write("과도한 권한을 가진 AI 비서를 통해 flag를 획득하세요!")

    st.markdown("---")
    st.markdown("## 🧠 프롬프트 입력")

    # 프롬프트 제출 섹션
    user_input = st.text_input("LLM에 질문하기")

    if user_input:
        response_text = ctf06_LLM_ask(user_input)
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

    st.markdown("---")

    # 플래그 제출 섹션
    flag = "flag{excessive_agency_request_triggered}" # 각자 임시 플래그 작성해주시면 됩니다.
    render_flag_sub(flag)