from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库设置
# DATABASE_URL = "postgresql://ally:20casia24@postgres/sensing"
DATABASE_URL = "postgresql://ally:20casia24@10.11.37.112:5431/sensing"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


