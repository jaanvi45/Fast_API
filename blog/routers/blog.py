from fastapi import APIRouter, Depends, status
from typing import List
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


get_db = database.get_db

@router.get("/", response_model=List[schemas.showBlog])
def all(db : Session = Depends(get_db),get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post("/",status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    return blog.create(request, db)


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db : Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)


@router.get("/{id}",status_code=200,response_model=schemas.showBlog)
def show(id:int, db : Session = Depends(get_db)):
    return blog.show(id, db)

