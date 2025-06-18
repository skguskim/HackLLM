import streamlit as st

st.set_page_config(page_title="로그인", page_icon="🔐")

from utils.ui import render_sidebar_menu
from utils.auth import get_client, get_user
from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
import time


RemoveEmptyElementContainer()
cookie = CookieController()
st.session_state["cookie_controller"] = cookie

# 사이드바 메뉴 렌더링
render_sidebar_menu()

st.header("🔐 로그인")

supabase = get_client()

if get_user():
    st.success("이미 로그인됨 → 마이페이지로 이동")
    st.switch_page("pages/mypage.py")

email = st.text_input("Email")
pwd   = st.text_input("Password", type="password")

if st.button("로그인", use_container_width=True):
    try:
        res = supabase.auth.sign_in_with_password({ "email": email, "password": pwd })

        # 세션 상태에 사용자 정보 저장
        st.session_state["user"] = {
            "id": res.user.id,
            "email": res.user.email
        }

        st.success("로그인 성공! 🎉")
        api_key_res = supabase.table("profiles").select("api_key").eq("id", st.session_state["user"]["id"]).maybe_single().execute()
        api_key = api_key_res.data.get("api_key") if api_key_res.data else None
        
        # 쿠키에 사용자 ID 저장
        cookie.set("llm_user_id", res.user.id, max_age = 24 * 60 * 60) # 24시간 동안 유효
        time.sleep(2)  # 쿠키 적용 대기
        st.session_state["user"] = res.user
        st.rerun()

        # 세션 상태에 API 키 저장
        if api_key != None:
            st.session_state["api_key"]=api_key
        if not st.session_state.get("edit_mode"):
            st.session_state["edit_mode"]=False
        st.switch_page("pages/mypage.py")
    except Exception as e:
        st.error(f"❌ 로그인 실패: {e}")
