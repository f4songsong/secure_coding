import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# ---------------------
# DB 연결 설정
# ---------------------
DATABASE_URL = "sqlite:///./fakepoomta.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------
# 비밀번호 해싱 및 검증 설정
# ---------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------
# 사용자 조회 함수
# ---------------------
def get_user(email):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT email, password, name FROM person WHERE email = :email
        """), {"email": email})
        user = result.fetchone()
        return user  # (email, hashed_password, name) or None
    finally:
        db.close()

# ---------------------
# 로그인 폼
# ---------------------
def login_form():
    st.title("🔐 로그인")

    with st.form("login_form"):
        email = st.text_input("이메일")
        password = st.text_input("비밀번호", type="password")
        submitted = st.form_submit_button("로그인")

    if submitted:
        user = get_user(email)
        if user:
            db_email, db_hashed_password, db_name = user
            if verify_password(password, db_hashed_password):
                st.success(f"환영합니다, {db_name} 님!")
                st.session_state['authenticated'] = True
                st.session_state['name'] = db_name
                st.rerun()
            else:
                st.error("비밀번호가 일치하지 않습니다.")
        else:
            st.error("존재하지 않는 사용자입니다.")

# ---------------------
# 실행
# ---------------------
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    login_form()
else:
    st.success(f"{st.session_state['name']} 님, 이미 로그인되어 있습니다.")
    if st.button("로그아웃"):
        st.session_state.clear()
        st.experimental_rerun()
