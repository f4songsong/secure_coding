import streamlit as st
import sqlite3

conn = sqlite3.connect("fakepoomta.db", check_same_thread=False)
cursor = conn.cursor()

st.title("🌍 커뮤니티 기록 공유")

cursor.execute("""
    SELECT r.record_id, r.title, r.created_at, p.name
    FROM record r
    JOIN person p ON r.person_id = p.person_id
    WHERE r.is_public = 1 AND r.deleted_at IS NULL
    ORDER BY r.created_at DESC
""")
records = cursor.fetchall()

if not records:
    st.info("공개된 기록이 없습니다.")
else:
    for record_id, title, created_at, author in records:
        with st.expander(f"📖 {title} - by {author} ({created_at})"):
            cursor.execute("""
                SELECT block_type, detail, started_at, ended_at, time_at
                FROM detail WHERE record_id = ?
            """, (record_id,))
            details = cursor.fetchall()
            for block_type, detail, started_at, ended_at, time_at in details:
                st.markdown(f"**[{block_type}]** {detail}")
                st.caption(f"🕒 {started_at} ~ {ended_at} (⏱️ {time_at}초)")
