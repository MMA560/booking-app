from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas, auth
from datetime import date



# CRUD operations for users
def create_user(db: Session, user: schemas.UserCreate):
    user_existing = db.query(models.User).filter(models.User.email == user.email).first()
    if user_existing:
        raise HTTPException(status_code=401, detail='Email already registered.')
    hash_pw = auth.hash_password(user.hashed_pw)
    user.hashed_pw = hash_pw
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user

def login_user(db : Session, username : str , password : str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        if auth.verify_password(password,user.hashed_pw):
            return user
        
    return None
    
def get_user_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}



# CRUD operations for rooms
def create_room(db: Session, room: schemas.RoomCreate):
    existing_room = db.query(models.Room).filter(models.Room.room_name == room.room_name).first()
    if existing_room:
        raise HTTPException(status_code=400, detail='Room name already exists.') 
    new_room = models.Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

def get_room(db: Session, room_id: int):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


def get_available_rooms(db: Session, check_in:date , check_out: date):

    rooms = db.query(models.Room).all()

    
    available_rooms = []

   
    for room in rooms:
        
        overlapping_booking = db.query(models.Booking).filter(
            models.Booking.room_id == room.room_id,
            and_(
                models.Booking.check_in_date < check_out,  
                models.Booking.check_out_date > check_in   
            )
        ).first()

        
        if not overlapping_booking:
            available_rooms.append(room)

    return available_rooms


def get_rooms(db: Session):
    return db.query(models.Room).all()


def delete_room(db: Session, room_id: int):
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"detail": "Room deleted successfully"}


# CRUD operations for bookings
def create_booking(db: Session, booking: schemas.BookingCreate):
    # Check if room is available during the booking period
    existing_booking = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        models.Booking.check_in_date < booking.check_out_date,
        models.Booking.check_out_date > booking.check_in_date
    ).first()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="Room is already booked for this period.")
    room = db.query(models.Room).filter(models.Room.room_id == booking.room_id).first()
    if not room:
        raise HTTPException(status_code= 404, detail=f"No room with id : {booking.room_id} found")
    new_booking = models.Booking(**booking.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def get_booking(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

def get_bookings_by_user_id(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

def update_booking(db: Session, booking_id: int, new_check_out_date: date):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if booking:
        booking.check_out_date = new_check_out_date  # تمرير التاريخ كـ date
        db.commit()
        db.refresh(booking)
    return booking
    
def get_bookings(db: Session):
    return db.query(models.Booking).filter(models.Booking.confirmation == True).all()

def delete_booking(db: Session, booking_id: int):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking deleted successfully"}


from PIL import Image
import os

# تحديد مسار مجلد الصور
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')  # المسار النسبي للمجلد

# التأكد من وجود المجلد، وإذا لم يكن موجودًا، إنشائه
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def save_image(image_data, filename):
    file_path = os.path.join(IMAGE_FOLDER, filename)
    with open(file_path, "wb") as f:
        f.write(image_data)
    return file_path
