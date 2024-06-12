from tortoise import Tortoise
from config import DB_URL


async def init_db():
    await Tortoise.init(db_url=DB_URL, modules={"models": ["models"]})
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
