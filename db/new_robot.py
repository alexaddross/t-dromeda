from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Robot

engine = create_engine("postgresql://postgres:123@localhost/")
engine.connect()


def create_new_robot(serial, location="No data", robot_type="No data"):
    new_robot = Robot(serial=serial, location=location, robot_type=robot_type)

    with Session(engine) as session:
        session.add(new_robot)
        session.commit()
    
    return 200, "Создан новый робот"


while True:
    if input('> ').lower() in ['new robot', 'nr']:
        serial = int(input('Serial\n> '))
        location = input('Location\n> ')
        robot_type = input('Robot Type\n> ')

        response = create_new_robot(serial, location, robot_type)
        print(response)
    else:
        print('Fuck you')
