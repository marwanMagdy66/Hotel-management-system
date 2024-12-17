from bson import ObjectId
from DBConnection import customers_collection

# Fetch all customers (pure function)
def fetch_customers():
    customers = customers_collection.find()
    return [
        {
            "id": str(customer["_id"]),
            "name": customer["name"],
            "email": customer["email"],
            "phone": customer["phone"],
            "paymentMethod": customer["paymentMethod"]
        }
        for customer in customers
    ]

# Fetch a specific customer by ID (pure function)
def fetch_customer_by_id(customer_id):
    customer = customers_collection.find_one({"_id": ObjectId(customer_id)})
    if not customer:
        return None
    return {
        "id": str(customer["_id"]),
        "name": customer["name"],
        "email": customer["email"],
        "phone": customer["phone"],
        "paymentMethod": customer["paymentMethod"]
    }

# Validate payment method (pure function)
def validate_payment_method(payment_method):
    valid_payments = ["visa", "cash"]
    return payment_method.lower() in valid_payments

# Prepare customer data (pure function)
def prepare_customer_data(name, email, phone, payment_method):
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "paymentMethod": payment_method
    }

# Save customer (side effect handler)
def save_customer(customer_data):
    customers_collection.insert_one(customer_data)

# Add a new customer (pure + side effect combined externally)
def add_customer(name, email, phone, payment_method):
    if not validate_payment_method(payment_method):
        return "Invalid payment method"

    customer_data = prepare_customer_data(name, email, phone, payment_method)
    return customer_data  # Return the prepared customer data instead of saving it here

# Save a new customer to database (side effect handler)
def save_new_customer(name, email, phone, payment_method):
    customer_data = add_customer(name, email, phone, payment_method)
    if isinstance(customer_data, str):  # If it's an error message
        return customer_data
    save_customer(customer_data)
    return "Customer added successfully"

# List customers (pure function)
def customers_list():
    customers = fetch_customers()
    customer_descriptions = [
        (
            f"Customer ID: {customer['id']} \n"
            f"Name: {customer['name']} \n"
            f"Email: {customer['email']} \n"
            f"Phone: {customer['phone']} \n"
            f"Payment Method: {customer['paymentMethod']}\n"
            f"-----------------------------------"
        )
        for customer in customers
    ]
    return "\n".join(customer_descriptions)

# Search for a customer by ID (pure function)
def search_customer_by_id(customer_id):
    customer = fetch_customer_by_id(customer_id)
    if not customer:
        return "Customer not found"
    return (
        f"Name: {customer['name']} \n"
        f"Email: {customer['email']} \n"
        f"Phone: {customer['phone']} \n"
        f"Payment Method: {customer['paymentMethod']}"
    )

# Update customer data (pure function)
def prepare_updated_customer_data(customer, name, email, phone, payment_method):
    updated_customer = customer.copy()
    updated_customer.update({
        "name": name,
        "email": email,
        "phone": phone,
        "paymentMethod": payment_method
    })
    return updated_customer

# Perform the update operation (side effect handler)
def update_customer_info(customer_id, name, email, phone, payment_method):
    customer = fetch_customer_by_id(customer_id)
    if not customer:
        return "Customer not found"

    updated_customer = prepare_updated_customer_data(
        customer, name, email, phone, payment_method
    )

    # Perform the database update
    result = customers_collection.update_one(
        {"_id": ObjectId(customer_id)},
        {"$set": {
            "name": updated_customer["name"],
            "email": updated_customer["email"],
            "phone": updated_customer["phone"],
            "paymentMethod": updated_customer["paymentMethod"]
        }}
    )

    if result.modified_count > 0:
        return f"Customer updated successfully:\n{updated_customer}"
    else:
        return "No changes were made to the customer record."
