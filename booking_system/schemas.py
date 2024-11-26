from pydantic import BaseModel, validator
from typing import Optional
from datetime import date



class UserBase(BaseModel):
    username: str
    email: str  #Check email validation
    role : str

#For create new user
class UserCreate(UserBase):
    hashed_pw: str

#For user login
class UserLogin(BaseModel):
    username : str
    password : str

#For user response
class User(UserBase):
    id: int
    is_active: bool

    class Config:  
        from_attributes = True

#For create new room
class RoomCreate(BaseModel):
    room_name: str
    room_type: str
    room_price: float
    max_guest: int
    image_url : str

#For room response model
class Room(RoomCreate):
    room_id: int
    room_availability: bool

    class Config:
        ofrom_attributes = True

#For create new booking
class BookingCreate(BaseModel):
    room_id: int
    user_id: int
    check_in_date: date
    check_out_date: date
    
#For booking response model
class Booking(BookingCreate):
    booking_id: int
    confirmation: bool

    class Config:  
        from_attributes = True


class BookingUpdate(BaseModel):
    new_check_out_date: date


    
