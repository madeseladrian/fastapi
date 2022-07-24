from fastapi import FastAPI
from .routers import login, post, user, vote

app = FastAPI()

app.include_router(login.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

@app.get("/")
def root():
  return {"message": "Welcome to FastApi"}
