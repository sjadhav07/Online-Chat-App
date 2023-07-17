import time
from client import Client
from threading import Thread

c1 = Client("Sudarshan")
c2 = Client("Rohit")


def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # updates every 1/10 of a second
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # displaying new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

c1.send_message("hi")
time.sleep(2)
c2.send_message("hello")
time.sleep(2)
c1.send_message("How are you?")
time.sleep(2)
c2.send_message("I am fine")
time.sleep(2)

c1.disconnect()
time.sleep(2)
c2.disconnect()