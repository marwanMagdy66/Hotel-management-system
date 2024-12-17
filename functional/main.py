from room_management import *
from Customers_Management import *
from Billing import *
from reservation_Management import *
from report import *

# ##############room management ###############
# print(add_room(101, 'single', 100))
# print(add_room(102, 'double', 150))
# print(add_room(105, 'suite', 300))
# print(add_room(106, 'suite', 300))

# print(booking_room(106))
# print(release2_room(101))
# print(list_rooms())
#########################################################

# ############## customers management #############
# print(add_customer(' mohamed','mohamed@gmail.com',"01032423",'cash'))

# print(list_customers())
# print(search_customer_by_id("6760b3b9e239fd1469eecfc5"))
# print(update_customer("6760b3b9e239fd1469eecfc5","magdy","mego@gmail.com","232341432","visa"))
######################################################



##############reservation management ###################
# print(book_reservation_and_update_db("6760b3b9e239fd1469eecfc5",105,"2025-5-10","2025-5-15"))
# print(list_reservations());



##############Bill##############

# print(generate_bill('ali',105,['meals','laundry'],.2,10))

############ reports###########
# generate_occupancy_report()
# generate_revenue_report()