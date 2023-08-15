from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Robot

engine = create_engine("postgresql://postgres:123@localhost/")
engine.connect()

def create_new_robot(serial, location="No data"):
    new_robot = Robot(serial=serial, location=location)

    with Session(engine) as session:
        session.add(new_robot)
        session.commit()
    
    return 200, "Создан новый робот"


while True:
    if input('> ').lower() in ['new robot', 'nr']:
        serial = int(input('Serial\n> '))
        location = input("Location\n>")

        create_new_robot(serial, location)
        print('Robot succesfully created')
    else:
        print('Fuck you')
