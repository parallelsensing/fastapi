from pydantic import BaseModel
from typing import Optional, Dict

# 用户信息模型
class UserInfo(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
