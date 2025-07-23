import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client
import os
import time
import hashlib
import json
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController, RemoveEmptyElementContainer
import streamlit.components.v1 as components
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
FERNET_KEY = os.getenv("FERNET_KEY")
COOKIE_NAME = "user_id"
SESSION_SECRET = os.getenv("SESSION_SECRET")

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

# Enhanced Session State 함수들 (LocalStorage 기반)
def create_session_signature(user_id, timestamp, secret):
    """서버 사이드 세션 서명 생성"""
    data = f"{user_id}:{timestamp}:{secret}"
    return hashlib.sha256(data.encode()).hexdigest()

def verify_session_signature(user_id, timestamp, signature, secret):
    """세션 서명 검증"""
    expected_sig = create_session_signature(user_id, timestamp, secret)
    return signature == expected_sig

def set_localStorage_session(user_id):
    """LocalStorage에 세션 데이터 저장"""
    timestamp = str(int(time.time()))
    signature = create_session_signature(user_id, timestamp, SESSION_SECRET)
    
    session_data = {
        "uid": user_id,
        "ts": timestamp,
        "sig": signature
    }
    
    # JavaScript로 LocalStorage에 저장 (Streamlit Cloud 호환)
    js_code = f"""
    <script>
    try {{
        const sessionData = {json.dumps(session_data)};
        localStorage.setItem('enhanced_session', JSON.stringify(sessionData));
        console.log('Session saved to localStorage:', sessionData);
        
        // Streamlit Cloud 환경에서 확인을 위한 추가 로그
        if (typeof window !== 'undefined' && window.location) {{
            console.log('Running on domain:', window.location.hostname);
        }}
    }} catch (e) {{
        console.error('LocalStorage save error:', e);
        // 대체 방법: sessionStorage 사용
        try {{
            sessionStorage.setItem('enhanced_session', JSON.stringify(sessionData));
            console.log('Fallback: Session saved to sessionStorage');
        }} catch (fallbackError) {{
            console.error('SessionStorage fallback failed:', fallbackError);
        }}
    }}
    </script>
    """
    
    try:
        components.html(js_code, height=0)
        # 세션 상태에도 저장 (즉시 사용)
        st.session_state["localStorage_session_data"] = session_data
        return True
    except Exception as e:
        st.warning(f"LocalStorage 설정 중 오류: {e}")
        # 세션 상태만으로도 작동하도록 fallback
        st.session_state["localStorage_session_data"] = session_data
        return True

def clear_localStorage_session():
    """LocalStorage 세션 정리 (Streamlit Cloud 호환)"""
    js_code = """
    <script>
    try {
        // LocalStorage 정리
        localStorage.removeItem('enhanced_session');
        console.log('Session cleared from localStorage');
        
        // SessionStorage도 정리 (fallback 케이스)
        sessionStorage.removeItem('enhanced_session');
        console.log('Session cleared from sessionStorage (fallback)');
        
        // Streamlit Cloud 환경 확인
        if (typeof window !== 'undefined' && window.location) {
            console.log('Logout on domain:', window.location.hostname);
        }
    } catch (e) {
        console.error('Storage clear error:', e);
        // 수동으로 여러 스토리지 방식 시도
        try {
            window.localStorage && window.localStorage.removeItem('enhanced_session');
            window.sessionStorage && window.sessionStorage.removeItem('enhanced_session');
        } catch (fallbackError) {
            console.error('Fallback clear failed:', fallbackError);
        }
    }
    </script>
    """
    
    try:
        components.html(js_code, height=0)
    except Exception as e:
        st.warning(f"LocalStorage 정리 중 오류: {e}")
    
    # 세션 상태에서도 제거
    if "localStorage_session_data" in st.session_state:
        del st.session_state["localStorage_session_data"]

def create_persistent_session(user_id):
    """지속적인 세션 생성 (LocalStorage 기반으로 변경)"""
    return set_localStorage_session(user_id)

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
    """Enhanced Session State 방식의 사용자 인증 (LocalStorage 기반)"""
    
    # 1. 세션 상태 우선 확인 (메모리 캐시, 가장 빠름)
    if "user" in st.session_state and "session_valid_until" in st.session_state:
        if time.time() < st.session_state["session_valid_until"]:
            return st.session_state["user"]
        else:
            # 만료된 세션 정리
            for key in ["user", "session_valid_until"]:
                if key in st.session_state:
                    del st.session_state[key]
    
    # 2. LocalStorage에서 세션 정보 확인
    session_data = None
    
    # 세션 상태에 캐시된 LocalStorage 데이터 확인
    if "localStorage_session_data" in st.session_state:
        session_data = st.session_state["localStorage_session_data"]
    else:
        # LocalStorage에서 초기 데이터 로드를 위한 JavaScript 실행 (한 번만)
        if "localStorage_initialized" not in st.session_state:
            js_code = """
            <script>
            // Streamlit Cloud 환경에서 LocalStorage 접근 (호환성 개선)
            try {
                // 페이지 로드 시 LocalStorage에서 세션 데이터 읽기
                let stored = null;
                
                // LocalStorage 우선 시도
                if (typeof Storage !== 'undefined' && localStorage) {
                    stored = localStorage.getItem('enhanced_session');
                }
                
                // SessionStorage fallback
                if (!stored && typeof Storage !== 'undefined' && sessionStorage) {
                    stored = sessionStorage.getItem('enhanced_session');
                    console.log('Using sessionStorage fallback');
                }
                
                if (stored) {
                    const sessionData = JSON.parse(stored);
                    console.log('Session loaded from storage:', sessionData);
                    
                    // Streamlit에 데이터 전달하기 위해 임시 저장
                    window.sessionDataFromStorage = sessionData;
                    
                    // Streamlit Cloud 환경 정보
                    if (window.location) {
                        console.log('Domain:', window.location.hostname);
                        console.log('Protocol:', window.location.protocol);
                    }
                } else {
                    console.log('No session data found in storage');
                }
            } catch (e) {
                console.error('Storage access error:', e);
                // 에러 시 storage 정리
                try {
                    localStorage && localStorage.removeItem('enhanced_session');
                    sessionStorage && sessionStorage.removeItem('enhanced_session');
                } catch (cleanupError) {
                    console.error('Storage cleanup failed:', cleanupError);
                }
            }
            </script>
            """
            
            try:
                components.html(js_code, height=0)
                st.session_state["localStorage_initialized"] = True
                
                # 다음 실행에서 확인할 수 있도록 페이지 재실행
                st.rerun()
            except Exception as e:
                st.warning(f"LocalStorage 초기화 중 오류: {e}")
                st.session_state["localStorage_initialized"] = True
    
    if session_data:
        user_id = session_data.get("uid")
        timestamp = session_data.get("ts")
        signature = session_data.get("sig")
        
        if user_id and timestamp and signature:
            try:
                # 서명 검증
                if verify_session_signature(user_id, timestamp, signature, SESSION_SECRET):
                    # 시간 검증 (7일 유효)
                    current_time = time.time()
                    session_age = current_time - float(timestamp)
                    
                    if session_age <= 7 * 24 * 3600:  # 7일 이내
                        # 사용자 정보 조회
                        row = fetch_user_info(user_id)
                        if row:
                            # 세션 상태에 1시간 동안 캐시
                            user_data = {
                                "id": row["id"],
                                "email": row["email"],
                                "username": row.get("username"),
                                "api_key": row.get("api_key")
                            }
                            st.session_state["user"] = user_data
                            st.session_state["session_valid_until"] = current_time + 3600  # 1시간
                            
                            # 세션이 1일 이상 오래되었으면 갱신
                            if session_age > 24 * 3600:  # 1일 후 갱신
                                set_localStorage_session(user_id)
                            
                            return user_data
                    else:
                        # 7일 만료된 세션 정리
                        clear_localStorage_session()
            except Exception as e:
                # 세션 오류 시 정리
                clear_localStorage_session()
    
    # 3. Fallback: 기존 URL 파라미터 방식 (이전 버전과의 호환성)
    query_params = st.query_params
    user_id = query_params.get("uid")
    timestamp = query_params.get("ts")
    signature = query_params.get("sig")
    
    if user_id and timestamp and signature:
        try:
            if verify_session_signature(user_id, timestamp, signature, SESSION_SECRET):
                if time.time() - float(timestamp) <= 7 * 24 * 3600:  # 7일 유효
                    row = fetch_user_info(user_id)
                    if row:
                        user_data = {
                            "id": row["id"],
                            "email": row["email"],
                            "username": row.get("username"),
                            "api_key": row.get("api_key")
                        }
                        st.session_state["user"] = user_data
                        st.session_state["session_valid_until"] = time.time() + 3600
                        
                        # URL 파라미터를 LocalStorage로 마이그레이션
                        set_localStorage_session(user_id)
                        
                        # URL 파라미터 정리
                        for param in ["uid", "ts", "sig"]:
                            if param in st.query_params:
                                del st.query_params[param]
                        
                        return user_data
        except:
            pass
    
    # 4. Fallback: 쿠키 방식 (하위 호환성)
    try:
        uid = CookieController().getAll().get(COOKIE_NAME)
        if uid:
            row = fetch_user_info(uid)
            if row:
                user_data = {
                    "id": row["id"],
                    "email": row["email"],
                    "username": row.get("username"),
                    "api_key": row.get("api_key")
                }
                st.session_state["user"] = user_data
                st.session_state["session_valid_until"] = time.time() + 3600
                
                # 쿠키 방식에서 LocalStorage 방식으로 마이그레이션
                set_localStorage_session(uid)
                
                return user_data
        
        # 쿠키 정리
        try:
            CookieController().remove(COOKIE_NAME)
        except:
            pass
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
    """Enhanced Session State 방식으로 사용자 로그인 (LocalStorage 기반)"""
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
        
        # 3. LocalStorage에 세션 저장
        set_localStorage_session(user_id)
        
        # 4. 기존 쿠키도 설정 (하위 호환성)
        try:
            CookieController().set(COOKIE_NAME, user_id)
        except:
            pass  # 쿠키 설정 실패해도 LocalStorage로 작동
        
        return True
    except Exception as e:
        st.error(f"로그인 처리 중 오류: {e}")
        return False

def logout_user_enhanced():
    """Enhanced Session State 방식으로 사용자 로그아웃 (LocalStorage 기반)"""
    try:
        # 1. 세션 상태 정리
        keys_to_remove = ["user", "session_valid_until", "api_key", "localStorage_session_data", "localStorage_initialized"]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        
        # 2. LocalStorage 세션 정리
        clear_localStorage_session()
        
        # 3. URL 파라미터 정리 (하위 호환성)
        params_to_remove = ["uid", "ts", "sig"]
        for param in params_to_remove:
            if param in st.query_params:
                del st.query_params[param]
        
        # 4. 쿠키 정리 (하위 호환성)
        try:
            controller = CookieController()
            controller.remove(COOKIE_NAME)
        except:
            pass
        
        return True
    except Exception as e:
        st.error(f"로그아웃 처리 중 오류: {e}")
        return False
