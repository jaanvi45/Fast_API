from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/blog")
def index(limit=10,published: bool=True,sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs form the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


@app.get("/about")
def about():
    return{'data':'about page'}

@app.get("/greeting/{name}")
def greeting(name: str):
    return {"greeting": f"Hello, {name}!"}

@app.get("/blog/unpublished")
def unpublished():
    return {"data": " All Unpublished blogs"}

@app.get("/blog/{id}")
def blog(id: int):
    return {"data": id}

@app.get("/blog/{id}/comments")
def comments(id: int):
    return {"data": f"Comments for blog {id}"}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.post("/blog")
def create_blog(request: Blog):
    return {"data": f"Blog is created with title as {request.title}"}