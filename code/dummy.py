from hotel_content import ContentBook
from TarsAutomation import logger

def set_hotel_rid():
    """Get and validate Hotel RID from the user."""
    while True:
        hotel_rid = input('Enter Hotel RID: ').upper()
        if len(hotel_rid) == 4 and hotel_rid.isalnum():
            break
        print("Hotel RID should be a string of exactly four letters.")
    return hotel_rid

def load_content_book(hotel_rid):
    """Load the content book for the provided RID."""
    while True:
        try:
            hotel_content = ContentBook(filepath=f'hotel_workbook/{hotel_rid}/{hotel_rid} Content Book Hotel Creation.xlsm')
            logger.info(f'{hotel_rid} : Content Book Loaded')
            break
        except FileNotFoundError:
            print("Content Book not found for the provided RID. Please enter a valid RID.")
            logger.error(f'{hotel_rid} : Content Book not found')
            hotel_rid = set_hotel_rid()
    return hotel_rid, hotel_content

if __name__ == "__main__":
    
    while True:
        hotel_rid = set_hotel_rid()
        hotel_rid, hotel_content = load_content_book(hotel_rid)
        print(hotel_content.hotel_direction)
        
        user_choice = input('press x for exit')
        if user_choice == 'x':
            break
        