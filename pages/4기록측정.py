import streamlit as st
import sqlite3
from datetime import datetime

# DB 연결
conn = sqlite3.connect("fakepoomta.db", check_same_thread=False)
cursor = conn.cursor()

st.title("⏱️ 시간 측정 및 기록")

# 세션 상태 초기화
if 'started_at' not in st.session_state:
    st.session_state.started_at = None

if 'ended_at' not in st.session_state:
    st.session_state.ended_at = None

if 'time_at' not in st.session_state:
    st.session_state.time_at = None

# 사용자 ID 가져오기 (예시용으로 name을 세션에서 가져옴)
if 'name' not in st.session_state:
    st.warning("로그인이 필요합니다.")
    st.stop()

cursor.execute("SELECT person_id FROM person WHERE name = ?", (st.session_state.name,))
user_row = cursor.fetchone()
if not user_row:
    st.error("유효하지 않은 사용자입니다.")
    st.stop()
person_id = user_row[0]

# 시간 측정 버튼
if st.button("▶ 시작"):
    st.session_state.started_at = datetime.now()
    st.success(f"시작 시간: {st.session_state.started_at}")

if st.button("■ 종료"):
    st.session_state.ended_at = datetime.now()
    if st.session_state.started_at:
        st.session_state.time_at = int((st.session_state.ended_at - st.session_state.started_at).total_seconds())
        st.success(f"종료 시간: {st.session_state.ended_at}, 소요 시간: {st.session_state.time_at}초")
    else:
        st.warning("시작 버튼을 먼저 눌러주세요.")

# 제목 및 상세 입력
st.subheader("기록 저장")
title = st.text_input("제목")
detail_text = st.text_area("내용")
block_type = st.selectbox("블록 타입", ["text", "todo", "code", "image", "etc"])

# 저장 함수 (공개 여부 추가)
# 🔧 수정된 save_record 함수
def save_record(is_public):
    if not title or not detail_text:
        st.error("제목과 내용을 모두 입력해주세요.")
    elif not st.session_state.started_at or not st.session_state.ended_at:
        st.error("시간 측정 후 저장해주세요.")
    else:
        # ✅ 1. record 저장 (is_public 포함) — ALTER TABLE 제거됨
        cursor.execute("""
            INSERT INTO record (person_id, title, is_public, created_at, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (person_id, title, 1 if is_public else 0))

        record_id = cursor.lastrowid

        # ✅ 2. detail 저장
        cursor.execute("""
            INSERT INTO detail (
                record_id, block_type, detail,
                started_at, ended_at, time_at,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (
            record_id, block_type, detail_text,
            st.session_state.started_at,
            st.session_state.ended_at,
            st.session_state.time_at
        ))

        conn.commit()
        st.success("기록이 저장되었습니다.")


# 저장 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("🔒 비공개 저장"):
        save_record(is_public=False)

with col2:
    if st.button("🌐 공개 저장"):
        save_record(is_public=True)