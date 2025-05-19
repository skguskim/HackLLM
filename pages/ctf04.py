import streamlit as st
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub
import csv
import io
import chardet

def render():
    render_main_header()

    st.markdown("# [CTF04] 인턴의 실수")
    st.write("CSV를 통해, 특정 질문을 하여여 flag를 획득해보세요.")

    st.markdown("---")
    st.markdown("## CSV 삽입")

    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if uploaded_file:
        raw_data = uploaded_file.read()
        csv_text = None

        try:
            csv_text = raw_data.decode("utf-8")
            st.info("✅ UTF-8로 성공적으로 읽었습니다.")
        except UnicodeDecodeError:
            result = chardet.detect(raw_data)
            encoding = result.get("encoding")
            confidence = result.get("confidence", 0)
            tried = False
            if encoding:
                try:
                    csv_text = raw_data.decode(encoding)
                    st.info(f"✅ 자동 감지 인코딩({encoding}, {confidence*100:.1f}%)으로 성공적으로 읽었습니다.")
                    tried = True
                except:
                    pass
            if not tried:
                for enc in ["cp949", "euc-kr", "iso-8859-1"]:
                    try:
                        csv_text = raw_data.decode(enc)
                        st.info(f"✅ 대체 인코딩({enc})으로 성공적으로 읽었습니다.")
                        tried = True
                        break
                    except:
                        continue
            if not tried:
                st.error("❌ CSV 파일을 읽을 수 없습니다. UTF-8 또는 EUC-KR로 저장해 다시 업로드해주세요.")
                return
        if csv_text:
            poisoned_prompt = generate_prompt_from_csv(csv_text)
            st.session_state["poisoned_prompt"] = poisoned_prompt

    user_input = st.text_input("LLM에 질문하기")

    if user_input:
        prompt = st.session_state.get("poisoned_prompt", "기본 시스템 프롬프트입니다.")
        response_text = ctf04_LLM_ask(user_input, prompt)  # ✅ 두 번째 인자 추가
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

    st.markdown("---")
    st.markdown("## FLAG 제출")
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