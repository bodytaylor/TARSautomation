import os
from TarsAutomation import driver, logger
import TarsAutomation as ta
from hotel_content import ContentBook

# Constants
VERSION = "1.0.2"

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
            hotel_content = ContentBook(filepath=f'hotel_workbook/{hotel_rid}/{hotel_rid}.xlsm')
            logger.info(f'{hotel_rid} : Content Book Loaded')
            break
        except FileNotFoundError:
            print("Content Book not found for the provided RID. Please enter a valid RID.")
            logger.error(f'{hotel_rid} : Content Book not found')
            hotel_rid = set_hotel_rid()
    return hotel_rid, hotel_content

# Clear console function
def clear_console():
    """Clear the console screen."""
    os.system('cls')

def main():
    """Main function to run the program."""
    print(f"Welcome to TARS Automation Tool ver.{VERSION}")

    # Store Hotel RID for using in the program
    hotel_rid = set_hotel_rid()

    # Load content book
    hotel_rid, hotel_content = load_content_book(hotel_rid)
    
    # Login and perform hotel search
    ta.login()
    ta.hotel_search(hotel_rid)

    # Main menu loop
    while True:
        clear_console()
        print("Enter f for full automation.")
        print("1. Add Hotel Language")
        print("2. Add Hotel Program")
        print("3. Add Automation Representation")
        print("4. Add Distribution Method")
        print("5. Add Address & Setup")
        print("6. Add Translate name & Address")
        print("7. Add General Information")
        print("8. Add Special Rating")
        print("9. Add Meal Option")
        print("10. Add Room")
        print("11. Add Room Translation")
        print("12. Add Web Description")
        print("13. Add Main Service")
        print("14. Add Other Service")
        print("15. Add Sports & Leisure")
        print("16. Add Restaurants")
        print("17. Add Restaurants Description")
        print("18. Add Bar")
        print("19. Add Bar Description")
        print("20. Add Meeting Rooms")
        print("21. Add Meeting Rooms Description")
        print("22. Add Mean of Access")
        print("23. Add Main Attraction")
        print("24. Add Surrounding Attraction")
        print("25. Add Hotel contact")
        print("26. Add Guarantee")
        print("27. Add Payment")
        print("Enter q for exit")

        # User Choice
        choice = input("Select a task: ")
        clear_console()
        
        if choice == "f":
            run_full_automation(hotel_rid, hotel_content)
        elif choice == '1':
            import add_language
            add_language.add(hotel_rid)
        elif choice == '2':
            import hotel_programs
            hotel_programs.add(hotel_rid, hotel_content)
        elif choice == '3':
            import add_automation_representation
            add_automation_representation.add(hotel_rid)
        elif choice == '4':
            import distribution_method
            distribution_method.add(hotel_rid, hotel_content)
        elif choice == '5':
            import address_and_setup
            address_and_setup.add(hotel_rid, hotel_content)
        elif choice == '6':
            import translate_name_and_address
            translate_name_and_address.add(hotel_rid, hotel_content)
        elif choice == '7':
            import general_info
            general_info.add(hotel_rid, hotel_content)
        elif choice == '8':
            import special_rating
            special_rating.add(hotel_rid, hotel_content)
        elif choice == '9':
            import meal_options
            meal_options.add(hotel_rid, hotel_content)
        elif choice =='10':
            import rooms
            rooms.add(hotel_rid, hotel_content)
        elif choice == '11':
            import room_translation
            room_translation.add(hotel_rid, hotel_content)
        elif choice == '12':
            import web_description
            web_description.add(hotel_rid, hotel_content.web_description_df)
        elif choice == '13':
            import main_service
            main_service.add(hotel_rid, hotel_content)
        elif choice == '14':
            import products
            products.add(hotel_rid, hotel_content)
        elif choice == '15':
            import sports_and_leisure
            sports_and_leisure.add(hotel_rid, hotel_content)
        elif choice == '16':
            import restaurant
            restaurant.add(hotel_rid, hotel_content.restaurants)
        elif choice == '17':
            import restaurant_translation
            restaurant_translation.add(hotel_rid, hotel_content.resaurant_description)
        elif choice == '18':
            import bar
            bar.add(hotel_rid, hotel_content.bars)
        elif choice == '19':
            import bar_translation
            bar_translation.add(hotel_rid, hotel_content.bars)
        elif choice == '20':
            import meeting_room
            meeting_room.add(hotel_rid, hotel_content.meeting_room)
        elif choice == '21':
            import meeting_room_translation
            meeting_room_translation.add(hotel_rid, hotel_content.meeting_room)
        elif choice == '22':
            import mean_of_access
            mean_of_access.add(hotel_rid, hotel_content)
        elif choice == '23':
            import main_attractions
            main_attractions.add(hotel_rid, hotel_content)
        elif choice == '24':
            import surrounding_attraction
            surrounding_attraction.add(hotel_rid, hotel_content)  
        elif choice == '25':
            import hotel_contact
            hotel_contact.add(hotel_rid)    
        elif choice == '26':
            import guarantees
            guarantees.add(hotel_rid)
        elif choice == '27':
            import payment
            payment.add(hotel_rid)
               
        elif choice == "q":
            print("Exiting the program. Goodbye!")
            driver.quit()
            break
        else:
            print("Invalid choice. Please input Valid Value.")
        
        # After each task, ask the user if they want to continue
        user_choice = input("Do you want to perform another task? (y/n): ")
        if user_choice.lower() != "y":
            print("Exiting the program. Goodbye!")
            driver.quit()
            break
        
def run_full_automation(hotel_rid, hotel_content):
    """Run full automation for the given hotel RID and content."""
    # Note Adding function for asking user for all infomaion needed for full automation.
    import add_language
    add_language.add(hotel_rid)

    import hotel_programs
    hotel_programs.add(hotel_rid, hotel_content)

    import add_automation_representation
    add_automation_representation.add(hotel_rid)

    import distribution_method
    distribution_method.add(hotel_rid, hotel_content)

    import address_and_setup
    address_and_setup.add(hotel_rid, hotel_content)

    import translate_name_and_address
    translate_name_and_address.add(hotel_rid, hotel_content)

    import general_info
    general_info.add(hotel_rid, hotel_content)

    import special_rating
    special_rating.add(hotel_rid, hotel_content)

    import meal_options
    meal_options.add(hotel_rid, hotel_content)

    import rooms
    rooms.add(hotel_rid, hotel_content)

    import room_translation
    room_translation.add(hotel_rid, hotel_content)

    import web_description
    web_description.add(hotel_rid, hotel_content.web_description_df)

    import main_service
    main_service.add(hotel_rid, hotel_content)

    import products
    products.add(hotel_rid, hotel_content)

    import sports_and_leisure
    sports_and_leisure.add(hotel_rid, hotel_content)

    import restaurant
    restaurant.add(hotel_rid, hotel_content.restaurants)

    import restaurant_translation
    restaurant_translation.add(hotel_rid, hotel_content.resaurant_description)

    import bar
    bar.add(hotel_rid, hotel_content.bars)

    import bar_translation
    bar_translation.add(hotel_rid, hotel_content.bars)

    import meeting_room
    meeting_room.add(hotel_rid, hotel_content.meeting_room)

    import meeting_room_translation
    meeting_room_translation.add(hotel_rid, hotel_content.meeting_room)

    import mean_of_access
    mean_of_access.add(hotel_rid, hotel_content)

    import main_attractions
    main_attractions.add(hotel_rid, hotel_content)

    import surrounding_attraction
    surrounding_attraction.add(hotel_rid, hotel_content)  

    import hotel_contact
    hotel_contact.add(hotel_rid)    

    import guarantees
    guarantees.add(hotel_rid)

    import payment
    payment.add(hotel_rid)

if __name__ == "__main__":
    main()
    