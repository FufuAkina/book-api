from fastapi import FastAPI, HTTPException
from app import schemas
from typing import List

# 创建 FastAPI 应用实例
app = FastAPI(
    title="BookAPI",
    description="图书管理系统 API",
    version="0.1.0"
)
# 模拟数据库(BOOKS字典为全局变量)
BOOKS_DB = {
    1: {
        "id": 1, 
        "title": "Python核心编程", 
        "author": "Wesley Chun",
        "isbn": "97871155114684",
        "publisher": "人民邮电出版社",
        "published_year": 2019,
        "price": 89.0,
        "descriptiton": "一本适合初学者的python教程",
        "stock": 50
        },
    
    2: {
        "id": 2,
        "title": "FastAPI实战",
        "author": "晴雯", 
        "isbn": "9787112234567",
        "publisher": "电子工业出版社",
        "published_year": 2023,
        "price": 79.0,
        "description": "FastAPI 框架实战教程",
        "stock" : 30
        },
    
    3: {
        "id": 3, 
        "title": "PostgreSQL权威指南", 
        "author": "苗小弟", 
        "isbn": "9787121345678",
        "publisher": "电子工业出版社",
        "published_year": 2020,
        "price": 99.0,
        "description": "PostgreSQL 数据库完整指南",
        "stock": 200
        }
}   # value为字典的字典


# 根路径端点 - 健康检查
@app.get("/")
def read_root():
    """
    根路径， 返回欢迎信息
    """     # FastAPI 自动把 docstring 作为端点的描述
    return {"message": "Welcome to BookAPI", "status": "running"}



# 获取所有图书(模拟数据)
@app.get("/books", response_model=List[schemas.BookResponse])  # 复数名词表示资源集合
def get_books():
    """
    获取图书列表
    
    返回：
        图书列表，每个图书包含完整信息
    """
    return list(BOOKS_DB.values())
    
# 根据 ID 获取单本图书
@app.get("/books/{book_id}")
def get_book(book_id: int):
    """
    根据 ID 获取图书详情
    
    参数: book_id: 图书ID
    
    返回： 图书详细信息
    
    异常： 404：图书不存在
    
    """
    if book_id not in BOOKS_DB:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
        # HTTPException自动设置HTTP状态码，生成白哦准的错误相应格式
    return BOOKS_DB[book_id]
    
# 搜索图书(查询参数)
@app.get("/search", response_model=List[schemas.BookResponse])
def search_books(keyword: str, limit: int=10):
    """
    搜索图书
    
    参数：
        - keyword: 搜索关键词
        - limit: 返回数量限制(默认10)
        
    返回： 匹配的图书列表
    
    """
    
    results = []
    
    # 遍历所有图书
    for book in BOOKS_DB.value():
        if(keyword.lower() in book["title"].lower() or
           keyword.lower() in book["author"].lower() or
           keyword in book["isbn"]):
            results.append(book)
            
            # 达到数量限制就停止
            if len(results) >= limit:
                break
            
    return results
    
# 创建图书
@app.post("/books", response_model=schemas.BookResponse, status_code=201)
def create_book(book:schemas.BookCreate):
    """
    创建新图书
    
    参数: book: 图书信息(不包含ID)
    
    返回： 创建成功的图书(包含新生成的ID)
    
    异常： 400: ISBN已存在
    
    """
    
    # 1. 检查ISBN是否已经存在
    for existing_book in BOOKS_DB.values():
        if existing_book["isbn"] == book.isbn:
            raise HTTPException(
                status_code=400,
                detail=f"ISBN {book.isbn} 已存在"
            )
            
    # 2. 生成新的ID
    if BOOKS_DB:
        new_id = max(BOOKS_DB.keys()) + 1
    else:
        new_id = 1
        
    # 3. 把 Pydantic 模型转换为字典
    book_dict = book.model_dump()
    
    # 4. 添加 ID
    book_dict["id"] = new_id
    
    # 5. 存到数据库中
    BOOKS_DB[new_id] = book_dict
    
    # 6. 返回新创建的图书
    return book_dict