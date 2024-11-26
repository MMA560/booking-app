from sqlalchemy import Column,Integer,String,Float, ForeignKey, Date,Boolean
from sqlalchemy.orm import relationship,validates
from database import Base
from schemas import BookingUpdate
from datetime import date




class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key= True)
    username = Column(String,nullable=False)
    email = Column(String,nullable=False, unique=True)
    hashed_pw = Column(String)
    role =  Column(String, nullable= False , default='user')
    is_active = Column(Boolean, default=True)
    

    #Relationship user => booking
    bookings = relationship("Booking", back_populates="user")



class Room(Base):
    __tablename__ = 'rooms'

    room_id = Column(Integer, primary_key= True, index = True)
    room_name = Column(String, nullable= False, unique=True)
    room_type = Column(String, nullable= False)
    room_price = Column(Float,nullable=False)
    max_guest = Column(Integer,nullable=False, default=0)
    availability_status = Column(Boolean,default=True)
    image_url = Column(String)
    #Relationship room => booking
    bookings = relationship("Booking", back_populates="room")

class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer,primary_key=True)
    room_id = Column(Integer,ForeignKey('rooms.room_id'),nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'),nullable=False)
    check_in_date = Column(Date,nullable=False)
    check_out_date = Column(Date,nullable= False)
    confirmation = Column(Boolean, default=True)

    #Relationship  booking => room & booking => user
    room = relationship("Room", back_populates="bookings")
    user = relationship("User", back_populates="bookings")

    
    #Checking validation of check(in/out) dates
    @validates('check_out_date')
    def validate_dates(self, key, check_out_date):
        # تحقق من أن check_out_date هو كائن من نوع date
        if isinstance(check_out_date, BookingUpdate):
            # استخراج التاريخ الفعلي من كائن BookingUpdate
            check_out_date = check_out_date.new_check_out_date
        
        # تأكد أن check_in_date هو أيضًا كائن من نوع date
        if not isinstance(self.check_in_date, date):
            raise ValueError("Check-in date is not a valid date.")
        
        if check_out_date <= self.check_in_date:
            raise ValueError("Check-out date must be after check-in date.")
        
        return check_out_date


