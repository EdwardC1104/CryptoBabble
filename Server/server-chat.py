from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


password = "peanutbutter".encode() # CHANGE THIS - INPUT!!!!
salt = b'\x15\x95\xd1{/\xec\x99\xac\x90\x99>\xa5\nw\xfb\xe3'
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))


def encryptMessage(msg):
    message = Fernet(key).encrypt(msg.encode())
    return message

def decryptMessage(msg):
    message = Fernet(key).decrypt(msg)
    return message.decode()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        #client.send(encryptMessage("Welcome! Now type your name and press enter!"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ)
    name = decryptMessage(name)
    global names
    names.append(name)
    welcome = 'Hello ' + name + '!' + "@#%" + ', '.join(names)
    client.send(encryptMessage(welcome))
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        msg = decryptMessage(msg)
        if msg != "%quit%":
            broadcast(msg, name+": ")
        else:
            client.close()
            del clients[client]
            names.remove(name)
            broadcast("%s has left the chat." % name)
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        tosend = prefix + msg + "@#%" + ', '.join(names)
        sock.send(encryptMessage(tosend))

        
clients = {}
addresses = {}
names = []

HOST = ''
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
