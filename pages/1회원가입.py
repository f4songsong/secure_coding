import streamlit as st
import smtplib
from email.mime.text import MIMEText
import re
import random
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# 비밀번호 해시 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 이메일 인증 메일 발송 함수
def send_verification_email(to_email, code):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'checkemail448@gmail.com'
    sender_password = 'ntkp yxiq zknr yjvw'

    subject = '회원가입 이메일 인증 코드'
    body = f'인증 코드는 {code} 입니다.'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, to_email, msg.as_string())
    server.quit()

# DB 세팅 (동기 방식)
DATABASE_URL = "sqlite:///./fakepoomta.db"  # 경로 필요에 맞게 조정

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 회원가입 입력 폼
st.title("회원가입")

name = st.text_input("이름을 입력하세요 (영문 또는 한글+숫자, 2~20자)")
password = st.text_input("비밀번호 (영어+ 숫자, 8자 이상)", type="password")
email = st.text_input("이메일")

def is_name_valid(name):
    pattern = r'^[a-zA-Z0-9가-힣]{2,20}$'
    return re.match(pattern, name) is not None

def is_password_valid(password):
    if len(password) < 8:
        return False
    has_letter = re.search(r'[a-zA-Z]', password)
    has_number = re.search(r'[0-9]', password)
    return bool(has_letter and has_number)

def is_email_valid(email):
    if not isinstance(email, str):
        return False
    email = email.strip()
    if not email:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# 세션 초기화
if 'email_verified' not in st.session_state:
    st.session_state['email_verified'] = False

# 인증 코드 발송
if st.button("인증 코드 보내기"):
    if email and is_email_valid(email):
        code = str(random.randint(100000, 999999))
        st.session_state['email_code'] = code
        st.session_state['email'] = email
        try:
            send_verification_email(email, code)
            st.success("인증 코드가 이메일로 발송되었습니다.")
        except Exception as e:
            st.error(f"이메일 발송 실패: {e}")
    else:
        st.error("올바른 이메일 주소를 입력하세요.")

# 인증 코드 입력
user_code = st.text_input("이메일로 받은 인증 코드를 입력하세요")

if st.button("인증 확인"):
    if 'email_code' in st.session_state and user_code == st.session_state['email_code']:
        st.success("이메일 인증이 완료되었습니다.")
        st.session_state['email_verified'] = True
    else:
        st.error("인증 코드가 일치하지 않습니다.")

# 동기 회원가입 처리 함수
def register_user_sync(name, email, password):
    db = SessionLocal()
    try:
        # 이메일 중복 확인
        result = db.execute(text("SELECT email FROM person WHERE email = :email"), {"email": email})
        existing = result.fetchone()
        if existing:
            st.error("이미 등록된 이메일입니다.")
            return

        # 비밀번호 해시 후 DB 저장
        hashed_pw = hash_password(password)
        db.execute(text("""
            INSERT INTO person (name, email, password)
            VALUES (:name, :email, :password)
        """), {"name": name, "email": email, "password": hashed_pw})
        db.commit()

        st.success("회원가입이 완료되었습니다.")
        st.session_state['email_verified'] = False  # 인증 초기화
    except Exception as e:
        st.error(f"회원가입 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

# 회원가입 버튼 처리
if st.button("회원가입"):
    if not is_name_valid(name):
        st.error("이름은 영문 또는 한글+숫자 조합, 2~20자여야 합니다.")
    elif not is_password_valid(password):
        st.error("비밀번호는 영어+숫자 포함, 8자 이상이어야 합니다.")
    elif not st.session_state.get('email_verified', False):
        st.error("이메일 인증을 먼저 완료해주세요.")
    else:
        register_user_sync(name, email, password)
