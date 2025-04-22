from fastapi import FastAPI, Request, Header, Cookie
from pydantic import BaseModel
from typing import Optional

from fastapi.responses import JSONResponse


app = FastAPI()

class EchoRequest(BaseModel):
    name: Optional[str] = "Anonymous"

@app.post("/echo")
def echo(
    data: EchoRequest, 
    user_agent: Optional[str] = Header(None),
    custom_cookie: Optional[str] = Cookie(None)
):
    return {
        "message":f"Hello, {data.name}!",
        "user_agent": user_agent, 
        "custom_cookie": custom_cookie
    }

@app.get("/set-cookie")
def set_cookie():
    response = JSONResponse(content = {"message": "Cookie set!"})
    response.set_cookie(key = "custom_cookie", value = "sriram9217")
    return response