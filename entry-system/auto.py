import time
from sysconfig import get_config_var
import re
from time import *
from tkinter import *
import json
import os



script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "arh.json")




try:
    # function -> open file for Wr.
    def writefile():
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)


    with open(file_path, "r", encoding="utf-8") as file:
        users = json.load(file)


    # function -> checking email spelling (incomplete)
    def correctemail(mail):
        if "@" not in mail:
            return False
        if len(mail) < 5:
            return False
        return True


    # function -> password strength check
    largepass = ["1234", "qwerty"]


    def strongpass(passcode):
        if len(passcode) < 8:
            return False
        if passcode.isdigit():
            return False
        if passcode.isalpha():
            return False
        if passcode.islower():
            return False
        if passcode.isupper():
            return False
        if passcode in largepass:
            return False
        return True


    tries2 = 0
    window = Tk()


    # function -> clearing fields (tk/frame/entry)
    def clear_lp():
        frame.after(3000, lambda: logingui.delete(0, END))
        frame.after(3000, lambda: passinp.delete(0, END))
        frame.after(3000, lambda: email.delete(0, END))


    # function -> If the password is incorrect:
    def noncorrect():

        global tries2
        if tries2 != 3:
            titlewinlog1 = Label(window, text="password wrong, try again", bg="red", font=("Arial", 10))
            titlewinlog1.place(relx=0.1, rely=0.40682)
            window.after(4000, lambda: titlewinlog1.place_forget())
            clear_lp()
            btnonoff()




        elif tries2 == 3:
            titlewinlog1 = Label(window, text="password wrong, wait sometime", bg="red", font=("Arial", 10))
            titlewinlog1.place(relx=0.1, rely=0.40682)
            window.after(4000, lambda: titlewinlog1.place_forget())

            logingui.delete(0, END)
            passinp.delete(0, END)
            email.delete(0, END)

            logingui.config(state="disabled")
            passinp.config(state="disabled")
            email.config(state="disabled")
            frame.after(16000, lambda: passinp.config(state="normal"))
            frame.after(16000, lambda: logingui.config(state="normal"))
            frame.after(16000, lambda: email.config(state="normal"))

            btn1.config(state="disabled")
            btn2.config(state="disabled")
            frame.after(16000, lambda: btn1.config(state="normal"))
            frame.after(16000, lambda: btn2.config(state="normal"))

            tries2 = tries2 - 3
        tries2 += 1


    # disabling and enabling buttons
    def btnonoff():
        btn1.config(state="disabled")
        btn2.config(state="disabled")
        frame.after(4000, lambda: btn1.config(state="normal"))
        frame.after(4000, lambda: btn2.config(state="normal"))


    # Central authorization system
    def autorez():

        login = logingui.get()
        passcode = passinp.get()
        mailM = email.get()
        if login == "" or passcode == "" or mailM == "":
            fg_some = Label(window, text="Fill in all lines!!!", bg="red", font=("Arial", 10))
            fg_some.place(relx=0.1, rely=0.40682)
            window.after(4000, lambda: fg_some.place_forget())


        else:
            if login in users and passcode == users[login]["password"]:
                if mailM == users[login]["mail"]:
                    titlewinlog = Label(window, text="Login successful", bg="white", font=("Arial", 10))
                    titlewinlog.place(relx=0.1, rely=0.40682)
                    info()
                    window.after(4000, lambda: titlewinlog.place_forget())
                    clear_lp()
                    btnonoff()
                    window.after(4500, start)  # Выполнить функцию открытия программы
                elif mailM != users[login]["mail"]:
                    massage_mail = Label(window, text="Wrong email!!!", bg="red", font=("Arial", 10))
                    massage_mail.place(relx=0.1, rely=0.40682)
                    window.after(4000, lambda: massage_mail.place_forget())


            elif login in users and passcode != users[login]["password"]:
                noncorrect()

            elif login not in users:
                titlewinlog2 = Label(window, text="Wrong login and pass,\n try again or register new account",
                                     bg="yellow", font=("Arial", 10))
                titlewinlog2.place(relx=0.1, rely=0.374)
                window.after(4000, lambda: titlewinlog2.place_forget())
                clear_lp()
                btnonoff()
                infoneg()


    # Registration system
    def regist():
        register = logingui.get()
        passcode = passinp.get()
        emailT = email.get()
        if register != "" and passcode != "":
            if register not in users:
                if strongpass(passcode) == True:
                    if correctemail(emailT) == True:
                        emailhave = any(user["mail"] == emailT for user in users.values())
                        if emailhave:
                            winhas = Label(window, text="Email already exists", bg="red", font=("Arial", 10))
                            winhas.place(relx=0.1, rely=0.40682)
                            window.after(4000, lambda: winhas.place_forget())

                        else:
                            users[register] = {"password": passcode, "mail": emailT}
                            writefile()


                            titlewin1 = Label(window, text="New account is registered", bg="white", font=("Arial", 10))
                            titlewin1.place(relx=0.1, rely=0.40682)
                            window.after(4000, lambda: titlewin1.place_forget())
                            btnonoff()


                    elif correctemail(emailT) == False:
                        titlewinmail = Label(window, text="Email is incorrect", bg="red", font=("Arial", 10))
                        titlewinmail.place(relx=0.1, rely=0.40682)
                        window.after(4000, lambda: titlewinmail.place_forget())

                elif strongpass(passcode) == False:
                    titlewin2 = Label(window, text="Password not strong, try again", bg="red", font=("Arial", 10))
                    titlewin2.place(relx=0.1, rely=0.40682)
                    window.after(4000, lambda: titlewin2.place_forget())
                    btnonoff()
            elif register in users:
                titlewin3 = Label(window, text="Account with that name already exists", bg="red", font=("Arial", 10))
                titlewin3.place(relx=0.1, rely=0.40682)
                window.after(4000, lambda: titlewin3.place_forget())
                btnonoff()
        else:
            pass


    # tkinter base ->
    window["bg"] = "black"
    window.title("login in system")
    window.geometry("500x500")
    window.resizable(width=False, height=False)
    window.wm_attributes("-alpha", 0.8)

    frame = Frame(window, bg="white")
    frame.place(relwidth=1, relheight=0.15, relx=0, rely=0.45)

    # Text panels ->
    title = Label(frame, text="Login ->", bg="white", font=("Arial", 10))
    title.place(relx=0.1, rely=0.03)

    title2 = Label(frame, text="Pass ->", bg="white", font=("Arial", 10))
    title2.place(relx=0.1, rely=0.32)

    title3 = Label(frame, text="Email ->", bg="white", font=("Arial", 10))
    title3.place(relx=0.0951, rely=0.61)

    # Input panels ->
    logingui = Entry(frame, bg="white", font=("Arial", 10))
    logingui.place(relx=0.20, rely=0.05)

    passinp = Entry(frame, bg="white", font=("Arial", 10))
    passinp.place(relx=0.20, rely=0.34)

    email = Entry(frame, bg="white", font=("Arial", 10))
    email.place(relx=0.20, rely=0.63)

    # Buttons ->
    btn1 = Button(frame, text="login", bg="green", fg="black", font=("Arial", 10), command=autorez)
    btn1.place(relx=0.50, rely=0.10)

    btn2 = Button(frame, text="register", bg="red", fg="black", font=("Arial", 10), command=regist)
    btn2.place(relx=0.50, rely=0.50)


    # output - ✓ ->
    def info():
        tyeslog = Label(frame, text="✓", fg="green", bg="white", font=("Arial", 8))
        tyeslog.place(relx=0.45, rely=0.04)

        tyespass = Label(frame, text="✓", fg="green", bg="white", font=("Arial", 8))
        tyespass.place(relx=0.45, rely=0.34)

        frame.after(3500, lambda: tyeslog.place_forget())
        frame.after(3500, lambda: tyespass.place_forget())


    # output - x ->
    def infoneg():
        tyeslog1 = Label(frame, text="x", fg="red", bg="white", font=("Arial", 8))
        tyeslog1.place(relx=0.45, rely=0.04)

        tyespass1 = Label(frame, text="x", fg="red", bg="white", font=("Arial", 8))
        tyespass1.place(relx=0.45, rely=0.34)
        frame.after(4000, lambda: tyeslog1.place_forget())
        frame.after(4000, lambda: tyespass1.place_forget())


    # the main function for starting authorization and subsequently the next function (part 1) ->
    set = None


    def start():
        global set
        window.destroy()
        set = True


    window.mainloop()


    # here is your function ->
    def exemple():
        print("Your function")


    # (part 2) ->
    if set == True:
        exemple()






except Exception as e:
    pass
    # import traceback
    #
    # print("One Error:")
    # traceback.print_exc()
    # input("Print Enter for exit...")

