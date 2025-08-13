import streamlit as st
import sqlite3
from datetime import datetime

# 세션 검사
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("로그인 후 이용 가능합니다.")
    st.stop()

conn = sqlite3.connect("fakepoomta.db", check_same_thread=False)
cursor = conn.cursor()

st.title("📂 내 기록 목록")

# 사용자 확인
cursor.execute("SELECT person_id FROM person WHERE name = ?", (st.session_state.name,))
user_row = cursor.fetchone()
if not user_row:
    st.error("사용자를 찾을 수 없습니다.")
    st.stop()
person_id = user_row[0]

# 기록 목록 불러오기
cursor.execute("""
    SELECT record_id, title, created_at, is_public FROM record
    WHERE person_id = ? AND deleted_at IS NULL
    ORDER BY created_at DESC
""", (person_id,))
records = cursor.fetchall()

if not records:
    st.info("아직 저장된 기록이 없습니다.")
else:
    for record_id, title, created_at, is_public in records:
        with st.expander(f"📌 {title} ({created_at})"):
            cursor.execute("SELECT person_id FROM record WHERE record_id = ?", (record_id,))
            owner_row = cursor.fetchone()
            if not owner_row or owner_row[0] != person_id:
                st.error("⚠️ 권한이 없습니다.")
                continue
            # 수정 및 삭제 폼
            with st.form(f"form_{record_id}"):
                new_title = st.text_input("제목 수정", value=title, key=f"title_{record_id}")
                new_is_public = st.selectbox("공개 여부", ["공개", "비공개"], index=0 if is_public else 1, key=f"pub_{record_id}")
                delete = st.checkbox("❌ 이 기록을 삭제하겠습니다.", key=f"del_{record_id}")
                submitted = st.form_submit_button("변경사항 저장")

                if submitted:
                    if delete:
                        now = datetime.now().isoformat()
                        cursor.execute("UPDATE record SET deleted_at = ? WHERE record_id = ?", (now, record_id))
                        conn.commit()
                        st.success("기록이 삭제되었습니다.")
                        st.rerun()

                    else:
                        cursor.execute("""
                            UPDATE record SET title = ?, is_public = ?
                            WHERE record_id = ?
                        """, (new_title, 1 if new_is_public == "공개" else 0, record_id))
                        conn.commit()
                        st.success("변경 사항이 저장되었습니다.")

            # 상세 내용 표시
            cursor.execute("""
                SELECT block_type, detail, started_at, ended_at, time_at
                FROM detail WHERE record_id = ?
            """, (record_id,))
            details = cursor.fetchall()

            for block_type, detail, started_at, ended_at, time_at in details:
                st.text(f"[{block_type}] {detail}")
                st.caption(f"🕒 {started_at} ~ {ended_at} (⏱️ {time_at}초)")
