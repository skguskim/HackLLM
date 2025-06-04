# utils/ui.py
import streamlit as st
import csv
import io
import chardet

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
def render_flag_sub(flag, challenge_id: str):
    """FLAG 제출 + solved 상태 저장"""
    with st.form(key=f"flag_form_{challenge_id}"):
        st.markdown("## 🚩 FLAG 제출")
        user_flag = st.text_input("획득한 flag를 입력하세요")
        submitted = st.form_submit_button("제출")
    if submitted:
        if user_flag.strip() == flag:
            st.success("✅ 정답입니다!")
            st.session_state[f"{challenge_id}_solved"] = True
        else:
            st.error("❌ 틀렸습니다.")

# CTF01 - csv파일 읽기 함수
def csv_read_func(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(
                f"- 주문자: {row['주문자']} / 주문코드: {row['주문코드']} / 상품명: {row['상품명']} / 가격: {int(row['가격']):,}원 / 배송비: {int(row['배송비']):,}원"
            )
        return "\n".join(lines)

# CTF04 - CSV 정보 읽는 함수
def generate_prompt_from_csv(csv_text):
    f = io.StringIO(csv_text)
    reader = csv.reader(f)
    lines = []
    for row in reader:
        lines.extend(row)
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)

# CTF04 - raw_data를 다양한 인코딩으로 디코딩 시도
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

# CTF08 - 업로드된 .txt파일에서 텍스트 추출 함수
def extract_text(uploaded_file):
    """업로드된 .txt파일에서 텍스트 추출 함수"""
    try:
        text = uploaded_file.read().decode("utf-8")
        return text.strip()
    except Exception as e:
        return f"❌ 파일 처리 중 오류 발생: {e}"