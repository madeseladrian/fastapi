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

my_posts = [
  {"title": "title of post 1", "content": "content of post 1", "id": 1},
  {"title": "favorite foods", "content": "I like pizza", "id": 2},
]

def find_post(id):
  for p in my_posts:
    if p['id'] == id: 
      return p

def find_index_post(id):
  for i, p in enumerate(my_posts):
    if p['id'] == id:
      return i

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
def delete_post(id: int):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  index = find_index_post(id)
  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
  post_dict = post.dict()
  post_dict['id'] = id
  my_posts[index] = post_dict
  return {"data": post_dict}
