from pydantic import BaseModel
from fastapi.responses import JSONResponse

from typing import Optional, Dict, Any

class ImageMetadata(BaseModel):
    image_name: str
    image_time: str
    placeholder: str
    
class ImageResponse(BaseModel):
    message:str
    filename:str
    image_name:str
    image_time:str
    image_url:str
    incident_type:str
    placeholder:str
class ImageListResponse(BaseModel):
    id:int
    image_name:str
    image_time:str
    image_url:str
    incident_type:str
    placeholder:str   
class ImageDeletResponse(BaseModel):
    id:int
    image_name:str
    image_time:str
    image_url:str
    incident_type:str
    placeholder:str   
    # media_type = "application/json"
    # def render(self, content: dict) -> bytes:
    #     return super().render(content)
