from typing import Set, Any, List, Optional
from pydantic import BaseModel,Field

class IInstitution(BaseModel):
  id:int|None = Field(
    default=None,
    title="id"
  )
  institution:str|None = Field(
    default='',
    title="institution"
  )
  department:str|None = Field(
    default=None,
    title="department"
  )
  address:str|None = Field(
    default='',
    title='address'
  )
  country:str|None = Field(
    default='',
    title='country'
  )
  province:str|None = Field(
    default='',
    title='province'
  )
  city:str|None = Field(
    default='',
    title='city'
  )
  postalCode:str|None = Field(
    default='',
    title='postal code'
  )
  phone:str|None = Field(
    default='',
    title="phone"
  )
  fax:str|None = Field(
    default='',
    title="fax"
  )
