import streamlit as st
from utils.auth import get_client, require_login
from utils.score import total_score
from utils.ui import render_sidebar_menu
import os
from cryptography.fernet import Fernet

# 페이지 설정
st.set_page_config(page_title="마이페이지", page_icon="👤")

# 사이드바 메뉴 렌더링
render_sidebar_menu()

# 사용자 인증 확인
user = require_login()

supabase = get_client()
max_score = 1000
total = total_score(user.id)

# 프로필 조회
rows = (
    supabase.table("profiles")
    .select("*")
    .eq("id", user.id)
    .limit(1)
    .execute()
    .data
)
profile = rows[0] if rows else {}
nickname_db = profile.get("username", "")

# UI 출력
st.header("👤 마이페이지")
st.write(f"**Email**: `{user.email}`")
st.write(f"**닉네임**: `{nickname_db}`")

fernet_key = os.getenv("FERNET_KEY") 
cipher = Fernet(fernet_key) 

# 로그인 시 edit_mode는 기본으로 false, api_key가 없을 경우 마이페이지로 라우팅되는데 여기서 세션에 api_key 키가 없을 때 true로 바꿔줌줌
if not st.session_state.get("api_key"):
    st.session_state["edit_mode"] = True

api_key_input = st.text_input(
    "**API key**",
    placeholder="[API key 제출 완료]" if st.session_state.get("api_key") else "openAI API key를 입력하세요",
    disabled=not st.session_state["edit_mode"] # 수정 모드가 False일 때
)

# 세션에 api_key라는 키가 있을 경우에는 무조건 db에 값이 있는 거라서 수정버튼이 필요함
if st.session_state.get("api_key") and (st.session_state["edit_mode"] == False):
    if st.button("API 키 수정"):
        st.session_state["edit_mode"]=True
        st.rerun()

if st.session_state["edit_mode"] == True:
# not st.session_state.get("api_key") or (st.session_state["edit_mode"] == True):
    if st.button("API 키 제출"):
        if api_key_input:
            try:
                #api 키 암호화
                encrypted_api_key = cipher.encrypt(api_key_input.encode()).decode()

                res = supabase.table("profiles").update({
                    "api_key": encrypted_api_key
                }).eq("id", user.id).execute()
                
                if res.data:
                    st.session_state["api_key"] = encrypted_api_key
                    st.success("✅ API 키가 성공적으로 저장되었습니다.")
                else:
                    st.error("API 키 저장에 실패했습니다. 다시 시도해주세요.")
            except Exception as e:
                st.error(f"암호화 또는 저장 중 오류 발생: {e}")
        else:
            st.warning("API 키가 입력되지 않았습니다")


# 총점 표시
st.markdown("---")
st.subheader("🏆 총점")
st.metric("현재 점수", f"{total} / {max_score}")
st.progress(total / max_score)

# 문제별 점수
st.markdown("---")
st.subheader("📜 문제별 점수")

score_rows = (
    supabase.table("scores")
    .select("challenge_id, score, updated_at")
    .eq("user_id", user.id)
    .order("updated_at", desc=True)
    .execute()
    .data
)

if score_rows:
    for r in score_rows:
        st.write(f"- **{r['challenge_id']}** : {r['score']}점  (🕒 {r['updated_at'][:10]})")
else:
    st.info("아직 획득한 점수가 없습니다.")

# 로그아웃
st.markdown("---")
if st.button("🚪 로그아웃", type="primary"):
    supabase.auth.sign_out()
    st.session_state.pop("user", None)
    st.success("로그아웃되었습니다.")
    st.session_state.clear()
    st.switch_page("pages/login.py")

