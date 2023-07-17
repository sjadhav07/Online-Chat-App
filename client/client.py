from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

class Client:
    """
    communicates with server
    """
    # Global constants
    HOST = 'localhost'
    PORT = 5500
    MAX_CONNECTIONS = 10
    ADDR = (HOST, PORT)
    BUFFSIZ = 512   

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = [] # keeping track of messages

        # creating new thread and running it concurrently in background
        reveive_thread = Thread(target=self.receive_messages)
        reveive_thread.start()

        self.send_message(name)

        self.lock = Lock()

    def receive_messages(self):
        """
        receive messages from server
        return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFSIZ).decode()

                # making memory safe to access
                self.lock.acquire()
                self.messages.append(msg) # NOTE: need a lock on this memory so I don't look at it twice
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_message(self, msg):
        """
        send message to server
        :param msg: str
        :return:
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            print("message is quit")
            self.client_socket.close()

    def get_messages(self):
        """
        :returns a list of str messages
        :return list[str]
        """
        messages_copy = self.messages[:]

        # making memory safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy
    
    def disconnect(self):
        self.send_message("{quit}")