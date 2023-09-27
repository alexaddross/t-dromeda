from sqlalchemy import MetaData, String, Integer, Column, BigInteger, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine


AuthBase = declarative_base()
DataBase = declarative_base()


class Robot(AuthBase):
    __tablename__ = "robots"
    
    id = Column(BigInteger, primary_key=True)
    telegram_ids = relationship("TelegramID", backref="robot")
    serial = Column(BigInteger, unique=True)
    robot_type = Column(String, nullable=True, default=None)
    location = Column(String, nullable=True, default=None)


class TelegramID(AuthBase):
    __tablename__ = 'telegram_ids'

    id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger)
    robot_id = Column(BigInteger, ForeignKey('robots.id'))


class RobotDataDB(DataBase):
    __tablename__ = "robot_data"
    serial = Column(BigInteger, primary_key=True, nullable=False)

    total_bags = Column(BigInteger, nullable=True)
    shift_bags = Column(BigInteger, nullable=True)

    left_status = Column(BigInteger, nullable=True)
    left_pallet_status = Column(BigInteger, nullable=True)

    right_status = Column(BigInteger, nullable=True)
    right_pallet_status = Column(BigInteger, nullable=True)

    connected = Column(Integer, nullable=True)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
