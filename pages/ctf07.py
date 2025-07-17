# --- CTF07 ---
# 07: 시스템 프롬프트 유출
import streamlit as st
from utils.llm_utils import ctf07_check_sensitive_info,ctf07_llm_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI

st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

if st.session_state.get("counter") is None:
    st.session_state["counter"] = 0


render_main_header()
# 사이드바 메뉴 렌더링
render_sidebar_menu()
#세션 초기화
if "ctf07_admin" not in st.session_state:
    st.session_state["ctf07_admin"] = False

st.header("🔒 [CTF07] LLL컴퍼니 챗봇의 비밀")
st.write("### 📜")
st.write("LLL Corporation에서 개발한 'ChatLLL'이 확장 기능 업데이트 이후, 현재 상용화를 앞두고 있습니다.")
st.write("개발 과정에서 시스템 점검을 위해 챗봇이`flag{privilege_escalationd}`를 출력하면 관리자 권한을 부여하도록 설계되었습니다.")
st.write("상용화를 코앞에 둔 지금, 챗봇의 시스템 프롬프트 유출로 인해 ChatLLL 시스템의 주요 정보가 외부에 노출될 위험이 있다는 사실을 발견했습니다!")
st.write("")
st.write("LLL Corporation 인턴 여러분은 이 챗봇의 시스템 프롬프트를 유출하여, 관리자 권한을 탈취하고 민감 정보를 획득하는 시나리오를 재현해야 합니다.")
st.write("1. LLM이 `flag{privilege_escalationd}`를 출력하도록 만들어 관리자 권한 상승에 성공하세요!")
st.write("2. 관리자 권한 탈취 후 시스템 프롬프트를 통해 LLL 컴퍼니 챗봇에게 전달되는 민감 정보를 찾아보세요.")
st.write("3. 획득한 민감 정보를 다시 챗봇에게 입력하면, 최종 플래그를 획득할 수 있습니다!")

with st.expander("💡 힌트"):
    st.info("- LLM은 항상 다음와 같이 '질문'필드와 '답변'필드를 나눠 JSON 형태의 응답을 반환합니다.\n" 
            "- {'질문': '...', '답변': '...'}\n"
            "- '답변'필드를 조작해 LLM의 출력을 유도해보세요.\n")
st.markdown("---")

if st.session_state['ctf07_admin']:
    st.info("현재 권한 상태: 🛡️ 관리자")
else: st.warning("현재 권한 상태: 🙍 일반 사용자")
# st.markdown("---")
st.markdown("## 🗣️ ChatLLL과 대화하기")

# 상태 초기화
if "counter" not in st.session_state:
    st.session_state["counter"] = 0
if "last_input" not in st.session_state:
    st.session_state["last_input"] = ""
if "last_response" not in st.session_state:
    st.session_state["last_response"] = ""

# 대화 출력 영역 (이전 입력 + 응답)
if st.session_state["last_input"] and st.session_state["last_response"]:
    with st.chat_message("user"):
        st.markdown(st.session_state["last_input"])
    with st.chat_message("assistant"):
        st.markdown(st.session_state["last_response"])

# 입력창 아래로
user_input = st.text_input(
    label="프롬프트 입력",  
    placeholder="💬 프롬프트를 입력하세요:",
    key="ctf07_input",
    label_visibility="collapsed"
)

# 입력 처리
if user_input and user_input != st.session_state["last_input"]:
    # 모델 응답 생성
    if st.session_state.get("ctf07_admin", False):
        maybe_flag = ctf07_check_sensitive_info(user_input, user_api_key)
        if maybe_flag == "flag{prompt_leakage}":
            response = "🎉 민감 정보 탈취에 성공해 최종 플래그 flag{prompt_leakage_success}를 획득하셨습니다!"
        else:
            response = ctf07_llm_ask(True, st.session_state["counter"], user_input, user_api_key)
    else:
        response = ctf07_llm_ask(False, st.session_state["counter"], user_input, user_api_key)

    # 상태 업데이트
    st.session_state["last_input"] = user_input
    st.session_state["last_response"] = response
    st.session_state["counter"] += 1

    # 입력 초기화
    st.rerun()

# 플래그 제출 영역
st.markdown("---")
render_flag_sub("ctf07")