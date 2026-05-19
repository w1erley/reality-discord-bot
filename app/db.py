import os

from tortoise import Tortoise

MODELS_MODULE = "app.models"


async def init(db_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(db_path)) or ".", exist_ok=True)
    await Tortoise.init(
        db_url=f"sqlite://{db_path}",
        modules={"models": [MODELS_MODULE]},
    )
    await Tortoise.generate_schemas(safe=True)


async def close() -> None:
    await Tortoise.close_connections()
