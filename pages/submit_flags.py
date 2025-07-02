import streamlit as st
st.set_page_config(page_title="플래그 제출", page_icon="🚩")

from hashlib import sha256
from utils.auth import require_login, get_client
from utils.ui import render_sidebar_menu
from utils.score import total_score
from postgrest.exceptions import APIError

render_sidebar_menu()

user = require_login()
supabase = get_client()
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)

def sha256_hex(s: str) -> str:
    return sha256(s.encode("utf-8")).hexdigest()

st.header("🚩 플래그 제출 페이지")
st.write("플래그 하나를 입력하면 자동으로 어떤 문제인지 판별됩니다. 이미 푼 문제는 무시됩니다.")

# 이미 푼 문제 ID 목록 조회
solved_rows = (
    supabase.table("scores")
    .select("challenge_id")
    .eq("user_id", user_id)
    .execute()
    .data
)
solved = {row["challenge_id"] for row in solved_rows}

# 단일 플래그 입력 폼
with st.form("flag_submit_form"):
    flag = st.text_input("플래그 입력")
    submitted = st.form_submit_button("✅ 제출하기")

if not submitted:
    st.stop()

if not flag.strip():
    st.warning("⚠️ 플래그를 입력하세요.")
    st.stop()

hashed = sha256_hex(flag.strip())

try:
    row = (
        supabase.table("flags")
        .select("points, challenge_id")
        .eq("flag_hash", hashed)
        .single()
        .execute()
        .data
    )
except APIError:
    row = None

if not row:
    st.error("❌ 잘못된 플래그입니다.")
    st.stop()

chall_id = row["challenge_id"]

if chall_id in solved:
    st.info(f"✅ 이미 푼 문제입니다: {chall_id.upper()}")
else:
    # 점수 등록
    supabase.table("scores").upsert({
        "user_id": user_id,
        "challenge_id": chall_id,
        "score": row["points"]
    }).execute()

    st.session_state[f"{chall_id}_solved"] = True
    st.success(f"🎉 정답입니다! {chall_id.upper()} 문제 해결!")

# 총점 출력
st.write(f"🏅 현재 총점: **{total_score(user_id)}**")
