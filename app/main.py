from fastapi import FastAPI

from app.routers import servicos

app = FastAPI()

app.include_router(servicos.router)