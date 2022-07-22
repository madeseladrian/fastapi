from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True

@app.get("/")
def root():
  return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
  return {"data": "This is your posts"}

@app.post("/create_posts")
def create_posts(new_post: Post):
  print(new_post)
  print(new_post.dict())
  return {"new_post": f"{new_post}"}
