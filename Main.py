# Main.py
'''
START THE PROGRAM IN THE PPEMenu.py FILE
'''
import os
import datetime
from pathlib import Path
import PPEMenu

# Elianna Catrina Herrera
# TP073631
# login functionality
def login(): #Function for users to log in the PPE System
    InvCon = ['IC1', 'IC2', 'IC3', 'IC4']
    Password = ['ventcon123', 'ventcon456', 'ventcon789', 'ventcon321']

    attempt = 0
    max_attempt = 3

    while attempt < max_attempt: #Users can only try logging in with a maximum of 3 attempts
        username = input("\nPlease enter your username: ")
        password = input("Please enter your password: ")

        SuccessfulLogin = False

        for x, y in zip(InvCon, Password):
            if username == x and password == y: #checking if user's input for username and password is valid
                SuccessfulLogin = True
                break
        if SuccessfulLogin:
            print("Login Successful")
            check_and_create_files()
            PPEMenu.menu()
            break
        else:
            attempt += 1
            if attempt < max_attempt:
                print("Username or password is incorrect. Please try again.")
            else:
                print("You have reached the maximum number of attempts to log in.")
                exit()


# Elianna Catrina Herrera
# TP073631
# update inventory
def getDateFromUser():  # ensuring users are inputting the correct date format
    while True:
        received_date = input("Enter the date of items received/distributed (YYYY-MM-DD): ")
        try:
            date = datetime.datetime.strptime(received_date, "%Y-%m-%d").date()
            return date  # returning the value of the date
        except ValueError:
            print("Date format is invalid. Please enter the date in the format of YYYY-MM-DD")


def read_file(filename):  # function to read the files
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return [line.strip().split(',') for line in lines]
    except FileNotFoundError:
        return []


def write_file(filename, data): #function to write in the files
    with open(filename, 'w') as file:
        for line in data:
            file.write(','.join(line) + '\n')

def update_hospital_detail(hcode, field, new_value): #Function to update hospital details
    hospitals = read_file('hospitals.txt')
    updated_hospitals = []
    hospital_found = False

    for hospital in hospitals:
        if hospital[0] == hcode:
            hospital_found = True
            if field == "name":
                hospital[1] = new_value
            elif field == "number":
                hospital[2] = new_value
            elif field == "email":
                hospital[3] = new_value
            updated_hospitals.append(hospital)
            print(f"Hospital Details have been updated.\n{hospital[1]}\n{hospital[2]}\n{hospital[3]}")
        else:
            updated_hospitals.append(hospital)

    if hospital_found:
        write_file('hospitals.txt', updated_hospitals)
        update()
    else:
        print("\nHospital Code not found.")
        update()


def get_input():
    hcode = input("Input the Hospital Code: ")
    ask = input("Which Hospital detail needs to be updated? (name/number/email): ").lower()
    new_value = input(f"Enter the new Hospital {ask.capitalize()}: ")

    if ask not in ["name", "number", "email"]:
        print("\nInvalid field. Please choose from 'name', 'number', or 'email'.")
        return get_input()  # retry input
    else:
        update_hospital_detail(hcode, ask, new_value)


def update(): #function to call the main update menu
    while True:
        try:
            update = int(input("""\nWhat would you like to update?\n 
                1: Hospital Details\n
                2: Item Inventory\n
                3: Main Menu\n
                Enter either number 1, 2, 3:
                """))
            if update == 1 or update == 2 or update == 3:
                break
            else:
                print('Please enter a valid input')
        except ValueError:
            print('Please enter a valid input')

    if update == 1:
        get_input()

    elif update == 2:
        item_update()

    elif update == 3:
        PPEMenu.menu()


def item_update():  # Function to update the items in inventory
    ICode = ['HC', 'FS', 'MS', 'GL', 'GW', 'SC']
    print("Inventory Code options:\n1) HC[Head Cover]\n2) FS[Face Shield]\n3) MS[Mask]\n4) GL[Gloves]\n5) GW[Gown]\n6) "
          "SC[Shoe Covers]")

    while True:
        Inven_Code = input("Enter Inventory Code: ").upper()
        if Inven_Code not in ICode:
            print("Invalid Inventory Code.")
            continue

        task = input("Would you like to receive or distribute items? (receive/distribute): ").lower()

        if task == "receive":
            received_date = getDateFromUser()
            try:
                item_name = read_file('ppe.txt')
                IName = input("Item Name:\n1) HC[Head Cover]\n2) FS[Face Shield]\n3) MS[Mask]\n4) GL[Gloves]\n5) "
                              "GW[Gown]\n6) SC[Shoe Covers]\nEnter the Item Name: ")
                name_found = False
                for name in item_name:
                    if name[1] == IName:
                        name_found = True
                        break
                if not name_found:
                    print("Item Name not found.")
                    continue

                UserQuantity = int(input("Please enter the amount of item quantity that has been received: "))
                SCode = input("Please enter Supplier Code: ")
            except ValueError:
                print("Invalid quantity. Please enter a number.")
                continue

            inventory_data = read_file('ppe.txt')
            for item in inventory_data:
                if item[0] == Inven_Code:
                    item[3] = str(int(item[3]) + UserQuantity)
                    print(f"{Inven_Code} has been updated with the total amount of {item[3]}")
                    break
            write_file('ppe.txt', inventory_data)
            with open("receive.txt", "a") as file:  # Use "a" to append to the file
                file.write(f"{received_date},{Inven_Code},{IName},{SCode},{UserQuantity}\n")

        elif task == "distribute":
            received_date = getDateFromUser()
            try:
                item_name = read_file('ppe.txt')
                IName = input("Item Name:\n1) Head Cover[HC]\n2) Face Shield[FS]\n3) Mask[MS]\n4) Gloves[GL]\n5) "
                              "Gown[GW]\n6) Shoe Covers[SC]\nEnter the Item Name: ")
                name_found = False
                for name in item_name:
                    if name[1] == IName:
                        name_found = True
                        break
                if not name_found:
                    print("Item Name not found.")
                    continue

                hospitals = read_file('hospitals.txt')
                hcode = input("Enter Hospital Code: ").upper()

                hospital_found = False
                for hospital in hospitals:
                    if hospital[0] == hcode:
                        hospital_found = True
                        break

                if not hospital_found:
                    print("Hospital code not found.")
                    continue

                UserQuantity = int(input("Enter the quantity of items distributed: "))
            except ValueError:
                print("Invalid quantity. Please enter a number.")
                continue

            inventory_data = read_file('ppe.txt')
            for item in inventory_data:
                if item[0] == Inven_Code:
                    if int(item[3]) < UserQuantity:
                        print(f"Not enough stock. Available: {item[3]}")
                        update()
                    item[3] = str(int(item[3]) - UserQuantity)
                    print(f"{Inven_Code} has been updated with the remaining amount of {item[3]} on the {received_date}")
                    break
            write_file('ppe.txt', inventory_data)
            with open("distribution.txt", "a") as file:
                file.write(f"{received_date},{Inven_Code},{IName},{hcode},{UserQuantity}\n")
        else:
            print("Invalid task. Please enter 'receive' or 'distribute'.")

        while True:
            try:
                update_again = input("Do you need to do more updates? (yes/no): ").strip().lower()
                if update_again == 'yes':
                    update()
                elif update_again == 'no':
                    PPEMenu.menu()
                else:
                    print('Please enter a valid input')
            except ValueError:
                print('Please enter a valid input')



# initial file checks and creation if not exist
# Suchitra Nambiar A/P Mahandran
# TP074762
def check_and_create_files():
    files = {
        'ppe.txt': create_inventory,
        'supplier.txt': create_supplier,
        'hospitals.txt': create_hospitals,
    }

    for file_name, create_function in files.items():
        path = Path(file_name)
        if path.is_file():
            print(f"\n{file_name.capitalize()} File exists")
        else:
            create_function()


def create_inventory():
    item = int(input("How many items do you want to input: "))
    with open("ppe.txt", "w") as file:
        for _ in range(item):
            ICode = input("Enter item code: ")
            IName = input("Enter item name: ")
            SCode = input("Enter supplier code: ")
            IQuantity = 100
            file.write(f"{ICode},{IName},{SCode},{IQuantity}\n")


def create_supplier():
    while True:
        try:
            user = int(input("How many suppliers are there: "))
            if user in [3, 4]:
                with open("supplier.txt", "w") as file:
                    for _ in range(user):
                        SCode = input("Input the Supplier Code: ")
                        SName = input("Input the Supplier Name: ")
                        SNumber = input("Input the Supplier Number: ")
                        SEmail = input("Input the Supplier Email: ")
                        file.write(f"{SCode},{SName},{SNumber},{SEmail}\n")
                print("Suppliers successfully added to supplier.txt.")
                break
            else:
                print("You can only have 3 or 4 suppliers")
        except ValueError:
            print("Invalid input. Please enter a valid number (3 or 4)")


def create_hospitals():
    while True:
        try:
            user = int(input("How many hospitals are there: "))
            if user in [3, 4]:
                with open("hospitals.txt", "w") as file:
                    for _ in range(user):
                        HCode = input("Input the Hospital Code: ")
                        HName = input("Input the Hospital Name: ")
                        HNumber = input("Input the Hospital Number: ")
                        HEmail = input("Input the Hospital Email: ")
                        file.write(f"{HCode},{HName},{HNumber},{HEmail}\n")
                print("Hospitals successfully added to hospitals.txt.")
                break
            else:
                print("You can only have 3 or 4 hospitals")
        except ValueError:
            print("Invalid input. Please enter a valid number (3 or 4)")

# item tracking
# Ng Vin Ee
# TP073088
def read_items(file_name):
    items = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                # to skip empty lines
                if not line.strip():
                    continue
                # split each line with a comma
                parts = line.strip().split(',')
                # ensure each line has at least 4 parts
                if len(parts) >= 4:
                    item_code = parts[0]
                    item_name = parts[1]
                    # assuming size is parts[2], skip to parts[3] for quantity
                    try:
                        quantity = int(parts[3])
                        # append dictionary with the item details to the items
                        items.append({'item_code': item_code, 'item_name': item_name, 'quantity': quantity})
                    except ValueError:
                        print(f"Error: Quantity '{parts[3]}' is not a valid integer.")
                else:
                    print(f"Error: Line '{line.strip()}' does not have at least four parts.")
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    return items


def print_total_quantity_sorted(items):
    # a function to print items sorted by their quantity
    items_sorted = sorted(items, key=lambda x: x['quantity'])
    for item in items_sorted:
        print(f"{item['item_code']}, {item['item_name']}, {item['quantity']}")


def print_low_stock_items(items):
    # another function to print items with quantity that is less than 25
    low_stock_found = False
    for item in items:
        if item['quantity'] < 25:
            print(f"{item['item_code']}, {item['item_name']}, {item['quantity']}")
            low_stock_found = True
    if not low_stock_found:
        print("No low stock items found.")


def item_inventory_tracking():
    # main function to track inventory based on user input
    while True:
        try:
            # loop created to ask user what they want to track
            print("\nItem Inventory Tracking\n\t1:Total Quantity\n\t2:Low Stock Items\n\t3.Menu")
            answer = int(input('\nPlease input the number of would you like to track [1 | 2 | 3]:'))
            items = read_items("ppe.txt")

            if answer == 1 or answer == 2 or answer == 3:
                break
            else:
                print('Please enter a valid input')
        except ValueError:
            print('Please enter a valid input')

        # based on user input, call the appropriate function mentioned
    if answer == 1:
        print_total_quantity_sorted(items)

    if answer == 2:
        print_low_stock_items(items)

    if answer == 3:
        PPEMenu.menu()

        # ask if the user wants to track again
    while True:
        try:
            again = input("\nDo you want to track again? (yes/no) ").strip().lower()
            if again == "yes":
                item_inventory_tracking()
            elif again == "no":
                PPEMenu.menu()
            else:
                print('Please enter a valid input')
        except ValueError:
            print('Please enter a valid input')



# search function
# Ejjaz Hakimi bin Mohamad Azan
# TP073318
def search():
    # prompt user for item they wish to search
    print('\nWhat item would like to search for ?')
    print('\nITEM CODES')
    print('\tHC: Head Cover',
          '\tFS: Face Shield',
          '\n\tMS: Mask',
          '\t\tGL: Gloves',
          '\n\tGW: Gown',
          '\t\tSC: Shoe Cover',
          '\n\n\tRE: Return to Main Menu')

    def obtain_hospital_info(hospital_file='hospitals.txt'):
        '''
        This is done to obtain &
        match the hospital name to
        its corresponding hospital code
        '''
        hospital_dict = {}
        try:
            with open(hospital_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        hospital_code, hospital_name = parts[0].strip(), parts[1].strip()
                        hospital_dict[hospital_code] = hospital_name
        except FileNotFoundError:
            print(f'{hospital_file} not found')

        return hospital_dict

    def search_result(distribution_file='distribution.txt', hospital_file='hospitals.txt'):
        '''
        This is done to produce search results
        '''
        hospital_info = obtain_hospital_info(hospital_file)  # call back the dictionary

        try:
            distributions = []
            with open(distribution_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    parts = [part.strip() for part in parts]

                    if len(parts) == 5:  # assign each index to its corresponding value
                        date, item_code, item_name, hospital_code, quantity = parts
                        quantity = int(quantity.strip())
                        distributions.append((hospital_code, item_code, item_name, quantity))
                        #  date is not appended as it is irrelevant

        except FileNotFoundError:
            print(f'{distribution_file} not found')

        return distributions, hospital_info

    def search_process():
        item_codes = ['HC', 'FS', 'MS', 'GL', 'GW', 'SC']

        # loop to ensure input is valid
        while True:
            try:
                item_input = input('\nPlease enter the item code you would like to search for [eg: MS]: ').strip()
                if item_input in item_codes:
                    break
                elif item_input == 'RE':
                    PPEMenu.menu()
                else:
                    print('Please enter a valid entry')
            except ValueError:
                print('Please enter a valid entry')

        distributions, hospital_info = search_result()

        combined_results = []  # to sore aggregated results

        for distribution in distributions:
            hospital_code, item_code, item_name, quantity = distribution
            if item_code == item_input:
                found = False  # check if the hospital code is already in the list
                for result in combined_results:
                    if result[0] == hospital_code:
                        result[2] += quantity
                        found = True
                        break
                if not found:  # if not found, add a new entry to the list
                    combined_results.append([
                        hospital_code,
                        hospital_info.get(hospital_code, 'Not Found'),
                        quantity
                    ])

        print(f'\nDISTRIBUTIONS FOR ITEM CODE {item_input}:')
        if combined_results:
            for result in combined_results:
                print(
                    f'Hospital Code: {result[0]}, Hospital Name: {result[1]}, Total Quantity Distributed: {result[2]}'
                )
        else:
            print('No distributions found for this item code.')

        while True:
            try:
                user_continue = input('\nWould you like to continue (yes/no)?').strip().lower()
                if user_continue == 'yes':
                    search()
                elif user_continue == 'no':
                    PPEMenu.menu()
                else:
                    print('Please enter a valid input')
            except ValueError:
                print('Please enter a valid input')

    search_process()


# report function
# Ejjaz Hakimi bin Mohamad Azan
# TP073318
def report():
    # prompt user for type of report
    print('\nWhat type of report would you like to generate ?')
    print('\t1. List of suppliers with their PPE equipment')
    print('\t2. List of hospitals with quantity of distribution items')
    print('\t3. Overall transaction report per month')
    print('\t4. Return to main menu')

    # loop ensures user enters a valid input
    while True:
        try:
            report_type = int(input('\nPlease select one of the above by inputting the number [1 | 2 | 3 | 4]:'))
            if report_type == 1 or report_type == 2 or report_type == 3 or report_type == 4:
                break
            else:
                print('Please enter a valid entry')
        except ValueError:
            print('Please enter a valid entry')

    if report_type == 1:
        # ppe report function
        def obtain_supplier_info(supplier_file='supplier.txt'):
            '''
            This is done to match the supplier name
            to its corresponding supplier code
            '''
            supplier_dict = {}
            try:
                with open(supplier_file, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')  # segment each line
                        if len(parts) >= 2:
                            supplier_code, supplier_name = parts[0].strip(), parts[1].strip()
                            supplier_dict[supplier_code] = supplier_name
            except FileNotFoundError:
                print(f'{supplier_file} not found')

            return supplier_dict

        def ppe_report(ppe_file='ppe.txt', supplier_file='supplier.txt'):
            '''
            This is done to generate the PPE report
            '''
            supplier_record = []
            supplier_info = obtain_supplier_info(supplier_file)  # call back the dictionary

            try:
                items = []
                with open(ppe_file, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')  # segment each line
                        parts = [part.strip() for part in parts]  # remove whitespace

                        if len(parts) == 4:
                            item_code, item_name, supplier_code, quantity = parts
                            items.append((item_code, item_name, supplier_code))
                            # quantity is not appended as it is irrelevant

                unique_suppliers = []  # make a list of all unique supplier codes
                for item in items:
                    supplier_code = item[2]
                    if supplier_code not in unique_suppliers:
                        unique_suppliers.append(supplier_code)

                for supplier_code in unique_suppliers:
                    supplier_name = supplier_info.get(supplier_code, 'No Supplier')
                    supplier_items = [item for item in items if item[2] == supplier_code]
                    supplier_record.append({
                        'Supplier Code': supplier_code,
                        'Supplier Name': supplier_name,
                        'Items': [{'Item Code': item[0], 'Item Name': item[1]} for item in supplier_items]
                    })

                order = ['S1', 'S2', 'S3', 'S4']  # order the output
                supplier_record.sort(
                    key=lambda x: order.index('Supplier Code'[0]) if 'Supplier Code'[0] in order else
                    len(order))
                return supplier_record

            except FileNotFoundError:
                print(f'{ppe_file} not found')
                return []

        import json
        ppe_report = ppe_report()
        print('\nSUPPLIER RECORD')
        print(json.dumps(ppe_report, indent=3))

        while True:
            try:
                user_continue = input('\nWould you like to continue (yes/no)?').strip().lower()
                if user_continue == 'yes':
                    report()
                elif user_continue == 'no':
                    PPEMenu.menu()
                else:
                    print('Please enter a valid input')
            except ValueError:
                print('Please enter a valid input')

    if report_type == 2:
        # hospital report function
        def obtain_hospital_info(hospital_file='hospitals.txt'):
            '''
            This is done to obtain &
            match the hospital name to
            its corresponding hospital
            code
            '''
            hospital_dict = {}
            try:
                with open(hospital_file, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            hospital_code, hospital_name = parts[0].strip(), parts[1].strip()
                            hospital_dict[hospital_code] = hospital_name
            except FileNotFoundError:
                print(f'{hospital_file} not found')

            return hospital_dict

        def distribution_report(distribution_file='distribution.txt', hospital_file='hospitals.txt'):
            '''
            This is done to generate the
            distribution report
            '''
            distribution_record = []
            distribution_info = obtain_hospital_info(hospital_file)

            try:
                distributions = []
                with open(distribution_file, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        parts = [part.strip() for part in parts]  # remove whitespace

                        if len(parts) == 5:
                            date, item_code, item_name, hospital_code, quantity = parts
                            distributions.append((hospital_code, item_code, item_name, date, quantity))

                unique_hospitals = []  # define unique hospital codes
                for distribution in distributions:
                    hospital_code = distribution[0]
                    if hospital_code not in unique_hospitals:
                        unique_hospitals.append(hospital_code)

                for hospital_code in unique_hospitals:
                    hospital_name = distribution_info.get(hospital_code, 'No Hospital')
                    distribution_items = [distribution for distribution in distributions if distribution[0] ==
                                          hospital_code]
                    distribution_record.append({
                        'Hospital Code': hospital_code,
                        'Hospital Name': hospital_name,
                        'Distributions': [
                            {'Item Code': item[1], 'Item Name': item[2], 'Date': item[3], 'Quantity': item[4]}
                            for item in distribution_items
                        ]
                    })

                order = ['H1', 'H2', 'H3']
                distribution_record.sort(
                    key=lambda x: order.index(x['Hospital Code']) if x['Hospital Code'] in order
                    else len(order))

                return distribution_record

            except FileNotFoundError:
                print(f'{distribution_file} not found')
                return []

        import json
        distribution_report = distribution_report()
        print('\nHOSPITAL RECORD')
        print(json.dumps(distribution_report, indent=3))

        while True:
            try:
                user_continue = input('\nWould you like to continue (yes/no)?').strip().lower()
                if user_continue == 'yes':
                    report()
                elif user_continue == 'no':
                    PPEMenu.menu()
                else:
                    print('Please enter a valid input')
            except ValueError:
                print('Please enter a valid input')

    if report_type == 3:
        from datetime import datetime, timedelta

        def read_file(filename):
            with open(filename, 'r') as file:
                return [line.strip().split(',') for line in file]

        def get_value_from_list(data_list, key, key_index, value_index):
            """
            Find value in a list
            based on a key.
            """
            for row in data_list:
                if len(row) > max(key_index, value_index) and row[key_index].strip() == key:
                    return row[value_index].strip()
            return 'Unknown'

        def generate_transaction(month, distributions, ppe_list, suppliers_list, hospitals_list, receives):
            """
            Generate the transaction report
            for the specified month.
            """
            month_start = datetime.strptime(f'{month}-01', '%Y-%m-%d')
            month_end = datetime(month_start.year, month_start.month + 1, 1) - timedelta(days=1)

            distributed = []
            received = []

            for row in distributions:
                try:
                    date = datetime.strptime(row[0].strip(), '%Y-%m-%d')
                    ppe_name = row[1].strip()
                    hospital_code = row[3].strip()
                    quantity = int(row[4].strip())
                    if month_start <= date <= month_end:    # match item code to item name
                        ppe_code = get_value_from_list(ppe_list, ppe_name, 0, 1)
                        hospital_name = get_value_from_list(hospitals_list, hospital_code, 0,
                                                            1)
                        found = False                       # match hospital code to hospital name
                        for item in distributed:
                            if item[0] == ppe_code and item[1] == hospital_code:
                                item[2] += quantity
                                found = True
                                break
                        if not found:
                            distributed.append([ppe_code, hospital_code, quantity, ppe_name, hospital_name])
                except (ValueError, IndexError) as e:
                    print(f"Error processing distribution row: {row}. Error: {e}")

            for row in receives:
                try:
                    date = datetime.strptime(row[0].strip(), '%Y-%m-%d')
                    ppe_code = row[1].strip()
                    quantity = int(row[4].strip())
                    if month_start <= date <= month_end:  # match item code to item name
                        ppe_name = get_value_from_list(ppe_list, ppe_code, 0, 1)
                        supplier_code = row[3].strip()
                        supplier_name = get_value_from_list(suppliers_list, supplier_code, 0,
                                                            1)
                        found = False                       # match supplier code to supplier name
                        for item in received:
                            if item[0] == ppe_code:
                                item[2] += quantity
                                found = True
                                break
                        if not found:
                            received.append([ppe_code, ppe_name, quantity, supplier_code, supplier_name])
                except (ValueError, IndexError) as e:
                    print(f"Error processing receive row: {row}. Error: {e}")

            return received, distributed

        def overall_transaction():
            """
            Main function to generate and display
            the overall transaction report.
            """
            hospitals_list = read_file('hospitals.txt')
            distributions_list = read_file('distribution.txt')
            ppe_list = read_file('ppe.txt')
            suppliers_list = read_file('supplier.txt')
            receives_list = read_file('receive.txt')

            month_input = input('Enter the desired month and year (YYYY-MM): ')
            try:
                datetime.strptime(month_input, '%Y-%m')
            except ValueError:
                print("Invalid month format. Please use YYYY-MM.")
                return

            received_details, distributed_details = generate_transaction(
                month_input, distributions_list, ppe_list, suppliers_list, hospitals_list, receives_list
            )

            print('\nSUPPLIES RECEIVED:')
            if received_details:
                for item in received_details:
                    print(
                        f'Item Code: {item[0]}, Item Name: {item[1]}, Received: {item[2]}, Supplier Code: {item[3]}, '
                        f'Supplier Name: {item[4]}')
            else:
                print('No PPE items received this month.')

            print('\nITEMS DISTRIBUTED:')
            if distributed_details:
                for item in distributed_details:
                    print(
                        f'Item Name: {item[0]}, Item Code: {item[3]}, Distributed: {item[2]}, Hospital Code: {item[1]},'
                        f'Hospital Name: {item[4]}')
            else:
                print('No PPE items distributed this month.')

        overall_transaction()

        while True:
            try:
                user_continue = input('\nWould you like to continue (yes/no)?').strip().lower()
                if user_continue == 'yes':
                    report()
                elif user_continue == 'no':
                    PPEMenu.menu()
                else:
                    print('Please enter a valid input')
            except ValueError:
                print('Please enter a valid input')

    # to return to main menu
    if report_type == 4:
        PPEMenu.menu()


print("Welcome to Inventory Management for Personal Protective Equipment (PPE)\nPlease Log in to proceed")
login()
