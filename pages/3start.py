import streamlit as st
import sqlite3
from datetime import datetime


def main_page():
    st.title("🎉 메인 페이지")
    st.success(f"환영합니다, {st.session_state.get('name', '사용자')} 님!")

# 세션 검사
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("로그인 후 이용 가능합니다.")
    st.stop()

conn = sqlite3.connect("fakepoomta.db", check_same_thread=False)
cursor = conn.cursor()

st.title("📂 내 기록 목록")

if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("로그인이 필요합니다.")
    st.stop()

cursor.execute("SELECT person_id FROM person WHERE name = ?", (st.session_state.name,))
user_row = cursor.fetchone()
if not user_row:
    st.error("사용자를 찾을 수 없습니다.")
    st.stop()
person_id = user_row[0]

# 사용자 기록 가져오기
cursor.execute("""
    SELECT record_id, title, created_at FROM record
    WHERE person_id = ? AND deleted_at IS NULL
    ORDER BY created_at DESC
""", (person_id,))
records = cursor.fetchall()

if not records:
    st.info("아직 저장된 기록이 없습니다.")
else:
    for record_id, title, created_at in records:
        with st.expander(f"📌 {title} ({created_at})"):
            cursor.execute("""
                SELECT block_type, detail, started_at, ended_at, time_at
                FROM detail WHERE record_id = ?
            """, (record_id,))
            details = cursor.fetchall()
            for block_type, detail, started_at, ended_at, time_at in details:
                st.markdown(f"**[{block_type}]** {detail}")
                st.caption(f"🕒 {started_at} ~ {ended_at} (⏱️ {time_at}초)")
