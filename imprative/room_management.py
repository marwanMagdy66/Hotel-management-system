from DBConnection import rooms_collection
def add_room(room_number,room_type,price):
    valid_room_type=['single','double','suite']
    if room_type not in valid_room_type:
        print(f"Invalid room type. Please choose from: {','.join(valid_room_type)}")
        return
    room={
        "roomNumber":room_number,
        "roomType":room_type,
        "price":price,
        "availability":True
    }
    
    rooms_collection.insert_one(room)
    print("room added successfully !")


#show all rooms 
def list_rooms():
    rooms = rooms_collection.find()
    for room in rooms:
                status = "Available" if room["availability"] else "Occupied"
                print(f"Room {room['roomNumber']}: {room['roomType']} - {room['price']} - {status}")
                                                                


#reservations room 
def book_room(room_number):
    room = rooms_collection.find_one({"roomNumber": room_number, "availability": True})
    if room:
        rooms_collection.update_one({"roomNumber": room_number}, {"$set": {"availability": False}})
        print(f"Room {room_number} booked successfully.")
    else:
        print(f"Room {room_number} is not available.")
       

### delete book 
def release_room(room_number):
     room = rooms_collection.find_one({"roomNumber": room_number, "availability": False})
     if room:
          rooms_collection.update_one({"roomNumber": room_number}, {"$set": {"availability": True}})
          print(f"Room {room_number} room canceld successfully.")
     else:
        print(f"Room {room_number} is already available.")
        

                                                                    