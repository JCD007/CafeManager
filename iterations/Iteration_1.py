#------------------------------------------------------------ Defining Variables ----------------------------------------------#

main = "\n1) See Menu\n2) See Menu (vegetarian)\n3) Exit Program" #Contains the main body user can view
menu = ['Ham_Sandwhich','Sausage Roll','Sushi','Hot Dog','Mince_and_Cheese_Pie','Pizza'] #List containing menu items
menu_price = ['$5.50','$4.50','$6.50','$3.50','$4.00','$4.99'] #List containing price for menu items
veg_menu = ['\nJam_Sandwhich','Vegan_Curry','Kale_Salad','Pesto_Pasta','Vegan_Chilli','Apple_Pie'] #List containing vegeterian/vegan menu items
veg_menu_price = ['$2.50','$4.50','$3.50','$4.00','$5.50','$4.00'] #List containing price for vegetarian/vegan menu items
i = 0

#------------------------------------------------------------ Functions -------------------------------------------------------#

priced_menu = [] #List containing menu items and prices
for str1, str2 in zip(menu, menu_price):
    split1 = str1.split() #Splits string from 'menu' list
    split2 = str2.split() #Splits string from 'menu_price' list
    merge = " : ".join(split1+split2) #Combines 'split1' and 'split2' variables into a variable
    priced_menu.append(merge) #Adds 'merge' to a list

priced_veg_menu = []#List containing vegeterian menu items and prices
for str1, str2 in zip(veg_menu, veg_menu_price):
    split1 = str1.split() #Splits string from 'veg_menu' list
    split2 = str2.split() #Splits string from 'veg_menu_price' list
    merge = " : ".join(split1+split2) #Combines 'split1' and 'split2' variables into a variable
    priced_veg_menu.append(merge) #Adds 'merge' to a list

#------------------------------------------------------------ Main ------------------------------------------------------------#

username = input("Enter Name: ")
print("\nWelcome {}, you are now being directed to the Botany Downs Secondary College's cafeteria menu".format(username))
while i <= 0:
    try:
        print(main)
        user_input = int(input("\nPlease enter choice in integer: "))
        if user_input == 1:
            print(priced_menu)
        elif user_input == 2: 
            print(priced_veg_menu) 
        elif user_input == 3:
            break
        else:
            print("\nPlease enter in the given values.")
    except:
        print("\nPlease enter value in integers.")