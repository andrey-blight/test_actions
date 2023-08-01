from fastapi import FastAPI
from first.routers import router as first_router

app = FastAPI()

app.include_router(first_router, tags=["first"])
