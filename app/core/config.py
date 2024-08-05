from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, EmailStr, field_validator
from typing import List, Union, Optional, Dict, Any
import os
class Settings():
    IMAGE_DIR: str

    def __init__(self, **data) -> None:
        self.IMAGE_DIR = self.GetImageDir()
    
    
    
    PROJECT_NAME: str = 'sensing'
    BASE_URL: str = 'https://www.j-sensing.com'
    sensing_URL: str = 'https://www.j-sensing.com'
    API_PATH: str = '/api/sensing'
    API_JIST: str = '/api/jist'
    FILES_DIR: str = './files'
    SECRET_KEY: str = 'R8DN0ClowMT5dqDNPEwG4dq-d_p-bkzZoeYG0Ne94uY'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAIL_TOKEN_EXPIRE_HOURS: int = 24 * 100

    OPENAI_API_KEY:str = ""
    OPENAI_BASE_URL:str =  "http://10.116.123.30:9997/v1"
    LLM_MODEL = "glm-4v"

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = 'smtp.office365.com'
    SMTP_USER: Optional[str] = 'aaa'
    SMTP_PASSWORD: Optional[str] = 'bbb'
    EMAILS_FROM_EMAIL: Optional[EmailStr] = 'pub@agist.org'
    EMAILS_FROM_NAME: Optional[str] = 'Journal of Cyber-Physical-Social Intelligence'

    ACCORD_TEMPLATE: str = './app/templates/accord.pdf'

    COMMENT_EXPIRE_WEEKS: int = 6
    REVIEW_RESPONSE_BUSSINESS_DAYS: int = 3
    REVIEW_EXPIRE_DAYS: int = 30

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:9701", "http://localhost:9711"]
    
    # @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = "casia"
    POSTGRES_PASSWORD: str = "2024"
    POSTGRES_DB: str = "sensing"
  
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    
    # @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )
    def GetImageDir(self) -> str:
        # 获取当前脚本文件的绝对路径
        current_file_path = os.path.abspath(__file__)
        # 获取项目根目录的路径
        project_root = os.path.dirname(os.path.dirname(current_file_path))
        # 构造文件保存目录路径
        UPLOAD_DIR = os.path.join(project_root, "uploads")
        # 确保文件保存目录存在
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        return UPLOAD_DIR
settings = Settings()