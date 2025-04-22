from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello World"}

@app.get("/hello_personal")
def say_hello_personal(name: str):
    return {"message": f"Hello {name}"}