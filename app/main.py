from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import engine, get_db
from typing import List

# 创建数据库表(使用 Alembic管理， 不再需要)
# models.Base.metadata.create_all(bind=engine)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="BookAPI",
    description="图书管理系统 API - 使用 PostgreSQL",
    version="0.3.0"
)


# 根路径端点 - 健康检查
@app.get("/")
def read_root():
    """
    根路径， 返回欢迎信息
    """     # FastAPI 自动把 docstring 作为端点的描述
    return {"message": "Welcome to BookAPI", "status": "running", "version": "0.3.0"}


# 获取所有图书(模拟数据): t图书列表
@app.get("/books", response_model=List[schemas.BookResponse])  # 复数名词表示资源集合
def get_books_endpoint(skip: int=0, limit:int=100, db:Session=Depends(get_db)):
    """
    获取图书列表
    """
    books = crud.get_books(db, skip=skip, limit=limit)
    return books
    
# 根据 ID 获取单本图书
@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book_endpoint(book_id: int, db: Session=Depends(get_db)):
    """
    根据 ID 获取图书详情
    """
    book = crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"图书ID{book_id} 不存在")
    return book

    
@app.get("/search", response_model=List[schemas.BookResponse])
def search_books_endpoint(keyword: str, limit: int = 10, db: Session = Depends(get_db)):
    """搜索图书"""
    books = crud.search_books(db, keyword=keyword, limit=limit)
    return books
    
# 创建图书
@app.post("/books", response_model=schemas.BookResponse, status_code=201)
def create_book_endpoint(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """创建新图书"""
    existing_book = crud.get_book_by_isbn(db, isbn=book.isbn)
    if existing_book:
        raise HTTPException(status_code=400, detail=f"ISBN {book.isbn} 已存在")
    
    return crud.create_book(db=db, book=book)
