#------------------------------------------------------------  Variables ----------------------------------------------#

# These variables are lists which will contain other variables

user_total_order = []
priced_menu = []
user_order_list = []
user_quantity_list = []
menu_list = ['Ham Sandwhich', 'Sausage Roll', 'Sushi', 'Hot Dog','Mince and Cheese Pie', 'Pizza', 'Noodles', 'Vegan Sandwhich', 'Vegan Salad', 'Vegan Pasta', 'Vegan Chilli', 'Vegan Pie'] #List containing menu items

# This variable is a dictionary containing strings with corresponding values

menu_price = { 
    "Ham Sandwhich": 5.50,
    "Sausage Roll": 4.50,
    "Sushi": 6.50,
    "Hot Dog": 3.50,
    "Mince and Cheese Pie": 4.00,
    "Pizza": 4.99,
    "Noodles": 1.50,
    "Vegan Sandwhich": 2.50,
    "Vegan Salad": 4.50,
    "Vegan Pasta": 3.50,
    "Vegan Chilli": 5.50,
    "Vegan Pie": 4.00
}

# These variables contain string based text

main = "\n1) See Menu\n2) Order\n3) Exit Program" 
login_main = "\n1) Login\n2) Register new account\n4) Exit Program"
login = ""
login_name = ""
password = ""
login_password = ""
banana = ''
user_price = ""

# These variables contain numbered integers

i = 0
total_price = 0

#------------------------------------------------------------ Functions -------------------------------------------------------#
    
# Register() function opens process to register new account and add to database / overwrite to file

def Register():
    with open("Iteration2_Login.txt", "w") as file:
        file.write("")
        login_name = input("\nPlease enter new login name: ")
        login_password = input("Please enter new password: ")
        login, password = login_name, login_password
        with open("Iteration2_Login.txt", "w") as file:
            file.write(f"{login},{password}")
        Main()

# Login() function opens process to get entry box information and see if user input matches login database

def Login():
    while i <= 0:
        try:
            login_name = input("\nPlease enter login name: ")
            login_password = input("Please enter password: ")
            if login_name in login:
                if login_password in password:
                    print("\nWelcome {}, you are now being directed to the Botany Downs Secondary College's cafeteria menu".format(login))
                    Main()
                else:
                    print("Login/Password is invalid.")
                    break
            else:
                print("Login/Password is invalid.")
                break
        except:
            print("Except Error")
            break

# Login_Main() function opens a process that allows the user to interact with a login menu

def Login_Main():
    print("\nWelcome to the Botany Downs Secondary College's cafeteria login page.".format(login))
    while i <= 0:
        try:
            print(login_main)
            user_input = input("\nPlease enter choice in integer: ")
            if user_input == '1': 
                Login()
            elif user_input == '2': 
                Register()
            elif user_input == '3': 
                Quit()
            else:
                print("\nPlease enter in the given values.")
        except:
            print("\nPlease enter value in integers.")

# Main() function opens a process that allows the user to interact with decisions in the main program

def Main():
    while i <= 0:
        try:
            print(main)
            user_input = input("\nPlease enter choice in integer: ")
            if user_input == '1':
               print("\nRegular Menu", priced_menu)
            elif user_input == '2': 
                Order()
            elif user_input == '3':
                Quit()
            else:
                print("\nPlease enter in the given values.")
        except:
            print("\nPlease enter value in integers.")

# Order() function opens a process where the user inputs menu item and quantity calculating the total cost and printing it back to the user

def Order():
    global user_total_order
    print(menu_price)
    i = 0
    while i <= 0:
        user_order = input("\nPlease enter name of the item on menu: ")
        if user_order in menu_list:
            user_quantity = int(input("Enter quantity of the item: "))
            user_price = (menu_price[user_order])
            user_total_order = {'MenuItem': user_order, 'Quantity': user_quantity, 'Price': user_price}
            print(user_total_order)
            total_price = user_price * user_quantity
            print("Total: ${}.".format(total_price))
            break
    else:
        print("This item is not on the menu.")

# Quit() function opens a process that changes integer value causing the program to exit

def Quit():
    global i
    i += 1

# Import() function opens a process that gets information from file, adding values to login and password to database

def Import():
    global login, password
    try:
        with open("Iteration2_Login.txt", "r") as file:
            line = file.readline().strip()
            login, password = line.split(',')
    except:
        print("Except Error")
    return login, password

#------------------------------------------------------------ Main ------------------------------------------------------------#

# These functions are placed here to begin immediantly upon opening program

Import()
Login_Main()
Main()
