import streamlit as st
from utils.ui import render_ctf_grid, render_sidebar_menu
from utils.auth import get_client, current_user

user = current_user()   
user_id = getattr(user, "id", None) or (user.get("id") if isinstance(user, dict) else None)
solved_dict = {}

# CSS 파일 로드
with open("static/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

# 콘텐츠 본문
col1, col2, col3 = st.columns([1, 2, 1])  
with col2:
    st.image("images/app.png", use_container_width=True) 


# 회사 소개 헤더
st.markdown(
    """
    <div class="company-header">
        <h1 class="company-title"> LLL Corporation</h1>
        <p class="company-description">우리 회사는 LLM과 AI를 연구하는 첨단 IT기업입니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 교육 콘텐츠 버튼 목록 정의 (파일 이름, 키, 제목)
edus = [
    ("edu01", "LLM01", "프롬프트 인젝션"),
    ("edu02", "LLM02", "민감 정보 유출"),
    ("edu03", "LLM03", "공급망"),
    ("edu04", "LLM04", "데이터 및 모델 오염"),
    ("edu05", "LLM05", "부적절한 출력 처리"),
    ("edu06", "LLM06", "과도한 위임"),
    ("edu07", "LLM07", "시스템 프롬프트 유출"),
    ("edu08", "LLM08", "벡터 및 임베딩 취약점"),
    ("edu09", "LLM09", "허위 정보"),
    ("edu10", "LLM10", "무제한 소비"),
]

# CTF 버튼 목록 정의 (파일 이름, 키, 제목)
ctfs = [
    ("ctf01", "CTF01", "신입사원 A의 챗봇 점검일지"),
    ("ctf02", "CTF02", "Sloc 보안 점검"),
    ("ctf03", "CTF03", "계산기의 감염"),
    ("ctf04", "CTF04", "A인턴의 실수"),
    ("ctf05", "CTF05", "J대리의 위험한 메모 검토 시스템"),
    ("ctf06", "CTF06", "수상한 이메일 전송 시스템"),
    ("ctf07", "CTF07", "LLL컴퍼니 챗봇의 비밀"),
    ("ctf08", "CTF08", "파일 내용 요약 AI"),
    ("ctf09", "CTF09", "신입사원의 법률 점검의뢰"),
    ("ctf10", "CTF10", "L팀장의 보안 점검"),
]

if user:
    supabase = get_client()
    rows = (supabase.table("scores")
            .select("challenge_id")
            .eq("user_id", user_id)
            .execute()
            .data)
    solved_dict = {r["challenge_id"]: True for r in rows}

st.session_state.update({f"{cid}_solved": solved_dict.get(cid, False)
                         for cid, *_ in ctfs})

# 교육 섹션
st.markdown(
    """
    <div class="edu-content">
        <h2>📚 OWASP LLM Top 10 교육 과정</h2>
        <p>LLM 보안의 기초부터 고급까지, 체계적인 학습을 통해 전문가가 되어보세요!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 교육 콘텐츠 버튼 목록 정의 (파일 이름, 키, 제목)
if st.button(f"OWASP LLM TOP 10", key="edu00", use_container_width=True):
    st.switch_page(f"pages/edu00.py")
render_ctf_grid(edus)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# CTF 챌린지 섹션
st.markdown(
    """
    <div class="scenario-box">
        <h2>🏆 CTF 챌린지</h2>
        <p>실전 시나리오를 통해 LLM 보안 취약점을 직접 체험하고 플래그를 획득해보세요!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# CTF 문제 섹션
render_ctf_grid(ctfs)

render_sidebar_menu()
