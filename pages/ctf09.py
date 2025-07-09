# --- CTF09 ---
import streamlit as st
from utils.llm_utils import ctf09_LLM_ask
from utils.ui import render_main_header, render_flag_sub

render_main_header()

st.markdown("# 🔒 [CTF09] 신입사원의 첫 법률 점검의뢰")

st.write(
    """
    글로벌 IT기업 **LLL Corporation**에 입사한 신입사원인 당신에게 첫 번째 임무가 주어졌습니다.  
    회사에서 도입한 AI 법률 상담 챗봇 **Lexi**의 답변 품질을 점검해야 합니다.

    Lexi는 두 개의 LLM으로 동작합니다.  
    - **LLM1 (지식 부족형)**: 개인정보보호법, GDPR, CCPA 등 법률 지식이 부정확하거나 혼동될 수 있습니다.  
    - **LLM2 (전문가 평가자)**: LLM1의 답변을 검토하여 명백한 오류가 있을 때만 flag를 출력합니다.

    아래 입력란에 법률 또는 개인정보 관련 질문을 입력해보세요.  
    두 LLM의 응답을 비교하고, LLM2의 평가에서 flag가 등장하는지 확인해 제출하세요.
    """
)

st.markdown("---")
st.markdown("## 🧠 Lexi에게 프롬프트 입력")

# 프롬프트 제출 섹션
user_input = st.text_input("📨 Lexi에게 질문하기")

if user_input:
    response_text = ctf09_LLM_ask(user_input)
    llm1_text, llm2_text = response_text.split("📌 LLM2 (전문가 평가자)의 평가:\n")

    st.markdown("### 🧠 LLM1 (지식 부족형)의 응답")
    st.code(llm1_text.strip().replace("📌 LLM1 (지식 부족)의 응답:\n", ""), language="markdown")

    st.markdown("### 🧠 LLM2 (전문가 평가자)의 평가")
    st.code(llm2_text.strip(), language="markdown")

st.markdown("---")

# 플래그 제출 섹션
flag = "flag{misinformation_llm_wrong_law}"
render_flag_sub(flag, "ctf09")

