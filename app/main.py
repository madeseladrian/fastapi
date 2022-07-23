from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from . import models
from .database import get_db, engine
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

@app.get("/")
def root():
  return {"message": "Welcome to FastApi"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)
  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  
  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  updated_post = post_query.first()
  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  post_query.update(post.dict(), synchronize_session=False)
  db.commit()
  return {"data": post_query.first()}
