from DBConnection import rooms_collection

def fetch_rooms():
    return list(rooms_collection.find())

def save_rooms(rooms):
    rooms_collection.delete_many({})  
    rooms_collection.insert_many(rooms)  


# Add a new room
def add_room(room_number, room_type, price):
    valid_room_types = {'single', 'double', 'suite'}
    rooms = fetch_rooms()

    if room_type not in valid_room_types:
        return "Invalid room type. Please choose from: single, double, suite"

    if any(room["roomNumber"] == room_number for room in rooms):
        return f"Room {room_number} already exists."

    new_room = {
        "roomNumber": room_number,
        "roomType": room_type,
        "price": price,
        "availability": True
    }

    save_rooms(rooms + [new_room])  
    return "Room added successfully!"



def list_rooms():
    rooms = fetch_rooms()
    return [
        f"Room {room['roomNumber']}: {room['roomType']} - {room['price']} - "
        f"{'Available' if room['availability'] else 'Occupied'}"
        for room in rooms
    ]



def booking_room(room_number):
    rooms = fetch_rooms()

    updated_rooms = list(
        map(lambda room: {**room, "availability": False} if room["roomNumber"] == room_number and room["availability"] else room, rooms)
    )

    if rooms == updated_rooms: 
        return f"Room {room_number} is not available."

    save_rooms(updated_rooms)
    return f"Room {room_number} booked successfully."


# Release a room
def release2_room(room_number):
    rooms = fetch_rooms()

    updated_rooms = list(
        map(lambda room: {**room, "availability": True} if room["roomNumber"] == room_number and not room["availability"] else room, rooms)
    )

    if rooms == updated_rooms:  # No room was updated
        return f"Room {room_number} is already available."

    save_rooms(updated_rooms)
    return f"Room {room_number} cancellation successful."
