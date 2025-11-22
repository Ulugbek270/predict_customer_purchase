import uvicorn
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from core.base import init_db
from api import orders, predict

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app...")
    await init_db()

    yield

    logging.info("Shutting down...")

app = FastAPI(
    title="Predict Future Clients",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

app.include_router(orders.router)
app.include_router(predict.router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
