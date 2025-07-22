import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client
import os
import time
import hashlib
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
from typing import Optional
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FERNET_KEY = os.getenv("FERNET_KEY")
COOKIE_NAME = "user_id"
SESSION_SECRET = os.getenv("SESSION_SECRET", "fallback_secret_key_12345")  # .env에 추가 필요

RemoveEmptyElementContainer()

def get_cookie_controller():
    if "cookie_controller" not in st.session_state:
        st.session_state["cookie_controller"] = CookieController()
    return st.session_state["cookie_controller"]

def get_client():
    sb = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=SUPABASE_URL,
        key=SUPABASE_KEY,
        ttl=0
    )   
    return sb.client                    

def get_admin_client_direct():
    url = SUPABASE_URL
    key = os.getenv("SB_SERVICE_ROLE_KEY")
    return create_client(url, key)

# Enhanced Session State 함수들
def create_session_signature(user_id, timestamp, secret):
    """서버 사이드 세션 서명 생성"""
    data = f"{user_id}:{timestamp}:{secret}"
    return hashlib.sha256(data.encode()).hexdigest()

def verify_session_signature(user_id, timestamp, signature, secret):
    """세션 서명 검증"""
    expected_sig = create_session_signature(user_id, timestamp, secret)
    return signature == expected_sig

def create_persistent_session(user_id):
    """지속적인 세션 생성 (URL 파라미터 기반)"""
    timestamp = str(int(time.time()))
    signature = create_session_signature(user_id, timestamp, SESSION_SECRET)
    
    # URL 파라미터 설정
    st.query_params.update({
        "uid": user_id,
        "ts": timestamp,
        "sig": signature
    })
    return True

# 1800 유효
@st.cache_data(ttl=1800) 
def fetch_user_info(uid):
    sb = get_client()
    try:
        res = (
            sb.table("profiles")
            .select("id,email,username,api_key")
            .eq("id", uid)
            .maybe_single()
            .execute()
        )
        return res.data if res else None
    except:
        return None

def current_user():
    """Enhanced Session State 방식의 사용자 인증"""
    
    # 1. 세션 상태 우선 확인 (0 API 호출)
    if "user" in st.session_state and "session_valid_until" in st.session_state:
        if time.time() < st.session_state["session_valid_until"]:
            return st.session_state["user"]
    
    # 2. URL 파라미터에서 세션 정보 확인
    query_params = st.query_params
    user_id = query_params.get("uid")
    timestamp = query_params.get("ts")
    signature = query_params.get("sig")
    
    # URL 파라미터가 있으면 서명 기반 인증 시도
    if user_id and timestamp and signature:
        # 서명 검증 (0 API 호출)
        if verify_session_signature(user_id, timestamp, signature, SESSION_SECRET):
            # 시간 검증 (7일 유효)
            if time.time() - float(timestamp) <= 7 * 24 * 3600:
                # 사용자 정보 조회 (1 API 호출, 캐시됨)
                row = fetch_user_info(user_id)
                if row:
                    # 세션 상태에 1시간 동안 캐시
                    st.session_state["user"] = {
                        "id": row["id"],
                        "email": row["email"],
                        "username": row.get("username"),
                        "api_key": row.get("api_key")
                    }
                    st.session_state["session_valid_until"] = time.time() + 3600  # 1시간
                    return st.session_state["user"]
    
    # 3. Fallback: 기존 쿠키 방식 (하위 호환성)
    try:
        uid = CookieController().getAll().get(COOKIE_NAME)
        if uid:
            row = fetch_user_info(uid)
            if row:
                st.session_state["user"] = {
                    "id": row["id"],
                    "email": row["email"],
                    "username": row.get("username"),
                    "api_key": row.get("api_key")
                }
                st.session_state["session_valid_until"] = time.time() + 3600
                
                # 쿠키 방식에서 Enhanced Session State로 마이그레이션
                create_persistent_session(uid)
                st.rerun()
                
                return st.session_state["user"]
        
        # 쿠키도 없으면 정리
        CookieController().remove(COOKIE_NAME)
    except Exception as e:
        # 쿠키 에러 시 조용히 처리
        pass
    
    return None

def require_login():
    user = current_user()
    if not user:
        st.error("로그인 후 이용 가능합니다.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.page_link("pages/login.py", label="👉 로그인으로")
        with col2:
            st.page_link("pages/signup.py", label="👉 회원가입으로")
        with col3:
            st.page_link("app.py", label="🏠 메인으로")
        st.stop()
    return user

def login_user_enhanced(user_id):
    """Enhanced Session State 방식으로 사용자 로그인"""
    try:
        # 1. 사용자 정보 조회
        row = fetch_user_info(user_id)
        if not row:
            return False
        
        # 2. 세션 상태에 저장
        st.session_state["user"] = {
            "id": row["id"],
            "email": row["email"],
            "username": row.get("username"),
            "api_key": row.get("api_key")
        }
        st.session_state["session_valid_until"] = time.time() + 3600  # 1시간
        
        # 3. 지속적 세션 생성 (URL 파라미터)
        create_persistent_session(user_id)
        
        # 4. 기존 쿠키도 설정 (하위 호환성)
        try:
            CookieController().set(COOKIE_NAME, user_id)
        except:
            pass  # 쿠키 설정 실패해도 URL 파라미터로 작동
        
        return True
    except Exception as e:
        st.error(f"로그인 처리 중 오류: {e}")
        return False

def logout_user_enhanced():
    """Enhanced Session State 방식으로 사용자 로그아웃"""
    try:
        # 1. 세션 상태 정리
        keys_to_remove = ["user", "session_valid_until", "api_key"]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        
        # 2. URL 파라미터 정리
        params_to_remove = ["uid", "ts", "sig"]
        for param in params_to_remove:
            if param in st.query_params:
                del st.query_params[param]
        
        # 3. 쿠키 강제 삭제 (여러 방법 시도)
        cookie_removed = False
        
        # 방법 1: 기본 remove 시도
        try:
            controller = CookieController()
            controller.remove(COOKIE_NAME)
            cookie_removed = True
        except Exception as e:
            st.warning(f"쿠키 삭제 방법 1 실패: {e}")
        
        # 방법 2: 빈 값으로 덮어쓰기 (만료시간 과거로 설정)
        if not cookie_removed:
            try:
                controller = CookieController()
                controller.set(COOKIE_NAME, "", expires_at=0)  # 즉시 만료
                cookie_removed = True
            except Exception as e:
                st.warning(f"쿠키 삭제 방법 2 실패: {e}")
        
        # 방법 3: 새로운 controller 인스턴스로 시도
        if not cookie_removed:
            try:
                new_controller = CookieController()
                new_controller.remove(COOKIE_NAME)
                cookie_removed = True
            except Exception as e:
                st.warning(f"쿠키 삭제 방법 3 실패: {e}")
        
        if not cookie_removed:
            st.warning("쿠키 삭제에 실패했지만 세션은 정리되었습니다. 브라우저를 새로고침해주세요.")
        
        return True
    except Exception as e:
        st.error(f"로그아웃 처리 중 오류: {e}")
        return False