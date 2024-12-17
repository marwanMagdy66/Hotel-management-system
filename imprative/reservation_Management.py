from DBConnection import customers_collection, reservations_collection,rooms_collection
from bson import ObjectId
from datetime import datetime
def add_reservation(customer_id, room_number, check_in, check_out):
        customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
        if not customer:
            return print("Customer data not found.")

        room = rooms_collection.find_one({"roomNumber": room_number})
        if not room:
            return print("Room not found.")
        if not room.get('availability', False): 
            return print("Room is not available.")
        check_in_date=datetime.strptime(check_in,"%Y-%m-%d")
        check_out_date=datetime.strptime(check_out,"%Y-%m-%d")
        total_days=(check_out_date - check_in_date).days
        reservation = {
            "customerName": customer['name'],
            "customerEmail": customer['email'],
            "customerPhone": customer['phone'],
            "roomNumber": room_number,
            "checkIn": check_in,
            "checkOut": check_out,
            "totalDays":total_days
        }
        reservations_collection.insert_one(reservation)

        rooms_collection.update_one({"roomNumber": room_number}, {"$set": {"availability": False}})
        return print("Reservation added successfully.")

def list_reservations():
    reservations = reservations_collection.find()
    for reservation in reservations:
        print(f"Customer: {reservation['customerName']}\n {reservation['customerEmail']}\n {reservation['customerPhone']}\n Room: {reservation['roomNumber']}, Check-in: {reservation['checkIn']}, Check-out: {reservation['checkOut']}")