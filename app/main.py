from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config.database import create_tables
from app.controllers.user_controller import router as user_router
from app.exceptions.base import AppException
from app.exceptions.handlers import app_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Users API",
    description="A simple REST API for managing users",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Users API is running!", "version": "0.1.0"}


app.add_exception_handler(AppException, app_exception_handler)
app.include_router(user_router)
