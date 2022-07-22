from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
  return {"data": "This is your posts"}

@app.post("/create_posts")
def create_posts(payload: dict = Body(...)):
  print(payload)
  return {
    "new_post": f"title: {payload['title']}, content: {payload['content']}"}