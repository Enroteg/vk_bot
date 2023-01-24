from typing import Union
import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

    
@app.post("/")
async def read_root(request: Request):
    content_type = request.headers.get('Content-Type')
    print(content_type)
    #return {"Hello": "World"}
    print(request.json())
    
if __name__ == '__main__':#start
    uvicorn.run(app, host="0.0.0.0", port = 23659)