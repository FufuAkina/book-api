from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import or_
from app import models, schemas

# ==================== 查询操作 ====================

async def get_book(db: AsyncSession, book_id: int):
    """根据 ID 获取单本图书（异步）"""
    result = await db.execute(
        select(models.Book).filter(models.Book.id == book_id)
    )
    return result.scalar_one_or_none()


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取图书列表（异步）"""
    result = await db.execute(
        select(models.Book).offset(skip).limit(limit)
    )
    return result.scalars().all()


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