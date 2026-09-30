from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.app import helloworld
from src.repositories.todo_repository import(init_db,) # 引入資料庫初始函式

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)


@app.get("/", include_in_schema=False)
def health_check():
    return {"message": "This page is for health check."}


app.include_router(helloworld)
