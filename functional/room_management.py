from DBConnection import rooms_collection



# Fetch all rooms as a list
def fetch_rooms():
    return list(rooms_collection.find())

# Save the updated list of rooms
def save_rooms(rooms):
    rooms_collection.delete_many({})  # Clear the collection
    rooms_collection.insert_many(rooms)  # Insert updated rooms




# Add a new room
def add_room(room_number, room_type, price):
    valid_room_type = ['single', 'double', 'suite']
    rooms = fetch_rooms() 

    if room_type not in valid_room_type:
        return "Invalid room type. Please choose from: single, double, suite"

   
    for room in rooms:
        if room["roomNumber"] == room_number:
            return f"Room {room_number} already exists."

    new_room = {
        "roomNumber": room_number,
        "roomType": room_type,
        "price": price,
        "availability": True
    }

    rooms.append(new_room) 
    save_rooms(rooms)  
    return "Room added successfully!"



# List all rooms
def list_rooms():
    rooms = fetch_rooms()
    room_descriptions = []

    for room in rooms:
        status = "Available" if room["availability"] else "Occupied"
        room_descriptions.append(f"Room {room['roomNumber']}: {room['roomType']} - {room['price']} - {status}")
    
    return room_descriptions



# Book a room
def book_room(room_number):
    rooms = fetch_rooms()  
    new_rooms = []
    room_found = False

    for room in rooms:
        if room["roomNumber"] == room_number and room["availability"]:
            room_found = True
            new_rooms.append({**room, "availability": False})  # Update room availability
        else:
            new_rooms.append(room)

    if room_found:
        save_rooms(new_rooms)  # Save updated list to the database
        return f"Room {room_number} booked successfully."
    else:
        return f"Room {room_number} is not available."




# Release a room
def release_room(room_number):
    rooms = fetch_rooms()  
    new_rooms = []
    room_found = False

    for room in rooms:
        if room["roomNumber"] == room_number and not room["availability"]:
            room_found = True
            new_rooms.append({**room, "availability": True}) 
        else:
            new_rooms.append(room)

    if room_found:
        save_rooms(new_rooms)  
        return f"Room {room_number} cancellation successful."
    else:
        return f"Room {room_number} is already available."



