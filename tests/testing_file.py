import tkinter as tk

window = tk.Tk()
window.geometry("500x500")

def yes():
    print("yes")
    global no
    def no():
        print("no")

button1 = tk.Button(window, text = "yes", command = yes)
button2 = tk.Button(window, text = "no", command = no)

window.mainloop()
