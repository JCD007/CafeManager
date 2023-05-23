
# Imports Tk Interface into the program and other tkinter extensions
import os
import yaml
import requests
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import datetime
import random

DEBUG = True

def _log(msg):
    if debug == True:
        print(msg)

## Init Server Connection
def init_server():
    global CONFIG, BASE_URI, SESSION
    with open(file="config.yaml", mode="r") as f:
        try:
            CONFIG = yaml.load(f, Loader=yaml.FullLoader) 
            BASE_URI = f"{CONFIG['SERVER']['URI']}:{CONFIG['SERVER']['PORT']}/api/v{CONFIG['SERVER']['VERSION']}"
            f.close()
            SESSION = requests.Session()
            if DEBUG:
                SESSION.verify = False
                SESSION.trust_env = False
                os.environ['CURL_CA_BUNDLE']="" # Disable SSL Verification for Test, you would not do this in production.
            return True
        except yaml.YAMLError as exc:
            print(exc) 
            return False   

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Defines function and appearance of the frame

window = ctk.CTk()
window.geometry(f"{500}x{400}")
window.title('Cafeteria Program')
window.resizable(False, False)

#------------------------------------------------------ variables  ----------------------------------------------------------#

# These variables are lists which will contain other variables

receipt_history = []
trolley_list = []
registered_accounts = []
vegan_list = ['Noodles', 'Garlic Bread', 'Salad', 'Sandwhich', 'Wrap', 'Slushies', 'Juicies', 'Water', 'Lipton', 'Soft Drink']
menu_list = ['Noodles', 'Meat Pie', 'Garlic Bread', 'Hot Dogs','Sushi', 'Sandwhich', 'Salad', 'Wrap', 'Magnum', 'Moosies', 'Slushies', 'Juicies', 'Water', 'Soft Drink', 'Lipton', 'Coffee'] #List containing menu items

# This variable is a dictionary containing strings with corresponding values

menu_price = { 
    "Noodles": 3.80,
    "Meat Pie": 4.80,
    "Garlic Bread": 2.00,
    "Hot Dogs": 4.00,
    "Sushi": 5.80,
    "Sandwhich": 4.80,
    "Salad": 7.50,
    "Wrap": 5.50,
    "Magnum": 4.50,
    "Moosies": 2.00,
    "Slushies": 2.50,
    "Juicies": 1.00,
    "Water": 4.00,
    "Soft Drink": 3.50,
    "Lipton": 4.50,
    "Coffee": 4.50
}

# These variables contain string based text

user_lg = ""
user_ps = ""
quantity = ""
user_order = ""
user_quantity = ""
remove_item = False
price = ""
login_key = ""
password_key = ""
registered = ""
reg_username = ""
reg_password = ""
user_total_order = ""

# These variables contain numbered integers

indicator = 0

vegan = False

#---------------------------------------------------- functions -------------------------------------------------------------#

def exit():
    msg = CTkMessagebox(title="Warning!", message="Are you sure you want to quit this program?",
                        icon="warning.png", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()
    if response=="Yes":
        window.destroy()       
    else:
        return

def validate(entry):
    if len(entry.get()) == 0:
        return False
    else:
        return True

def register():
    global user_lg, user_ps
    user_lg = lp_entry1.get()
    user_ps = lp_entry2.get()
    msg = CTkMessagebox(title="Confirm?", message="Are you sure you want to register this account?",
                            icon="info.png", option_1="Cancel", option_2="No", option_3="Yes")
    response = msg.get()
    if response == "Yes":
        if len(user_lg) <= 8:
            for account in registered_accounts:
                        if user_lg == account['Login']:
                            msg = CTkMessagebox(title="Error!", message="Sorry, this username has been taken.",
                                icon="failure.png", option_1="Ok")
                            return
            if not validate(lp_entry1) or not validate(lp_entry2):
                CTkMessagebox(title="Important!", message="Login and Password cannot be empty.",
                                icon="warning.png", option_1="Ok")
                return
            else:
                msg = CTkMessagebox(title="Confirm?", message="Are you a student between the ages of 13 - 18 and currently enrolled at Botany Downs Secondary College?",
                                icon="info.png", option_1="No", option_2="Yes")
                response = msg.get()
                if response == "Yes":
                    with open("Iteration5_Login.txt", "a") as file:
                        file.write(f"{user_lg},{user_ps}\n") 
                        registered_accounts.append({'Login': user_lg, 'Password': user_ps})  
                        CTkMessagebox(title="Confirmed!", message="Your account has been successfully registered!",
                        icon="success.png", option_1="Ok")
                else:
                    CTkMessagebox(title="Access Denied!", message="Sorry, you are not eligible to use this program.",
                                icon="failure.png", option_1="Ok")
        else:
            CTkMessagebox(title="Error!", message="Sorry, you are above the accepted username limit of 8 characters.",
                                icon="failure.png", option_1="Ok")
    else:
        return

def login():
    global registered_accounts, account

    # Create a session to the webservice to login
    res = SESSION.post(url=F"{BASE_URI}/auth", json={"username": lp_entry1.get(), "password": lp_entry2.get()}) 

    # user_lg = lp_entry1.get()
    # user_ps = lp_entry2.get()

    if res.status_code == 200: # Authrised
        page2()
    elif res.status_code == 401: # Invalid
        pass
    elif res.status_code == 500:
        pass



    # if not registered_accounts:
    #     msg = CTkMessagebox(title="Error!", message="Login Failed, Please register an account first.",
    #                         icon="warning.png", option_1="Ok")
    #     return
    # elif not validate(lp_entry1) or not validate(lp_entry2):
    #     msg = CTkMessagebox(title="Error!", message="Login Failed, Login and Password cannot be empty.",
    #                         icon="warning.png", option_1="Ok")
    #     return
    # else:
    #     for account in registered_accounts:
    #         if user_lg == account['Login'] and user_ps == account['Password']:
    #             page2()
    #             return
    #     msg = CTkMessagebox(title="Error!", message="Login Failed, Invalid Username/Password.",
    #                         icon="warning.png", option_1="Ok")

# def imported():
#     global registered_accounts
#     registered_accounts = []  # Clear the existing registered accounts list
#     with open("Iteration5_Login.txt", "r") as file:
#         for line in file:
#             line = line.strip()
#             try:
#                 reg_username, reg_password = line.split(',')
#                 registered_accounts.append({'Login': reg_username, 'Password': reg_password})
#             except ValueError:
#                 return

def show_password():
    if lp_check.get():
        lp_entry2.configure(show="")
    else:
        lp_entry2.configure(show="•")

#-------------------------------------------------- Login Page ---------------------------------------------------------------#

def page1():

    global lp_entry1, lp_entry2, lp_check, img_path

    img_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")

    b_img = ctk.CTkImage(Image.open(os.path.join(img_path, "log_in_screen_2.png")), size = (500, 400))
                         
    b_img_label = ctk.CTkLabel(window, image = b_img, width = 500, height = 400)
    b_img_label.place(x=0,y=0)

    login_frame = ctk.CTkFrame(window, corner_radius=30, fg_color='#ffffff', bg_color="#ffffff")
    login_frame.pack(pady = 40, padx = 100, fill = 'both', expand = True)

    lp_label = ctk.CTkLabel(login_frame, text="Cafeteria Sign in\nWeb Portal", font=("Roboto", 24))
    lp_label.pack(pady = 12, padx =10)

    lp_entry1 = ctk.CTkEntry(login_frame, placeholder_text = "Username", width = 175, bg_color="#ffffff", border_width = 1.5)
    lp_entry1.pack(padx = 10, pady = 10)

    lp_entry2 = ctk.CTkEntry(login_frame, placeholder_text = "Password", show = "•", width = 175, bg_color="#ffffff", border_width = 1.5)
    lp_entry2.pack(padx = 10, pady = 5)

    lp_check = ctk.CTkCheckBox(login_frame, text = "Show Password?", command = show_password, checkbox_height= 18, checkbox_width=18)
    lp_check.place(x = 63, y = 173)

    lp_button1 = ctk.CTkButton(login_frame, text = "Login", command = login, width = 175)
    lp_button1.pack(padx = 10, pady = 50)

    lp_button2 = ctk.CTkButton(login_frame, text = "Register", command = register, width = 75)
    lp_button2.place(x = 63, y = 260)

    lp_button3 = ctk.CTkButton(login_frame, text = "Quit", command = exit, width=75)
    lp_button3.place(x = 162, y = 260)

#-------------------------------------------------- Menu Page ---------------------------------------------------------------#

main = ctk.CTkFrame(window, fg_color='#2a2a2a', corner_radius = 10, bg_color='#191819')

def page2():

    global main, side_nav

    background = ctk.CTkFrame(window, fg_color='#191819')
    background.configure(width = 500, height =400)
    background.place(x = 0 ,y = 0)

    main = ctk.CTkFrame(window, fg_color='#2a2a2a', corner_radius = 10, bg_color='#191819')
    main.configure(width = 300, height =360)
    main.place(x = 180 ,y = 20)

    side_nav_top = ctk.CTkFrame(window, fg_color='#2a2a2a', corner_radius = 10, bg_color='#191819')
    side_nav_top.configure(width = 140, height = 110)
    side_nav_top.place(x = 20, y = 20)

    side_nav = ctk.CTkFrame(window, fg_color='#2a2a2a', corner_radius = 10, bg_color='#191819')
    side_nav.configure(width = 140, height = 240)
    side_nav.place(x = 20, y = 140)

    p2_img0 = ctk.CTkImage(Image.open("bdsc logo.png"), size = (125, 90))
    bdsc_logo = ctk.CTkLabel(side_nav_top, text = "", image = p2_img0, width = 125, height = 80)
    bdsc_logo.place(x = 10, y = 10)

    p2_img1 = ctk.CTkImage(Image.open("menu.png"), size = (100, 30))
    menu = ctk.CTkButton(side_nav, text="", image = p2_img1, width= 120, command = menu_frame, height = 40)
    menu.place(x = 10, y = 10)

    p2_img2 = ctk.CTkImage(Image.open("order.png"), size = (100, 30))
    order = ctk.CTkButton(side_nav, text="", image = p2_img2, width= 120, command = order_frame, height = 40)
    order.place(x = 10, y = 60)

    p2_img3 = ctk.CTkImage(Image.open("history.png"), size = (100, 30))
    history = ctk.CTkButton(side_nav, text="", image = p2_img3, command = history_frame, width= 120, height = 40)
    history.place(x = 10, y = 110)

    p2_img4 = ctk.CTkImage(Image.open("exit.png"), size = (100, 30))
    quit = ctk.CTkButton(side_nav, text="", image = p2_img4, command = exit, width= 120, height = 40)
    quit.place(x = 10, y = 190)

    menu_frame()

#-------------------------------------------- Menu Page Configuration ---------------------------------------------------------------#

mf_title = ctk.CTkLabel(main, text = "Transaction\nHistory", font = ("bold", 35), text_color = "#ffffff")
mf_button1 = ctk.CTkButton(main)
mf_button2 = ctk.CTkButton(main)
mf_button3 = ctk.CTkButton(main)
mf_button4 = ctk.CTkButton(main)
mf_title1 = ctk.CTkLabel(main)
mf_title2 = ctk.CTkLabel(main)

goback_arrow = ctk.CTkButton(main)

hotfood_title = ctk.CTkLabel(main)
hotfood_label_t1 = ctk.CTkLabel(main)
hotfood_label_t2 = ctk.CTkLabel(main)
hotfood_label_t3 = ctk.CTkLabel(main)
hotfood_label_t4 = ctk.CTkLabel(main)
hotfood_label1 = ctk.CTkLabel(main)
hotfood_label2 = ctk.CTkLabel(main)
hotfood_label3 = ctk.CTkLabel(main)
hotfood_label4 = ctk.CTkLabel(main)
hotfood_label5 = ctk.CTkLabel(main)
hotfood_label6 = ctk.CTkLabel(main)
hotfood_label7 = ctk.CTkLabel(main)
hotfood_label8 = ctk.CTkLabel(main)

coldfood_title = ctk.CTkLabel(main)
coldfood_label_t1 = ctk.CTkLabel(main)
coldfood_label_t2 = ctk.CTkLabel(main)
coldfood_label_t3 = ctk.CTkLabel(main)
coldfood_label_t4 = ctk.CTkLabel(main)
coldfood_label1 = ctk.CTkLabel(main)
coldfood_label2 = ctk.CTkLabel(main)
coldfood_label3 = ctk.CTkLabel(main)
coldfood_label4 = ctk.CTkLabel(main)
coldfood_label5 = ctk.CTkLabel(main)
coldfood_label6 = ctk.CTkLabel(main)
coldfood_label7 = ctk.CTkLabel(main)
coldfood_label8 = ctk.CTkLabel(main)

desserts_title = ctk.CTkLabel(main)
desserts_label_t1 = ctk.CTkLabel(main)
desserts_label_t2 = ctk.CTkLabel(main)
desserts_label_t3 = ctk.CTkLabel(main)
desserts_label_t4 = ctk.CTkLabel(main)
desserts_label1 = ctk.CTkLabel(main)
desserts_label2 = ctk.CTkLabel(main)
desserts_label3 = ctk.CTkLabel(main)
desserts_label4 = ctk.CTkLabel(main)
desserts_label5 = ctk.CTkLabel(main)
desserts_label6 = ctk.CTkLabel(main)
desserts_label7 = ctk.CTkLabel(main)
desserts_label8 = ctk.CTkLabel(main)

drinks_title = ctk.CTkLabel(main)
drinks_label_t1 = ctk.CTkLabel(main)
drinks_label_t2 = ctk.CTkLabel(main)
drinks_label_t3 = ctk.CTkLabel(main)
drinks_label_t4 = ctk.CTkLabel(main)
drinks_label1 = ctk.CTkLabel(main)
drinks_label2 = ctk.CTkLabel(main)
drinks_label3 = ctk.CTkLabel(main)
drinks_label4 = ctk.CTkLabel(main)
drinks_label5 = ctk.CTkLabel(main)
drinks_label6 = ctk.CTkLabel(main)
drinks_label7 = ctk.CTkLabel(main)
drinks_label8 = ctk.CTkLabel(main)

of_title = ctk.CTkLabel(main)
of_item = ctk.CTkComboBox(main)
of_price = ctk.CTkEntry(main)
of_add = ctk.CTkComboBox(main)
of_quantity = ctk.CTkComboBox(main)
of_fprice = ctk.CTkEntry(main)
of_add = ctk.CTkButton(main)
of_title2 = ctk.CTkLabel(main)
of_pitem = ctk.CTkComboBox(main)
of_fpprice = ctk.CTkEntry(main)
of_buy = ctk.CTkButton(main)
of_check = ctk.CTkCheckBox(main)
of_rid = ctk.CTkButton(main)

hf_title = ctk.CTkLabel(main)
hf_receipt = ctk.CTkComboBox(main)
hf_food_item = ctk.CTkComboBox(main)
hf_food_quantity = ctk.CTkComboBox(main)
hf_food_tp = ctk.CTkComboBox(main)
hf_food_price = ctk.CTkComboBox(main)
hf_date = ctk.CTkComboBox(main,)

#-------------------------------------------------------------------------------------------------------------------#

# menu_frame() function opens process creating a frame for the programs menu

def menu_frame():

    global mf_title, mf_button1, mf_button2, mf_button3, mf_button4, mf_title1, mf_title2

    hide()

    mf_title1 = ctk.CTkLabel(main, text = "Welcome back,", font = ("bold", 12), text_color = "#ffffff")
    mf_title1.place(x = 17, y = 10)
    mf_title2 = ctk.CTkLabel(main, text = "", font = ("bold", 35), text_color = "#ffffff")
    mf_title2.place(x = 15, y = 30)
    mf_title2.configure(text=f"{account['Login']}!")
    mf_img1 = ctk.CTkImage(Image.open("hot food.png"), size = (100, 100))
    mf_button1 = ctk.CTkButton(main, image = mf_img1, text="", command = menu_hotfood, height = 125, width = 125)
    mf_button1.place(x = 15, y = 80)
    mf_img2 = ctk.CTkImage(Image.open("cold food.png"), size = (100, 100))
    mf_button2 = ctk.CTkButton(main, image = mf_img2, text="", command = menu_coldfood, height = 125, width = 125)
    mf_button2.place(x = 160, y = 80)
    mf_img3 = ctk.CTkImage(Image.open("dessert.png"), size = (100, 100))
    mf_button3 = ctk.CTkButton(main, image = mf_img3, text="", command = menu_desserts, height = 125, width = 125)
    mf_button3.place(x = 15, y = 220)
    mf_img4 = ctk.CTkImage(Image.open("drinks.png"), size = (100, 100))
    mf_button4 = ctk.CTkButton(main, image = mf_img4, text="", command = menu_drinks, height = 125, width = 125)
    mf_button4.place(x = 160, y = 220)

# go_back() function opens process changing to the menu frame

def go_back():

    global goback_arrow

    goback_arrow_img = ctk.CTkImage(Image.open("go back.png"), size = (20, 20))
    goback_arrow = ctk.CTkButton(main, image = goback_arrow_img, text = "", command = menu_frame, width= 25, height = 35, fg_color="#191819")
    goback_arrow.place(x=15, y=15)

# go_back() function opens process 

def menu_hotfood():

    global hotfood_title, hotfood_label_t1, hotfood_label_t2, hotfood_label_t3, hotfood_label_t4 ,hotfood_label1, hotfood_label2, hotfood_label3, hotfood_label4, hotfood_label5, hotfood_label6, hotfood_label7, hotfood_label8

    hide()
    go_back()

    hotfood_title = ctk.CTkLabel(main, text = "Hot Foods", font = ("bold", 35), text_color = "#ffffff")
    hotfood_title.place(x = 70, y = 20)
    hotfood_img1 = ctk.CTkImage(Image.open("noodles.png"), size = (125, 100))
    hotfood_label_t1 = ctk.CTkLabel(main, image = hotfood_img1, text="", height = 80, width = 125)
    hotfood_label_t1.place(x = 15, y = 70)
    hotfood_label1 = ctk.CTkLabel(main, width= 40, height = 20, text="$3.80", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    hotfood_label1.place(x = 15, y = 175)
    hotfood_label2 = ctk.CTkLabel(main, width= 75, height = 21, text="Noodles", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    hotfood_label2.place(x = 65, y = 175)

    hotfood_img2 = ctk.CTkImage(Image.open("pie.png"), size = (125, 100))
    hotfood_label_t2 = ctk.CTkLabel(main, image = hotfood_img2, text="", height = 80, width = 125)
    hotfood_label_t2.place(x = 15, y = 215)
    hotfood_label3 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.80", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    hotfood_label3.place(x = 15, y = 325)
    hotfood_label4 = ctk.CTkLabel(main, width= 75, height = 21, text="Meat Pie", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    hotfood_label4.place(x = 65, y = 325)

    hotfood_img3 = ctk.CTkImage(Image.open("garlic bread.png"), size = (125, 100))
    hotfood_label_t3 = ctk.CTkLabel(main, image = hotfood_img3, text="", height = 80, width = 125)
    hotfood_label_t3.place(x = 160, y = 70)
    hotfood_label5 = ctk.CTkLabel(main, width= 40, height = 20, text="$2.00", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    hotfood_label5.place(x = 160, y = 175)
    hotfood_label6 = ctk.CTkLabel(main, width= 75, height = 21, text="Garlic Bread", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    hotfood_label6.place(x = 210, y = 175)

    hotfood_img4 = ctk.CTkImage(Image.open("hot dogs.png"), size = (125, 100))
    hotfood_label_t4 = ctk.CTkLabel(main, image = hotfood_img4, text="", height = 80, width = 125)
    hotfood_label_t4.place(x = 160, y = 215)
    hotfood_label7 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.00", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    hotfood_label7.place(x = 160, y = 325)
    hotfood_label8 = ctk.CTkLabel(main, width= 75, height = 21, text="Hot Dogs", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    hotfood_label8.place(x = 210, y = 325)

    veganlabel_img = ctk.CTkImage(Image.open("vegan.png"), size = (35, 35))
    veganlabel1 = ctk.CTkLabel(hotfood_label_t1, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel1.place(x = 5, y = 5)
    veganlabel2 = ctk.CTkLabel(hotfood_label_t3, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel2.place(x = 5, y = 5)
      
def menu_coldfood():
    
    global coldfood_title, coldfood_label_t1, coldfood_label_t2, coldfood_label_t3, coldfood_label_t4 ,coldfood_label1, coldfood_label2, coldfood_label3, coldfood_label4, coldfood_label5, coldfood_label6, coldfood_label7, coldfood_label8

    hide()
    go_back()

    coldfood_title = ctk.CTkLabel(main, text = "Cold Foods", font = ("bold", 35), text_color = "#ffffff")
    coldfood_title.place(x = 70, y = 20)
    coldfood_img1 = ctk.CTkImage(Image.open("sushi.png"), size = (125, 100))
    coldfood_label_t1 = ctk.CTkLabel(main, image = coldfood_img1, text="", height = 80, width = 125)
    coldfood_label_t1.place(x = 15, y = 70)
    coldfood_label1 = ctk.CTkLabel(main, width= 40, height = 20, text="$5.80", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    coldfood_label1.place(x = 15, y = 175)
    coldfood_label2 = ctk.CTkLabel(main, width= 75, height = 21, text="Sushi", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    coldfood_label2.place(x = 65, y = 175)

    coldfood_img2 = ctk.CTkImage(Image.open("sandwhich.png"), size = (125, 100))
    coldfood_label_t2 = ctk.CTkLabel(main, image = coldfood_img2, text="", height = 80, width = 125)
    coldfood_label_t2.place(x = 15, y = 215)
    coldfood_label3 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.80", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    coldfood_label3.place(x = 15, y = 325)
    coldfood_label4 = ctk.CTkLabel(main, width= 75, height = 21, text="Sandwhich", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    coldfood_label4.place(x = 65, y = 325)

    coldfood_img3 = ctk.CTkImage(Image.open("salad.png"), size = (125, 100))
    coldfood_label_t3 = ctk.CTkLabel(main, image = coldfood_img3, text="", height = 80, width = 125)
    coldfood_label_t3.place(x = 160, y = 70)
    coldfood_label5 = ctk.CTkLabel(main, width= 40, height = 20, text="$7.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    coldfood_label5.place(x = 160, y = 175)
    coldfood_label6 = ctk.CTkLabel(main, width= 75, height = 21, text="Salad", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    coldfood_label6.place(x = 210, y = 175)

    coldfood_img4 = ctk.CTkImage(Image.open("wrap.png"), size = (125, 100))
    coldfood_label_t4 = ctk.CTkLabel(main, image = coldfood_img4, text="", height = 80, width = 125)
    coldfood_label_t4.place(x = 160, y = 215)
    coldfood_label7 = ctk.CTkLabel(main, width= 40, height = 20, text="$5.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    coldfood_label7.place(x = 160, y = 325)
    coldfood_label8 = ctk.CTkLabel(main, width= 75, height = 21, text="Wrap", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    coldfood_label8.place(x = 210, y = 325)

    veganlabel_img = ctk.CTkImage(Image.open("vegan.png"), size = (35, 35))
    veganlabel1 = ctk.CTkLabel(coldfood_label_t1, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel1.place(x = 5, y = 5)
    veganlabel2 = ctk.CTkLabel(coldfood_label_t2, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel2.place(x = 5, y = 5)
    veganlabel3 = ctk.CTkLabel(coldfood_label_t3, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel3.place(x = 5, y = 5)
    veganlabel4 = ctk.CTkLabel(coldfood_label_t4, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel4.place(x = 5, y = 5)

def menu_desserts():
    
    global desserts_title, desserts_label_t1, desserts_label_t2, desserts_label_t3, desserts_label_t4 ,desserts_label1, desserts_label2, desserts_label3, desserts_label4, desserts_label5, desserts_label6, desserts_label7, desserts_label8

    hide()
    go_back()

    desserts_title = ctk.CTkLabel(main, text = "Desserts", font = ("bold", 35), text_color = "#ffffff")
    desserts_title.place(x = 85, y = 20)
    desserts_img1 = ctk.CTkImage(Image.open("magnum.png"), size = (125, 100))
    desserts_label_t1 = ctk.CTkLabel(main, image = desserts_img1, text="", height = 80, width = 125)
    desserts_label_t1.place(x = 15, y = 70)
    desserts_label1 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    desserts_label1.place(x = 15, y = 175)
    desserts_label2 = ctk.CTkLabel(main, width= 75, height = 21, text="Magnum", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    desserts_label2.place(x = 65, y = 175)

    desserts_img2 = ctk.CTkImage(Image.open("moosies.png"), size = (125, 100))
    desserts_label_t2 = ctk.CTkLabel(main, image = desserts_img2, text="", height = 80, width = 125)
    desserts_label_t2.place(x = 15, y = 215)
    desserts_label3 = ctk.CTkLabel(main, width= 40, height = 20, text="$2.00", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    desserts_label3.place(x = 15, y = 325)
    desserts_label4 = ctk.CTkLabel(main, width= 75, height = 21, text="Moosies", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    desserts_label4.place(x = 65, y = 325)

    desserts_img3 = ctk.CTkImage(Image.open("slushies.png"), size = (125, 100))
    desserts_label_t3 = ctk.CTkLabel(main, image = desserts_img3, text="", height = 80, width = 125)
    desserts_label_t3.place(x = 160, y = 70)
    desserts_label5 = ctk.CTkLabel(main, width= 40, height = 20, text="$2.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    desserts_label5.place(x = 160, y = 175)
    desserts_label6 = ctk.CTkLabel(main, width= 75, height = 21, text="Slushies", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    desserts_label6.place(x = 210, y = 175)

    desserts_img4 = ctk.CTkImage(Image.open("juicies.png"), size = (125, 100))
    desserts_label_t4 = ctk.CTkLabel(main, image = desserts_img4, text="", height = 80, width = 125)
    desserts_label_t4.place(x = 160, y = 215)
    desserts_label7 = ctk.CTkLabel(main, width= 40, height = 20, text="$1.00", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    desserts_label7.place(x = 160, y = 325)
    desserts_label8 = ctk.CTkLabel(main, width= 75, height = 21, text="Juicies", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    desserts_label8.place(x = 210, y = 325)

    veganlabel_img = ctk.CTkImage(Image.open("vegan.png"), size = (35, 35))
    veganlabel3 = ctk.CTkLabel(desserts_label_t3, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel3.place(x = 5, y = 5)
    veganlabel4 = ctk.CTkLabel(desserts_label_t4, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel4.place(x = 5, y = 5)

def menu_drinks():
    
    global drinks_title, drinks_label_t1, drinks_label_t2, drinks_label_t3, drinks_label_t4 ,drinks_label1, drinks_label2, drinks_label3, drinks_label4, drinks_label5, drinks_label6, drinks_label7, drinks_label8

    hide()
    go_back()

    drinks_title = ctk.CTkLabel(main, text = "Drinks", font = ("bold", 35), text_color = "#ffffff")
    drinks_title.place(x = 105, y = 20)
    drinks_img1 = ctk.CTkImage(Image.open("water.png"), size = (125, 100))
    drinks_label_t1 = ctk.CTkLabel(main, image = drinks_img1, text="", height = 80, width = 125)
    drinks_label_t1.place(x = 15, y = 70)
    drinks_label1 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.00", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    drinks_label1.place(x = 15, y = 175)
    drinks_label2 = ctk.CTkLabel(main, width= 75, height = 21, text="Water", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    drinks_label2.place(x = 65, y = 175)

    drinks_img2 = ctk.CTkImage(Image.open("soft drink.png"), size = (125, 100))
    drinks_label_t2 = ctk.CTkLabel(main, image = drinks_img2, text="", height = 80, width = 125)
    drinks_label_t2.place(x = 15, y = 215)
    drinks_label3 = ctk.CTkLabel(main, width= 40, height = 20, text="$3.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    drinks_label3.place(x = 15, y = 325)
    drinks_label4 = ctk.CTkLabel(main, width= 75, height = 21, text="Soft Drink", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    drinks_label4.place(x = 65, y = 325)

    drinks_img3 = ctk.CTkImage(Image.open("lipton.png"), size = (125, 100))
    drinks_label_t3 = ctk.CTkLabel(main, image = drinks_img3, text="", height = 80, width = 125)
    drinks_label_t3.place(x = 160, y = 70)
    drinks_label5 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    drinks_label5.place(x = 160, y = 175)
    drinks_label6 = ctk.CTkLabel(main, width= 75, height = 21, text="Lipton", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    drinks_label6.place(x = 210, y = 175)

    drinks_img4 = ctk.CTkImage(Image.open("coffee.png"), size = (125, 100))
    drinks_label_t4 = ctk.CTkLabel(main, image = drinks_img4, text="", height = 80, width = 125)
    drinks_label_t4.place(x = 160, y = 215)
    drinks_label7 = ctk.CTkLabel(main, width= 40, height = 20, text="$4.50", text_color = "#ffffff", fg_color="#2a8711", corner_radius=5)
    drinks_label7.place(x = 160, y = 325)
    drinks_label8 = ctk.CTkLabel(main, width= 75, height = 21, text="Coffee", text_color = "#ffffff", fg_color="#191819", corner_radius=5)
    drinks_label8.place(x = 210, y = 325)

    veganlabel_img = ctk.CTkImage(Image.open("vegan.png"), size = (35, 35))
    veganlabel1 = ctk.CTkLabel(drinks_label_t1, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel1.place(x = 5, y = 5)
    veganlabel2 = ctk.CTkLabel(drinks_label_t2, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel2.place(x = 5, y = 5)
    veganlabel3 = ctk.CTkLabel(drinks_label_t3, width= 35, height= 35, fg_color="#028756", bg_color = "#028756", image = veganlabel_img, text = "")
    veganlabel3.place(x = 5, y = 5)

def order_values(*args):
        
        of_quantity.set("1")
        user_order = of_item.get()
        of_price.configure(text="$%.2f" % menu_price[user_order])
        calculate()

def calculate(*args):

    global user_order, price, quantity, total_price, approve
    approve = False
    user_order = of_item.get()
    if user_order in menu_list:
        user_quantity = ctk.StringVar() 
        user_quantity.set(of_quantity.get())
        quantity = int(user_quantity.get())
        price = float(menu_price[user_order])
        total_price = quantity * price
        of_fprice.configure(text="$%.2f" % total_price)
        approve = True
    else:
        CTkMessagebox(title="Warning!", message="Please select a menu item before changing quantity.",
                                    icon="warning.png", option_1="Ok")
        of_quantity.set("1")

def check():
    global vegan
    vegan = not vegan

def add_verify():
    if user_order in menu_list:
        if vegan == True:
            if user_order in vegan_list:
                add()
            else:
                msg = CTkMessagebox(title="Warning!", message="You've indicated that you are vegan/vegetarian, the selected menu items have no suitable substitutes. Are you sure you want to add this to your cart?",
                                        icon="warning.png", option_1="No", option_2 = "Yes")
                msg = msg.get()
                if msg == "Yes":
                    add()
                else:
                    return
        else:
            add()
    else:
        CTkMessagebox(title="Warning!", message="Please select a menu item before adding to cart.",
                                    icon="warning.png", option_1="Ok")

def add():
    global of_pitem, trolley, indicator, trolley_list, number, record_date
    calculate()
    date = datetime.datetime.now()
    record_date = date.strftime("%d/%m/%Y : %I:%M%p")
    number = random.randint(100, 999)
    trolley = {'MenuItem': str(user_order), 'Price': str(price), 'Quantity': str(quantity), 'Total Price': str(total_price), 'Date': str(record_date), 'Key': number}
    trolley_list.append(trolley)
    indicator += 1
    menu_items = [f"{item['MenuItem']} : QTY {item['Quantity']} : ${item['Price']} : #{item['Key']}" for item in trolley_list]
    of_pitem.configure(values=menu_items)
    msg = CTkMessagebox(title="Confirmed!", message="Your order has been added to cart.",
                                                    icon="success.png", option_1="Ok")

def remove():
    global remove_item
    remove_item = True
    purchase()

def purchase():
    global of_pitem, trolley, trolley_list, indicator, receipt_history, remove_item
    if indicator >= 0:
        try:
            selected_item = int(of_pitem.get().split('#')[-1])
            selected_dict1 = next(item for item in trolley_list if item['Key'] == selected_item)
            selected_dict2 = int(float(selected_dict1['Key']))
            for trolley in trolley_list:
                if remove_item == False:
                        if selected_dict2 in trolley.values():
                            msg = CTkMessagebox(title="Warning!", message="Are you sure you want to purchase this order?",
                                                            icon="warning.png", option_1="No", option_2 = "Yes")
                            msg = msg.get()
                            if msg == "Yes":
                                indicator -= 1
                                of_fpprice.configure(text="$0.00")
                                selected1 = of_pitem.get()
                                selected2 = None
                                receipt_history.append(selected_dict1)
                                for item in trolley_list:
                                    if item['Key'] == int(selected1.split('#')[-1]):
                                        selected2 = item
                                        break
                                if selected2:
                                    trolley_list.remove(selected2)
                                    menu_items = [f"{item['MenuItem']} : QTY {item['Quantity']} : ${item['Price']} : #{item['Key']}" for item in trolley_list]
                                    of_pitem.configure(values=menu_items)
                                    of_pitem.set("Select Ticket Here")
                                    msg = CTkMessagebox(title="Confirmed!", message="Your order has been successfully purchased.",
                                                        icon="success.png", option_1="Ok")
                            else:
                                msg = CTkMessagebox(title="Important!", message="Cancelled Purchase.",
                                                            icon="failure.png", option_1="Ok")
                else:
                    if selected_dict2 in trolley.values():
                        selected1 = of_pitem.get()
                        selected2 = None
                        for item in trolley_list:
                            if item['Key'] == int(selected1.split('#')[-1]):
                                selected2 = item
                                break
                        if selected2:
                            trolley_list.remove(selected2)
                            menu_items = [f"{item['MenuItem']} : QTY {item['Quantity']} : ${item['Price']} : #{item['Key']}" for item in trolley_list]
                            msg = CTkMessagebox(title="Confirmed!", message="Your order has been removed from your cart.",
                                                    icon="success.png", option_1="Ok")
                            of_pitem.configure(values=menu_items)
                            of_pitem.set("Select Ticket Here")
                            remove_item = False
                
        
        except ValueError:
            msg = CTkMessagebox(title="Error!", message="Please select a ticket first.",
                                                    icon="warning.png", option_1="Ok")
    else:
        print("Invalid indicator value")

def update(*args):
    global selected_it2
    selected_it = int(of_pitem.get().split('#')[-1])
    selected_it2 = next(item for item in trolley_list if item['Key'] == selected_it)
    abba = int(float(selected_it2['Total Price']) * 100) / 100
    of_fpprice.configure(text="$%.2f" % abba)

def order_frame():

    global of_title, of_item, of_price, of_quantity, of_fprice, of_add, of_pitem, of_fpprice,of_buy, of_rid, of_check, of_title2

    hide()

    of_title = ctk.CTkLabel(main, text = "Checkout", font = ("bold", 35), text_color = "#ffffff")
    of_title.place(x = 80, y = 20)
    of_item = ctk.CTkComboBox(main, width = 180, height = 30, command = order_values, state = "readonly", border_color = "#191819", button_color = "#191819", values=menu_list)
    of_item.set("Select Item Here")
    of_item.place(x=30, y=90)
    of_price = ctk.CTkLabel(main, width = 50, height = 30, fg_color="#2a8711", text = "$0.00", text_color="#ffffff", corner_radius=10)
    of_price.place(x=220, y=90)
    of_quantity = ctk.CTkComboBox(main, width = 55, height = 30, command = calculate, border_color = "#191819", button_color = "#191819", variable = user_quantity, values = [str(i) for i in range(1, 11)])
    of_quantity.place(x=30, y=130)
    of_quantity.set("1")
    of_fprice = ctk.CTkLabel(main, width = 50, height = 30, fg_color="#2a8711", text = "$0.00", text_color="#ffffff", corner_radius=10)
    of_fprice.place(x=93, y=130)
    of_add = ctk.CTkButton(main, text = "Add to Checkout", command = add_verify, width = 50, height = 30)
    of_add.place(x=160, y=130)
    of_check = ctk.CTkCheckBox(main, text = "I am vegeterian/vegan", command = check, checkbox_height= 18, checkbox_width=18, text_color="#ffffff", border_color="#ffffff")
    of_check.place(x = 30, y = 165)

    of_title2 = ctk.CTkLabel(main, text = "Payment", font = ("bold", 35), text_color = "#ffffff")
    of_title2.place(x = 80, y = 200)
    of_pitem = ctk.CTkComboBox(main, width = 245, height = 30, command = update, state = "readonly", border_color = "#191819", button_color = "#191819", values = [f"{item['MenuItem']} : QTY {item['Quantity']} : ${item['Price']}" for item in trolley_list])
    of_pitem.place(x=30, y=260)
    of_pitem.set("Select Item Here")

    of_fpprice = ctk.CTkLabel(main, width = 100, height = 30, fg_color="#2a8711", text = "$0.00", text_color="#ffffff", corner_radius=10)
    of_fpprice.place(x=30, y=310)
    of_buy = ctk.CTkButton(main, text = "Purchase", command = purchase, width = 50, height = 30)
    of_buy.place(x=208, y=310)
    of_rid = ctk.CTkButton(main, text = "Remove", command = remove, width = 50, height = 30)
    of_rid.place(x=138, y=310)

def history_frame():

    global hf_title, hf_receipt, hf_food_item, hf_food_quantity, hf_food_tp, hf_food_price, hf_date

    hide()

    hf_title = ctk.CTkLabel(main, text = "Transaction\nHistory", font = ("bold", 35), text_color = "#ffffff")
    hf_title.place(x = 60, y = 20)
    hf_receipt = ctk.CTkComboBox(main, width = 235, height = 30, state = "readonly", command = historical, border_color = "#191819", button_color = "#191819", values = [f"#{item['Key']}" for item in receipt_history])
    hf_receipt.place(x=30, y=120)
    hf_receipt.set("Select Item Here")
    hf_food_item = ctk.CTkLabel(main, width = 150, height = 30, fg_color = "#191819", text = "", text_color = "#ffffff", corner_radius = 10)
    hf_food_item.place(x=70, y=200)
    hf_food_quantity = ctk.CTkLabel(main, width = 100, height = 30, fg_color = "#191819", text = "QTY : 0", text_color = "#ffffff", corner_radius = 10)
    hf_food_quantity.place(x=30, y=250)
    hf_food_tp = ctk.CTkLabel(main, width = 100, height = 30, fg_color="#2a8711", text = "TP : $0.00", text_color="#ffffff", corner_radius=10)
    hf_food_tp.place(x=30, y=300)
    hf_food_price = ctk.CTkLabel(main, width = 130, height = 30, fg_color="#2a8711", text = "$0.00", text_color="#ffffff", corner_radius=10)
    hf_food_price.place(x=140, y=250)
    hf_date = ctk.CTkLabel(main, width = 130, height = 30, fg_color = "#191819", text = "0/0/0 0:00", text_color = "#ffffff", corner_radius = 10)
    hf_date.place(x=140, y=300)

item = ""

def historical(*args):
    global selected_ticket, hf_food_item
    _log(f" args {args}")

    selected_ticket = hf_receipt.get()
    _log(f"Selected Item, {selected_ticket}")
    _log(f" Receipt History {receipt_history}")

    item = None
    for item in receipt_history:
        _log(f"iter {item}")
        if item["Key"] == int(selected_ticket.replace("#","")):
            _log("Item Found")
            item = item
            break
    if item:
        hf1 = item['MenuItem']
        _log(f" This Item {item}")
        _log(f"  This  {hf1}")
        hf_food_item.configure(text=f"{hf1}")
        hf2 = item['Price']
        hf_food_price.configure(text=f"${hf2}0")
        hf3 = item['Quantity']
        hf_food_quantity.configure(text=f"QTY: {hf3}")
        hf4 = item['Total Price']
        hf_food_tp.configure(text=f"TC: ${hf4}0")
        hf5 = item['Date']
        hf_date.configure(text=hf5)

    selected_ticket = ""    
    item = None


def hide():
    mf_title.place_forget()
    mf_button1.place_forget()
    mf_button2.place_forget()
    mf_button3.place_forget()
    mf_button4.place_forget()
    mf_title1.place_forget()
    mf_title2.place_forget()

    goback_arrow.place_forget()
    hotfood_label_t1.place_forget()
    hotfood_label_t2.place_forget()
    hotfood_label_t3.place_forget()
    hotfood_label_t4.place_forget()
    hotfood_title.place_forget()
    hotfood_label1.place_forget()
    hotfood_label2.place_forget()
    hotfood_label3.place_forget()
    hotfood_label4.place_forget()
    hotfood_label5.place_forget()
    hotfood_label6.place_forget()
    hotfood_label7.place_forget()
    hotfood_label8.place_forget()

    coldfood_label_t1.place_forget()
    coldfood_label_t2.place_forget()
    coldfood_label_t3.place_forget()
    coldfood_label_t4.place_forget()
    coldfood_title.place_forget()
    coldfood_label1.place_forget()
    coldfood_label2.place_forget()
    coldfood_label3.place_forget()
    coldfood_label4.place_forget()
    coldfood_label5.place_forget()
    coldfood_label6.place_forget()
    coldfood_label7.place_forget()
    coldfood_label8.place_forget()

    desserts_label_t1.place_forget()
    desserts_label_t2.place_forget()
    desserts_label_t3.place_forget()
    desserts_label_t4.place_forget()
    desserts_title.place_forget()
    desserts_label1.place_forget()
    desserts_label2.place_forget()
    desserts_label3.place_forget()
    desserts_label4.place_forget()
    desserts_label5.place_forget()
    desserts_label6.place_forget()
    desserts_label7.place_forget()
    desserts_label8.place_forget()

    drinks_label_t1.place_forget()
    drinks_label_t2.place_forget()
    drinks_label_t3.place_forget()
    drinks_label_t4.place_forget()
    drinks_title.place_forget()
    drinks_label1.place_forget()
    drinks_label2.place_forget()
    drinks_label3.place_forget()
    drinks_label4.place_forget()
    drinks_label5.place_forget()
    drinks_label6.place_forget()
    drinks_label7.place_forget()
    drinks_label8.place_forget()

    of_title.place_forget()
    of_item.place_forget()
    of_price.place_forget()
    of_add.place_forget()
    of_quantity.place_forget()
    of_fprice.place_forget()
    of_add.place_forget()
    of_title2.place_forget()
    of_pitem.place_forget()
    of_fpprice.place_forget()
    of_fpprice.place_forget()
    of_buy.place_forget()
    of_check.place_forget()
    of_rid.place_forget()

    hf_title.place_forget()
    hf_receipt.place_forget()
    hf_food_item.place_forget()
    hf_food_quantity.place_forget()
    hf_food_tp.place_forget()
    hf_food_price.place_forget()
    hf_date.place_forget()

#-------------------------------------------------- starting program ---------------------------------------------------------------#

# These functions are placed here to begin immediantly upon opening program
if __name__ == "__main__":
    server_up = init_server()
    if(server_up):
        # imported()
        page1()
        window.mainloop()