import streamlit as st
import requests

# 옵션: localhost 또는 네트워크용 IP 주소를 사용
USE_LOCALHOST = True

if USE_LOCALHOST:
    API_URL = "http://localhost:8000/ping"
else:
    API_URL = "http://192.168.200.123:8000/ping" 

st.title("기본페이지로 이동해주세요!")

# 백엔드에 GET 요청 보내기
try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()  # 상태 코드 오류가 있으면 예외 발생시킴
    data = response.json()
    st.success(f"메시지: {data['message']}")
except requests.exceptions.ConnectionError:
    st.error("연결 실패: FastAPI 서버가 실행 중인지 확인하세요.")
except requests.exceptions.Timeout:
    st.error("요청 시간이 초과되었습니다.")
except requests.exceptions.HTTPError as e:
    st.error(f"HTTP 오류 발생: {e}")
except Exception as e:
    st.error(f"기타 오류 발생: {e}")