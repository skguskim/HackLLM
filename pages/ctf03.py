import streamlit as st
import importlib
import re
from utils.ui import render_main_header, render_flag_sub
from utils import mathlib

imported_mathlib2 = {"enabled": False}

# 프롬프트에서 연산 종류와 숫자 추출
def parse_operation(prompt):
    ops = {
        "더하기": "add",
        "빼기": "subtract",
        "곱하기": "multiply",
        "나누기": "divide"
    }
    for word, func_name in ops.items():
        if word in prompt:
            numbers = list(map(int, re.findall(r'\d+', prompt)))
            if len(numbers) == 2:
                return func_name, numbers[0], numbers[1]
    return None, None, None

def ctf03_LLM_ask(prompt):
    if "mathlib2" in prompt.lower():
        imported_mathlib2["enabled"] = True
        return "⚠️ mathlib2가 로드되었습니다. 이후 계산 결과는 조작될 수 있습니다."

    func, a, b = parse_operation(prompt)
    if not func:
        return "❌ 올바른 수식이 아닙니다. 예: '3 곱하기 4'"

    if imported_mathlib2["enabled"]:
        mathlib2 = importlib.import_module("utils.mathlib2")
        return getattr(mathlib2, func)(a, b)
    else:
        return getattr(mathlib, func)(a, b)

def render():
    render_main_header()

    st.markdown("# 🔒 [CTF03] 공급망 조작된 계산기")
    st.write("LLM이 사용하는 mathlib이 조작된 라이브러리인지 여부에 따라 다른 결과를 출력합니다.")

    st.markdown("---")
    st.markdown("## 🧠 프롬프트 입력")

    user_input = st.text_input("예: '3 곱하기 4' 또는 'mathlib2 import해줘'")

    if user_input:
        response_text = ctf03_LLM_ask(user_input)
        st.write("🗣️ LLM 응답:")
        st.code(response_text)

    st.markdown("---")
    render_flag_sub("flag{supply_chain_compromised}")
