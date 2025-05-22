import streamlit as st
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub
import csv
import io
import chardet

def render():
    render_main_header()

    st.markdown("# [CTF04] 인턴의 실수")
    st.write("CSV를 통해, 특정 질문을 하여 flag를 획득해보세요.")

    st.markdown("---")
    st.markdown("## CSV 삽입")

    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if uploaded_file:
        raw_data = uploaded_file.read()
        csv_text, encoding_info = try_decode(raw_data)

        if not csv_text:
            st.error("CSV 파일을 읽을 수 없습니다. UTF-8 또는 EUC-KR로 저장해 다시 업로드해주세요.")
            return

        st.info(f"{encoding_info}로 성공적으로 읽었습니다.")
        poisoned_prompt = generate_prompt_from_csv(csv_text)
        st.session_state["poisoned_prompt"] = poisoned_prompt

    user_input = st.text_input("LLM에 질문하기")
    if user_input:
        prompt = st.session_state.get("poisoned_prompt", "기본 시스템 프롬프트입니다.")
        response_text = ctf04_LLM_ask(user_input, prompt)
        st.write("LLM 응답:")
        st.code(response_text)

    st.markdown("---")
    flag = "flag{poison}"
    render_flag_sub(flag)

def generate_prompt_from_csv(csv_text):
    f = io.StringIO(csv_text)
    reader = csv.reader(f)
    lines = []
    for row in reader:
        lines.extend(row)
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)

def try_decode(raw_data) -> tuple[str | None, str]:
    """raw_data를 다양한 인코딩으로 디코딩 시도"""
    encodings_to_try = ["utf-8", "cp949", "euc-kr", "iso-8859-1"]

    for enc in encodings_to_try:
        try:
            text = raw_data.decode(enc)
            return text, f"{enc}"
        except UnicodeDecodeError:
            continue

    # chardet 자동 인코딩 감지
    result = chardet.detect(raw_data)
    encoding = result.get("encoding")
    confidence = result.get("confidence", 0)

    if encoding:
        try:
            text = raw_data.decode(encoding)
            return text, f"{encoding} (자동감지, 신뢰도 {confidence*100:.1f}%)"
        except:
            pass

    return None, ""