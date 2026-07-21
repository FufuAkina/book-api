from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

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
    
    def __repr__(self):
        """开发时打印对象的表示"""
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"