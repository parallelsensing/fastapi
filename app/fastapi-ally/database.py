from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # 示例使用SQLite

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # 仅限SQLite。其他数据库不需要这个参数
)

# 创建Session本地实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建一个Base类，所有模型都将继承这个类
Base = declarative_base()

# 依赖函数，用于获取数据库会话实例
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
