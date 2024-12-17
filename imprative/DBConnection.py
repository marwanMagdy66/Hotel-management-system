from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client.hotel_management
rooms_collection = db.rooms
customers_collection = db.customers
reservations_collection = db.reservations
Bill_collection=db.Bills
Report_collection=db.Reports


