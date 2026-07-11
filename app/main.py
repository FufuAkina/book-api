from fastapi import FastAPI

# 创建 FastAPI 应用实例
app = FastAPI(
    title="BookAPI",
    description="图书管理系统 API",
    version="0.1.0"
)

# 根路径 - 健康检查
@app.get("/")
def read_root():
    """
    根路径， 返回欢迎信息
    """
    return {"message": "Welcome to BookAPI", "status": "running"}

# 获取所有图书(模拟数据)
@app.get("/books")
def get_books():
    """
    获取图书列表(模拟数据)
    """
    return [
        {
            "id": 1,
            "title": "Python核心编程",
            "author": "Wesley Chun",
            "year": 2019,
            "isbn": "9787115514684"
        },
        {
            "id": 2,
            "title": "FastAPI实战",
            "author": "晴雯",
            "year": 2023,
            "isbn": "97887121234567"
        },
        {
            "id": 3,
            "title": "PostgreSQL权威指南",
            "author": "苗小弟",
            "year": 2020,
            "isbn": "9787121345678"
        }
    ]
    
# 根据 ID 获取单本图书
@app.get("/books/{book_id}")
def get_book(book_id: int):
    """
    根据 ID 获取图书详情
    """
    # 模拟数据库查询
    books = {
        1 : {
            "id": 1,
            "title": "Python核心编程",
            "author": "Wesley Chun",
            "year": 2019,
            "isbn": "9787115514684"
        },
        2: {
             "id": 2,
            "title": "FastAPI实战",
            "author": "晴雯",
            "year": 2023,
            "isbn": "97887121234567"
        }
    }
    
    if book_id in books:
        return books[book_id]
    else:
        return {"error": "Book not found "}, 404
    
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