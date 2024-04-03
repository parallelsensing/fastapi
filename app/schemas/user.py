from pydantic import BaseModel
from typing import Optional, Dict, Any

# 用户信息模型
class UserInfo(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    class Config:
        orm_mode = True

# 用户请求模型
class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    phone: str


class UserResponse(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: str