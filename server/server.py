from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global constants
HOST = 'localhost'
PORT = 5500
MAX_CONNECTIONS = 10
ADDR = (HOST, PORT)
BUFFSIZ = 512


# Global variables
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)   # Set up server


def broadcast(msg, name):
    """
    send new message to all clients
    :param msg: bytes["utf8]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION]",e)


def handle_client(person):
    """
    Tread to handle all message from client
    :param person: Person
    :return: None
    """
    client = person.client
    name = client.recv(BUFFSIZ).decode("utf8") #get person name
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!","utf8")
    broadcast(msg, "") # broadcast welcome message
    
    while True:
        try:
            msg = client.recv(BUFFSIZ)
            # print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"): # disconnect client if message is quit
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")

                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name+": ")
                print(f"{name}:", msg.decode("utf8"))
        except Exception as e:
            print("[EXCEPTION]", e)
            break
            

def wait_for_connection(SERVER):
    """
    wait for connection from new clients, start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """
    while True:
        try:
            client, addr = SERVER.accept() # wait for new connections
            person = Person(addr, client) # new person created for connection
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to server at {time.time()}")
            Thread(target=handle_client, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break
    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # open server for listening to connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()