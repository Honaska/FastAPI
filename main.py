from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import SessionLocal, engine
from models import Post, Base

Base.metadata.create_all(bind =engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostCreate(BaseModel):
    title : str
    content : str
class PostOut(PostCreate):
    id : int
    date_created : str

    class Config:
        orm_mode = True

@app.get("/posts", response_model=List[PostOut])
def add_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.post("/posts", response_model=PostOut)
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post