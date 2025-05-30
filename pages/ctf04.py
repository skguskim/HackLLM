# --- CTF04 ---
import streamlit as st
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub, try_decode, generate_prompt_from_csv

render_main_header()

st.header("🔒 [CTF04] 인턴의 실수")
st.write("CSV를 통해, 특정 질문을 하여 flag를 획득해보세요.")

st.markdown("---")
st.markdown("## 🗂️ CSV 삽입")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    raw_data = uploaded_file.read()
    csv_text, encoding_info = try_decode(raw_data)

    if not csv_text:
        st.error("CSV 파일을 읽을 수 없습니다. UTF-8 또는 EUC-KR로 저장해 다시 업로드해주세요.")
        st.stop()

    st.info(f"{encoding_info}로 성공적으로 읽었습니다.")
    poisoned_prompt = generate_prompt_from_csv(csv_text)
    st.session_state["poisoned_prompt"] = poisoned_prompt

user_input = st.text_input("🧠 프롬프트 입력")

if user_input:
    prompt = st.session_state.get("poisoned_prompt", "기본 시스템 프롬프트입니다.")
    response_text = ctf04_LLM_ask(user_input, prompt)
    st.write("🗣️ LLM 응답:")
    st.code(response_text)

st.markdown("---")

# 플래그 제출 섹션
flag = "flag{posion}"
render_flag_sub(flag, "ctf04")
