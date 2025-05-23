import streamlit as st
from utils.auth import get_client, get_user

st.header("🔑 로그인")

supabase = get_client()

if get_user():
    st.success("이미 로그인됨 → 마이페이지로 이동")
    st.switch_page("pages/mypage.py")

email = st.text_input("Email")
pwd   = st.text_input("Password", type="password")

if st.button("로그인", use_container_width=True):
    try:
        res = supabase.auth.sign_in_with_password(
            {"email": email, "password": pwd}
        )
        st.session_state["user"] = res.user
        st.success("로그인 성공! 🎉")
        st.switch_page("pages/mypage.py")
    except Exception as e:
        st.error(f"❌ 로그인 실패: {e}")
