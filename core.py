from fastapi import APIRouter
from starlette import status
from starlette.responses import Response
from fastapi_models.base import RobotData
from fastapi_models.base import AuthTelegram
from fastapi_models.base import RobotSerial
from fastapi_models.base import RobotOnData
from fastapi_models.base import TelegramAccount
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import requests

import uvicorn

import sqlalchemy
from sqlalchemy.orm import Session
from db.models import DataBase, RobotDataDB, Robot, TelegramID

from config import *



app = FastAPI()
api_router = APIRouter()

memory_engine = sqlalchemy.create_engine('sqlite:///:memory:')
memory_engine.connect()
DataBase.metadata.create_all(memory_engine)

auth_engine = sqlalchemy.create_engine("postgresql://postgres:123@localhost/")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@api_router.post('/put_robot_data/')
async def get_robot_data(*, body: RobotData):
    with Session(memory_engine) as session:
        new_robot_data = RobotDataDB(
            serial=body.serial,
            total_bags=body.total_bags,
            shift_bags = body.shift_bags,
            left_status = body.left_status,
            left_pallet_status = body.left_pallet_status,
            right_status = body.right_status,
            right_pallet_status = body.right_pallet_status
        )

        session.merge(new_robot_data)
        session.commit()

    return Response(status_code=status.HTTP_200_OK)


@api_router.post('/robot_on')
async def robot_on(body: RobotOnData):
    with Session(memory_engine) as session:
        new_robot_data = RobotDataDB(
            serial=body.serial,
            connected=body.connected
        )

        session.merge(new_robot_data)
        session.commit()

    return Response(status_code=status.HTTP_200_OK)


@api_router.post('/system_on')
async def system_startup(body: RobotSerial):
    with Session(auth_engine) as session:
        robot: Robot = session.query(Robot).where(Robot.serial == body.serial).one()
        tg_ids: list[TelegramID] = robot.telegram_ids

    for tg_id in tg_ids:
        print(requests.post(f"https://api.telegram.org/bot6343881202:AAEBAXFJMKTcIunpBkXfzoAIZiT8vp2F0Z0/sendMessage?chat_id={tg_id.group_id}&text=Система паллетизации запущена").content)


@api_router.post('/new_auth')
async def new_authentificated_user(body: AuthTelegram):
    with Session(auth_engine) as session:
        matches = session.query(Robot).where(Robot.serial == body.serial).all()
        
        if len(matches) >= 1:
            new_tg_node = TelegramID(group_id=body.telegram_id)
            for match in matches:
                if match.telegram_ids is None:
                    match.telegram_ids = new_tg_node
                else:
                    match.telegram_ids.append(new_tg_node)

            session.add(new_tg_node)
            session.add_all(matches)
            session.commit()

            return Response(status_code=status.HTTP_202_ACCEPTED)
        else:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    

@api_router.get('/get_robot_data')
async def get_robot_data(body: TelegramAccount):
    with Session(memory_engine) as session:
        with Session(auth_engine) as auth:
            records: list[AuthTelegram] = auth.query(AuthTelegram).where(AuthTelegram.telegram_id == body.telegram_id).all()

        for record in records:
            result = session.query(RobotDataDB).where(RobotDataDB.serial==record.serial).one()
    
    return Response(content=str(result.as_dict()), status_code=status.HTTP_200_OK)


app.include_router(api_router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
