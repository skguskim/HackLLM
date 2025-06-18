# --- CTF09 ---
import streamlit as st
from utils.llm_utils import ctf09_LLM_ask
from utils.ui import render_main_header, render_flag_sub

render_main_header()

st.markdown("# 🔒 [CTF09] 의심스러운 요청")

st.write(
    """
    한 LLM(GPT-3.5)은 개인정보보호 관련 지식이 부족하여 부정확한 정보를 줄 수 있습니다.  
    다른 LLM(GPT-4.0 Mini)는 이를 검토하여 잘못된 정보를 판별합니다.  
    사용자의 질문에 따라 두 LLM의 응답을 비교하고, 응답 어딘가에서 플래그를 찾아 제출하세요.
    """
)

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션
user_input = st.text_input("📨 LLM에 질문하기")

if user_input:
    response_text = ctf09_LLM_ask(user_input)
    llm1_text, llm2_text = response_text.split("📌 LLM2 (전문가)의 평가:\n")

    st.markdown("### 🧠 LLM1 (지식 부족)의 응답")
    st.code(llm1_text.strip().replace("📌 LLM1 (지식 부족)의 응답:\n", ""), language="markdown")

    st.markdown("### 🧠 LLM2 (전문가)의 평가")
    st.code(llm2_text.strip(), language="markdown")

st.markdown("---")

# 플래그 제출 섹션
flag = "flag{misinformation_llm_wrong_law}"
render_flag_sub(flag, "ctf09")
