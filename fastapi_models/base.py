from pydantic import BaseModel


class RobotData(BaseModel):
    serial: int
    
    total_bags: int
    shift_bags: int
    
    left_status: int
    left_pallet_status: int
    
    right_status: int
    right_pallet_status: int


class AuthTelegram(BaseModel):
    telegram_id: int
    serial: int


class RobotSerial(BaseModel):
    serial: int


class RobotOnData(BaseModel):
    serial: int
    connected: int