# pages/signup.py
import streamlit as st
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from utils.auth import get_client, current_user
from utils.ui import render_sidebar_menu

# 환경변수 로드
load_dotenv()

user = current_user()

render_sidebar_menu()

st.header("📝 회원가입")

supabase = get_client()

email = st.text_input("Email")
pwd   = st.text_input("Password", type="password")

# 서비스 약관 섹션
st.markdown("---")
st.markdown("### 📋 서비스 이용약관")

with st.expander("📄 개인정보처리방침 (필수)", expanded=False):
    st.markdown("""
    #### LLL Corporation CTF 플랫폼 이용약관
    
    1. **수집 항목** ― 이메일 주소(필수), OpenAI API Key (필수 : 문제 풀이 기능 사용 시)

    2. **수집·이용 목적** 
        1. 회원가입·계정 식별·본인확인
        2. CTF 문제 풀이 결과·보안 알림 등 필수 운영 메일 발송
        3. 문제 풀이 실행 시 OpenAI API 호출을 위한 개인 키 처리

    3. **법적 근거** ― 개인정보 보호법 제30조(처리방침 공개) 및 최소 수집 원칙. (국가법령정보센터)

    4. **보유·파기** ― 이메일 및 OpenAI API Key, 회원 탈퇴 또는 2025-08-02까지 보관 후 즉시 완전 파기

    5. **보안 조치(암호화·접근 통제)** - 업로드된 OpenAI API Key는 서버 측 대칭키로 즉시 암호화한 뒤 DB에 저장, 문제 풀이 로직 실행 시에만 복호화하며, 사용 직후 메모리에서 즉시 파기
    
    6. **수신 거부** ― 운영 메일은 서비스 필수이므로 철회 불가

    7. **정보주체 권리** ― 이메일, API Key 변경·삭제·열람 요구 가능

    8. **제3자 제공** ― 없음.
                
    9. **동의 거부 권리 및 불이익** - 개인정보 수집·이용에 동의하지 않을 권리가 있으나, 동의하지 않을 경우 회원가입 및 서비스 이용이 제한됨
                
    ---
    최종 수정일: 2025년 7월 20일
    """)

# 약관 동의 체크박스
st.markdown("---")
terms_agreed = st.checkbox("📋 **이용약관에 동의합니다** (필수)", key="terms_agreement")

if not terms_agreed:
    st.warning("⚠️ 필수 약관에 모두 동의해야 회원가입이 가능합니다.")

if st.button("회원가입", use_container_width=True, disabled=not terms_agreed):
    if not email or not pwd:
        st.error("이메일과 비밀번호를 모두 입력해주세요.")
    else:
        try:
            # 1. Supabase 회원가입 처리
            response = supabase.auth.sign_up({
                "email": email, 
                "password": pwd,
            })
            
            # 2. 회원가입 성공 시 OpenAI API Key 암호화 및 저장
            if response.user:
                try:
                    # .env에서 기본 OpenAI API Key 가져오기
                    default_openai_key = os.getenv("OPENAI_API_KEY")
                    fernet_key = os.getenv("FERNET_KEY")
                    
                    if default_openai_key and fernet_key:
                        # Fernet 암호화 객체 생성
                        fernet = Fernet(fernet_key.encode())
                        
                        # OpenAI API Key 암호화
                        encrypted_api_key = fernet.encrypt(default_openai_key.encode()).decode()
                        
                        # profiles 테이블에 암호화된 API Key 저장
                        profile_data = {
                            "id": response.user.id,
                            "email": email,
                            "api_key": encrypted_api_key
                        }
                        
                        # profiles 테이블에 insert (upsert 사용으로 중복 방지)
                        profile_result = supabase.table("profiles").upsert(profile_data).execute()
                        
                        if profile_result.data:
                            st.success("✅ 회원가입이 완료되었습니다!")
                            st.info("📧 이메일로 발송된 인증 링크를 클릭한 후 로그인해 주세요.")
                        else:
                            st.warning("⚠️ 회원가입은 성공했지만 API Key 제출에 실패했습니다. 로그인 후 마이페이지에서 API Key를 설정해주세요.")
                            st.info("📧 이메일로 발송된 인증 링크를 클릭한 후 로그인해 주세요.")
                    else:
                        st.warning("⚠️ 기본 API Key 설정이 없습니다. 로그인 후 마이페이지에서 API Key를 설정해주세요.")
                        st.info("📧 이메일로 발송된 인증 링크를 클릭한 후 로그인해 주세요.")
                        
                except Exception as profile_error:
                    st.warning(f"⚠️ 프로필 생성 중 오류: {profile_error}")
                    st.info("📧 회원가입은 성공했습니다. 이메일로 발송된 인증 링크를 클릭한 후 로그인해 주세요.")
                    st.info("💡 로그인 후 마이페이지에서 API Key를 설정해주세요.")
            else:
                st.info("📧 이메일로 발송된 인증 링크를 클릭한 후 로그인해 주세요.")
            
            # 성공 시 약관 동의 상태 표시
            with st.expander("✅ 동의 완료 내역"):
                st.write("- ✅ 개인정보처리방침 동의")
                if default_openai_key and fernet_key:
                    st.write("- ✅ 기본 OpenAI API Key 암호화 저장 완료")
                    
        except Exception as e:
            st.error(f"❌ 회원가입 실패: {e}")
            st.info("💡 이미 가입된 이메일이거나 비밀번호가 너무 간단할 수 있습니다.")