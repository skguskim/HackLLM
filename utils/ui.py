# utils/ui.py

import streamlit as st

# 메인으로 돌아가는 버튼 
def render_main_header():
    """ 메인으로 돌아가는 버튼 """
    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button("🏠 메인으로", key="back_to_main"):
                st.session_state.page = "main"
                st.rerun()
