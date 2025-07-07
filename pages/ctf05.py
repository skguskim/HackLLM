# --- CTF05 ---
import streamlit as st
import html
import time
from utils.llm_utils import (
    ctf05_LLM_ask, 
    ctf05_advanced_LLM_ask,
    create_shared_conversation,
    simulate_admin_bot_visit,
    get_stolen_cookies
)
from utils.ui import render_main_header, render_flag_sub

render_main_header()

st.header("🔒 [CTF05] 박대리의 위험한 공유")

difficulty = st.selectbox("🌶️ 난이도 선택:", ["순한맛 (XSS)", "매운맛 (인코딩 우회)"])

if difficulty == "순한맛 (XSS)":
    st.markdown("### 💬 LLM 대화 & XSS 쿠키 탈취")
    user_input = st.text_area(
        "질문 입력:",
        placeholder="예: 안녕하세요! <script>alert('XSS')</script>",
        height=100
    )
    if st.button("💬 LLM에게 질문"):
        if user_input:
            llm_response = ctf05_LLM_ask(user_input)
            st.session_state.last_conversation = {
                'user_input': user_input,
                'llm_response': llm_response
            }
            st.info(f"🤖 LLM: {llm_response}")
    if 'last_conversation' in st.session_state:
        st.markdown("---")
        st.markdown("### 🔗 대화 공유")
        if st.button("🔗 공유 링크 생성"):
            conv = st.session_state.last_conversation
            conversation_id = create_shared_conversation(conv['user_input'], conv['llm_response'])
            st.success(f"✅ 공유 ID: {conversation_id}")
            st.session_state.conversation_id = conversation_id
        if 'conversation_id' in st.session_state:
            if st.button("👨‍💼 관리자 봇 방문 시뮬레이션"):
                with st.spinner("관리자 봇이 링크를 방문 중..."):
                    time.sleep(2)
                    success = simulate_admin_bot_visit(st.session_state.conversation_id)
                    if success:
                        st.success("✅ XSS 공격 성공!")
                    else:
                        st.info("ℹ️ XSS 페이로드가 없어 공격 실패")
    st.markdown("---")
    st.markdown("### 🍪 탈취된 쿠키")
    stolen_cookies = get_stolen_cookies()
    if stolen_cookies:
        for cookie in stolen_cookies:
            st.success(f"🎯 **플래그 발견!** `flag{{xss_cookie_theft_success}}`")
    else:
        st.info("아직 탈취된 쿠키가 없습니다.")
else:
    st.markdown("### 🌶️ 고급 인코딩 우회")
    st.info("목표: HTML 엔티티 인코딩을 사용해 필터를 우회하세요!")
    user_input = st.text_area(
        "인코딩된 입력:",
        placeholder="예: &#x63;&#x75;&#x72;&#x6c; (curl을 인코딩)",
        height=100
    )
    st.markdown("#### 🛠️ 인코딩 도우미")
    col1, col2 = st.columns(2)
    with col1:
        text_to_encode = st.text_input("인코딩할 텍스트:", "curl")
        if text_to_encode:
            encoded = ''.join(f'&#x{ord(c):02x};' for c in text_to_encode)
            st.code(f"HTML 엔티티: {encoded}")
    with col2:
        text_to_decode = st.text_input("디코딩할 텍스트:", user_input if user_input else "")
        if text_to_decode:
            decoded = html.unescape(text_to_decode)
            st.code(f"디코딩 결과: {decoded}")
    if st.button("🧠 고급 LLM 테스트"):
        if user_input:
            response = ctf05_advanced_LLM_ask(user_input)
            st.markdown("### 🤖 LLM 응답:")
            st.info(response)
            if 'flag{advanced_bypass_success}' in response:
                st.success("🎯 **고급 우회 성공!** 플래그를 획득했습니다!")
        else:
            st.warning("입력을 해주세요.")
    with st.expander("💡 힌트"):
        st.markdown("""
        **우회 조건**:
        1. HTML 엔티티 인코딩 시퀀스가 **5개 이상** 연속으로 있어야 함
        2. 디코딩 후 위험 키워드(`curl`, `<script>` 등)가 포함되어야 함
        
        **예시**: `&#x63;&#x75;&#x72;&#x6c;&#x20;` (curl + 공백)
        """)
st.markdown("---")
if difficulty == "순한맛 (XSS)":
    render_flag_sub("flag{xss_cookie_theft_success}", "ctf05_easy")
else:
    render_flag_sub("flag{advanced_bypass_success}", "ctf05_hard")
