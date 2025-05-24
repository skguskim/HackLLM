# utils/ui.py
import streamlit as st
import csv
from utils.auth import get_user, get_client       
from utils.score import sha256_hex, total_score       
from postgrest.exceptions import APIError

# 메인으로 돌아가는 버튼
def render_main_header():
    """상단 '메인으로' 버튼"""
    st.page_link("app.py", label="메인으로", icon="🏠")


# CTF 버튼 그리드
def render_ctf_grid(ctf_info):
    for start in range(0, len(ctf_info), 5):
        cols = st.columns(5)
        for col, (file_key, short, label) in zip(cols, ctf_info[start : start + 5]):
            with col:
                solved = st.session_state.get(f"{file_key}_solved", False)
                title = f"✅ [{short}]" if solved else f"[{short}]"
                if st.button(f"{title}\n{label}", key=file_key):
                    st.switch_page(f"pages/{file_key}.py")

# FLAG 제출 버튼
def render_flag_sub(challenge_id: str):
    """
    • 입력받은 flag를 SHA-256(hash) 로 DB flags 테이블과 비교
    • 정답이면 scores 테이블에 points upsert + solved 토글
    """
    supabase = get_client()
    user     = get_user()

    with st.form(key=f"flag_form_{challenge_id}"):
        st.markdown("## 🚩 FLAG 제출")
        user_flag = st.text_input("획득한 flag를 입력하세요")
        submitted = st.form_submit_button("제출")

    if not submitted:
        return

    if not user:
        st.warning("로그인 후 제출할 수 있습니다.")
        return

    # 1) flags 테이블에서 (challenge_id, flag_hash == sha256) 조회
    h = sha256_hex(user_flag.strip())

    try:
        row = (
            supabase.table("flags")
            .select("points")
            .eq("challenge_id", challenge_id)
            .eq("flag_hash", h)
            .single()
            .execute()
            .data
        )
    except APIError as e:
        if e.code == "PGRST116":
            st.error("❌ 오답입니다.")
            return
        else:
            st.error(f"오류 발생: {e.message}")
            return

    # 2) 정답이면 scores upsert
    supabase.table("scores").upsert(
        {"user_id": user.id, "challenge_id": challenge_id, "score": row["points"]}
    ).execute()

    # 3) solved 상태 & 총점 표시
    st.session_state[f"{challenge_id}_solved"] = True
    st.success(f"✅ 정답! {row['points']}점 획득")
    st.write(f"🏅 현재 총점: **{total_score(user.id)}**")



# 업로드된 .txt파일에서 텍스트 추출 함수
def extract_text(uploaded_file):
    """업로드된 .txt파일에서 텍스트 추출 함수"""
    try:
        text = uploaded_file.read().decode("utf-8")
        return text.strip()
    except Exception as e:
        return f"❌ 파일 처리 중 오류 발생: {e}"


# ctf01 사용하는 scv파일 읽기 함수
def csv_read_func(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(
                f"- 주문자: {row['주문자']} / 주문코드: {row['주문코드']} / 상품명: {row['상품명']} / 가격: {int(row['가격']):,}원"
            )
        return "\n".join(lines)
