#------------------------------------------------------ tkinter ----------------------------------------------------------#

# Imports Tk Interface into the program and other tkinter extensions

import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

# Defines function and appearance of the frame

window = tk.Tk()
window.title('Frame Window')    
window.geometry("500x600")  
window.grid()
window.resizable(False, False)

#------------------------------------------------------ variables ----------------------------------------------------------#

# This variable is a dictionary containing strings with corresponding values

menu_price = { 
    "Ham Sandwhich": 5.50,
    "Sausage Roll": 4.50,
    "Sushi": 6.50,
    "Hot Dog": 3.50,
    "Mince and Cheese Pie": 4.00,
    "Pizza": 4.50,
    "Noodles": 1.50,
    "Vegan Sandwhich": 2.50,
    "Vegan Salad": 4.50,
    "Vegan Pasta": 3.50,
    "Vegan Chilli": 5.50,
    "Vegan Pie": 4.00
}

# These variables contain lists that will contain variables

menu_list = ['Ham Sandwhich', 'Sausage Roll', 'Sushi', 'Hot Dog','Mince and Cheese Pie', 'Pizza', 'Noodles', 'Vegan Sandwhich', 'Vegan Salad', 'Vegan Pasta', 'Vegan Chilli', 'Vegan Pie']
receipt_history = []
receipt_history = []

# These variables contain string based text

user_lg = ""
user_ps = ""
user_order = ""
user_quantity = ""
login_key = ""
password_key = ""

#---------------------------------------------------- functions -------------------------------------------------------#

# exit() function opens a process that destroys the frame causing the program to exit

def exit():
    messagebox.showwarning("Pending...", "Exiting Program...")
    window.destroy()

# write() function opens a process that gets information from file, adding values to login and password to database

def write():
    global login_key, password_key
    try:
        with open("Cafe_Iteration3.txt", "r") as file:
            line = file.readline().strip()
            login_key, password_key = line.split(',')
    except:
        print("Except Error")
    return login_key, password_key

def return_():
    mainpage.grid()
    orderpage.grid_remove()
    orderhistory.grid_remove()

# register() function opens process to register new account and add to database / overwrite to file

def register():
    global user_lg, user_ps
    user_lg = lp_entry_lg.get()
    user_ps = lp_entry_ps.get()
    if messagebox.askyesno("Pending...", 'Are you a student between the ages of 13 - 18 and currently enrolled at Botany Downs Secondary College?') == True:
        messagebox.showinfo("Confirmed!", "You are eligible to use our service.")
        with open("Cafe_Iteration3.txt", "w") as file:
            file.write("")
            file.write(f"{user_lg},{user_ps}")
        messagebox.showinfo("Confirmed!", "Account succesfully registered!")
    else:
        messagebox.showerror("Error!", "Sorry, you are not eligible to use this program.")

# Login() function opens process to get entry box information and see if user input matches login database

def login():
    user_lg = lp_entry_lg.get()
    user_ps = lp_entry_ps.get()
    if user_lg in login_key:
        if user_ps in password_key:
            print("Confirmed!", "Successfully signed in")
            mainpage.grid()
            loginpage.grid_remove()
        else:
            messagebox.showerror("Error!", "Invalid Password")
    else:
        messagebox.showerror("Error!", "Invalid Username")

# order() function opens a process that switches from 'mainpage' frame to 'orderpage' frame in the program

def order():
    orderpage.grid()
    mainpage.grid_remove()

# history() function opens a process that switches from 'mainpage' frame to 'orderhistory' frame in the program

def history():
    orderhistory.grid()
    mainpage.grid_remove()

# purchase() function opens a process where the user inputs menu item and quantity calculating the total cost and printing it back to the user

def purchase():
    global user_order, user_quantity, user_total_order
    user_order = od_combobox_mn.get()
    user_quantity = od_spinbox_mn.get()
    user_price = (menu_price[user_order])
    user_total_order = {'MenuItem': user_order, 'Quantity': user_quantity, 'Price': user_price}
    print(user_total_order)
    total_price = float(user_price) * float(user_quantity)
    print("Total: ${}.".format(total_price))
    receipt_history.append(user_total_order)

#----------------------------------------------------- Login Page ---------------------------------------------------------#

# Variables define tkinter class labels in a login page inside the window frame

loginpage = Frame(window, highlightbackground='red',highlightthickness=3, pady=15,padx=15)
loginpage.grid(row=0, column=0,padx=10,pady=10)

lp_label_t = Label(loginpage, text="Botany Downs Secondary College\nCafeteria Manager", font = ('bold', 18))
lp_label_t.grid(row = 0, column = 0, pady=6,padx=6)

lp_label_lg = Label(loginpage, text="Login:", font = ('Arial', 8))
lp_label_lg.grid(row = 4, column = 0,pady=6,padx=6)
lp_entry_lg = Entry(loginpage)
lp_entry_lg.grid(row = 5, column = 0,pady=3, padx=3)

lp_label_ps = Label(loginpage, text="Password:", font = ('Arial', 8))
lp_label_ps.grid(row = 6, column = 0,pady=6,padx=6)
lp_entry_ps = Entry(loginpage)
lp_entry_ps.grid(row = 7, column = 0,pady=3, padx=3)

lp_button_lg = Button(loginpage, text = "Login", command = login, font = ('semibold', 12))
lp_button_lg.grid(row = 8, column = 0, pady=10, padx=10)
lp_button_rg = Button(loginpage, text = "Register", command = register, font = ('semibold', 12))
lp_button_rg.grid(row = 9, column = 0, pady=10, padx=10)

lp_button_ex = Button(loginpage, text = "Exit Program", command = exit, font = ('semibold', 12))
lp_button_ex.grid(row = 10, column = 0, pady=10, padx=10)

#--------------------------------------------------- Main Page -------------------------------------------------------------#

# Variables define tkinter class labels in the frame of the main program inside the window frame

mainpage = Frame(window, width=100, highlightbackground='red',highlightthickness=5, pady=15,padx=15)
mainpage.grid(row=1, column=0,padx=10,pady=10)

mp_label_t = Label(mainpage, text="Botany Downs Secondary College\nCafeteria Manager", font = ('bold', 18))
mp_label_t.grid(row = 2, column = 0, pady=6,padx=6)

mp_button_od = Button(mainpage, text = "Order", command = order, font = ('semibold', 12))
mp_button_od.grid(row = 3, column = 0, pady=10, padx=10)

mp_button_oh = Button(mainpage, text = "Order History", command = history, font = ('semibold', 12))
mp_button_oh.grid(row = 4, column = 0, pady=10, padx=10)

mp_button_ex = Button(mainpage, text = "Exit Program", command = exit, font = ('semibold', 12))
mp_button_ex.grid(row = 10, column = 0, pady=10, padx=10)

#-------------------------------------------------- Order Page ---------------------------------------------------------#

# Variables define tkinter class labels in the order page inside the window frame

orderpage = Frame(window, highlightbackground='red',highlightthickness=3, pady=15,padx=15)
orderpage.grid(row=0, column=0,padx=10,pady=10)

od_label_t = Label(orderpage, text="Order Menu", font = ('bold', 18))
od_label_t.grid(row = 0, column = 0, pady=6,padx=6, sticky = EW)

od_combobox_mn = ttk.Combobox(orderpage, values=menu_list) 
od_combobox_mn.grid(row = 1, column = 0,padx= 10, pady = 10)

od_spinbox_mn = tk.Spinbox( 
    orderpage,
    from_=1, to=10
)
od_spinbox_mn.grid(row=1, column=2,padx=10,pady=10)

od_button_qt = Button(orderpage, text = "Return", command = return_, font = ('semibold', 12))
od_button_qt.grid(row = 2, column = 0, pady=10, padx=10, sticky = W)
od_button_ad = Button(orderpage, text = "Purchase", command = purchase, font = ('semibold', 12))
od_button_ad.grid(row = 2, column = 1, pady=10, padx=10, sticky = E)

#------------------------------------------------------ Order History ---------------------------------------------------------#

# Variables define tkinter class labels in a login page inside the window frame

orderhistory = Frame(window, highlightbackground='red',highlightthickness=3, pady=15,padx=15)
orderhistory.grid(row=0, column=0,padx=10,pady=10)

oh_label_t = Label(orderhistory, text="Order Menu", font = ('bold', 18))
oh_label_t.grid(row = 0, column = 0, pady=6,padx=6, sticky = EW)

# Checks if var 'receipt_history' exists and attempts to change combobox values to 'user_total_order' variable

if receipt_history: 
    oh_combobox_mn = ttk.Combobox(orderhistory, values=[user_total_order])
    oh_combobox_mn.current(0)
else:
    oh_combobox_mn = ttk.Combobox(orderhistory, values=["No recorded order"]) 
oh_combobox_mn.grid(row = 1, column = 0, pady=10, padx=10)

oh_button_qt = Button(orderhistory, text = "Return", command = return_, font = ('semibold', 12))
oh_button_qt.grid(row = 2, column = 0, pady=10, padx=10,)

#------------------------------------------------------ Main ---------------------------------------------------------#

# Runs the tkinter loop event opening the program

window.mainloop()

# These functions / processes are placed here to begin immediantly upon opening program

write()
loginpage.grid()
mainpage.grid_remove()
orderpage.grid_remove()
orderhistory.grid_remove()
