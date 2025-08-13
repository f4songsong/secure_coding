import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime, timedelta

# DB 연결 설정
DATABASE_URL = "sqlite:///./fakepoomta.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 비밀번호 해싱 및 검증 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 사용자 조회 함수
def get_user(email):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT email, password, name, is_admin FROM person WHERE email = :email
        """), {"email": email})
        user = result.fetchone()
        return user  # (email, hashed_password, name, is_admin) or None
    finally:
        db.close()

#로그인 시도 제한 초기화
if 'login_attempts' not in st.session_state:
    st.session_state['login_attempts'] = 0

if 'lock_until' not in st.session_state:
    st.session_state['lock_until'] = None



# 로그인 폼
def login_form():
    st.title("🔐 로그인")

    with st.form("login_form"):
        email = st.text_input("이메일")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인")

    if submitted:
        #잠금 상태 확인
        if st.session_state['lock_until']:
            if datetime.now() < st.session_state['lock_until']:
                remaining = (st.session_state['lock_until'] - datetime.now()).seconds // 60 + 1
                st.error(f"계정이 잠겨있습니다. {remaining}분 후 다시 시도하세요.")
                return
            else:
                # 잠금 해제
                st.session_state['lock_until'] = None
                st.session_state['login_attempts'] = 0

        user = get_user(email)
        if user:
            db_email, db_hashed_password, db_name, is_admin = user
            if verify_password(password, db_hashed_password):
                # 로그인 성공
                st.success(f"환영합니다, {db_name} 님!")
                st.session_state['authenticated'] = True
                st.session_state['name'] = db_name
                st.session_state['is_admin'] = (is_admin == 1) #관리자 여부 확인
                #로그인 성공 시 시도 횟수 초기화
                st.session_state['login_attempts'] = 0
                st.session_state['lock_until'] = None
                st.rerun()
            else:
                #로그인 실패 시 시도 증가 및 잠금 적용
                st.session_state['login_attempts'] += 1
                remaining_attempts = 5 - st.session_state['login_attempts']
                if remaining_attempts <= 0:
                    st.session_state['lock_until'] = datetime.now() + timedelta(minutes=5)
                    st.error("비밀번호 5회 실패. 5분 동안 잠겼습니다.")
                else:
                    st.error(f"비밀번호가 일치하지 않습니다. 남은 시도: {remaining_attempts}")
        else:
            st.error("존재하지 않는 사용자입니다.")

# 실행
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login_form()
else:
    st.success(f"{st.session_state['name']} 님, 이미 로그인되어 있습니다.")
    if st.session_state.get('is_admin'):
        st.info("관리자 계정입니다.")
    else:
        st.info("일반 사용자 계정입니다.")
    if st.button("로그아웃"):
        st.session_state.clear()
        st.rerun()
