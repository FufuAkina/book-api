from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
from app import crud_async as crud
from app.database_async import get_async_db
from typing import List

# 创建FastAPI实例
app = FastAPI(
    title="BookAPI",
    description="图书管理系统API-异步版本(PostgreSQL + asyncpg)",
    version="0.4.0"
)

@app.get("/")
async def read_root():
    """根路径，返回欢迎信息"""
    return {"message": "Welcome to BookAPI(Async)", "status": "running", "version":"0.4.0"}

@app.get("/books", response_model=List[schemas.BookResponse])
async def get_books_endpoint(skip:int=0, limit:int=100, db:AsyncSession=Depends(get_async_db)):
    """获取图书列表(异步)"""
    books = await crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_book_endpoint(book_id: int, db: AsyncSession = Depends(get_async_db)):
    """根据 ID 获取图书详情（异步）"""
    book = await crud.get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
    return book


@app.get("/search", response_model=List[schemas.BookResponse])
async def search_books_endpoint(keyword: str, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    """搜索图书（异步）"""
    books = await crud.search_books(db, keyword=keyword, limit=limit)
    return books


@app.post("/books", response_model=schemas.BookResponse, status_code=201)
async def create_book_endpoint(book: schemas.BookCreate, db: AsyncSession = Depends(get_async_db)):
    """创建新图书（异步）"""
    existing_book = await crud.get_book_by_isbn(db, isbn=book.isbn)
    if existing_book:
        raise HTTPException(status_code=400, detail=f"ISBN {book.isbn} 已存在")
    
    return await crud.create_book(db=db, book=book)


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book_endpoint(book_id: int, book: schemas.BookCreate, db: AsyncSession = Depends(get_async_db)):
    """更新图书信息（异步）"""
    updated_book = await crud.update_book(db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
    return updated_book


@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_async_db)):
    """删除图书（异步）"""
    deleted_book = await crud.delete_book(db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
    return deleted_book