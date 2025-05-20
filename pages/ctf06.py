# --- CTF06 ---
import streamlit as st
from utils.llm_utils import ctf06_LLM_ask
from utils.ui import render_main_header, render_flag_sub

# #나중에 langchain 에이전트로 LLM에게 알려줄 tool
# def send_email(user):
#     if (user == "admin"):
#         flag = "flag{excessive_agency_request_triggered}"
#         return flag
#     else pass

# tools = [
#     Tool(
#         name="send_email",
#         func=send_email, #함수 이름름
#         description="admin 계정으로 이메일 전송 시 flag를 반환하는 함수"
#     )
# ]

# agent = initialize_agent(tools, llm, agent="zero-shot-react-description") #llm 모델 정의 필요
# agent.run("사용자 입력 부분")

def render():
    render_main_header()

    st.markdown("# 🔒 [CTF06] ")
    st.write("설명")

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
    flag = "flag{...}" # 각자 임시 플래그 작성해주시면 됩니다.
    render_flag_sub(flag)