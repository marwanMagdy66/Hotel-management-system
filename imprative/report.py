from DBConnection import Report_collection,rooms_collection,reservations_collection

def generate_occupancy_report():
    total_rooms = rooms_collection.count_documents({})
    occupied_rooms = rooms_collection.count_documents({"availability": False})
    occupancy_rate = (occupied_rooms / total_rooms) * 100
    report=Report_collection.insert_one({
        "total_rooms":total_rooms,
        "Occupied_Rooms":occupied_rooms,
        "Occupancy_Rate":occupancy_rate
    })
    print(f"--- Room Occupancy Report ---")
    print(f"Total Rooms: {total_rooms}")
    print(f"Occupied Rooms: {occupied_rooms}")
    print(f"Occupancy Rate: {occupancy_rate:.2f}%")

def generate_revenue_report():
    reservations = reservations_collection.find()
    total_revenue = 0
    for reservation in reservations:
        room = rooms_collection.find_one({"roomNumber": reservation["roomNumber"]})
        if room:
            duration = reservation["totalDays"]
            total_revenue += room["price"] * duration
    print(f"--- Revenue Report ---")
    print(f"Total Revenue: ${total_revenue:.2f}")


