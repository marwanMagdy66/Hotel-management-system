from room_management import *
from Customers_Management import *
from Billing import *
from reservation_Management import *
from report import *

# ##############room management ###############
# print(add_room(101, 'single', 100))
# print(add_room(102, 'double', 150))
# print(add_room(103, 'suite', 300))
# print(book_room(103))
# print(release_room(101))
# print(list_rooms())
#########################################################

# ############## customers management #############
# print(add_customer('magyd mego','magdy@gmail.com',"01032423",'visa'))

# print(customers_list())
print(searching("6760b3b9e239fd1469eecfc5"))
# Update_info("67575984db308d205951e7d4","ali","ali@gmail.com","232341432","visa")
######################################################



##############reservation management ###################
# print(add_reservation("67575984db308d205951e7d4",101,"2025-5-10","2025-5-15"))
# print(list_reservations());



##############Bill##############

# generate_Bill('ali',102,['meals','laundry'],.2,10)


############ reports###########
# generate_occupancy_report()
# generate_revenue_report()