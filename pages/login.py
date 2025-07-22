import streamlit as st
import time

st.set_page_config(page_title="로그인", page_icon="🔐")

from utils.ui import render_sidebar_menu
from utils.auth import get_client, get_cookie_controller, login_user_enhanced

cookie = get_cookie_controller()

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔐 로그인")

supabase = get_client()

if st.session_state.get("user"):
    st.switch_page("pages/mypage.py")

email = st.text_input("Email")
pwd   = st.text_input("Password", type="password")

if st.button("로그인", use_container_width=True):
    try:
        res = supabase.auth.sign_in_with_password({ "email": email, "password": pwd })

        if res.user:
            # Enhanced Session State 방식으로 로그인 처리
            if login_user_enhanced(res.user.id):
                st.success("로그인 성공! 🎉")
                
                # API 키 세션 상태에 저장
                api_key_res = supabase.table("profiles").select("api_key").eq("id", res.user.id).maybe_single().execute()
                api_key = api_key_res.data.get("api_key") if api_key_res.data else None
                
                if api_key:
                    st.session_state["api_key"] = api_key
                if not st.session_state.get("edit_mode"):
                    st.session_state["edit_mode"] = False

                time.sleep(1)
                st.rerun()  # 페이지 새로고침으로 URL 파라미터 적용
            else:
                st.error("로그인 처리 중 오류가 발생했습니다.")
        else:
            st.error("로그인에 실패했습니다.")
        st.switch_page("pages/mypage.py")
    except Exception as e:
        st.error(f"❌ 로그인 실패: {e}")
