from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 동기 DB URL (파일 경로 조정 필요)
DATABASE_URL = "sqlite:///./fakepoomta.db"

# 동기 DB 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 동기 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()