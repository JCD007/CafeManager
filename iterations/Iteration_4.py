#------------------------------------------------------ tkinter ----------------------------------------------------------#

# Imports Tk Interface into the program and other tkinter extensions

import tkinter as tk
from tkinter import * 
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image
from getpass import getpass

# Defines function and appearance of the frame

window = tk.Tk()
window.geometry('500x400')
window.title('Cafeteria Program')

#--------------------------------------------------- Variables --------------------------------------------------------------------#

# These variables are lists which will contain other variables

menu_list = ['Ham Sandwhich', 'Sausage Roll', 'Sushi', 'Hot Dog','Mince and Cheese Pie', 'Pizza', 'Noodles', 'Vegan Sandwhich', 'Vegan Salad', 'Vegan Pasta', 'Vegan Chilli', 'Vegan Pie']
receipt_history = []

# This variable is a dictionary containing strings with corresponding values

menu_price = { #Dictionary containing price for menu items
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

# These variables contain string based text

registered = ""
reg_username = ""
reg_password = ""
user_total_order = ""
user_lg = ""
user_ps = ""
user_order = ""
user_quantity = ""
login_key = ""
password_key = ""

#--------------------------------------------------- Functions --------------------------------------------------------------------#

# quit() function opens a process that destroys the frame causing the program to exit

def quit():
    if messagebox.askyesno("Warning!", "Are you sure you want to exit this program?") == True:
        messagebox.showinfo("Pending...", "Exiting Program...")
        window.destroy()
    else:
        return

# login() function opens process to get entry box information and see if user input matches login database

def login():
    global registered
    if not registered:
        messagebox.showerror("Login Failed", "Please register an account first.")
        return
    elif not validate(login_user_entrybox) or not validate(login_pass_entrybox):
        messagebox.showerror("Login Failed", "Login and Password cannot be empty.")
        return
    else:
        global user_lg, user_ps
        user_lg = login_user_entrybox.get()
        user_ps = login_pass_entrybox.get()
        if user_lg == registered['Login'] and user_ps == registered['Password']:
            login_main.destroy()
            label.destroy()
            logo_label.destroy()
            side_panel.pack()
            main_menu.pack()
            order.pack()
        else:
            messagebox.showerror("Error!", "Invalid Username/Password")

# validate() function checks user input entry box if values are empty

def validate(entry):
    if len(entry.get()) == 0:
        return False
    else:
        return True

# Register() function opens process to register new account and add to database / overwrite to file

def register():
    global user_lg, user_ps
    user_lg = login_user_entrybox.get()
    user_ps = login_pass_entrybox.get()
    if messagebox.askyesno("Register New Account", "This action will delete your current registered account and its contents, do you wish to proceed?") == True:
        if not validate(login_user_entrybox) or not validate(login_pass_entrybox):
            messagebox.showerror("Failed to Register Account", "Login and Password cannot be empty.")
            return
        else:
            if messagebox.askyesno("Pending...", 'Are you a student between the ages of 13 - 18 and currently enrolled at Botany Downs Secondary College?') == True:
                with open("Iteration4_Login.txt", "w") as file:
                    file.write("")
                    file.write(f"{user_lg},{user_ps}")
                    global registered
                    registered = {'Login': user_lg, 'Password': user_ps}
                    messagebox.showinfo("Confirmed!", "Account succesfully registered!")
            else:
                messagebox.showerror("Error!", "Sorry, you are not eligible to use this program.")
    else:
        return

# order_menu() function opens a process that switches from 'orderh' frame to 'orderh' frame in the program

def order_history():
    order.pack_forget()
    orderh.pack()

# order_menu() function opens a process that switches from 'orderh' frame to 'order' frame in the program

def order_menu():
    orderh.pack_forget()
    order.pack()

# imported() function opens a process that gets information from file, adding values to login, password, and receipts to database

def imported():
    combo()
    with open("Iteration4_Login.txt", "r") as file:
        for line in file:
            line = line.strip()
            try:
                global registered
                reg_username, reg_password = line.split(',')
                registered = {'Login': reg_username, 'Password': reg_password}
            except ValueError:
                return
            
    with open("Iteration4_Receipts.txt", "r") as file:
        for line in file:
            try:
                user_total_order = line.split(',')
                receipt_history.append(user_total_order)
            except ValueError:
                return

# purchase() function opens a process where the user inputs menu item and quantity calculating the total cost and printing it back to the user

def purchase():
    global user_order, user_quantity, user_total_order
    user_order = order_combobox.get()
    user_quantity = order_spinbox.get()
    user_price = (menu_price[user_order])
    total_price = float(user_price) * float(user_quantity)
    user_total_order = {'MenuItem': user_order, 'Quantity': user_quantity, 'Price': user_price, 'Total': total_price}
    if messagebox.askyesno("Important!", "Are you sure you would like to purchase {} {}/s for ${}?".format(user_quantity, user_order, total_price)) == True:
        messagebox.showinfo("Purchase Confirmed", "Thank you for ordering with us! Your receipt is {}.".format(user_total_order))
        with open("Iteration4_Receipts.txt", "w") as file:
            receipt_history.append(user_total_order)
            for user_total_order in receipt_history:
                file.write(f"{user_total_order}\n")
                combo()

    else:
        return
    
# combo function opens process which changes 'orderh_combobox' combobox values to 'receipt_history' list

def combo():
    global orderh_combobox
    orderh_combobox['values'] = receipt_history

#---------------------------------------------- Main Page ----------------------------------------------------------#

# Variables define tkinter class labels in an 'Main Page' inside the window frame

main_menu = tk.Frame(window)
main_menu.configure(width = 500, height = 400) 
main_menu.place(x=0,y=0)

side_panel = tk.Frame(main_menu, bg = '#121212')
side_panel.pack(side = tk.LEFT)
side_panel.pack_propagate(False)
side_panel.configure(width = 150, height = 400)

main = tk.Frame(main_menu, bg = '#b6d8d2')
main.pack(side = tk.RIGHT)
main.pack_propagate(False)
main.configure(width = 350, height = 400)

side_order = tk.Button(side_panel, text = "Order Menu", command = order_menu, font = ('Franklin Gothic Heavy', 15), bg = '#121212', fg = '#d5d5d5', bd = 0)
side_order.place(x=10, y = 50)

side_orderh = tk.Button(side_panel, text = "Order History", command = order_history, font = ('Franklin Gothic Heavy', 15), bg = '#121212', fg = '#d5d5d5', bd = 0)
side_orderh.place(x=10, y = 100)

side_orderh = tk.Button(side_panel, text = "Quit", command = quit, font = ('Franklin Gothic Heavy', 15), bg = '#121212', fg = '#d5d5d5', bd = 0)
side_orderh.place(x=10, y = 150)

order = tk.Frame(main)
order.pack()
order.propagate(False)
order.configure(width = 350, height = 400, bg = '#d5d5d5')

order_title = tk.Label(order, text="Cafeteria Menu and Ordering", font=('Franklin Gothic Heavy', 18), bg = "#d5d5d5", fg = '#121212')
order_title.pack(pady = 20)

order_combobox = ttk.Combobox(order, values = menu_list, justify = 'center')
order_combobox.pack(padx = 20, pady = 30, side="left", anchor="n")

order_spinbox = tk.Spinbox(order, from_=1, to=10, justify = 'center')
order_spinbox.pack(padx = 10, pady = 30, side="left", anchor="n")

order_button = tk.Button(order, text = "Purchase", command = purchase, font = ('Franklin Gothic Heavy', 15), bg = '#d5d5d5', fg = '#121212', bd = 0)
order_button.place(x=125, y = 180)

#---------------------------------------------- Order Menu ----------------------------------------------------------#

# Variables define tkinter class labels in an 'Order Menu' inside the window frame

orderh = tk.Frame(main)
orderh.pack()
orderh.propagate(False)
orderh.configure(width = 350, height = 400, bg = '#d5d5d5')

orderh_title = tk.Label(orderh, text="Cafeteria Menu Order\nHistory and Transactions", font=('Franklin Gothic Heavy', 18), bg = "#d5d5d5", fg = '#121212')
orderh_title.pack(pady = 20)

orderh_combobox = ttk.Combobox(orderh, width = 50, justify = 'center')
orderh_combobox["values"] = receipt_history
orderh_combobox.pack(padx = 10, pady = 30, anchor="n")

#-------------------------------------------- login webportal ------------------------------------------------------------

# Variables define tkinter class labels in an 'login webportal' inside the window frame

img = tk.PhotoImage(file = "Log In Screen.png")
label =tk.Label(window, image = img)
label.configure(width = 500, height = 400) 
label.place(x=0,y=0)

logo = tk.PhotoImage(file = "bdsc.png")
logo_label =tk.Label(window, image = logo)
logo_label.configure(padx = 10, pady = 10) 
logo_label.place(x=0,y=0)
logo_label.tkraise()

login_main = tk.Frame(window, bg = "#ffffff",)
login_main.pack(expand=True)
login_main.pack_propagate(False)
login_main.configure(width = 300, height = 300, ) 
login_main.pack_configure(anchor=tk.CENTER)
login_main.tkraise()

login_title = tk.Label(login_main, text="Botany Downs Secondary College\nCafeteria Webportal", font=('Franklin Gothic Heavy', 12),  bg = "#ffffff", fg = '#121212')
login_title.pack(pady = 10)

login_user_label = tk.Label(login_main, text = "Login:", font = ('semibold', 10), bg = "#ffffff", fg = '#121212')
login_user_label.pack(pady = 1)
login_user_entrybox = tk.Entry(login_main)
login_user_entrybox.pack(pady = 10)

login_pass_label = tk.Label(login_main, text = "Password:", font = ('semibold', 10), bg = "#ffffff", fg = '#121212')
login_pass_label.pack(pady = 1)
login_pass_entrybox = tk.Entry(login_main)
login_pass_entrybox.pack(pady = 10)

login_login_button = tk.Button(login_main, text = "Login", command = login, font = ('Franklin Gothic Heavy', 10), bg = "#ffffff", fg = '#121212', relief="flat")
login_login_button.pack(padx = 5,pady = 5,side=tk.LEFT)
login_login_button.pack(expand=True)
login_login_button.pack_configure(anchor=tk.CENTER)

login_register_button = tk.Button(login_main, text = "Register", command = register, font = ('Franklin Gothic Heavy', 10), bg = "#ffffff", fg = '#121212', relief="flat")
login_register_button.pack(padx = 5,pady = 5,side=tk.LEFT)
login_register_button.pack(expand=True)
login_register_button.pack_configure(anchor=tk.CENTER)

login_quit_button = tk.Button(login_main, text = "Quit", command = quit, font = ('Franklin Gothic Heavy', 10), bg = "#ffffff", fg = '#121212', relief="flat")
login_quit_button.pack(pady = 5,side=tk.LEFT)
login_quit_button.pack(expand=True)
login_quit_button.pack_configure(anchor=tk.CENTER)

#--------------------------------------------------------------------------------------------------------------------------

# These functions are placed here to begin immediantly upon opening program

imported()
side_panel.pack_forget()
orderh.pack_forget()
window.mainloop()