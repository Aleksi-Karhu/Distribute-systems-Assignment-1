import socket
import threading
import sys

IP = str(input("Give an IP address: "))
port = int(input("Give a port: "))
username = input("Choose a username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break


def write():
    while True:
        message = f'{username}: {input("")}'
        if message[len(username) + 2:].startswith("!"):
            if message[len(username) + 2:].startswith("!commands"):
                print("COMMANDS:")
                print("!quit to disconnect")
                print("!channels to see open channels")
                print("!join [channel] to join channel")
                print("!leave [channel] to leave channel")
                print("!group [channel] [message] to message channel")
                print("!private [user] [message] to send private message")
            elif message[len(username) + 2:].startswith("!channels"):
                print("CHANNELS:")
                print("Lounge")
                print("Homework")
            elif message[len(username) + 2:].startswith("!quit"):
                print("Disconnected from server.")
                sys.exit()
            elif message[len(username) + 2:].startswith("!join"):
                client.send(message.encode("utf-8"))
            elif message[len(username) + 2:].startswith("!leave"):
                client.send(message.encode("utf-8"))
            elif message[len(username) + 2:].startswith("!group"):
                client.send(message.encode("utf-8"))
            elif message[len(username) + 2:].startswith("!private"):
                client.send(message.encode("utf-8"))
            else:
                print("Invalid command")
        else:
            client.send(message.encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
