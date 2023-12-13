from hotel_content import ContentBook

hotel = ContentBook(r"C:\Users\NSANGKARN\bodytaylor\TARSautomation\hotel_workbook\C0C1\C0C1 Content Book Hotel Creation.xlsm")

print(hotel.mean_of_access)

def enter_data(data):
    element_list = [
        'hotelAccess.name', 'hotelAccess.direction', 'hotelAccess.line', 'hotelAccess.station'
    ]
    # Loop through the data and enter it
    for i, value in enumerate(data):
        if value != None:
            print(element_list[i], value)
            
enter_data(hotel.mean_of_access)