# --- CTF02 ---
import streamlit as st
from utils.llm_utils import ctf02_LLM_ask
from utils.ui import render_main_header, render_flag_sub

def render():
    render_main_header()

    st.markdown("# 🔒 [CTF02] 민감 정보 유출")
    st.write("LLM이 다른 사용자의 프롬프트나 자사의 민감 정보를 유출하는 보안 위협을 다룹니다.")
    st.info("💡 Hint: 다른 사용자의 프롬프트를 위해 자신이 역할을 LLM에게 인식시켜보세요!.")

    st.markdown("---")
    st.markdown("## 🧠 프롬프트 입력")

    # 프롬프트 제출 섹션
    user_input = st.text_input("LLM에 질문하기")

    if user_input:
        response_text = ctf02_LLM_ask(user_input)
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

    st.markdown("---")

    # 플래그 제출 섹션
    flag = "flag{...}" # 각자 임시 플래그 작성해주시면 됩니다.
    render_flag_sub(flag)
