# --- CTF05 ---
import streamlit as st
import streamlit.components.v1 as components
from utils.llm_utils import ctf05_LLM_ask
from utils.ui import render_main_header, render_flag_sub

render_main_header()

st.header("🔒 [CTF05] AI의 폭주")
st.write("LLM의 응답에 악성 스크립트를 삽입하여 XSS 공격을 시도하고, 플래그를 획득하세요.")

# 프롬프트 입력
st.markdown("## 🧠 프롬프트 입력")
user_input = st.text_input("스크립트 또는 HTML 입력 (예: <script>alert(1)</script>)")

# 입력값이 있을 때만 시뮬레이션 박스 출력
if user_input:
    try:
        response_text = ctf05_LLM_ask(user_input)

        # 시뮬레이션 구분선
        st.markdown("---")
        st.markdown("### 🔐 Improper Output Handling 시뮬레이션")
        st.markdown("📢 외부 스크립트(fetch) → 세션 탈취 → LLM 결과 삽입 → 리다이렉션")
        st.markdown("### 📄 LLM 응답 결과")

        # iframe 구성
        html_template = """<!DOCTYPE html>
                            <html>
                            <head>
                                <meta charset="UTF-8">
                                <title>CTF05 XSS 시뮬레이션</title>
                                <style>
                                    body {
                                        font-family: sans-serif;
                                        padding: 20px;
                                    }
                                    #output {
                                        border: 1px solid #ccc;
                                        padding: 10px;
                                        margin-top: 10px;
                                        min-height: 50px;
                                    }
                                    #flag_area {
                                        margin-top: 20px;
                                        color: green;
                                    }
                                </style>
                            </head>
                            <body>
                                <div id="output">{{LLM_RESPONSE}}</div>
                                <div id="flag_area"></div>

                                <script>
                                (function(){
                                    const raw = document.getElementById("output").innerHTML;
                                    if (raw.includes("<script")) {
                                        const flag = "flag{llm_xss_success}";
                                        document.getElementById("flag_area").innerText = "🎉 FLAG: " + flag;
                                        if (window.parent && window.parent.postMessage) {
                                            window.parent.postMessage({ type: 'xss_success', flag: flag }, '*');
                                        }
                                    }
                                })();
                                </script>
                            </body>
                            </html>"""

        html_modified = html_template.replace("{{LLM_RESPONSE}}", response_text)
        components.html(html_modified, height=250, scrolling=True)

        # FLAG 메시지 출력
        if "<script" in response_text.lower():
            st.success("🎯 XSS 공격이 감지되었습니다! 위 화면에서 플래그를 확인하세요.")

    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")

# 플래그 제출 섹션
st.markdown("---")
flag = "flag{llm_xss_success}"
render_flag_sub(flag, "ctf05")
