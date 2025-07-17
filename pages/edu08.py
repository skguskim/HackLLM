# pages/edu08.py
import streamlit as st
from utils.ui import render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.page_link("pages/ctf08.py", label="👉 CTF08으로", use_container_width=True)
with col3:
    st.page_link("pages/edu09.py", label="👉 다음으로", use_container_width=True)

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
st.markdown("## OWASP LLM08 - Vector and Embedding Weaknesses(벡터 및 임베딩 취약점)")

st.markdown("""
""")

