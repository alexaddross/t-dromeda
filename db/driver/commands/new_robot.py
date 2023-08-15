from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.models import Robot

engine = create_engine("postgresql://postgres:123@localhost/")
engine.connect()

def create_new_robot(serial, location="No data"):
    new_robot = Robot(serial=serial, location=location)

    with Session(engine) as session:
        session.add(new_robot)
        session.commit()
    
    return 200, "Создан новый робот"


serial = int(input('Serial\n> '))
location = input("Location\n>")

create_new_robot(serial, location)
