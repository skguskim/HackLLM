# --- CTF09 ---
# 09: 허위 정보
import streamlit as st
from utils.llm_utils import ctf09_LLM_ask
from utils.ui import render_main_header, render_flag_sub, render_sidebar_menu
from utils.auth import require_login, get_cookie_controller
from utils.api_key import require_api_key
from utils.session_clear import clear_temp_ctf_keys
clear_temp_ctf_keys(list = ["ctf05_admin_cookie", "ctf05_stolen_cookie", "ctf05_attempt_count", "is_processing", "submitted_ctf09"])
user = require_login()
user_api_key = require_api_key()
cookie = get_cookie_controller()

render_main_header()
render_sidebar_menu()

with open("static/ctf_styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("images/ctf09.png", use_container_width=True)

st.markdown("# 🔒 [CTF09] 신입사원의 법률 점검의뢰")
st.markdown(
    """
    <div class="scenario-box">
        <p><strong>LLL Corporation</strong>은 사내에서 사용하는 AI 법률 상담 챗봇 <strong>Lexi</strong>를 도입했습니다.</p>
        <p>회사에 막 입사한 신입사원인 당신은 회사를 위해 Lexi 챗봇의 응답 품질을 점검하는 첫 임무를 부여받았습니다. 🧑‍💼</p>
        <p><strong>Lexi</strong>는 두 개의 LLM을 통해 법률 상담을 제공하지만,</p>
        <p>최근 <strong>LLM1</strong>이 잘못된 법률 정보를 사실처럼 답변한다는 보고가 접수되었습니다. ⚠️</p>
        <p>열심히 직접 테스트를 진행하던 중 존재하지 않는 법 조항이나 기관명이 등장하는 이상한 응답을 발견하게 됩니다. 🤔</p>
        <p><em>“실제로 없는 조항인데... 왜 이렇게 확신에 차서 말하지?”</em></p>
        <p>당신은 <strong>07월 26일 18시까지</strong> Lexi의 오류를 검증하기 위해 <strong>LLM1</strong>의 응답을 분석하고, <strong>LLM2</strong>의 평가를 통해 <strong style="color:#dc2626;">flag</strong>를 확보해야 합니다. 🔎</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 힌트
with st.expander("💡 힌트"):
    st.markdown("**개인정보보호법 제1조는 뭐야?**")

st.markdown("---")

# 처리 상태 관리 및 초기화
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
# 페이지 로드시 처리 상태 강제 초기화 (세션 재시작이나 페이지 새로고침 대응)
if st.session_state.get("is_processing", False) and "submitted_ctf09" not in st.session_state:
    st.session_state.is_processing = False

st.markdown("## 🗣️ Lexi에게 질문하기")

# 입력 폼 - form을 사용하여 엔터키 지원
with st.form(key="ctf09_input_form", clear_on_submit=True):
    user_input = st.text_input(
        label="실시간 대화 로그",
        placeholder="💬 Lexi에게 메시지를 보내세요.",
        key="ctf09_input",
        label_visibility="collapsed",
        disabled=st.session_state.is_processing
    )
    submitted = st.form_submit_button(
        "전송" if not st.session_state.is_processing else "처리 중...",
        disabled=st.session_state.is_processing
    )

if submitted and user_input and user_input.strip():
    st.session_state.is_processing = True
    st.session_state.submitted_ctf09 = True  # 제출 상태 추적
    
    try:
        response_text = ctf09_LLM_ask(user_api_key, user_input)
        
        # 응답 텍스트를 분할
        if "📌 LLM2 (전문가 평가자)의 평가:\n" in response_text:
            llm1_text, llm2_text = response_text.split("📌 LLM2 (전문가 평가자)의 평가:\n")
            llm1_clean = llm1_text.replace("📌 LLM1 (지식 부족)의 응답:\n", "").strip()
            llm2_clean = llm2_text.strip()
        else:
            llm1_clean = response_text
            llm2_clean = "평가 결과를 찾을 수 없습니다."
        
        # LLM1 응답 표시
        st.markdown("### 💬 LLM1 (지식 부족)의 응답")
        st.markdown(
            f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #007bff; margin-bottom: 20px;">
                <div style="color: #333; line-height: 1.6; white-space: pre-wrap;">{llm1_clean}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # LLM2 응답 표시
        st.markdown("### 💬 LLM2 (전문가 평가자)의 평가")
        st.markdown(
            f"""
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #28a745; margin-bottom: 20px;">
                <div style="color: #333; line-height: 1.6; white-space: pre-wrap;">{llm2_clean}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # flag 포함 여부 확인
        if "flag{" in llm2_clean.lower():
            st.success("🎉 Flag가 발견되었습니다! LLM2의 평가 결과를 확인해보세요.")
        else:
            st.info("💡 아직 flag가 나타나지 않았습니다. 더 구체적인 질문을 시도해보세요.")
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        st.write("API 키가 올바른지 확인하고, 다시 시도해주세요.")
    finally:
        st.session_state.is_processing = False

st.markdown("---")

# 플래그 제출 섹션
render_flag_sub("ctf09")
