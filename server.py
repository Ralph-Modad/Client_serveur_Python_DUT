import socket
import threading
import time

HEADER = 64
PORT = 5000

#partie socket création

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#gerer les clients

def handle_client(conn, addr):
    print(f"[NEW CONNECTION FROM] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg ==" DISCONNECT_MESSAGE":#message du client = disconnect ca renvoie
                connected = False
            print(f"[{addr}] ")
            conn.send("Msg received".encode(FORMAT))  #message envoyé au client comme quoi le serv a recu les données
            dash = open("dashboard.html", "a") # ouverture fichier html qui contient les données
            dash.write(msg) #écriture a l'intérieur du fichier
            dash.close() #fermeture du fichier
    conn.close()

web = open("web.html", "r")
webcontent = web.readlines()
web.close()
newweb= open("dashboard.html", "w")

for jesuisfort in webcontent:
    newweb.write(jesuisfort)  # copie les données de web.html dans dashboard.html
newweb.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() #multi client grace au thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[THER IS {threading.activeCount() - 1} ACTIVE CONNECTIONS] ")


print("[STARTING] server is starting...")
start()
print(SERVER)
print(handle_client())




