from pydantic import BaseModel, HttpUrl
from typing import Optional, Tuple, Any

# 项目模型
class ItemCreate(BaseModel):
    LngLat: Tuple[float, float]  # 经纬度坐标
    color: str
    image_url: str # HttpUrl  # 图片URL，使用Pydantic的HttpUrl类型进行简单验证
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True  

class ItemResponse(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: str

class ItemUploadResponse(BaseModel):
    message: str  # 成功或错误信息
    filename: str  # 成功上传的文件名
    image_name: str  # 上传的图片名字
    image_time: str  # 上传的图片时间
    placeholder: str  # 占位字段内容（如果有的话）