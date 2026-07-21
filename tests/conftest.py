import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main_async import app
from app.database_async import get_async_db
from app.models import Base
from app.auth import get_password_hash

# 使用开发数据库（测试完会清理数据）
TEST_DATABASE_URL = "postgresql+asyncpg://bookuser:bookpass@localhost:5432/bookdb"

# 创建测试引擎
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 覆盖依赖
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_async_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_database():
    """每个测试前后清理数据"""
    # 测试前清理
    async with engine.begin() as conn:
        # 只清理数据，不删表
        await conn.run_sync(lambda sync_conn: sync_conn.execute(Base.metadata.tables['books'].delete()))
        await conn.run_sync(lambda sync_conn: sync_conn.execute(Base.metadata.tables['users'].delete()))
    
    yield
    
    # 测试后清理（可选）
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: sync_conn.execute(Base.metadata.tables['books'].delete()))
        await conn.run_sync(lambda sync_conn: sync_conn.execute(Base.metadata.tables['users'].delete()))

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """数据库会话"""
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture
async def test_user(db_session):
    """创建测试用户"""
    from app.models import User
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("123456"),
        is_active=True,
        is_admin=False
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture
async def admin_user(db_session):
    """创建管理员用户"""
    from app.models import User
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_admin=True
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin

@pytest_asyncio.fixture
async def auth_headers(client, test_user):
    """普通用户认证头"""
    response = await client.post("/auth/login", data={
        "username": "testuser",
        "password": "123456"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest_asyncio.fixture
async def admin_headers(client, admin_user):
    """管理员认证头"""
    response = await client.post("/auth/login", data={
        "username": "admin",
        "password": "admin123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
