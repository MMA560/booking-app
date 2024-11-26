from fastapi import FastAPI, HTTPException,  Depends
from sqlalchemy.orm import Session
from datetime import date
from database import Base, get_db, engine
import crud, schemas



Base.metadata.create_all(bind= engine)

app = FastAPI()

#End points of users

@app.post('/users')
def create_user( user : schemas.UserCreate,db :Session = Depends(get_db)):
    return crud.create_user(db , user)

@app.post('/login')
def login(user_login : schemas.UserLogin, db : Session = Depends(get_db)):
    user=  crud.login_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=401 , detail='Login failed')
    return {'msg':'login successful',
            'user':user_login.username,
            'role' : user.role,
            'id':user.user_id}

@app.get('/users/{user_id}')
def get_user(user_id : int, db : Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db , user_id)
    if not db_user:
        raise HTTPException(status_code= 404, detail='User not found')
    return db_user

@app.get('/users')
def get_users(db : Session = Depends(get_db)):
    return crud.get_users(db)

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


#End points of rooms
@app.post('/rooms')
def create_room(room : schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db , room)

@app.get('/rooms/{room_id}')
def get_room(room_id : int , db : Session = Depends(get_db)):
    room = crud.get_room(db,room_id)
    if not room:
        raise HTTPException(status_code=404, detail='Room not Found')
    return room

@app.get('/rooms')
def get_rooms(db : Session = Depends(get_db)):
    return crud.get_rooms(db)

@app.get('/rooms-available')
def get_available_rooms(check_in : date, check_out : date,db : Session = Depends(get_db)):
    return crud.get_available_rooms(db,check_in , check_out)

@app.delete('/rooms/{room_id}')
def delete_room(room_id: int, db: Session = Depends(get_db)):
    return crud.delete_room(db, room_id)



#End points of bookings
@app.post('/bookings')
def create_booking(booking : schemas.BookingCreate, db : Session = Depends(get_db)):
    return crud.create_booking(db, booking)

@app.get('/bookings/{booking_id}')
def get_booking(booking_id : int, db : Session = Depends(get_db)):
    booking = crud.get_booking(db , booking_id)
    if not booking :
        raise HTTPException(status_code= 404, detail='Booking not found')
    return booking
@app.get('/bookings')
def get_bookings(db : Session = Depends (get_db)):
    return crud.get_bookings(db)

@app.put('/bookings/{booking_id}')
def update_booking(booking_id: int, new_check_out_date: schemas.BookingUpdate, db: Session = Depends(get_db)):
    booking = crud.update_booking(db, booking_id, new_check_out_date)
    
    if not booking:
        raise HTTPException(status_code=404, detail='Booking not found')
    return booking

@app.get('/bookings/user/{user_id}')
def get_bookings_of_user(user_id : int, db : Session = Depends(get_db)):
    bookings = crud.get_bookings_by_user_id(db, user_id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings

@app.delete('/bookings/{booking_id}')
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    return crud.delete_booking(db, booking_id)
