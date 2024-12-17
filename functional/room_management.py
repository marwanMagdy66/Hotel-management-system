from DBConnection import rooms_collection

def fetch_rooms():
    return list(rooms_collection.find())

def save_rooms(rooms):
    rooms_collection.delete_many({})  
    rooms_collection.insert_many(rooms)  

def validate_room_type():
    return ["Single", "Double", "Suite"]

# Add a new room
def add_room(room_number, room_type, price):
    rooms = fetch_rooms()

    if room_type not in validate_room_type():
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


#recursive function 
def list_rooms_recursive(rooms, index=0):
    if index == len(rooms):
        return ""

    room = rooms[index]
    room_info = (
        f"Room {room['roomNumber']}: {room['roomType']} - {room['price']} - "
        f"{'Available' if room['availability'] else 'Occupied'}\n"
    )
    return room_info + list_rooms_recursive(rooms, index + 1)


def list_rooms():
    rooms = fetch_rooms()
    return list_rooms_recursive(rooms)



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
