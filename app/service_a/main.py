import uvicorn
from fastapi import FastAPI
from .api import server_a

app = FastAPI()

app.include_router(server_a)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)