from app import oauth2
from ..database import get_db
from .. import models, schemas
from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)

# @router.get("/all", response_model=List[schemas.Post])
# def get_all_posts(
#   db: Session = Depends(get_db), 
#   current_user: int = Depends(oauth2.get_current_user),
#   limit: int = 10,
#   skip: int = 0,
#   search: OpTional[str] = ""
# ):
#   posts = db.query(models.Post).filter(
#     models.Post.title.contains(search)
#   ).limit(limit).offset(skip).all()
#   return posts

@router.get("/all", response_model=List[schemas.Post])
def get_all_posts(
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user),
  limit: int = 10
):
  posts = db.query(models.Post).limit(limit).all()
  return posts

@router.get("/", response_model=List[schemas.Post])
def get_posts(
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user),
  limit: int = 10
):
  posts = db.query(models.Post).filter(
    models.Post.owner_id == current_user.id
  ).all()
  return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
  post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user),
  limit: int = 10
):
  print("Current User ID: ", current_user.id)
  new_post = models.Post(owner_id = current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(
  id: int, 
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user),
  limit: int = 10
):
  post = db.query(models.Post).filter(models.Post.id == id).first()

  if not post:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )
  return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
  id: int, 
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user)
):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  post = post_query.first()
  if post == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )

  if post.owner_id != current_user.id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN, 
      detail=f"Not authorized to perform request action"
    )
  
  post_query.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(
  id: int, updated_post: schemas.PostCreate, 
  db: Session = Depends(get_db), 
  current_user: int = Depends(oauth2.get_current_user)
):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()

  if post == None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, 
      detail=f"post with id: {id} was not found"
    )
  
  if post.owner_id != current_user.id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN, 
      detail=f"Not authorized to perform request action"
    )
  
  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()
  return post_query.first()
