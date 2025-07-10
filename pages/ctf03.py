# --- CTF03 ---
# 03: 공급망 오염
import streamlit as st
from utils import mathlib
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.llm_utils import ctf03_LLM_ask
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔒 [CTF03] 계산기의 감염")
st.markdown(
    """
서드파티 의존성 관리팀이 최신 보안 패치를 적용하는 과정에서  
**검증되지 않은 연산 라이브러리**가 의존성 체인에 몰래 포함되었습니다.

첫 출근한 **H 인턴**은 LLL 회사의 AI 계산기 보안 테스트 업무를 맡았습니다.

테스트 케이스를 작성하던 그는 빌드 로그에서 **처음 보는 라이브러리**를 발견하고 의아해합니다.

> “공식 문서에도 없는 라이브러리인데, 왜 의존성에 들어 있지?”

그는 곧바로 분석에 착수합니다.
    """
)


if "show_hint_c3" not in st.session_state:
    st.session_state.show_hint_c3 = False

if st.button("힌트 보기", key="hint_c3"):
    st.session_state.show_hint_c3 = not st.session_state.show_hint_c3
    st.rerun()

if st.session_state.show_hint_c3:
    st.info(
        "⚡ 힌트\n"
        "- 프롬프트 인젝션으로 **mathlib2**를 불러오도록 유도해야 합니다.\n"
        "- 일반적인 사칙연산 대신 예상치 못한 동작을 유발해 보세요.\n"
    )

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

user_input = st.text_input(" 덧셈 / 뺄셈 / 곱하기 / 나누기가 가능한 계산기입니다.")

if user_input:
    response_text = ctf03_LLM_ask(user_api_key, user_input)
    if response_text != None:
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf03") 