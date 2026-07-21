# 数据验证和文档生成 (验证用户的输入，生成API文档)
# 输入验证、输出格式化、生成自动文档
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
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
    # 封面字段
    cover_image: Optional[str] = None
    
# 创建图书
class BookCreate(BookBase):
    pass  # 继承 BookBase 的所有字段

# 返回图书数据
class BookResponse(BookBase):
    id: int
    
    model_config = {"from_attributes": True}
    
    
# 5.1阶段添加:查询的更多功能
from typing import Optional, List
from enum import Enum

# 新增： 排序字段枚举
class SortField(str, Enum):
    id = "id"
    title = "title"
    author = "author"
    price = "price"
    created_at = "created_at"
    
# 新增： 排序方向枚举
class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
    
# 新增：查询参数模型
class BookQueryParams(BaseModel):
    """图书查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")
    sort_by: SortField = Field(default=SortField.id, description="排序字段")
    order: SortOrder = Field(default=SortOrder.asc, description="排序方式")
    author: Optional[str] = Field(default=None, description="作者筛选")
    min_price: Optional[float] = Field(default=None, ge=0, description="最低价格")
    max_price: Optional[float] = Field(default=None, ge=0, description="最高价格")

# 新增：分页响应模型
class BookListResponse(BaseModel):
    """分页响应"""
    total:int
    page:int
    page_size:int
    total_pages:int
    items:List[BookResponse]
    
# 5.2 JWT验证机制
# ========== 用户相关 Schema ==========

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')  # 简单邮箱验证

class UserCreate(UserBase):
    """用户注册"""
    password: str = Field(min_length=6, max_length=100)

class UserResponse(UserBase):
    """用户响应"""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token 中的数据"""
    user_id: Optional[int] = None
