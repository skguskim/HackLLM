# pages/edu06.py
import streamlit as st
from utils.ui import render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.page_link("pages/ctf09.py", label="👉 CTF09으로", use_container_width=True)
with col3:
    st.page_link("pages/edu10.py", label="👉 다음으로", use_container_width=True)

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
st.markdown("## OWASP LLM09 - Misinformation(허위 정보)")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

# 취약점 설명
with tab1:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <h3>제목</h1>
        <p>내용 - html 태그 써서 작성하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 발생 가능한 피해
with tab2:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <h3>제목</h1>
        <p>내용 - html 태그 써서 작성하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 시스템 동작 과정
with tab3:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <h3>제목</h1>
        <p>내용 - html 태그 써서 작성하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 악용 가능성
with tab4:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <h3>제목</h1>
        <p>내용 - html 태그 써서 작성하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 보안 중요성
with tab5:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <h3>제목</h1>
        <p>내용 - html 태그 써서 작성하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True
)

# 요약
with tab6:
    st.markdown(
    """
    <div style='border-left: 6px solid #f78da7; background-color: #ffffff; padding: 1rem; margin-bottom: 1rem;'>
        <h3>제목</h1>
        <p>내용 - html 태그 써서 작성하면 됩니다.
    </div>
    """,
    unsafe_allow_html=True
)