from gino_starlette import Gino

from app.settings import settings

db = Gino(dsn=settings.db_url)
