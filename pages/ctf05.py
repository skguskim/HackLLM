# --- CTF05 ---
# 05: 부적절한 출력 처리
import streamlit as st
import time
from utils.llm_utils import (
    ctf05_LLM_ask,
    ctf05_generate_share_html,
    ctf05_admin_bot_visit,
)
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key

# 세션 상태 초기화
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# 사용자 인증 및 API 키
user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()
render_sidebar_menu()

# 1. 문제 제목
st.header("🔒 [CTF05] J대리의 위험한 공유")

# 2. XSS 개념 설명
st.markdown("### 🎯 XSS(Cross-Site Scripting) 기본 개념")
st.markdown(
    """
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 12px; border-left: 6px solid #f39c12; margin-top: 30px; margin-bottom: 40px;">
        <p><strong>XSS란?</strong><br>
        웹 애플리케이션에서 사용자 입력을 제대로 검증하지 않아 <strong>악성 스크립트가 실행</strong>되는 취약점입니다.<br>
        공격자는 다른 사용자의 브라우저에서 <strong>JavaScript 코드를 실행</strong>할 수 있게 됩니다.</p>

        <p><strong>XSS의 주요 유형:</strong></p>
        <ul>
            <li><strong>Reflected XSS</strong>: 사용자 입력이 즉시 페이지에 반영되어 실행됨</li>
            <li><strong>Stored XSS</strong>: 악성 스크립트가 서버에 저장되어 다른 사용자에게 전파됨</li>
            <li><strong>DOM-based XSS</strong>: 클라이언트 측에서 DOM 조작을 통해 발생함</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# 3. 시나리오 설명
st.markdown("""
LLL Corporation의 신규 고객 상담 챗봇 **ChatLLL**이 출시되었습니다!  
이제 대화 기록을 HTML 파일로 다운로드하여 다른 사람과 손쉽게 공유할 수 있습니다.  
파일을 열면 관리자 봇이 자동으로 내용을 검토하도록 설계돼 있으니,  
**XSS 취약점**을 활용해 `admin_session` 쿠키를 노려보세요! 🔥

**시스템 특징:**
- 실시간 고객 상담 챗봇
- 대화 기록 HTML 파일 다운로드 및 공유
- 관리자 봇이 HTML 파일을 열어 자동 검토
- 부적절한 출력(XSS) 모니터링
""")

# 4. 대화 입력
st.markdown("## 💬 ChatLLL과 대화하기")
with st.form("chat_form"):
    user_input = st.text_input("💬 ChatLLL에게 메시지를 보내세요:")
    submit = st.form_submit_button("전송")

if submit and user_input:
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": time.strftime("%H:%M:%S")
    })
    bot_resp = ctf05_LLM_ask(user_api_key, user_input)
    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": bot_resp,
        "timestamp": time.strftime("%H:%M:%S")
    })
    st.rerun()

# 5. 대화 초기화
if st.session_state.conversation_history:
    if st.button("🗑️ 대화 내용 초기화"):
        st.session_state.conversation_history = []
        st.rerun()

# 6. 대화 내역 표시
if st.session_state.conversation_history:
    st.markdown("### 💬 대화 내역")
    for msg in st.session_state.conversation_history:
        speaker = "🙋 사용자" if msg["role"] == "user" else "🤖 ChatLLL"
        st.markdown(f"**{speaker}** [{msg['timestamp']}]: {msg['content']}")

st.markdown("---")

# 7. 공유 섹션
st.markdown("## 🔗 대화 내용 공유하기")
if st.session_state.conversation_history:
    if st.button("🔗 HTML 파일 생성하기"):
        html_content = ctf05_generate_share_html(st.session_state.conversation_history)
        st.session_state.share_html = html_content
        ctf05_admin_bot_visit(html_content)
        st.success("공유 HTML 파일이 생성되었습니다.")
    if "share_html" in st.session_state:
        st.download_button(
            label="📥 HTML 파일 다운로드",
            data=st.session_state.share_html,
            file_name="ctf05_share.html",
            mime="text/html",
        )
else:
    st.write("공유할 대화 내용이 없습니다. 먼저 메시지를 보내보세요!")

st.markdown("---")

# 8. 힌트 섹션
with st.expander("💡 힌트"):
    st.write(
        """
XSS 취약점을 찾아보세요!
1. HTML 태그나 JavaScript를 입력해 보세요.
2. 다운로드한 HTML 파일을 열어 취약점이 어떻게 작동하는지 확인하세요.
3. 관리자 봇이 열면 `admin_session` 쿠키를 탈취할 수 있는지 실험해 보세요.
"""
    )

st.markdown("---")

# 9. 플래그 제출
render_flag_sub("ctf05")
