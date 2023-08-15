from sqlalchemy import MetaData, String, Integer, Column, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine


AuthBase = declarative_base()
DataBase = declarative_base()


class Robot(AuthBase):
    __tablename__ = "robots"
    
    id = Column(Integer, primary_key=True)
    telegram_ids = relationship("TelegramID", backref="robot")
    serial = Column(Integer, unique=True)
    location = Column(String, nullable=True, default=None)


class TelegramID(AuthBase):
    __tablename__ = 'telegram_ids'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    robot_id = Column(Integer, ForeignKey('robots.id'))


class RobotDataDB(DataBase):
    __tablename__ = "robot_data"
    serial = Column(Integer, primary_key=True, nullable=False)

    total_bags = Column(Integer, nullable=True)
    shift_bags = Column(Integer, nullable=True)

    left_status = Column(Integer, nullable=True)
    left_pallet_status = Column(Integer, nullable=True)

    right_status = Column(Integer, nullable=True)
    right_pallet_status = Column(Integer, nullable=True)

    connected = Column(Integer, nullable=True)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
