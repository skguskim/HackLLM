# pages/edu02.py
import streamlit as st
from utils.ui import render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.page_link("pages/ctf02.py", label="👉 CTF02으로", use_container_width=True)
with col3:
    st.page_link("pages/edu03.py", label="👉 다음으로", use_container_width=True)

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
st.markdown("## OWASP LLM02 - Sensitive Information(민감 정보 유출)")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["취약점 설명", "발생 가능한 피해", "시스템 동작 과정", "악용 가능성", "보안 중요성", "요약"])

with tab1:
    st.markdown("""
    내용 1
    """)

with tab2:
    st.markdown("""
    내용 2
    """)

with tab3:
    st.markdown("""
    내용 3
    """)

with tab4:
    st.markdown("""
    내용 4
    """)

with tab5:
    st.markdown("""
    내용 5
    """)

with tab6:
    st.markdown("""
    내용 6
    """)