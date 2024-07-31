from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from conf import BASE_DIR

# 创建数据库连接
engine = create_engine("sqlite:///" + BASE_DIR + "/db/social_auto_upload.db")

# 定义全局 session
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# 定义基础类
Base = declarative_base()


# 定义模型
class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    video_path = Column(String)
    Vide_uploaded_path = Column(String)
    cookies = Column(String)
    cookie_path = Column(String)


if not engine.dialect.has_table(engine, Account.__tablename__):
    Base.metadata.create_all(engine)
