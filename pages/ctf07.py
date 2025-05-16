# --- CTF07 ---
# 07: 시스템 프롬프트 유출
import streamlit as st
from utils.llm_utils import ctf07_LLM_ask
from utils.ui import render_main_header

def render():
    render_main_header()

    st.markdown("# 🔒 [CTF07] K대리의 비밀")
    st.write("오직 K대리만을 위한 LLM입니다. 해당 모델을 우회하여 Flag를 탈취해 보세요.")

    st.markdown("---")
    st.markdown("## 🧠 프롬프트 입력")

    # 프롬프트 제출 섹션
    user_input = st.text_input("K대리의 LLM에 질문하기")

    if user_input:
        response_text = ctf07_LLM_ask(user_input)
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

    st.markdown("---")

    # 플래그 제출 섹션
    st.markdown("## 🚩 FLAG 제출")
    submitted_flag = st.text_input("획득한 flag를 제출하세요", key="flag_input")

    if submitted_flag:
        if submitted_flag.strip() == "flag{test1234test}":
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸습니다.")