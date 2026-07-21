from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, models
from app import crud_async as crud
from app.database_async import get_async_db
from typing import List

import math
from typing import Optional

from app.routers import router as auth_router

from app.auth import get_current_user
from app import models

from fastapi import File, UploadFile
from pathlib import Path
import shutil
import uuid
# 创建FastAPI实例
app = FastAPI(
    title="BookAPI",
    description="图书管理系统API-异步版本(PostgreSQL + asyncpg)",
    version="0.4.0"
)

# 注册认证路由
app.include_router(auth_router)

# 5.4配置静态文件目录
UPLOAD_DIR = Path("uploads/covers")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 5.4挂载静态文件服务
from fastapi.staticfiles import StaticFiles
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
async def read_root():
    """根路径，返回欢迎信息"""
    return {"message": "Welcome to BookAPI(Async)", "status": "running", "version":"0.4.0"}

@app.get("/books", response_model=schemas.BookListResponse)
async def get_books_endpoint(
    page: int = 1,
    page_size: int = 10,
    sort_by: schemas.SortField = schemas.SortField.id,
    order: schemas.SortOrder = schemas.SortOrder.asc,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_async_db)
):
    """获取图书列表（支持分页、排序、过滤）"""
    # 计算 offset
    skip = (page - 1) * page_size
    
    # 获取数据
    books = await crud.get_books(
        db, skip=skip, limit=page_size,
        sort_by=sort_by.value, order=order.value,
        author=author, min_price=min_price, max_price=max_price
    )
    
    # 获取总数
    total = await crud.get_books_count(db, author=author, min_price=min_price, max_price=max_price)
    total_pages = math.ceil(total / page_size)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "items": books
    }

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
async def create_book_endpoint(
    book: schemas.BookCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user)  # 新增：需要登录
):
    """创建新图书（需要登录）"""
    existing_book = await crud.get_book_by_isbn(db, isbn=book.isbn)
    if existing_book:
        raise HTTPException(status_code=400, detail=f"ISBN {book.isbn} 已存在")
    
    return await crud.create_book(db=db, book=book)


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book_endpoint(
    book_id: int,
    book: schemas.BookCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user)  # 新增：需要登录
):
    """更新图书信息（需要登录）"""
    updated_book = await crud.update_book(db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
    return updated_book


@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
async def delete_book_endpoint(
    book_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user)  # 需要登录
):
    """删除图书（需要管理员权限）"""
    # 检查是否为管理员
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="权限不足：只有管理员可以删除图书"
        )
    
    deleted_book = await crud.delete_book(db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
    return deleted_book

@app.post("/books/{book_id}/cover")
async def upload_book_cover(
    book_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user)
):
    """上传图书封面（需要登录）"""
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="只支持 JPG、PNG、WEBP 格式")
    
    # 检查图书是否存在
    book = await crud.get_book(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"图书ID {book_id} 不存在")
    
    # 生成唯一文件名
    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # 保存文件
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 更新数据库
    cover_url = f"/uploads/covers/{unique_filename}"
    book.cover_image = cover_url
    await db.commit()
    await db.refresh(book)
    
    return {
        "message": "封面上传成功",
        "cover_url": cover_url,
        "book": book
    }