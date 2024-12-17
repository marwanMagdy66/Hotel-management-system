from bson import ObjectId
from datetime import datetime
from DBConnection import customers_collection, rooms_collection, reservations_collection

# Fetch customer by ID
def fetch_customer(customer_id):
    customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
    if not customer:
        return None
    return {
        "id": str(customer["_id"]),
        "name": customer.get("name"),
        "email": customer.get("email"),
        "phone": customer.get("phone")
    }

# Fetch room by room number
def fetch_room(room_number):
    room = rooms_collection.find_one({"roomNumber": room_number})
    if not room:
        return None
    return {
        "roomNumber": room["roomNumber"],
        "availability": room.get("availability", False),
        "type": room.get("type", "Standard")
    }

# Prepare reservation object
def prepare_reservation(customer, room, check_in, check_out):
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    total_days = (check_out_date - check_in_date).days

    return {
        "customerName": customer["name"],
        "customerEmail": customer["email"],
        "customerPhone": customer["phone"],
        "roomNumber": room["roomNumber"],
        "checkIn": check_in,
        "checkOut": check_out,
        "totalDays": total_days
    }

# Update room availability (pure function)
def update_room_data(room, availability):
    updated_room = room.copy()
    updated_room["availability"] = availability
    return updated_room

# Add a reservation functionally
def add_reservation(customer_id, room_number, check_in, check_out):
    customer = fetch_customer(customer_id)
    if not customer:
        return "Customer data not found."

    room = fetch_room(room_number)
    if not room:
        return "Room not found."

    if not room['availability']:
        return "Room is not available."

    # Prepare the reservation object
    reservation = prepare_reservation(customer, room, check_in, check_out)

    # Prepare the updated room data
    updated_room = update_room_data(room, availability=False)

    return {
        "reservation": reservation,
        "updated_room": updated_room
    }

# Save reservation and update room availability (side effect handler)
def save_reservation_and_update_room(data):
    reservations_collection.insert_one(data["reservation"])
    rooms_collection.update_one(
        {"roomNumber": data["updated_room"]["roomNumber"]},
        {"$set": {"availability": data["updated_room"]["availability"]}}
    )
    return "Reservation added successfully."

# List all reservations
def fetch_reservations():
    reservations = list(reservations_collection.find())
    return [
        {
            "customerName": reservation["customerName"],
            "customerEmail": reservation["customerEmail"],
            "customerPhone": reservation["customerPhone"],
            "roomNumber": reservation["roomNumber"],
            "checkIn": reservation["checkIn"],
            "checkOut": reservation["checkOut"]
        }
        for reservation in reservations
    ]

def list_reservations():
    reservations = fetch_reservations()
    reservation_descriptions = [
        (
            f"---------------------------------------\n"
            f"Customer Name: {reservation['customerName']}\n"
            f"Email: {reservation['customerEmail']}\n"
            f"Phone: {reservation['customerPhone']}\n"
            f"Room Number: {reservation['roomNumber']}\n"
            f"Check-in: {reservation['checkIn']}\n"
            f"Check-out: {reservation['checkOut']}\n"
            f"---------------------------------------\n"
        )
        for reservation in reservations
    ]
    return '\n'.join(reservation_descriptions)
