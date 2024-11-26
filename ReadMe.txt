
# Hotel Management System Documentation

## Overview

This application is a Hotel Management System built using **FastAPI** for the backend and **Streamlit** for the frontend interface. It allows administrators to manage users, rooms, and bookings in a hotel setting. The application provides a RESTful API for interaction with the database, facilitating user management, room management, and booking management.

## Features

- User authentication with role-based access (admin and customer).
- Management of user accounts, including creation and deletion.
- Management of hotel rooms, including adding new rooms and checking availability.
- Booking management that includes creating, retrieving, updating, and deleting bookings.

## Technologies Used

- **FastAPI**: For building the API.
- **SQLAlchemy**: For database interactions.
- **Streamlit**: For creating the frontend user interface.
- **SQLite**: For database management (configured in `database.py`).

## API Endpoints

### User Management Endpoints

- **Create User**
  - **POST** `/users`
  - **Request Body**: User details (username, email, role, hashed password).
  - **Response**: User object if created successfully.

- **Login User**
  - **POST** `/login`
  - **Request Body**: Login credentials (username, password).
  - **Response**: Success message with user role and ID.

- **Get User by ID**
  - **GET** `/users/{user_id}`
  - **Response**: User object if found.

- **Get All Users**
  - **GET** `/users`
  - **Response**: List of all users.

- **Delete User**
  - **DELETE** `/users/{user_id}`
  - **Response**: Confirmation message.

### Room Management Endpoints

- **Create Room**
  - **POST** `/rooms`
  - **Request Body**: Room details (room name, type, price, max guests).
  - **Response**: Room object if created successfully.

- **Get Room by Name**
  - **GET** `/rooms/{room_name}`
  - **Response**: Room object if found.

- **Get All Rooms**
  - **GET** `/rooms`
  - **Response**: List of all rooms.

- **Get Available Rooms**
  - **GET** `/rooms-available`
  - **Query Parameters**: Check-in date, check-out date.
  - **Response**: List of available rooms for the specified dates.

- **Delete Room**
  - **DELETE** `/rooms/{room_id}`
  - **Response**: Confirmation message.

### Booking Management Endpoints

- **Create Booking**
  - **POST** `/bookings`
  - **Request Body**: Booking details (user ID, room ID, check-in date, check-out date).
  - **Response**: Booking object if created successfully.

- **Get Booking by ID**
  - **GET** `/bookings/{booking_id}`
  - **Response**: Booking object if found.

- **Get All Bookings**
  - **GET** `/bookings`
  - **Response**: List of all bookings.

- **Update Booking**
  - **PUT** `/bookings/{booking_id}`
  - **Request Body**: New check-out date.
  - **Response**: Updated booking object.

- **Get Bookings by User ID**
  - **GET** `/bookings/user/{user_id}`
  - **Response**: List of bookings for the specified user.

- **Delete Booking**
  - **DELETE** `/bookings/{booking_id}`
  - **Response**: Confirmation message.


   ```

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API at `http://localhost:8000`.

5. For the Streamlit frontend, run:
   ```bash
   streamlit run main.py
   ```

6. Access the frontend interface at `http://localhost:8501`.

## Usage

- Log in with admin credentials to manage users, rooms, and bookings.
- Use the sidebar in the Streamlit app to navigate between management options.
- Create, update, and delete users, rooms, and bookings as needed.

## Contributing

Feel free to fork the repository and make contributions. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
