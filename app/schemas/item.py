from pydantic import BaseModel, HttpUrl
from typing import Optional, Tuple, Any

# 项目模型
class ItemCreate(BaseModel):
    coordinates: Tuple[float, float]  # 经纬度坐标
    color: str
    image_url: HttpUrl  # 图片URL，使用Pydantic的HttpUrl类型进行简单验证
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True  # 如果你想从ORM模型创建Pydantic模型，需要这个配置

class ItemResponse(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: str

