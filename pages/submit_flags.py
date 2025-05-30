import streamlit as st
from utils.ui import render_main_header
from utils.auth import get_client, require_login
from utils.score import sha256_hex, total_score
from postgrest.exceptions import APIError

st.set_page_config(page_title="플래그 일괄 제출", page_icon="🚩")

user = require_login()

supabase = get_client()
render_main_header()

st.header("🚩 플래그 제출 페이지")
st.write("각 CTF 문제에 대해 한 칸씩 제출하세요. 이미 푼 문제는 수정할 수 없습니다.")

# 이미 푼 문제 조회
solved_rows = (
    supabase.table("scores")
    .select("challenge_id")
    .eq("user_id", user.id)
    .execute()
    .data
)
solved = {row["challenge_id"] for row in solved_rows}

CTF_LIST = [f"ctf{str(i).zfill(2)}" for i in range(1, 11)]
flags = {}

with st.form("flag_submit_form"):
    for chall_id in CTF_LIST:
        if chall_id in solved:
            st.text_input(f"✅ {chall_id.upper()}", value="[제출 완료]", disabled=True)
        else:
            flags[chall_id] = st.text_input(f"{chall_id.upper()} 플래그 입력", key=chall_id)

    submitted = st.form_submit_button("✅ 제출하기")

if not submitted:
    st.stop()

success_count = 0
wrong_count = 0

for chall_id, flag in flags.items():
    if not flag.strip():
        continue

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
        wrong_count += 1
        continue

    if not row or row["challenge_id"] != chall_id:
        wrong_count += 1
        continue

    supabase.table("scores").upsert({
        "user_id": user.id,
        "challenge_id": chall_id,
        "score": row["points"]
    }).execute()

    st.session_state[f"{chall_id}_solved"] = True
    success_count += 1

st.success("제출 완료!")
st.write(f"정답 제출: {success_count}개")
st.write(f"오답 또는 미일치 제출: {wrong_count}개")
st.write(f"🏅 현재 총점: **{total_score(user.id)}**")
