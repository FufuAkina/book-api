from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import or_
from app import models, schemas

from sqlalchemy import select, func, or_
from typing import Optional

# ==================== 查询操作 ====================

async def get_book(db: AsyncSession, book_id: int):
    """根据 ID 获取单本图书（异步）"""
    result = await db.execute(
        select(models.Book).filter(models.Book.id == book_id)
    )
    return result.scalar_one_or_none()


async def get_books(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "id",
    order: str = "asc",
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """获取图书列表（支持过滤、排序、分页）"""
    # 构建查询
    query = select(models.Book)
    
    # 过滤条件
    if author:
        query = query.where(models.Book.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.where(models.Book.price >= min_price)
    if max_price is not None:
        query = query.where(models.Book.price <= max_price)
    
    # 排序
    sort_column = getattr(models.Book, sort_by, models.Book.id)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # 分页
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

# 新增：获取总数
async def get_books_count(
    db: AsyncSession,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> int:
    """获取图书总数（用于分页）"""
    query = select(func.count(models.Book.id))
    
    if author:
        query = query.where(models.Book.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.where(models.Book.price >= min_price)
    if max_price is not None:
        query = query.where(models.Book.price <= max_price)
    
    result = await db.execute(query)
    return result.scalar()


async def get_book_by_isbn(db: AsyncSession, isbn: str):
    """根据 ISBN 获取图书（异步）"""
    result = await db.execute(
        select(models.Book).filter(models.Book.isbn == isbn)
    )
    return result.scalar_one_or_none()


async def search_books(db: AsyncSession, keyword: str, limit: int = 10):
    """搜索图书（标题、作者、ISBN）（异步）"""
    search_pattern = f"%{keyword}%"
    result = await db.execute(
        select(models.Book)
        .filter(
            or_(
                models.Book.title.ilike(search_pattern),
                models.Book.author.ilike(search_pattern),
                models.Book.isbn.ilike(search_pattern)
            )
        )
        .limit(limit)
    )
    return result.scalars().all()


# ==================== 创建操作 ====================

async def create_book(db: AsyncSession, book: schemas.BookCreate):
    """创建新图书（异步）"""
    book_dict = book.model_dump()
    db_book = models.Book(**book_dict)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


# ==================== 更新操作 ====================

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookCreate):
    """更新图书信息（异步）"""
    db_book = await get_book(db, book_id)
    if db_book is None:
        return None
    
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book


# ==================== 删除操作 ====================

async def delete_book(db: AsyncSession, book_id: int):
    """删除图书（异步）"""
    db_book = await get_book(db, book_id)
    if db_book is None:
        return None

    # 使用 delete 语句执行删除操作
    await db.execute(
        delete(models.Book).where(models.Book.id == book_id)
    )
    await db.commit()
    return db_book