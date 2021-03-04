import socket
import threading

server_host = "127.0.0.1" # localhost
port = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_host, port))
server.listen()

clients = []
usernames = []
channel_members = [[], []] # Lounge = 0, Homework = 1


def broadcast(message):
    for client in clients:
        print(client)
        client.send(message)


def join(index, client):  # adds user to channel
    for i in channel_members[index]:  # Looks for the member from channels
        if i == client:  # error handling
            client.send("Already in the channel.".encode("utf-8"))
            return
    channel_members[index].append(client)  # adds member to list and channel
    client.send("Channel joined.".encode("utf-8"))


def leave(index, client):  # removes user from channel
    for i in channel_members[index]:  # Looks for the member from channels
        if i == client:  # finds member and removes from list
            channel_members[index].remove(client)
            client.send("Channel left.".encode("utf-8"))
            return
    client.send("Join the channel first".encode("utf-8"))  # error handling


def group(index, session, client, channel_name, msg):  # sends message to group
    for i in channel_members[index]:  # Looks for the member from channels
        if i == session:
            try:
                for session in channel_members[index]:  # sends message to every connection in channel
                    group_msg = ("@" + channel_name + " [" + client + "]: " + msg).encode("utf-8")
                    session.send(group_msg)
                return
            except:
                print("Error sending group message")
    session.send('Join the channel first.'.encode("utf-8"))  # error handling


def private(sender, to, msg):  # for sending private messages
    i = 0
    for client in clients:  # searches for recipiant in list
        if (to == usernames[i]):
            try:  # sending a private message
                private_msg = ("@" + to + " [" + sender + "]: " + msg).encode("utf-8")
                clients[i].send(private_msg)
                return
            except:
                print("Error sending private message")
                return
        else:
            i += 1


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            msg = message.decode("utf-8")
            msg_username = msg.split(' ')[0].strip()
            msg_command = msg.split(' ')[1].strip()
            username_len = len(msg_username)
            command_len = len(msg_command)
            print(msg_command)
            if (msg_command.startswith("!join")):
                msg_location = msg.split(' ')[2].strip()
                print(msg_location)
                if(msg_location == "Lounge"):
                    channel_index = 0
                    join(channel_index, client)
                elif(msg_location == "Homework"):
                    channel_index = 1
                    join(channel_index, client)
                else:
                    client.send("Invalid channel".encode("utf-8"))
            elif (msg_command.startswith('!leave')):
                msg_location = msg.split(' ')[2].strip()
                if(msg_location == "Lounge"):
                    channel_index = 0
                    leave(channel_index, client)
                elif (msg_location == "Homework"):
                    channel_index = 1
                    leave(channel_index, client)
                else:
                    client.send("Invalid channel".encode("utf-8"))
            elif (msg_command.startswith('!group')):
                print(message)
                msg_location = msg.split(' ')[2].strip()
                location_len = len(msg_location)
                msg_content = msg[username_len + command_len + location_len + 3:]
                if (msg_location == "Lounge"):
                    channel_index = 0
                    group(channel_index, client, msg_username[:-1], msg_location, msg_content)
                elif (msg_location == "Homework"):
                    channel_index = 1
                    group(channel_index, client, msg_username[:-1], msg_location, msg_content)
                else:
                    client.send("Invalid channel".encode("utf-8"))
            elif (msg_command.startswith('!private')):
                print("private")
                msg_location = msg.split(' ')[2].strip()
                location_len = len(msg_location)
                msg_content = msg[username_len + command_len + location_len + 3:]
                private(msg_username[:-1], msg_location, msg_content)
            else:
                print("viesti lähtee")
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            username = usernames[index]
            broadcast(f'{username} left the chat'.encode("utf-8"))
            usernames.remove(username)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Connection with {str(address)}')

        client.send('USERNAME'.encode("utf-8"))
        username = client.recv(1024).decode("utf-8")
        usernames.append(username)
        clients.append(client)

        print(f'Username of the client is {username}!')
        broadcast(f'{username} joined the chat!'.encode("utf-8"))
        client.send("Conneced to the server!".encode("utf-8"))
        client.send("Welcome to the Chat. !commands for instructions".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server online and listening")
receive()

