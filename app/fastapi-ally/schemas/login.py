from pydantic import BaseModel
from typing import Optional, Dict, Any

# 请求体schema
class LoginRequest(BaseModel):
    phone: str
    password: str

# 响应数据schema
class LoginResponse(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: str
