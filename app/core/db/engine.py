from sqlmodel import create_engine

from app.config import settings

database_url = settings.database_url


engine = create_engine(database_url)