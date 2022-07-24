from ..database import get_db
from .. import models, schemas
from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()

  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )
  return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)

  if post.first() == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )
  
  post.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  updated_post = post_query.first()

  if updated_post == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )
  
  post_query.update(post.dict(), synchronize_session=False)
  db.commit()
  return post_query.first()