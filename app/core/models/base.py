from datetime import datetime
from typing import Any

import pydantic
from pydantic import ConfigDict
from sqlalchemy import event, TIMESTAMP, Column
from sqlmodel import SQLModel, Field, Index
from app.core.db.session import db

class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_datetime: datetime = Field(default=datetime.utcnow, index=True)
    modified_datetime: datetime = Field(default=datetime.utcnow, index=True)

    @classmethod
    def get_all(cls, offset: int = 0, limit: int = 10, order_by: str = "id"):
        query = db.query(cls).offset(offset).limit(limit).order_by(getattr(cls, order_by))
        return query.all()


class PostgresTimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow, nullable=False)
    created_at._creation_order = 9990  # type: ignore
    updated_at = Column(TIMESTAMP(), default=datetime.datetime.utcnow, nullable=False)
    updated_at._creation_order = 9991  # type: ignore

    @staticmethod
    def _updated_at(mapper: Any, connection: Any, target: Any) -> None:
        target.updated_at = datetime.datetime.utcnow()

    @classmethod
    def __declare_last__(cls) -> None:
        event.listen(cls, "before_update", cls._updated_at)




class DictMixin:
    def to_dict(self):
        """Converts an instance of any class to a dictionary."""
        # Get the class's namespace and filter out private attributes
        class_dict = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        }
        return class_dict