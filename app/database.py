from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载环境变量（明确指定 .env 文件路径）
load_dotenv(dotenv_path=BASE_DIR / ".env")

# 从环境变量获取数据库 URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 调试：打印数据库 URL（开发时用）
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL 未设置！请检查 .env 文件是否存在且配置正确。")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 开发时打印 SQL 语句
    pool_pre_ping=True,  # 连接前检查连接是否有效
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 依赖注入函数：获取数据库会话
def get_db():
    """
    获取数据库会话的依赖函数
    使用 yield 确保会话在使用后关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()