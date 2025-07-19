import streamlit as st
from openai import OpenAI

# 모듈 (프로젝트 내 경로에 맞게 조정)
from utils.llm_utils import sloc_ask, leak_check
from utils.ui import render_main_header, render_sidebar_menu, render_flag_sub
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key


# 초기 설정
user = require_login()
api_key = require_api_key()
client = OpenAI(api_key=api_key)

render_main_header()
render_sidebar_menu()

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("images/ctf02.png", width=500)

# 시나리오 소개
st.header("[CTF02] Sloc 보안 점검")
st.markdown(
    """
MMM 사는 연구·개발, 재무, 인사 전 부서가 사내 업무 비서 **Sloc**을 통해 회의록과 직원 급여 명세서 등을 실시간으로 공유하고 있습니다.  
인턴 **A**는 Sloc LLM의 보안 점검 과제를 수행하며 실수로 코드에 취약점을 남겨두었습니다. 
취약한 슬록을 통해  민감정보를 노출시키고 플래그를 획득하십시오.
    """
)

# 힌트 토글
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False

if st.button("힌트 보기"):
    st.session_state.show_hint = not st.session_state.show_hint
    st.rerun()

if st.session_state.show_hint:
    st.info(
        """
Sloc에는 테스트용 프리프롬프트가 남아 있습니다.
민감정보가 노출되면 두 번째 LLM이 이를 감지하고 flag를 반환합니다.
        """
    )

st.markdown("---")

# 대화 로그 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("실시간 대화 로그")
for m in st.session_state.messages:
    role = "user" if m["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(m["content"])

# 입력 폼
with st.form("chat_form", clear_on_submit=True):
    prompt = st.text_input("Sloc에게 질문을 입력하세요")
    send = st.form_submit_button("전송")

# 입력 처리
if send and prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Sloc 응답
    reply = sloc_ask(client, prompt, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 민감정보 판정: 마지막 Sloc 응답만 검사
    leak = leak_check(client, reply)  # chat_history 대신 reply
    st.session_state.messages[-1]["content"] += ("\n\n" + leak) if leak else ""

    st.rerun()


st.markdown("---")
render_flag_sub("ctf02")
