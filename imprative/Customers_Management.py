from DBConnection import customers_collection
from bson import ObjectId
def add_customer(name, email, phone, paymentMethod):
    valid_payment=['visa','cash'];
    if paymentMethod.lower() not in valid_payment:
        return print("Invalid payment method")

    customer={
        "name": name,
        "email": email,
        "phone": phone,
        "paymentMethod": paymentMethod
    }
    customers_collection.insert_one(customer)
    return print("Customer added successfully")

def customers_list():
    customers = customers_collection.find()
    for customer in customers:
        print(f"customer ID: {customer['_id']} \n ------------ ")
        print(f"Name: {customer['name']} \nEmail: {customer['email']} \nPhone: {customer['phone']} \npaymentMethod: {customer['paymentMethod']}")
        print("\n -----------------------------------")

def searching(id):
        customer = customers_collection.find_one({"_id": ObjectId(id)})
        if customer:
           print(f"Name: {customer['name']} \nEmail: {customer['email']} \nPhone: {customer['phone']} \npaymentMethod: {customer['paymentMethod']}")
        else:
            return print("Customer not found")




def Update_info(id, name, email, phone, paymentMethod):
    customer = customers_collection.find_one({"_id": ObjectId(id)})
    
    if customer:
        result = customers_collection.update_one(
            {"_id": ObjectId(id)},  
            {"$set": {               
                "name": name,
                "email": email,
                "phone": phone,
                "paymentMethod": paymentMethod
            }}
        )
        
        if result.modified_count > 0:
            print(f"Customer updated successfully:\nName: {name}\nEmail: {email}\nPhone: {phone}\nPayment Method: {paymentMethod}")
        else:
            print("No changes made to the customer record.")
    else:
        print("Customer not found")
