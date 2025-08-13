import streamlit as st
import sqlite3

# DB 연결
conn = sqlite3.connect("fakepoomta.db", check_same_thread=False)
cursor = conn.cursor()

# 사용자 관리 화면
def show_user_management():
    st.header("사용자 관리")
    cursor.execute("SELECT person_id, name, email FROM person WHERE is_admin = 0")
    users = cursor.fetchall()

    for person_id, name, email in users:
        col1, col2 = st.columns([7, 1])
        with col1:
            st.write(f"{person_id}: {name} ({email})")
        with col2:
            if st.button(f"탈퇴", key=f"del_user_{person_id}"):
                cursor.execute("DELETE FROM person WHERE person_id = ?", (person_id,))
                conn.commit()
                st.success(f"사용자 {name} 탈퇴 처리 완료")
                st.rerun()  

# 게시글 관리 화면
def show_post_management():
    st.header("게시글 관리")
    cursor.execute("SELECT record_id, title, person_id FROM record")
    posts = cursor.fetchall()

    for record_id, title, person_id in posts:
        col1, col2 = st.columns([7, 1])
        with col1:
            st.write(f"{record_id}: {title} (작성자 ID: {person_id})")
        with col2:
            if st.button(f"삭제", key=f"del_post_{record_id}"):
                cursor.execute("DELETE FROM record WHERE record_id = ?", (record_id,))
                conn.commit()
                st.success(f"게시글 {record_id} 삭제 완료")
                st.rerun()

# 메인 함수
def main():
    st.title("⛳ 관리자 시스템")

    # 관리자 여부 확인
    if 'is_admin' in st.session_state and st.session_state['is_admin']:
        st.sidebar.title("관리자 메뉴")
        menu = st.sidebar.radio("메뉴 선택", ["사용자 관리", "게시글 관리"])

        if menu == "사용자 관리":
            show_user_management()
        elif menu == "게시글 관리":
            show_post_management()
    else:
        st.sidebar.title("일반 사용자 메뉴")
        st.write(f"{st.session_state.get('user_name', '손님')}님, 환영합니다!")

if __name__ == "__main__":
    main()
