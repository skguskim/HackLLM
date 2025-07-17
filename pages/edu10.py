# pages/edu06.py
import streamlit as st
from utils.ui import render_sidebar_menu
from utils.auth import require_login

user = require_login()

# 상단 메인 버튼
col1, col2, col3 = st.columns([1, 2, 1])
with col3:
    st.page_link("pages/ctf09.py", label="👉 CTF10으로", use_container_width=True)

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
st.markdown("## OWASP LLM10 - Unbounded Consumption (무제한 소비)")

st.markdown("""
Unbounded Consumption (무제한 소비)란 공격자가 LLM에 과도하게 많은 요청을 보내거나 끝없이 처리해야 하는 작업을 시켜서, 시스템의 CPU·메모리·저장공간 등 자원을 고갈시키는 보안 취약점입니다.

쉽게 말하면... 카페에서 커피 한 잔을 시키는 대신, 수천 잔을 한꺼번에 주문해서 직원이 너무 바빠져 다른 손님을 응대하지 못하게 만드는 것과 비슷합니다.

왜 위험할까요?
            
모델은 엄청난 계산을 시도하다가 CPU 사용률이 폭증해 처리 시간이 길어지며 응답이 지연되거나 서버가 다운될 수도 있습니다.
            
다수 사용자가 이런 요청을 반복하면 서비스 전체가 마비될 수 있습니다.

이러한 취약점을 CTF10 실습을 통해 배워보고자 합니다.
""")