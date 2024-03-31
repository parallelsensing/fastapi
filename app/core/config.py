from pydantic import BaseSettings, AnyHttpUrl, validator, PostgresDsn, EmailStr
from typing import List, Union, Optional, Dict, Any

class Settings(BaseSettings):
  PROJECT_NAME:str = 'cpsi'
  BASE_URL:str = 'https://www.j-cpsi.com'
  CPSI_URL:str = 'https://www.j-cpsi.com'
  API_PATH:str = '/api/cpsi'
  API_JIST:str = '/api/jist'
  FILES_DIR:str = './files'
  SECRET_KEY: str = 'R8DN0ClowMT5dqDNPEwG4dq-d_p-bkzZoeYG0Ne94uY'
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
  EMAIL_TOKEN_EXPIRE_HOURS: int = 24 * 100


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
  @validator("BACKEND_CORS_ORIGINS", pre=True)
  def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    if isinstance(v, str) and not v.startswith("["):
      return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
      return v
    raise ValueError(v)
  POSTGRES_SERVER: str = "postgres"
  POSTGRES_USER: str = "casia"
  POSTGRES_PASSWORD: str = "2024"
  POSTGRES_DB: str = "cpsi"
  
  SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
  @validator("SQLALCHEMY_DATABASE_URI", pre=True)
  def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    if isinstance(v, str):
      return v
    return PostgresDsn.build(
      scheme="postgresql",
      user=values.get("POSTGRES_USER"),
      password=values.get("POSTGRES_PASSWORD"),
      host=values.get("POSTGRES_SERVER"),
      path=f"/{values.get('POSTGRES_DB') or ''}",
    )

settings = Settings()
