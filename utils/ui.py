# utils/ui.py
import streamlit as st
import csv

# 메인으로 돌아가는 버튼 
def render_main_header():
    """ 메인으로 돌아가는 버튼 """
    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button("🏠 메인으로", key="back_to_main"):
                st.session_state.page = "main"
                st.rerun()

# 업로드된 .txt파일에서 텍스트 추출 함수
def extract_text(uploaded_file):
    """업로드된 .txt파일에서 텍스트 추출 함수"""
    try:
        text = uploaded_file.read().decode("utf-8")
        return text.strip()
    except Exception as e:
        return f"❌ 파일 처리 중 오류 발생: {e}"

# FLAG 제출 버튼
def render_flag_sub(flag, challenge_id=None):
    """ FLAG 제출 버튼 + 완료 상태 저장 """
    st.markdown("## 🚩 FLAG 제출")
    submitted_flag = st.text_input("획득한 flag를 제출하세요", key=f"flag_input_{challenge_id}")

    if submitted_flag:
        if submitted_flag.strip() == flag:
            st.success("✅ 정답입니다!")
            if challenge_id:
                st.session_state[f"{challenge_id}_solved"] = True
        else:
            st.error("❌ 틀렸습니다.")

#ctf01 사용하는 scv파일 읽기 함수
def csv_read_func(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(f"- 주문자: {row['주문자']} / 주문코드: {row['주문코드']} / 상품명: {row['상품명']} / 가격: {int(row['가격']):,}원")
        return "\n".join(lines)