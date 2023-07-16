from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

# Global constants
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
BUFFSIZ = 512

# Global variables
messages = []

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)   # Set up 

def receive_messages():
    """
    receive messages from server
    return: None
    """
    while True:
        try:
            msg = client_socket.recv(BUFFSIZ).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break
# def receive_messages():
#     """
#     receive messages from server
#     return: None
#     """
#     while True:
#         try:
#             msg = client_socket.recv(BUFFSIZ).decode()
#             if msg.startswith("Sudarshan"):
#                 msg = "Sudarshan: " + msg[len("Sudarshan"):].lstrip(":")
#             messages.append(msg)
#             print(msg)
#         except Exception as e:
#             print("[EXCEPTION]", e)
#             break
        
def send_message(msg):
    """
    send message to server
    :param msg: str
    :return:
    """
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()




reveive_thread = Thread(target=receive_messages)
reveive_thread.start()

send_message("Sudarshan")
time.sleep(1)
send_message("hello")