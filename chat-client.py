import socket
import ssl
from tkinter import *
from functools import partial
import random
import hashlib

def register_user(username, password):
    client_username = username.get()
    client_password = password.get()
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 2048

    MESSAGE = 'register_user,' + client_username + "," + client_password
    MESSAGE = MESSAGE.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    s.connect((TCP_IP, TCP_PORT))
    s.sendall(MESSAGE)

    data = s.recv(BUFFER_SIZE)
    response_string = data.decode()
    s.close()
    print("Received data:", response_string)
    if response_string == "Registration Successful":
        print("YES")
        usernameLabel.destroy()
        usernameEntry.destroy()
        passwordLabel.destroy()
        passwordEntry.destroy()
        registerButton.destroy()
        loginButton.destroy()
        get_users(client_username)


def login(username, password):
    client_username = username.get()
    client_password = password.get()
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 2048

    MESSAGE = 'login,' + client_username + "," + client_password
    MESSAGE = MESSAGE.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    s.connect((TCP_IP, TCP_PORT))
    s.sendall(MESSAGE)

    data = s.recv(BUFFER_SIZE)
    response_string = data.decode()
    s.close()
    print("Received data:", response_string)
    if response_string == "Access Granted":
        print("YES")
        usernameLabel.destroy()
        usernameEntry.destroy()
        passwordLabel.destroy()
        passwordEntry.destroy()
        registerButton.destroy()
        loginButton.destroy()
        get_users(client_username)

def send_server(plaintext, sender, receiver):
    print("MESSAGE: " + plaintext)
    ptxt = plaintext
    print("SENDER: " + sender)
    print("RECEIVER: " + receiver)

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5010
    BUFFER_SIZE = 1000000
    messag = plaintext.encode()
    ctxt = hashlib.sha256(messag).hexdigest()
    print(ctxt)
    MESSAGE = 'send_message_server,' + sender + ',' + ctxt + ',' + receiver + ',' + ptxt
    MESSAGE = MESSAGE.encode()
    s5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s5.settimeout(10)

    s5.connect((TCP_IP, TCP_PORT))
    s5.send(MESSAGE)

    data = s5.recv(BUFFER_SIZE)
    response_string = data.decode()
    s5.close()
    print("Received data:", response_string)

def key_handshake(plaintext, sender, receiver):
    print("MESSAGE: " + plaintext)
    print("SENDER: " + sender)
    print("RECEIVER: " + receiver)
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5009
    BUFFER_SIZE = 2048

    g = 9
    p = 1001
    a = random.randint(5, 10)
    b = random.randint(10, 20)

    B = (g ** b) % p
    keyA = (B ** a) % p

    g2 = str(g)
    p2 = str(p)
    a2 = str(a)
    b2 = str(b)

    public_key = hashlib.sha256(str(keyA).encode()).hexdigest()
    print("Key: "+public_key)

    MESSAGE = g2 + ',' + p2 + ',' + a2 + ',' + b2
    MESSAGE = MESSAGE.encode()
    s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s4.settimeout(10)

    s4.connect((TCP_IP, TCP_PORT))
    s4.send(MESSAGE)

    data = s4.recv(BUFFER_SIZE)
    response_string = data.decode()
    s4.close()
    print("Received data:", response_string)

    if response_string == public_key:
        print("Key Exchange Successful")
        send_server(plaintext, sender, receiver)


def message_board(message_string, sender, receiver):
    ms = str(message_string)
    ms = ms.split('/n')
    snd = str(sender)
    rvr = str(receiver.get())
    mb = Label(window, text=rvr, width=0, font="Arial 14 bold", fg='#FF6B6B')
    mb.pack(side=TOP)

    pmsg = StringVar()

    def send_message(plaintext, sender, receiver):
        pt = str(plaintext.get())
        rer = str(receiver.get())
        print("MESSAGE: "+pt)
        print("SENDER: "+sender)
        print("RECEIVER: "+rer)
        if snd == sender and rvr == rer:
            mmm = Label(window, text=pt, borderwidth=2, relief="groove")
            mmm.pack(side=TOP, anchor=NE)
        elif snd == rrr and rvr == sender:
            mmm = Label(window, text=pt, borderwidth=2, relief="groove")
            mmm.pack(side=TOP, anchor=NW)
        pmsgEntry.delete(0, 'end')
        key_handshake(pt,sender,rer)

    send_message = partial(send_message, pmsg, sender, receiver)

    registerButton = Button(window, text="SEND->", command=send_message)
    registerButton.pack(side=BOTTOM)

    pmsgEntry = Entry(window, textvariable=pmsg)
    pmsgEntry.pack(side=BOTTOM)

    for object in ms:
        objecter = object.split(',')
        if len(objecter) == 4:
            print(objecter)
        else:
            continue
        curr = objecter[0]
        sms = objecter[1]
        rrr = objecter[2]
        if snd == curr and rvr == rrr:
            mmm = Label(window, text=sms, borderwidth=2, relief="groove")
            mmm.pack(side=TOP, anchor=NE)
        elif snd == rrr and rvr == curr:
            mmm = Label(window, text=sms, borderwidth=2, relief="groove")
            mmm.pack(side=TOP, anchor=NW)

def get_users(username):
    current_user = str(username)
    print(current_user)

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5006
    BUFFER_SIZE = 2048

    MESSAGE = 'get_users,'+current_user
    MESSAGE = MESSAGE.encode()
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.settimeout(10)

    s2.connect((TCP_IP, TCP_PORT))
    s2.send(MESSAGE)

    data = s2.recv(BUFFER_SIZE)
    response_string = data.decode()
    s2.close()
    print("Received data:", response_string)
    users_list = response_string.split(',')
    users_list.pop()
    print(users_list)
    friends = Label(window, text="Friends")
    friends.pack(side=TOP)
    labell_0 = Label(window, text="_______________________________________", width=0, fg="#FF6B6B", font=("bold", 9))
    labell_0.pack(side=TOP)
    list_users = ''
    for user in users_list:
        list_users = list_users + user + ' | '
    messageUser = Label(window, text=list_users)
    messageUser.pack(side=TOP)

    who = Label(window, text="Enter the user you wish to message!")
    who.pack(side=TOP)

    who_dat = StringVar()
    who_name = Entry(window, textvariable=who_dat)
    who_name.pack(side=TOP)

    def get_messages(sender, receiver):
        se = str(sender)
        rr = receiver.get()
        print(se)
        print(str(rr))

        TCP_IP = '127.0.0.1'
        TCP_PORT = 5008
        BUFFER_SIZE = 2048

        MESSAGE = 'get_messages,' + se + ',' + rr
        MESSAGE = MESSAGE.encode()
        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s3.settimeout(10)

        s3.connect((TCP_IP, TCP_PORT))
        s3.send(MESSAGE)

        dataa = s3.recv(BUFFER_SIZE)
        response_stringg = dataa.decode()
        s3.close()
        print("Received data:", response_stringg)
        labell_0.destroy()
        friends.destroy()
        messageUser.destroy()
        messageUser.destroy()
        who.destroy()
        who_name.destroy()
        messenger.destroy()
        message_board(response_stringg, sender, receiver)

    get_messages = partial(get_messages, current_user, who_dat)

    messenger = Button(window, text="MSG", command=get_messages)
    messenger.pack(side=TOP)


window = Tk()

window.title("Secure End-to-End Chat App")

window.geometry('300x500')

headerLabel = Label(window, text="ChatApp", font="Arial 18 bold", fg='#FF6B6B')
headerLabel.pack(side=TOP)

label_0 = Label(window, text="_______________________________________", width=0, fg="#FF6B6B", font=("bold", 9))
label_0.pack(side=TOP)

usernameLabel = Label(window, text="Username")
usernameLabel.pack(side=TOP)

username = StringVar()
usernameEntry = Entry(window, textvariable=username)
usernameEntry.pack(side=TOP)

passwordLabel = Label(window,text="Password")
passwordLabel.pack(side=TOP)

password = StringVar()
passwordEntry = Entry(window, textvariable=password, show='*')
passwordEntry.pack(side=TOP)

register_user = partial(register_user, username, password)

registerButton = Button(window, text="Register", command=register_user)
registerButton.pack(side=TOP)

login = partial(login, username, password)

loginButton = Button(window, text="Login", command=login)
loginButton.pack(side=TOP)


window.mainloop()
