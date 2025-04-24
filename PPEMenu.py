#PPEMenu.py
"""
START THE PROGRAM IN THIS FILE
"""
import sys
import Main


def menu():
    print('\nWelcome ! What would you like to access ?')
    print('\n\t1. Item Inventory Update')
    print('\t2. Item Inventory Tracking')
    print('\t3. Item Inventory Searching')


    print('\t4. Report Generator')
    print('\t5. Exit')

    while True:
        try:
            user_choice = int(
                input('\nPlease select one of the following by inputting the number [1 | 2 | 3 | 4 | 5]:').strip())

            if user_choice == 1 or user_choice == 2 or user_choice == 3 or user_choice == 4 or user_choice == 5:
                break
            else:
                print('Please enter a valid input')

        except ValueError:
            print('Please enter a valid input')

    if user_choice == 1:
        Main.update()
    elif user_choice == 2:
        Main.item_inventory_tracking()
    elif user_choice == 3:
        Main.search()
    elif user_choice == 4:
        Main.report()
    elif user_choice == 5:
        print('Exiting program...')
        sys.exit(0)

