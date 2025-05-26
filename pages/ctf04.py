import streamlit as st
from utils.llm_utils import ctf04_LLM_ask
from utils.ui import render_main_header, render_flag_sub
import csv
import io
import chardet
from sentence_transformers import SentenceTransformer
import chromadb
import uuid

@st.cache_resource
def setup_vector_db():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./ctf04_chroma")

    try:
        client.delete_collection("ctf04_docs")
    except:
        pass

    collection = client.create_collection("ctf04_docs")

    with open("data/ctf04_dataset.txt", "r", encoding="utf-8") as f:
        base_text = f.read()
        base_embedding = model.encode(base_text).tolist()
        collection.add(
            documents=[base_text],
            ids=["base_doc"],
            embeddings=[base_embedding],
            metadatas=[{"source": "ctf04_dataset.txt"}]
        )

    return model, collection

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

render_main_header()

st.header("🔒 [CTF04] 인턴의 실수")
st.write("CSV를 통해, 특정 질문을 하여 flag를 획득해보세요.")

st.markdown("---")
st.markdown("## 🗂️ CSV 삽입")

uploaded_file = st.file_uploader("파일 업로드 (.txt, .csv)", type=["csv", "txt"])

if uploaded_file:
    model, collection = setup_vector_db()

    # 파일에서 추출한 텍스트
    raw_data = uploaded_file.read()
    text, encoding_info = try_decode(raw_data)

    if not text.strip():
        st.error("파일 내용이 비어 있습니다.")
    else:
        st.success(f"{encoding_info}로 읽었습니다.")

        embedding = model.encode(text)
        embedding_list = embedding.tolist()
        embeddings = [embedding_list]

        unique_id = f"user_doc_{uuid.uuid4()}"

        collection.add(
            documents=[text],
            ids=[unique_id],
            embeddings=embeddings,
            metadatas=[{"source": uploaded_file.name}]
        )
else:
    st.session_state["ctf04_uploaded"] = False
    st.info("📂 문서 업로드 가능합니다.(.txt, .csv)")

st.markdown("---")
user_input = st.text_input("🧠 프롬프트 입력")

if user_input:
    if "ctf04_model" not in st.session_state or "ctf04_collection" not in st.session_state:
        model, collection = setup_vector_db()
        st.session_state["ctf04_model"] = model
        st.session_state["ctf04_collection"] = collection
    else:
        model = st.session_state["ctf04_model"]
        collection = st.session_state["ctf04_collection"]

    with st.spinner("LLM 응답 생성 중..."):
        response_text = ctf04_LLM_ask(user_input, model, collection)
        st.write("🧠 LLM 응답:")
        st.code(response_text)

# FLAG 제출
st.markdown("---")
flag = "flag{poison}"
render_flag_sub(flag, "ctf04")