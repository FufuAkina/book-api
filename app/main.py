from fastapi import FastAPI
from fastapi import HTTPException
# 创建 FastAPI 应用实例
app = FastAPI(
    title="BookAPI",
    description="图书管理系统 API",
    version="0.1.0"
)

# 根路径端点 - 健康检查
@app.get("/")
def read_root():
    """
    根路径， 返回欢迎信息
    """     # FastAPI 自动把 docstring 作为端点的描述
    return {"message": "Welcome to BookAPI", "status": "running"}

# 模拟数据库(BOOKS字典为全局变量)
BOOKS_DB = {
    1: {"id": 1, "title": "Python核心编程", "author": "Wesley Chun", "year": 2019},
    2: {"id": 2, "title": "FastAPI实战", "author": "晴雯", "year": 2023},
    3: {"id": 3, "title": "PostgreSQL权威指南", "author": "苗小弟", "year": 2020}
}   # value为字典的字典

# 获取所有图书(模拟数据)
@app.get("/books")  # 复数名词表示资源集合
def get_books():
    """
    获取图书列表(模拟数据)
    """
    return list(BOOKS_DB.values())
    
# 根据 ID 获取单本图书
@app.get("/books/{book_id}")
def get_book(book_id: int):
    """
    根据 ID 获取图书详情
    """
    if book_id not in BOOKS_DB:
        raise HTTPException(status_code=404, detail="Book not found")
        # HTTPException自动设置HTTP状态码，生成白哦准的错误相应格式
    return BOOKS_DB[book_id]
    
# 搜索图书(查询参数)
@app.get("/search")
def search_books(keyword: str, limit: int=10):
    """
    搜索图书
    - keyword: 搜索关键词
    - limit: 返回数量限制(默认10)
    """
    # 模拟搜索
    return{
        "keyword": keyword,
        "limit": limit,
        "results":[
            {"id": 1, "title": f"包含 '{keyword}' 的图书1"},
            {"id": 2, "title": f"包含 '{keyword}' 的图书2"}
        ]
    }