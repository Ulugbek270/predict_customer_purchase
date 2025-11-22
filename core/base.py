import asyncio
import os
import logging
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

logging.info("Loading DB setup...")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass
async def init_db():
    async with engine.begin() as conn:
        from models.tables.clients import Client
        from models.tables.customers import Customer
        from models.tables.goods import Goods
        from models.tables.orders import Order
        from models.tables.order_items import OrderItem
        await conn.run_sync(Base.metadata.create_all)
        logging.info("Schema created.")
