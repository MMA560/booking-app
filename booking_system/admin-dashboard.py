import streamlit as st
import requests
from datetime import date
import base64
from crud import save_image

# Setting the API URL
API_URL = "http://localhost:8000"

# Login interface
def login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            user_data = response.json()
            if user_data.get("role") == "admin":
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("You do not have access to this application.")
                st.session_state["logged_in"] = False
        else:
            st.error("Login failed. Please check your username and password.")

# User management interface
def manage_users():
    st.title("Manage Users")
    try:
        response = requests.get(f"{API_URL}/users")
        users = response.json()
        st.write(users)

        st.subheader("Add New User")
        username = st.text_input("New Username")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["customer", "admin"])
        password = st.text_input("New Password", type="password")

        if st.button("Add User"):
            response = requests.post(f"{API_URL}/users", json={
                "username": username,
                "email": email,
                "role": role,
                "hashed_pw": password
            })
            if response.status_code == 200:
                st.success("User added successfully!")
            else:
                st.error("Failed to add user. Error: " + response.json().get("detail", "Unknown error"))

        
        # Delete user
        st.subheader("Delete User")
        user_id_delete = st.number_input("User ID to delete", min_value=1)
        if st.button("Delete User"):
            response = requests.delete(f"{API_URL}/users/{user_id_delete}")
            if response.status_code == 200:
                st.success("User deleted successfully!")
            else:
                st.error("Failed to delete user.")

    except Exception as e:
        st.error(f"Error retrieving users: {e}")

# Room management interface
def manage_rooms():
    st.title("Manage Rooms")
    try:
        response = requests.get(f"{API_URL}/rooms")
        rooms = response.json()
        st.write(rooms)

        st.subheader("Add New Room")
        room_name = st.text_input("Room Name")
        room_type = st.text_input("Room Type")
        room_price = st.number_input("Price per Night", min_value=0)
        max_guest = st.number_input("Max number of Guests", min_value=0)

        # حقل رفع الصورة من الجهاز
        room_image = st.file_uploader("Upload Room Image", type=["jpg", "jpeg", "png"])
        
        if st.button("Add Room"):
            if room_image is not None:
                image_data = room_image.read()
                image_filename = room_image.name
                image_path = save_image(image_data, image_filename)  
                
                response = requests.post(f"{API_URL}/rooms", json={
                    "room_name": room_name,
                    "room_type": room_type,
                    "room_price": room_price,
                    "max_guest": max_guest,
                    "image_url": image_path  
                })
                if response.status_code == 200:
                    st.success("Room added successfully!")
                else:
                    st.error("Failed to add room. Error: " + response.json().get("detail", "Unknown error"))
            else:
                st.error("Please upload an image for the room.")

        # Get available rooms
        st.title("Available Rooms Checker")
        check_in_date = st.date_input("Check-in Date", min_value=date.today())
        check_out_date = st.date_input("Check-out Date", min_value=check_in_date)
        if st.button("Check Available Rooms"):
            if check_in_date >= check_out_date:
                st.error("Check-out date must be after check-in date.")
            else:
                response = requests.get(f"{API_URL}/rooms-available", params={
                    "check_in": check_in_date,
                    "check_out": check_out_date
                })
                if response.status_code == 200:
                    available_rooms = response.json()
                    st.write("API Response:", available_rooms)
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

        # Delete room
        st.subheader("Delete Room")
        room_id_delete = st.number_input("Room ID to delete", min_value=1)
        if st.button("Delete Room"):
            response = requests.delete(f"{API_URL}/rooms/{room_id_delete}")
            if response.status_code == 200:
                st.success("Room deleted successfully!")
            else:
                st.error("Failed to delete room.")

    except Exception as e:
        st.error(f"Error retrieving rooms: {e}")

# Booking management interface
def manage_bookings():
    st.title("Manage Bookings")
    try:
        response = requests.get(f"{API_URL}/bookings")
        bookings = response.json()
        st.write(bookings)

        st.subheader("Add New Booking")
        booking_user_id = st.number_input("User ID for booking", min_value=1)
        booking_room_id = st.number_input("Room ID for booking", min_value=1)
        check_in_date = st.date_input("Check in Date")
        check_out_date = st.date_input("Check out Date")

        if st.button("Add Booking"):
            response = requests.post(f"{API_URL}/bookings", json={
                "user_id": booking_user_id,
                "room_id": booking_room_id,
                "check_in_date": str(check_in_date),
                "check_out_date": str(check_out_date)
            })
            if response.status_code == 200:
                st.success("Booking added successfully!")
            else:
                st.error("Failed to add booking. Error: " + response.json().get("detail", "Unknown error"))

        # Display bookings with room images
        st.subheader("Users Bookings")
        for booking in bookings:
            st.write(f"Booking ID: {booking['booking_id']}, Room ID: {booking['room_id']}, "
                     f"Check-in: {booking['check_in_date']}, Check-out: {booking['check_out_date']}")
            
            # Get room details
            room_response = requests.get(f"{API_URL}/rooms/{booking['room_id']}")
            if room_response.status_code == 200:
                room = room_response.json()
                if room.get('image_url'):
                    st.image(room['image_url'], caption=room['room_name'], use_column_width=True)
                else:
                    st.warning(f"No image available for Room ID: {booking['room_id']}.")
            else:
                st.error(f"Failed to retrieve room details for Room ID: {booking['room_id']}. Error: {room_response.status_code}")

        # Edit booking
        st.subheader("Edit Booking")
        booking_id = st.number_input("Booking ID to edit", min_value=1)
        if st.button("Retrieve Booking Details"):
            booking_details = requests.get(f"{API_URL}/bookings/{booking_id}").json()
            st.write(booking_details)

        new_check_out_date = st.date_input("New check out date")
        if st.button("Update Booking"):
            response = requests.put(f"{API_URL}/bookings/{booking_id}", json={
                'new_check_out_date': str(new_check_out_date)
            })
            if response.status_code == 200:
                st.success("Booking updated successfully!")
            else:
                st.error(f"Failed to update booking. Error: {response.text}")

        # Delete booking
        st.subheader("Delete Booking")
        booking_id_delete = st.number_input("Booking ID to delete", min_value=1)
        if st.button("Delete Booking"):
            response = requests.delete(f"{API_URL}/bookings/{booking_id_delete}")
            if response.status_code == 200:
                st.success("Booking deleted successfully!")
            else:
                st.error("Failed to delete booking.")

    except Exception as e:
        st.error(f"Error retrieving bookings: {e}")

# Main function to run the application
def main():
    if "logged_in" not in st.session_state:
        login()  # Show login if not logged in
    else:
        if st.session_state.get("logged_in"):
            st.sidebar.title("Control Panel")
            option = st.sidebar.selectbox("Choose Function", 
                                            ["Manage Users", "Manage Rooms", "Manage Bookings"])

            if option == "Manage Users":
                manage_users()  # Show user management options
            elif option == "Manage Rooms":
                manage_rooms()  # Show room management options
            elif option == "Manage Bookings":
                manage_bookings()  # Show booking management options
        else:
            st.error("You need to log in to access the application.")

if __name__ == "__main__":
    main()
