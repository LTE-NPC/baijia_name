from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/baijia?charset=utf8", max_overflow=5,
                       encoding='utf-8')
Base = declarative_base()


class BaijiaName(Base):
    __tablename__ = 'baijia_name'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键，自增
    name = Column(String(512))
    gender = Column(String(4))

    def __repr__(self):
        output = "(%s,%s)" % (self.id, self.name)
        return output


Base.metadata.create_all(engine)
