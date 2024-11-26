import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

def user_login():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            user_data = response.json()

            if user_data.get("role") in ["customer", "user"]:
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["id"] = user_data.get("id")
            else:
                st.error("You do not have access to this application.")
                st.session_state["logged_in"] = False
        else:
            st.error("Login failed. Please check your username and password.")

def view_available_rooms():
    st.title("Check Available Rooms")
    
    check_in_date = st.date_input("Check-in Date", min_value=date.today())
    check_out_date = st.date_input("Check-out Date", min_value=check_in_date)
    
    if st.button("Search for Available Rooms"):
        if check_in_date >= check_out_date:
            st.error("Check-out date must be after check-in date.")
        else:
            response = requests.get(f"{API_URL}/rooms-available", params={
                "check_in": check_in_date,
                "check_out": check_out_date
            })
            
            if response.status_code == 200:
                available_rooms = response.json()
                
                if available_rooms:
                    st.success(f"Available rooms from {check_in_date} to {check_out_date}:")
                    for room in available_rooms:
                        st.write(f"Room ID: {room['room_id']}, Type: {room['room_type']}, Price: {room['room_price']}")
                        if room.get('image_url'):
                            st.image(room['image_url'], caption=room['room_name'], use_column_width=True)
                else:
                    st.warning("No rooms available for the selected dates.")
            else:
                st.error(f"Failed to fetch available rooms. Error: {response.status_code}")

def manage_user_bookings():
    st.title("Manage Your Bookings")
    
    # عرض الحجوزات الحالية
    st.subheader("Your Bookings")
    try:
        username = st.session_state.get("username")
        user_id = st.session_state.get("id")
        if username:
            response = requests.get(f"{API_URL}/bookings/user/{user_id}")
            if response.status_code == 200:
                bookings = response.json()
                if bookings:
                    for booking in bookings:
                        st.write(f"Booking ID: {booking['booking_id']}, Room ID: {booking['room_id']}, "
                                 f"Check-in: {booking['check_in_date']}, Check-out: {booking['check_out_date']}")
                        
                        room_id = booking['room_id']
                        
                        room_response = requests.get(f"{API_URL}/rooms/{room_id}")
                        if room_response.status_code == 200:
                            room = room_response.json()
                            if room.get('image_url'):
                                st.image(room['image_url'], caption=room['room_name'], use_column_width=True)
                            else:
                                st.warning(f"No image available for Room ID: {room_id}.")
                        elif room_response.status_code == 404:
                            st.error(f"Room ID {room_id} does not exist in the database.")
                        else:
                            st.error(f"Failed to retrieve room details. Error: {room_response.status_code} - {room_response.text}")
                else:
                    st.info("No bookings found.")
            else:
                st.error(f"Failed to retrieve bookings. Error: {response.status_code} - {response.text}")
        else:
            st.error("Please log in first.")
    
    except Exception as e:
        st.error(f"Error retrieving bookings: {e}")

    # New booking
    st.subheader("New Booking")
    booking_room_id = st.number_input("Room ID for booking", min_value=1)
    check_in_date = st.date_input("Check-in Date")
    check_out_date = st.date_input("Check-out Date", min_value=check_in_date)

    # Retrieve room price before booking
    if booking_room_id:
        room_response = requests.get(f"{API_URL}/rooms/{booking_room_id}")
        if room_response.status_code == 200:
            room = room_response.json()
            st.write(f"Room Name: {room['room_name']}")
            st.write(f"Room Price: {room['room_price']} per night")
            if room.get('image_url'):
                st.image(room['image_url'], caption=room['room_name'], use_column_width=True)
        else:
            st.warning("Room image not found or room does not exist.")
    
    if st.button("Confirm Booking"):
        if check_in_date >= check_out_date:
            st.error("Check-out date must be after check-in date.")
        else:
            response = requests.post(f"{API_URL}/bookings", json={
                "user_id": st.session_state.get("id"),  
                "room_id": booking_room_id,
                "check_in_date": str(check_in_date),
                "check_out_date": str(check_out_date)
            })
            
            if response.status_code == 200:
                st.success("Booking added successfully!")
                # Get room details
                if room.get('image_url'):
                    st.image(room['image_url'], caption=room['room_name'], use_column_width=True)
            else:
                st.error(f"Failed to add booking. Error: {response.text}")

def main():
    if "logged_in" not in st.session_state:
        user_login()  
    else:
        if st.session_state.get("logged_in"):
            st.sidebar.title("User Control Panel")
            option = st.sidebar.selectbox("Choose Function", 
                                          ["View Available Rooms", "Manage Bookings"])
            
            if option == "View Available Rooms":
                view_available_rooms()  
            elif option == "Manage Bookings":
                manage_user_bookings()  
        else:
            st.error("You must be logged in to access this application.")

if __name__ == "__main__":
    main()
