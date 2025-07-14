from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {'data':{'name': 'Janvi'}}


@app.get("/about")
def about():
    return{'data':'about page'}

@app.get("/greet/{name}")
def greet_user(name: str):
    return {"greeting": f"Hello, {name}!"}