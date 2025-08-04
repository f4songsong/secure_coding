    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    # 1. 데이터베이스 주소 설정
    DATABASE_URL = "sqlite+aiosqlite:///./fakepoomta.db"

    # 2. 비동기 DB 엔진 만들기
    engine = create_async_engine(DATABASE_URL, echo=True)

    # 3. 세션 팩토리 만들기 (DB와 대화하는 객체)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # 4. 실제 요청에서 사용할 세션 생성 함수
    async def get_db():
        async with async_session() as session:
            yield session
