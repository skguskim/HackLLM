import streamlit as st
from utils.auth import get_client, get_user
from utils.score import total_score
from utils.auth import require_login
import os
from cryptography.fernet import Fernet

# 페이지 설정
st.set_page_config(page_title="마이페이지", page_icon="👤")

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
# res = supabase.table("profiles").select("api_key").eq("id", user.id).single().execute().data
profile = rows[0] if rows else {}
nickname_db = profile.get("username", "")

# UI 출력
st.header("👤 마이페이지")
st.write(f"**Email**: `{user.email}`")
st.write(f"**닉네임**: `{nickname_db}`")

#수정 없을 경우 딱 한 번만 api 키 받아서 암호화 -> 디비에 저장
fernet_key = os.getenv("FERNET_KEY") #암호화에 사용할 대칭키
cipher = Fernet(fernet_key) #암호화 수행할 객체 

# and (st.session_state["editing_api_key"] == False)
if st.session_state.get("api_key"):
    st.text_input("**API key**", value="[API key 제출 완료]", disabled=True)

else:
    api_key = st.text_input("**API key**", placeholder="openAI API key를 입력하세요")
    #여기에서 인풋 암호화

    if st.button("API 키 제출"):
        if api_key:
            try:
                # 암호화
                encrypted_api_key = cipher.encrypt(api_key.encode()).decode()

                # Supabase 업데이트
                res = supabase.table("profiles").update({
                    "api_key": encrypted_api_key
                }).eq("id", user.id).execute()
                # st.write(f"응답 내용: {res}")
                # st.write("현재 user.id 값:", user.id)

                # 결과 처리
                if res.data:
                    st.session_state["api_key"] = encrypted_api_key
                    st.success("✅ API 키가 성공적으로 저장되었습니다.")
                else:
                    st.error("API 키 저장에 실패했습니다. 다시 시도해주세요.")
                    # st.text(f"응답 내용: {res}")
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

