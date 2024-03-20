from typing import Any
from pydantic import BaseModel,Field

from app.core.error import ERR_RES

class IResponse(BaseModel):
  code:int|str = Field(
    default=0,
    title="error code"
  )
  msg:str = Field(
    default='',
    title='error message'
  )
  data:Any = None
  def setErr(self, code:int):
    self.code = code
    self.msg = ERR_RES[code]

