from DBConnection import customers_collection, reservations_collection, rooms_collection
from bson import ObjectId
from datetime import datetime


def fetch_customer(customer_id):
    return customers_collection.find_one({'_id': ObjectId(customer_id)})


def fetch_room(room_number):
    return rooms_collection.find_one({"roomNumber": room_number})


def calculate_total_days(check_in, check_out):
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    return (check_out_date - check_in_date).days


def create_reservation(customer, room_number, check_in, check_out, total_days):
    return {
        "customerName": customer['name'],
        "customerEmail": customer['email'],
        "customerPhone": customer['phone'],
        "roomNumber": room_number,
        "checkIn": check_in,
        "checkOut": check_out,
        "totalDays": total_days
    }


def is_room_available(room):
    return room.get('availability', False)


def book_room(room):
    return {**room, "availability": False}


def release_room(room):
    return {**room, "availability": True}


def add_reservation(customer_id, room_number, check_in, check_out):
    customer = fetch_customer(customer_id)
    if not customer:
        return "Customer data not found."

    room = fetch_room(room_number)
    if not room:
        return "Room not found."

    if not is_room_available(room):
        return "Room is not available."

    total_days = calculate_total_days(check_in, check_out)
    return create_reservation(customer, room_number, check_in, check_out, total_days)


def insert_reservation_to_db(reservation):
    reservations_collection.insert_one(reservation)


def update_room_availability(room_number, availability):
    rooms_collection.update_one(
        {"roomNumber": room_number},
        {"$set": {"availability": availability}}
    )


def book_reservation_and_update_db(customer_id, room_number, check_in, check_out):
    reservation = add_reservation(customer_id, room_number, check_in, check_out)

    if isinstance(reservation, str):
        return reservation

    insert_reservation_to_db(reservation)

    room = fetch_room(room_number)
    if room:
        updated_room = book_room(room)
        update_room_availability(room_number, updated_room['availability'])

    return "Reservation added successfully."


def list_reservations():
    reservations = reservations_collection.find()

    return list(map(
        lambda res: (
            f"Customer: {res['customerName']}, Email: {res['customerEmail']},\n"
            f"Phone: {res['customerPhone']}, Room: {res['roomNumber']},\n"
            f"Check-in: {res['checkIn']}, Check-out: {res['checkOut']}\n"
            f"Total Days: {res['totalDays']}\n"
            f"--------------------------------"
        ), reservations
    ))
