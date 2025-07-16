from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas, models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog",status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    #return {"data": f"Blog is created with title as {new_blog.title}"}
    return new_blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    blog = blog_query.first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available"
        )
    blog_query.update(request.dict(), synchronize_session=False)
    db.commit()
    db.refresh(blog)  
    
    return blog

@app.get("/blog", response_model=List[schemas.showBlog])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}",status_code=200,response_model=schemas.showBlog)
def show(id, response:Response,db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{"detail":f"Blog with the id {id} is not available"}
    return blog



@app.post("/user", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user