import os

# Store Hotel RID for using in program
hotel_rid = None

def set_hotel_rid():
    global hotel_rid
    hotel_rid = str(input('Enter Hotel RID: '))
    hotel_rid = hotel_rid.upper()

def main():
    # Welcome message to user and get the rid
    print("Welcome to TARS Automation Tool ver.1.0.0")
    print("[WARNING] - This Version for content book V.10, (Cell mean of Access at C79)\nOtherwise Use version xx")
    set_hotel_rid()
    clear_console()
    
    # Enter main menu
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
        print("Enter q for exit")
        
        # User Choice
        choice = input("Select a task: ")
        clear_console()
        if choice == "f":
            pass
            
        elif choice == '1':
            import add_language
            add_language.add(hotel_rid)
        elif choice == '2':
            import hotel_programs
            hotel_programs.add(hotel_rid)
        elif choice == '3':
            import add_automation_representation
            add_automation_representation.add(hotel_rid)
        elif choice == '4':
            import distribution_method
            distribution_method.add(hotel_rid)
        elif choice == '5':
            import address_and_setup
            address_and_setup.add(hotel_rid)
        elif choice == '6':
            import translate_name_and_address
            translate_name_and_address.add(hotel_rid)
        elif choice == '7':
            import general_info
            general_info.add(hotel_rid)
        elif choice == '8':
            import special_rating
            special_rating.add(hotel_rid)
        elif choice == '9':
            import meal_options
            meal_options.add(hotel_rid)
        elif choice =='10':
            import rooms
            rooms.add(hotel_rid)
        elif choice == '11':
            import room_translation
            room_translation.add(hotel_rid)
        elif choice == '12':
            import web_description
            web_description.add(hotel_rid)
        elif choice == '13':
            import main_service
            main_service.add(hotel_rid)
        elif choice == '14':
            import products
            products.add(hotel_rid)
        elif choice == '15':
            import sports_and_leisure
            sports_and_leisure.add(hotel_rid)
        elif choice == '16':
            import restaurant
            restaurant.add(hotel_rid)
        elif choice == '17':
            import restaurant_translation
            restaurant_translation.add(hotel_rid)
        elif choice == '18':
            import bar
            bar.add(hotel_rid)
        elif choice == '19':
            import bar_translation
            bar_translation.add(hotel_rid)
        elif choice == '20':
            import meeting_room
            meeting_room.add(hotel_rid)
        elif choice == '21':
            import meeting_room_translation
            meeting_room_translation.add(hotel_rid)
        elif choice == '22':
            import mean_of_access
            mean_of_access.add(hotel_rid)
        elif choice == '23':
            import main_attractions
            main_attractions.add(hotel_rid)
        elif choice == '24':
            import surrounding_attraction
            surrounding_attraction.add(hotel_rid)  
        elif choice == '25':
            import hotel_contact
            hotel_contact.add(hotel_rid)          
        elif choice == "q":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please input Valid Value.")
        
        # After each task, ask the user if they want to continue
        user_choice = input("Do you want to perform another task? (y/n): ")
        if user_choice.lower() != "y":
            print("Exiting the program. Goodbye!")
            break

# Clear console function
def clear_console():
    os.system('cls')

if __name__ == "__main__":
    main()
    