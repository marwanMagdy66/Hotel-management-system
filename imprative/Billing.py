from DBConnection import Bill_collection,rooms_collection,reservations_collection




def generate_Bill(customer_name,room_number,services=None,tax_rate=0.1, discount=0):
    room=rooms_collection.find_one({"roomNumber":room_number})
    if not room:
        print ("room not found ")
        return
    reservation=reservations_collection.find_one({"roomNumber":room['roomNumber']})
    if not reservation:
        print ("reservation not found ")
    base_price=room['price']
    services_charges=0
    for service in services:
        if service=='meals':
            services_charges+=50
        elif service=='internet':
            services_charges+=20
        elif service=='laundry':
            services_charges+=30
        else:
            services_charges+=0;
    
    total_price = services_charges + (base_price * reservation['totalDays'])
    tax = total_price * tax_rate
    discount_amount = total_price * discount / 100

    if discount_amount > total_price + tax:
        discount_amount = total_price + tax

    bill_amount = total_price + tax - discount_amount

    bill=Bill_collection.insert_one({"customerName":customer_name,"roomNumber":room_number,"services":services,"billAmount":bill_amount})
    print(f"--- Bill for Reservation ID: {reservation['_id']} ---")
    print(f"Room Cost: {base_price}")
    print(f"Additional Services: {services_charges}")
    print(f"Subtotal: {total_price}")
    print(f"Tax ({tax_rate * 100}%): {tax}")
    print(f"Discount ({discount * 100}%): -{discount_amount}")
    print(f"Total: {bill_amount}")
    print("-------------------------------------")
