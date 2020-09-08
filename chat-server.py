import socket
import ssl
import mysql.connector
import hashlib

def send_server():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5010
    BUFFER_SIZE = 2048

    s5 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s5.bind((TCP_IP, TCP_PORT))
    s5.listen(100)

    conneeee, addreeee = s5.accept()
    print('Connection address:', addreeee)

    datareee = conneeee.recv(BUFFER_SIZE)
    newereee_string = datareee.decode()
    arreeee = newereee_string.split(',')
    print("Received data:", arreeee)

    try:
        cnx_sent = mysql.connector.connect(user='root', password='Parjun1514$', host='127.0.0.1', database='sys')
        cursor_sent = cnx_sent.cursor()

        sql_sent = "INSERT INTO messages (sender, message, receiver) VALUES (%s, %s, %s)"
        val_sent = (arreeee[1], arreeee[4], arreeee[3])
        print(val_sent)

        cursor_sent.execute(sql_sent, val_sent)
        cnx_sent.commit()
        print("Success")
        good_sent = "Registration Successful"
        good_sent = good_sent.encode()
        conneeee.sendall(good_sent)
    except mysql.connector.Error as err:
        print('Fail')
        bad_sent = "Registration Fail"
        bad_sent = bad_sent.encode()
        conneeee.sendall(bad_sent)
    cnx_sent.close()
    conneeee.close()


def key_handshake():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5009
    BUFFER_SIZE = 2048

    s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s4.bind((TCP_IP, TCP_PORT))
    s4.listen(100)

    conneee, addreee = s4.accept()
    print('Connection address:', addreee)

    dataree = conneee.recv(BUFFER_SIZE)
    neweree_string = dataree.decode()
    arreee = neweree_string.split(',')
    print("Received data:", arreee)

    g = int(arreee[0])
    p = int(arreee[1])
    a = int(arreee[2])
    b = int(arreee[3])

    A = (g ** a) % p
    keyB = (A ** b) % p

    public_key = hashlib.sha256(str(keyB).encode()).hexdigest()
    print("Key: " + public_key)

    key_response = public_key
    key_response = key_response.encode()
    conneee.sendall(key_response)
    send_server()

    conneee.close()


def send_messages():

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5008
    BUFFER_SIZE = 2048

    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3.bind((TCP_IP, TCP_PORT))
    s3.listen(100)

    connee, addree = s3.accept()
    print('Connection address:', addree)

    datare = connee.recv(BUFFER_SIZE)
    newere_string = datare.decode()
    arree = newere_string.split(',')
    print("Received data:", arree)

    try:
        msg_cnx = mysql.connector.connect(user='root', password='Parjun1514$', host='127.0.0.1', database='sys')

        msg_sql = "SELECT * FROM messages WHERE sender='"+arree[1]+"' AND receiver='"+arree[2]+"'"

        msg_cursor = msg_cnx.cursor()

        msg_cursor.execute(msg_sql)
        msg_records = msg_cursor.fetchall()

        msg_cnx.close()

        msgr_cnx = mysql.connector.connect(user='root', password='Parjun1514$', host='127.0.0.1', database='sys')

        msgr_sql = "SELECT * FROM messages WHERE sender='" + arree[2] + "' AND receiver='" + arree[1] + "'"

        msgr_cursor = msgr_cnx.cursor()

        msgr_cursor.execute(msgr_sql)
        msgr_records = msgr_cursor.fetchall()

        msgr_cnx.close()

        print(msg_records)
        print(msgr_records)

        msg_good = ''
        for msg in msg_records:
            msg = str(msg)
            msg = msg.strip('(')
            msg = msg.strip(')')
            msg = msg.strip("'")
            msg = msg.split(', ')
            message_data = ''
            for item in msg:
                item = item.strip("'")
                message_data = message_data + item + ','
            msg_good = msg_good + message_data + '/n'
        for msg in msgr_records:
            msg = str(msg)
            msg = msg.strip('(')
            msg = msg.strip(')')
            msg = msg.strip("'")
            msg = msg.split(', ')
            message_data = ''
            for item in msg:
                item = item.strip("'")
                message_data = message_data + item + ','
            msg_good = msg_good + message_data + '/n'
        msg_good = msg_good.encode()
        connee.sendall(msg_good)
        key_handshake()
    except mysql.connector.Error as err:
        print('Fail')

    connee.close()


def send_users(username):
    us = str(username)
    print(us)

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5006
    BUFFER_SIZE = 2048

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind((TCP_IP, TCP_PORT))
    s2.listen(100)

    conne, addre = s2.accept()
    print('Connection address:', addre)

    datar = conne.recv(BUFFER_SIZE)
    newer_string = datar.decode()
    arre = newer_string.split(',')
    print("Received data:", arre)

    try:
        users_cnx = mysql.connector.connect(user='root', password='Parjun1514$', host='127.0.0.1', database='sys')

        users_sql = "SELECT username FROM users"

        users_cursor = users_cnx.cursor()

        users_cursor.execute(users_sql)
        users_records = users_cursor.fetchall()

        print(users_records)
        users_good = ''
        for word in users_records:
            word = str(word)
            word = word.strip("('")
            word = word.strip("',)")
            if word == us:
                continue
            else:
                users_good = users_good + word + ','
        users_good = users_good.encode()
        conne.sendall(users_good)
        send_messages()
    except mysql.connector.Error as err:
        print('Fail')
        badest = "Users Fail"
        badest = badest.encode()
        conne.sendall(badest)

    conne.close()


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(100)

conn, addr = s.accept()
print('Connection address:', addr)

while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    new_string = data.decode()
    arr = new_string.split(',')
    print("Received data:", new_string)
    if arr[0] == 'register_user':
        try:
            cnx = mysql.connector.connect(user='root', password='Parjun1514$', host='127.0.0.1', database='sys')
            cursor = cnx.cursor()

            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            val = (arr[1], arr[2])
            print(val)

            cursor.execute(sql, val)
            cnx.commit()
            print("Success")
            good = "Registration Successful"
            good = good.encode()
            conn.sendall(good)
            send_users(arr[1])
            break
        except mysql.connector.Error as err:
            print('Fail')
            bad = "Registration Fail"
            bad = bad.encode()
            conn.sendall(bad)
    elif arr[0] == 'login':
        try:
            cnx = mysql.connector.connect(user='root', password='Parjun1514$', host='127.0.0.1', database='sys')

            sql = "SELECT * FROM users WHERE username='"+arr[1]+"'"

            cursor = cnx.cursor()

            cursor.execute(sql)
            records = cursor.fetchone()
            if records[0] == arr[1] and records[1] == arr[2]:
                print("Success")
                gooder = "Access Granted"
                gooder = gooder.encode()
                conn.sendall(gooder)
                send_users(arr[1])
                break
            else:
                print('Fail')
                bader = "Access Failed"
                bader = bader.encode()
                conn.sendall(bader)
        except mysql.connector.Error as err:
            print('Fail')
            bader = "Access Failed"
            bader = bader.encode()
            conn.sendall(bader)

    cnx.close()

conn.close()

