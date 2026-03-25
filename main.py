from fastapi import Depends, FastAPI, HTTPException

import crud
from database import Base
import schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine


Base().metadata.create_all(bind=engine)
app = FastAPI(
    title="Book API",
    description="A simple API for managing books",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Dependendy to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.BookRead])
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    success = crud.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}
