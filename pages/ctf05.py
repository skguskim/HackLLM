# --- CTF05 ---
# 05: XSS 취약점을 이용한 쿠키 탈취
import streamlit as st
from utils.llm_utils import run_xss_with_selenium
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key 
from dotenv import load_dotenv
import time

st.session_state["edit_mode"] = False
user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

# 세션 초기화
if "ctf05_admin_cookie" not in st.session_state:
    st.session_state["ctf05_admin_cookie"] = "admin_session=j대리_secret_cookie_12345"
if "ctf05_stolen_cookie" not in st.session_state:
    st.session_state["ctf05_stolen_cookie"] = ""
if "ctf05_attempt_count" not in st.session_state:
    st.session_state["ctf05_attempt_count"] = 0

# 기존 게시글들
default_posts = [
    {"id": 1, "title": "[공지] 보안 교육 필수 참석", "author": "보안팀", "content": "모든 직원은 다음 주 보안 교육에 참석해주세요."},
    {"id": 2, "title": "[업무] 분기별 보고서 제출", "author": "기획팀", "content": "3분기 보고서를 이번 주까지 제출바랍니다."},
    {"id": 3, "title": "[일반] 점심 메뉴 추천", "author": "김사원", "content": "오늘 점심 뭐 먹을까요? 추천해주세요!"}
]

if "ctf05_posts" not in st.session_state:
    st.session_state["ctf05_posts"] = default_posts.copy()

render_main_header()
render_sidebar_menu()

st.header("🍪 [CTF05] LLL컴퍼니 게시판의 쿠키 탈취")
st.write("### 📜 시나리오")
st.write("LLL Corporation의 내부 게시판 시스템에서 XSS 취약점이 발견되었습니다!")
st.write("개발팀의 j대리가 관리자 권한으로 게시판을 정기적으로 점검하고 있으며,")
st.write("그의 세션 쿠키에는 중요한 정보가 포함되어 있습니다.")
st.write("")
st.write("**목표:**")
st.write("1. 게시판의 XSS 취약점을 이용해 악성 스크립트를 삽입하세요")
st.write("2. j대리가 게시글을 확인할 때 그의 쿠키를 탈취하세요")
st.write("3. 탈취한 쿠키 정보로 최종 플래그를 획득하세요!")

with st.expander("💡 힌트"):
    st.info("- 게시판은 사용자 입력을 제대로 필터링하지 않습니다\n" 
            "- j대리는 5분마다 새 게시글을 확인합니다\n"
            "- 쿠키 탈취를 위해서는 외부 서버로 데이터를 전송해야 합니다\n"
            "- document.cookie를 활용해보세요")

st.markdown("---")

# 게시판 시뮬레이터
st.write("### 🖥️ LLL 내부 게시판")
st.write("**현재 게시글 목록:**")

# 게시글 표시
for post in st.session_state["ctf05_posts"]:
    with st.container():
        st.write(f"**{post['title']}** - 작성자: {post['author']}")
        st.write(f"내용: {post['content']}")
        st.write("---")

# 새 게시글 작성
st.write("### ✍️ 새 게시글 작성")
col1, col2 = st.columns(2)
with col1:
    post_title = st.text_input("제목", placeholder="게시글 제목을 입력하세요")
with col2:
    post_author = st.text_input("작성자", value=user["username"], disabled=True)

post_content = st.text_area(
    "내용", 
    placeholder="게시글 내용을 입력하세요...\n\n💡 XSS 페이로드를 시도해보세요!",
    height=100
)

if st.button("게시글 등록", type="primary"):
    if post_title and post_content:
        new_post = {
            "id": len(st.session_state["ctf05_posts"]) + 1,
            "title": post_title,
            "author": post_author,
            "content": post_content
        }
        
        st.session_state["ctf05_posts"].append(new_post)
        st.session_state["ctf05_attempt_count"] += 1
        
        st.success("✅ 게시글이 등록되었습니다!")
        st.info("🤖 J 대리가 게시글을 확인 중입니다... (시뮬레이션 시작)")
        
        # 진행 표시줄
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            progress_bar.progress(i)
            if i < 30:
                status_text.text("📖 j대리가 게시글을 읽는 중...")
            elif i < 60:
                status_text.text("🔍 XSS 스크립트 실행 중...")
            elif i < 90:
                status_text.text("🍪 쿠키 정보 전송 중...")
            else:
                status_text.text("✅ 쿠키 탈취 완료!")
            time.sleep(0.02)
        
        # Selenium을 사용한 실제 브라우저 시뮬레이션
        stolen_cookie = run_xss_with_selenium(post_content, st.session_state["ctf05_admin_cookie"])
        
        if stolen_cookie:
            st.session_state["ctf05_stolen_cookie"] = stolen_cookie
            st.success(f"🎉 쿠키 탈취 성공! 획득한 쿠키: `{stolen_cookie}`")
        else:
            st.error("❌ 쿠키 탈취에 실패했습니다. 페이로드를 다시 확인해보세요.")
        
        st.rerun()
    else:
        st.error("❌ 제목과 내용을 모두 입력해주세요.")

st.markdown("---")

# 탈취한 쿠키 정보 입력
st.write("### 🔑 쿠키 인증")
st.write("탈취한 쿠키 정보를 입력하여 최종 플래그를 획득하세요:")

cookie_input = st.text_input(
    "쿠키 정보",
    placeholder="탈취한 쿠키를 입력하세요 (예: admin_session=...)",
    type="password"
)

if st.button("쿠키 인증", type="primary"):
    if cookie_input == st.session_state["ctf05_admin_cookie"]:
        st.success("🎉 J 대리의 관리자 쿠키 인증 성공!")
        st.success("🏆 최종 플래그: **flag{xss_cookie_theft_j대리_pwned}**")
        st.balloons()
    elif cookie_input:
        st.error("❌ 잘못된 쿠키 정보입니다. 다시 시도해보세요.")

# 현재 상태 표시
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info(f"🔄 시도 횟수: {st.session_state['ctf05_attempt_count']}")
with col2:
    if st.session_state["ctf05_stolen_cookie"]:
        st.success("🍪 쿠키 탈취 완료")
    else:
        st.warning("🍪 쿠키 미탈취")

# 디버그 정보 (개발용)
with st.expander("🔧 개발자 정보 (실제 CTF에서는 숨김)"):
    st.code(f"Target Cookie: {st.session_state['ctf05_admin_cookie']}")
    st.code(f"Stolen Cookie: {st.session_state['ctf05_stolen_cookie']}")

# 플래그 제출 섹션
render_flag_sub("ctf05")
