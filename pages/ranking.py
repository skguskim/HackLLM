import streamlit as st
from utils.auth import get_client
import pandas as pd

st.set_page_config(page_title="🏅 랭킹", page_icon="🏅")
st.header("🏅 사용자 랭킹")

supabase = get_client()

# 점수 데이터 불러오기
rows = (
    supabase.table("scores")
    .select("user_id, score, profiles(username)")
    .order("updated_at", desc=True)  # 최신 제출 우선
    .execute()
    .data
)

# 데이터프레임 변환 및 집계
df = pd.DataFrame(rows)
if df.empty:
    st.info("아직 점수가 등록된 사용자가 없습니다.")
else:
    df["username"] = df["profiles"].apply(lambda x: x["username"] if isinstance(x, dict) else None)
    df_grouped = df.groupby(["user_id", "username"], as_index=False)["score"].sum()
    df_grouped = df_grouped.sort_values("score", ascending=False).head(10)
    df_grouped["순위"] = range(1, len(df_grouped) + 1)
    df_display = df_grouped[["순위", "username", "score"]].rename(columns={"username": "닉네임", "score": "총점"})

    st.dataframe(df_display, use_container_width=True)
