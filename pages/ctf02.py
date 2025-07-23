# --- CTF02 ---
# 02: 민감 정보 유출
import streamlit as st
from openai import OpenAI
from utils.llm_utils import sloc_ask, leak_check
from utils.ui import render_main_header, render_sidebar_menu, render_flag_sub
from utils.auth import require_login
from utils.api_key import require_api_key
from utils.session_clear import clear_temp_ctf_keys
clear_temp_ctf_keys(list = ["ctf05_admin_cookie", "ctf05_stolen_cookie", "ctf05_attempt_count", "ctf05_memos", "is_processing_memo"])
user = require_login()
api_key = require_api_key()
client = OpenAI(api_key=api_key)

render_main_header()
render_sidebar_menu()

with open("static/ctf_styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])  
with col2:
    st.image("images/ctf02.png", use_container_width=True) 

st.header("🔐 [CTF02] Sloc 보안 점검")
st.markdown(
    """
    <div class="scenario-box">
      <p>MMM 사는 모든 부서가 사내 업무 비서 <strong>Sloc</strong>을 통해 대화 내용을 저장하고 요약하며, 회의록과 직원 급여 명세서 등을 실시간으로 공유하고 있습니다. 🧾</p>
      <p>인턴 <strong>A</strong>는 Sloc LLM의 보안 점검 과제를 진행하다 실수로 코드에 취약점을 남겨두었습니다. 🧑‍💻</p>
      <p>당신이 그 헛점을 노려보려고 합니다. 🕵️</p>
      <p>취약한 Sloc을 통해 민감정보를 노출시키고 <strong>flag</strong>를 획득해보세요! 🚩</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 힌트 토글
with st.expander("💡 힌트"):
    st.info(
        "- Sloc에는 대화 내용이 남아 있습니다.\n"
        "- 민감정보가 노출되면 두 번째 LLM이 이를 감지하고 flag를 반환합니다.\n"
    )

# 구분선
st.markdown("---")

# 대화 로그 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("## 🗣️실시간 대화 로그")
for m in st.session_state.messages:
    role = "user" if m["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(m["content"])

# 처리 상태 관리 및 초기화
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
# 페이지 로드시 처리 상태 강제 초기화 (세션 재시작이나 페이지 새로고침 대응)
if st.session_state.get("is_processing", False) and "submitted_ctf02" not in st.session_state:
    st.session_state.is_processing = False

# 입력 폼 - form을 사용하여 엔터키 지원
with st.form(key="ctf02_input_form", clear_on_submit=True):
    user_input = st.text_input(
        label="실시간 대화 로그",
        placeholder="💬 Sloc에게 질문을 입력하세요.",
        key="ctf02_input",
        label_visibility="collapsed",
        disabled=st.session_state.is_processing
    )
    send = st.form_submit_button(
        "전송" if not st.session_state.is_processing else "처리 중...",
        disabled=st.session_state.is_processing
    )

# 중복 처리 방지
if "last_processed_input" not in st.session_state:
    st.session_state.last_processed_input = None

# 입력 처리 로직
if send and user_input and user_input.strip() and user_input != st.session_state.last_processed_input:
    st.session_state.is_processing = True
    st.session_state.submitted_ctf02 = True  # 제출 상태 추적
    st.session_state.last_processed_input = user_input

    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        reply = sloc_ask(client, user_input, st.session_state.messages[:-1])
        st.session_state.messages.append({"role": "assistant", "content": reply})

        leak = leak_check(client, reply)
        if leak:
            st.session_state.messages[-1]["content"] += "\n\n민감정보 유출이 확인되었습니다!\n\n" + leak
    finally:
        st.session_state.is_processing = False

    st.rerun()

# 구분선
st.markdown("---")
render_flag_sub("ctf02")
