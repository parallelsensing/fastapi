from pydantic import BaseModel
from typing import Optional, Dict, Any

# 用户信息模型
class UserInfo(BaseModel):
    username: Optional[str] = None
    nickname: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[int] = None
    class Config:
        orm_mode = True

# 用户请求模型
class UserCreate(BaseModel):
    username: str
    nickname: str
    password: str
    phone: str
    role: int


class UserResponse(BaseModel):
    code: int
    data: Optional[dict] = None
    msg: str

class UserResetPasswordRequest(BaseModel):
    phone: str
    old_password: str
    new_password: str
class UserForgotPasswordRequest(BaseModel):
    phone: str
    new_password: str