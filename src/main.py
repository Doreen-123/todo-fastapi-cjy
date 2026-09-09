from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.app import helloworld

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)


@app.get("/", include_in_schema=False)
def health_check():
    return {"This page is for health check."}


app.include_router(helloworld)
