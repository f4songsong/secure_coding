from fastapi import FastAPI, Depends #백엔드 실행하는 대표 파일
from sqlalchemy.ext.asyncio import AsyncSession
from db_connection import get_db

app = FastAPI()

@app.get("/ping")
async def test_connection(db: AsyncSession = Depends(get_db)):
    return {"message": "DB 연결 성공!"}