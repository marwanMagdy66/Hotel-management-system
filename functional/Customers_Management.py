from DBConnection import customers_collection
from bson import ObjectId


# Fetch all customers from the database
def fetch_customers():
    return list(customers_collection.find())


# Save customers to the database
def save_customers(customers):
    customers_collection.delete_many({})
    customers_collection.insert_many(customers)


# Validate payment method (pure function)
def validate_payment_method(payment_method):
    return payment_method.lower() in ["visa", "cash"]


# Add a new customer
def add_customer(name, email, phone, payment_method):
    if not validate_payment_method(payment_method):
        return "Invalid payment method. Please choose 'visa' or 'cash'."

    customers = fetch_customers()

    # Check if customer already exists
    if any(customer["email"] == email for customer in customers):
        return f"Customer with email {email} already exists."

    # Create new customer
    new_customer = {
        "name": name,
        "email": email,
        "phone": phone,
        "paymentMethod": payment_method
    }

    # Append customer immutably
    save_customers(customers + [new_customer])
    return "Customer added successfully!"


# List all customers
def list_customers():
    return list(map(
        lambda customer: (
            f"Name: {customer['name']}, Email: {customer['email']}, "
            f"Phone: {customer['phone']}, Payment Method: {customer['paymentMethod']}"
        ),
        fetch_customers()
    ))


def search_customer_by_id(customer_id):
    customers = fetch_customers()
    customer = next(
        filter(lambda c: str(c["_id"]) == customer_id, customers),
        None
    )
    return (
        f"Name: {customer['name']}, Email: {customer['email']}, "
        f"Phone: {customer['phone']}, Payment Method: {customer['paymentMethod']}"
    ) if customer else "Customer not found."


def update_customer(customer_id, name, email, phone, payment_method):
    if not validate_payment_method(payment_method):
        return "Invalid payment method. Please choose 'visa' or 'cash'."

    customers = fetch_customers()

    def update_if_match(customer):
        if str(customer["_id"]) == customer_id:
            return {
                **customer,
                "name": name,
                "email": email,
                "phone": phone,
                "paymentMethod": payment_method
            }
        return customer

    updated_customers = list(map(update_if_match, customers))

    if customers == updated_customers:  
        return "Customer not found."

    save_customers(updated_customers)
    return "Customer updated successfully!"
