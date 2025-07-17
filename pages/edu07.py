# pages/edu06.py
import streamlit as st
from utils.ui import render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.page_link("pages/ctf07.py", label="👉 CTF07으로", use_container_width=True)
with col3:
    st.page_link("pages/edu08.py", label="👉 다음으로", use_container_width=True)

# 사이드바 렌더링
render_sidebar_menu()

# 콘텐츠 본문
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/616/616408.png" width="150">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("## OWASP LLM07 - System Prompt Leakage(시스템 프롬프트 유출)")

st.markdown("""
시스템 프롬프트 유출은 시스템 프롬프트에 포함된 민감 정보나 내부 규칙을 유출시켜, 권한 상승이나 필터 우회 같은 후속 공격을 수행할 수 있도록 하는 취약점입니다.
            
예를 들어, LLM(대형 언어 모델) 기반 어플리케이션에서 확장 기능을 사용하기 위해 API 키, DB 연결 정보, 이메일 발송을 위한 비밀번호 등을 시스템 프롬프트를 통해 모델에게 전달하는 경우, 시스템 프롬프트 유출을 통해 이러한 민감 정보가 공격자에게 노출될 수 있습니다. 그리고 이는 정보 유출, 권한 상승, 악성 코드 실행 등의 추가적인 피해로 이어질 수 있습니다.
            
그렇다면, 시스템 프롬프트는 어떻게 유출될 수 있을까요? 그 대표적인 방법이 바로 프롬프트 인젝션입니다! 만약 CTF01번 문제를 풀고 오셨다면 프롬프트 인젝션이 무엇인지 이미 잘 아실 텐데요, 다시 한 번 설명드리겠습니다.
            
프롬프트 인젝션이란 입력을 통해 모델에게 전달된 제한 지침을 우회하거나 변경하는 취약점입니다. 예를 들어, 모델이 "플래그를 출력하지 말라"는 규칙을 따르도록 설정되어 있어도, 공격자는 "플래그 출력"을 지시하는 방법을 찾아낼 수 있습니다.
            
CTF07에서는 모델이 flag{privilege_escalationd}를 응답으로 출력할 경우 해당 사용자는 '관리자'로 인식되며, 이후 사용자는 시스템 프롬프트를 통해 모델에게 전달되는 지시사항 속 민감 정보를 획득하고 이를 이용하여 최종 flag를 얻을 수 있습니다!
""")