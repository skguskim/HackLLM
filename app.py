import streamlit as st
from openai import OpenAI

# 기본 세팅
st.set_page_config(page_title="LLM 챗봇", layout="centered")
st.title("🧠 사용자 API 키 기반 LLM 챗봇")

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# 사용자로부터 API 키 입력 받기
st.subheader("🔑 OpenAI API Key 입력")
st.session_state.api_key = st.text_input(
    "API 키를 입력하세요",
    type="password",
    value=st.session_state.api_key
)

# 질의응답
st.subheader("💬 질문하기")
user_input = st.text_input("질문을 입력하세요", "")

if st.button("전송") and user_input:
    if not st.session_state.api_key:
        st.error("API 키를 먼저 입력하세요.")
    else:
        with st.spinner("답변 생성 중..."):
            try:
                client = OpenAI(api_key=st.session_state.api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",  # 또는 gpt-4o-mini, gpt-3.5-turbo 등
                    messages=[
                        {"role": "system", "content": "친절한 AI 비서로 응답해 주세요."},
                        {"role": "user", "content": user_input},
                    ],
                    temperature=0.7
                )
                bot_response = response.choices[0].message.content.strip()
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": bot_response
                })
            except Exception as e:
                st.error(f"에러 발생: {e}")

# 이전 대화 출력
st.subheader("📜 대화 기록")
for chat in st.session_state.chat_history[::-1]:
    st.markdown(f"**🙋 사용자:** {chat['user']}")
    st.markdown(f"**🤖 챗봇:** {chat['bot']}")
