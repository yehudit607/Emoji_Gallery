import logging
from contextlib import contextmanager
from typing import Callable, Generator, Iterator, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from starlette.requests import Request
from starlette.responses import Response


from app.core.db.engine import engine
from app.core.models.base import PostgresTimeStampMixin, DictMixin

logger = logging.getLogger(__name__)


class BasePostgresORM(PostgresTimeStampMixin, DictMixin):
    pass


BaseORM = declarative_base(cls=BasePostgresORM)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    try:
        session = sessionmaker(bind=engine)()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


async def db_session_middleware(request: Request, call_next: Callable) -> Response:
    # with session_scope() as session:
    #     request.state.db = session
    return await call_next(request)


def get_session(request: Request) -> Iterator[Session]:
    with session_scope() as session:
        request.state.db = session
        yield request.state.db
