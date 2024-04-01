from pydantic import BaseModel,Field
from enum import Enum
from typing import Set, Any, List, Optional

class IAccount(BaseModel):
  email:str|None = Field(
    default=None,
    title="user email"
  )
  password:str|None = Field(
    default=None,
    title='user password'
  )

class IAdminInvite(BaseModel):
  email:str = Field(
    default=None,
    title="email"
  )
  articleID:int|None = Field(
    default=None,
    title="article id"
  )
  status:int = Field(
    default=0,
    title="status"
  )
class IAdminStatusType(str, Enum):
  Login = 0 # 待登录
  Manuscript = 1 # 待提交
  Sign = 2 # 待签署
  Proof = 3 # 待证明
  Publish = 4 # 待发布

class ICreateAccount(IAccount):
  repassword:str|None = Field(
    default=None,
    title='user password confirm'
  )
  agree:bool = Field(
    default=False,
    title="agree private policy"
  )

class IUser(IAccount):
  authorID:int|None = Field(
    default=None,
    title='author id'
  )

class IUserSearch(BaseModel):
  email:str|None = Field(
    default=None,
    title='email'
  )
  exclude:int|None = Field(
    default=None,
    title='exclude user id'
  )
  privileges:Set[int]|None = Field(
    default=None,
    title='Role privilleges'
  )


class IToken(BaseModel):
  token:str|None = None
