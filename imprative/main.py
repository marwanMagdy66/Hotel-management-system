from room_management import *
from Customers_Management import *
from Billing import *
from reservation_Management import *
from report import *

# ##############room management ###############
# add_room(102, "single", 100.0)
# book_room(101)
# release_room(101)
# list_rooms()
#########################################################

# ############## customers management #############
# add_customer('marwan','maro@gmail.com',"01032423",'visa')
# customers_list();
# searching("67575984db308d205951e7d4");
# Update_info("67575984db308d205951e7d4","ali","ali@gmail.com","232341432","visa")
######################################################



##############reservation management ###################
# add_reservation("67575984db308d205951e7d4",102,"2025-5-10","2025-5-15")
# list_reservations();



##############Bill##############

# generate_Bill('ali',102,['meals','laundry'],.2,10)


############ reports###########
# generate_occupancy_report()
generate_revenue_report()