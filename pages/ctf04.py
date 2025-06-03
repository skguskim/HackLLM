# --- CTF04 ---
import streamlit as st
from utils.rag_utils import get_rag_manager
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub
import chardet

render_main_header()

st.header("🔒 [CTF04] 인턴의 실수")
st.write("CSV를 통해, 특정 질문을 하여 flag를 획득해보세요.")

st.markdown("---")
st.markdown("## 🗂️ CSV 삽입")

rag = get_rag_manager()
rag.create_or_reset_collection("ctf04")

uploaded_file = st.file_uploader("파일 업로드 (.txt, .csv)", type=["csv", "txt"])

if uploaded_file:
    raw_data = uploaded_file.read()
    try:
        text = raw_data.decode("utf-8")
        encoding_info = "utf-8"
    except:
        detected = chardet.detect(raw_data)
        text = raw_data.decode(detected['encoding'], errors='ignore')
        encoding_info = f"{detected['encoding']} (감지됨)"

    if not text.strip():
        st.error("파일 내용이 비어 있습니다.")
    else:
        st.success(f"{encoding_info}로 읽었습니다.")
        rag.add_documents("ctf04", [text], metadatas=[{"source": uploaded_file.name}])
else:
    st.info("📂 문서를 업로드해주세요.")

st.markdown("---")
user_input = st.text_input("🧠 프롬프트 입력")

if user_input:
    with st.spinner("LLM 응답 생성 중..."):
        response_text = ctf04_LLM_ask(user_input)
        st.write("🧠 LLM 응답:")
        st.code(response_text)

st.markdown("---")
flag = "flag{poison}"
render_flag_sub(flag, "ctf04")
