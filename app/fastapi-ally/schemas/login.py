from pydantic import BaseModel
from typing import Optional, Dict

# 请求体schema
class LoginRequest(BaseModel):
    username: str
    password: str

# 响应数据schema
class LoginResponse(BaseModel):
    code: int
    data: Optional[Dict[str, str]] = None
    msg: str
