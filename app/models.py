from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 创建基类
Base = declarative_base()

# 定义 Book 模型(对应数据库表)
class Book(Base):
    __tablename__ = "books"  # 表名
    
    # 定义列
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False, index=True)
    publisher = Column(String(100), nullable=True)
    published_year = Column(Integer,  nullable=True)
    price = Column(Float, nullable=True)
    description  = Column(Text, nullable=True)
    stock = Column(Integer, default=0, nullable=True)
    cover_image = Column(String, nullable=True)  # 新增：封面图片路径
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """开发时打印对象的表示"""
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"
    
# 5.2 JWT验证
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 加密后的密码
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # 是否管理员（Phase 5.3 用）
    created_at = Column(DateTime, default=datetime.utcnow)