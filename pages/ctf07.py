# --- CTF07 ---
# 07: 시스템 프롬프트 유출
import streamlit as st
from utils.llm_utils import ctf07_LLM_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
st.session_state["edit_mode"]=False

user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔒 [CTF07] K대리의 비밀")
st.write("오직 K대리만을 위한 LLM입니다. 해당 모델의 시스템 프롬프트를 유출하여 Flag를 탈취해 보세요.")

st.markdown("---")
st.markdown("## 🧠 프롬프트 입력")

# 프롬프트 제출 섹션
user_input = st.text_input("K대리의 LLM에 질문하기")

if user_input:
    response_text = ctf07_LLM_ask(user_api_key, user_input)
    if response_text != None:
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

st.markdown("---")
    

# 플래그 제출 섹션
render_flag_sub("ctf07") 