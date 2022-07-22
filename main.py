from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

my_posts = [
  {"title": "title of post 1", "content": "content of post 1", "id": 1},
  {"title": "favorite foods", "content": "I like pizza", "id": 2},
  ]

@app.get("/")
def root():
  return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
  return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
  print(post)
  print(post.dict())
  return {"data": post}
