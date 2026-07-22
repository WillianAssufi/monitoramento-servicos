# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import servicos
from app.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(servicos.router)