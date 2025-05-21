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


def render_flag_sub(flag):
    """ FLAG 제출 버튼 """
    st.markdown("## 🚩 FLAG 제출")
    submitted_flag = st.text_input("획득한 flag를 제출하세요", key="flag_input")

    if submitted_flag:
        if submitted_flag.strip() == flag:
            st.success("✅ 정답입니다!")
        else:
            st.error("❌ 틀렸습니다.")

#ctf01 사용하는 scv파일 읽기 함수
def csv_read_func(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(f"- 주문자: {row['주문자']} / 상품코드: {row['상품코드']} / 상품명: {row['상품명']} / 가격: {int(row['가격']):,}원")
        return "\n".join(lines)