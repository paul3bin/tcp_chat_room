import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

def broadcast(msg):
    for client in clients:
        client.send(msg)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # accepting the clients
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        
        # prompting the client to enter a nickname and appending the nickname to the list
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # broadcasting the nickname of the client to everyone connected
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server.'.encode('ascii'))

        # creating a thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()