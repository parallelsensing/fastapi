from typing import Set, Any, List, Optional
from pydantic import BaseModel,Field
from enum import Enum
from .institution import IInstitution

class IAuthor(BaseModel):
  id:int|None = Field(
    default=None,
    title="id"
  )
  email:str|None = Field(
    default=None,
    title="email"
  )
  orcid:str|None = Field(
    default=None,
    title="orcid"
  )
  firstName:str|None = Field(
    default=None,
    title="first_name"
  )
  lastName:str|None = Field(
    default=None,
    title="last_name"
  )
  zones: Optional[List[str]] = Field(
    default=None,
    title="author zones"
  )
  updatedUserID:int|None = Field(
    default=None,
    title='updated user id'
  )
  createdUserID:int|None = Field(
    default=None,
    title='created user id'
  )
  institutions: Optional[List[IInstitution]] = Field(
    default=None,
    title="institutions"
  )
  
class IZone (BaseModel):
  name:str|None = Field(
    default=None,
    title="zone name"
  )