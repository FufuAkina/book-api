from pydantic import BaseModel, Field
from typing import Optional

# 基础模型
class BookBase(BaseModel):
    # 必填无默认值
    title: str = Field(..., min_length=1, max_length=200, description="书籍标题：1-200个字符")
    author: str = Field(..., min_length=1, max_length=100, description="作者：1-100字符")
    isbn: str = Field(..., min_length=10, max_length=20, description="ISBN编号：10-20字符")
    # 选填无默认值
    publisher: Optional[str] = Field(None, max_length=100, description="出版社：最多100字符")
    published_year: Optional[int] = Field(None, ge=1000, le=9999, description="出版年份：1000-9999之间")
    price: Optional[float] = Field(None, ge=0, description="价格：大于等于0")
    description: Optional[str] = Field(None, description="书籍描述")
    # 带默认值
    stock:  int = Field(default=0, ge=0)
    
# 创建图书
class BookCreate(BookBase):
    pass  # 继承 BookBase 的所有字段

# 返回图书数据
class BookResponse(BookBase):
    id: int
    
    model_config = {"from_attributes": True}