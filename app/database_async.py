from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载环境变量
load_dotenv(dotenv_path=BASE_DIR / ".env")

# 从环境变量中获取数据库URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 将 postgresql:// 替换为 postgresql+asyncpg://，并强制使用 IPv4
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
# 强制使用 127.0.0.1 而不是 localhost，避免 IPv6 问题
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("localhost", "127.0.0.1")

# 调试:打印数据库URL
if ASYNC_DATABASE_URL  is None:
    raise ValueError("ASYNC_DATABASE_URL 未设置！ 请检查.env文件是否存在且配置正确。")

# 创建异步数据库引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, # 开发时打印SQL语句
    pool_pre_ping=True, # 连接前检查连接是否有效
    connect_args={
        "server_settings": {"jit": "off"},
        "ssl": False,  # Windows环境禁用SSL
    }
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 异步依赖注入函数： 获取数据库会话
async def get_async_db():
    """
    获取异步数据库会话的以来函数
    使用yield确保绘画在使用后关闭
    """
    async with AsyncSessionLocal() as session:
        yield session