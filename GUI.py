'''
-- CA A Basic Blogging App
-- Name: Giovanni Fonzo
-- Student ID: D19124775
-- Module: Programming and Algorithms 2 CMPU1017: 2020-21
-- Year: 2020/2021 
-- Course: DT249 - Stage 2
-- D19124775_GiovanniFonzo_BasicBloggingApp
'''

#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from functools import partial
from tkinter import *
import requests
import random
import datetime


run = True

txt = None




def receive():
    """Handles receiving of messages."""
    global run
    while True and run:
        res = requests.get('http://127.0.0.1:5000/get_blog?id=' + id)
        if res.status_code == 200:
            msg_list.insert(tkinter.END, res.content)
        '''
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break'''


def send(my_msg, msg_list, event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    data = {"text": msg}
    res = requests.get('http://127.0.0.1:5000/post_blog?data=' + msg)
    msg_list.insert(tkinter.END, msg)
    msg_list.insert(tkinter.END, " ")
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def validateLogin(loginUsername, loginPassword, tkWindow):
	global id
	print("username entered: " + loginUsername.get())
	print("password entered: " + loginPassword.get())
	x = requests.get('http://127.0.0.1:5000/login?uname=' + loginUsername.get() + '&pass=' + loginPassword.get())
	print(x.content)
	if x.content == b'Correct':
		tkWindow.destroy()
		id = loginUsername.get()
		showMain()
	else:
		print("Wrong creds")
		tkWindow.destroy()
	return

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

def register_(f, l, p, tk, is_admin = "false"):
    email = f.get() + "." + l.get() + "@gmail.com"
    token = random.randint(11111, 99999)
    x = datetime.datetime.now()
    created = str(x.year) + "-" + str(x.month) + "-" + str(x.day)
    modified = created
    data = "?fname=" + f.get() + "&lname=" + l.get() + "&email=" + email + "&token=" + str(token) + "&pass=" + p.get() + "&is_admin=" + is_admin + "&created=" + created + "&modified=" + modified 
    x = requests.get('http://127.0.0.1:5000/register' + data)



def register(prevWin = None):
    if prevWin:
        prevWin.destroy()

    #global loginUsername
    #global loginPassword

    tkWindow = tkinter.Tk()  
    tkWindow.geometry('400x150')  
    tkWindow.title('Register')

    firstName = StringVar()
    lastName = StringVar()
    password = StringVar()

    fNameLabel = Label(tkWindow, text="First name").grid(row=0, column=0)
    fNameEntry = Entry(tkWindow, textvariable=firstName).grid(row=0, column=1)  

    lNameLabel = Label(tkWindow,text="Last name").grid(row=1, column=0)  
    lNameEntry = Entry(tkWindow, textvariable=lastName).grid(row=1, column=1)  

    passwordLabel = Label(tkWindow,text="Password").grid(row=2, column=0)  
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=2, column=1)  

    cmd = partial(register_, firstName, lastName, password, tkWindow)

    #login button
    regButton = Button(tkWindow, text="Register", command=cmd).grid(row=4, column=0)  

    lg = partial(login, tkWindow)
    regButton = Button(tkWindow, text="Login instead", command=lg).grid(row=7, column=0)  

    tkWindow.mainloop()


def login(prevWin = None):
    if prevWin:
        prevWin.destroy()

    global loginUsername
    global loginPassword

    tkWindow = tkinter.Tk()  
    tkWindow.geometry('400x150')  
    tkWindow.title('Login')

    loginUsername = StringVar()
    loginPassword = StringVar()
    #username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    #username = StringVar()
    usernameEntry = Entry(tkWindow, textvariable=loginUsername).grid(row=0, column=1)  

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
    #password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=loginPassword, show='*').grid(row=1, column=1)  

    validate = partial(validateLogin, loginUsername, loginPassword, tkWindow)

    reg = partial(register, tkWindow)

    #login button
    loginButton = Button(tkWindow, text="Login", command=validate).grid(row=4, column=0)  
    regButton = Button(tkWindow, text="Register instead", command=reg).grid(row=5, column=0)  

    tkWindow.mainloop()


def showMain():
    top = tkinter.Tk()
    top.title("Blog")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type here")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    cmd = partial(send, my_msg, msg_list)
    send_button = tkinter.Button(top, text="Post", command= cmd)
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing)

    #----Now comes the sockets part----
    #HOST = input('Enter host: ')
    #PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Starts GUI execution.

if __name__ == "__main__":
    register()
    login()
    while True:
        if login():
            showMain()