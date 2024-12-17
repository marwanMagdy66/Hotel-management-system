from DBConnection import Bill_collection, rooms_collection, reservations_collection

def calculate_services_charges(services):
    service_costs = {'meals': 50, 'internet': 20, 'laundry': 30}
    return sum(service_costs.get(service, 0) for service in services)

def calculate_total_price(base_price, days, services_charges):
    return (base_price * days) + services_charges

def calculate_tax(total_price, tax_rate):
    return total_price * tax_rate

def calculate_discount(total_price, tax, discount_rate):
    discount_amount = total_price * discount_rate / 100
    if discount_amount > total_price + tax:
        discount_amount = total_price + tax
    return discount_amount

def generate_bill(customer_name, room_number, services=None, tax_rate=0.1, discount=0):
    room = rooms_collection.find_one({"roomNumber": room_number})
    if not room:
        raise ValueError("Room not found")
    
    reservation = reservations_collection.find_one({"roomNumber": room['roomNumber']})
    if not reservation:
        raise ValueError("Reservation not found")
    
    base_price = room['price']
    services_charges = calculate_services_charges(services or [])
    total_price = calculate_total_price(base_price, reservation['totalDays'], services_charges)
    tax = calculate_tax(total_price, tax_rate)
    discount_amount = calculate_discount(total_price, tax, discount)
    
    bill_amount = total_price + tax - discount_amount
    
    bill_data = {
        "customerName": customer_name,
        "roomNumber": room_number,
        "services": services,
        "billAmount": bill_amount,
        "details": {
            "roomCost": base_price,
            "additionalServices": services_charges,
            "subtotal": total_price,
            "tax": tax,
            "discount": discount_amount,
            "total": bill_amount
        }
    }
    
    # Insert the bill data into the database
    Bill_collection.insert_one(bill_data)
    
    return bill_data

def insert_bill_to_db(bill_data):
    Bill_collection.insert_one(bill_data)
    return bill_data

