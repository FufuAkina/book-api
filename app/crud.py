from sqlalchemy.orm import Session
from app import models, schemas

# 查询操作
def get_book(db:Session, book_id:int):
    """根据 ID 获取单本图书"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db:Session, skip: int=0, limit:int=100):
    """获取图书列表"""
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_isbn(db:Session, isbn:str):
    """根据 ISBN  获取图书"""
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def search_books(db: Session, keyword: str, limit: int = 10):
    """搜索图书（标题、作者、ISBN）"""
    search_pattern = f"%{keyword}%"
    return (
        db.query(models.Book)
        .filter(
            (models.Book.title.ilike(search_pattern)) | 
            (models.Book.author.ilike(search_pattern)) |
            (models.Book.isbn.ilike(search_pattern))
        )
        .limit(limit)
        .all()
    )

# 创建操作
def create_book(db:Session, book: schemas.BookCreate):
    """创建新图书"""
    book_dict = book.model_dump()
    db_book = models.Book(**book_dict)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# 更新操作
def update_book(db: Session, book_id: int, book:schemas.BookCreate):
    """更新图书信息"""
    db_book = get_book(db, book_id)
    if db_book is None:
        return None
    
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
        
    db.commit()
    db.refresh(db_book)
    return db_book

# 删除操作
def delete_book(db:Session, book_id:int):
    """删除图书"""
    db_book  = get_book(db, book_id)
    if db_book is None:
        return None

    db.delete(db_book)
    db.commit()
    return db_book


    
    
    