from typing import Any
from datetime import datetime
from re import sub
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, sql
from pydantic import BaseModel


@as_declarative()
class Base:
  id: Any
  __name__: str
  @declared_attr
  def __tablename__(cls) -> str:
    """
    Generate __tablename__ automatically
    Auto set table name, CamelCase to snake_case
    """
    return sub(r"(?P<key>[A-Z])", r"_\g<key>", cls.__name__).lower().strip('_')

class Clock:
  """
  Vessel db table
  """
  updatedAt = Column("updated_at", TIMESTAMP(), default=datetime.now())
  createdAt = Column("created_at", TIMESTAMP, nullable=False, server_default=sql.func.now())


class Common(Clock):
  """
  Common db table
  """
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)

