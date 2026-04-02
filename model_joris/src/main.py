import socket
print("This is Joris model running")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 9999))

client.send("Hello from client".encode())
print(client.recv(1024).decode())
print(client.recv(1024).decode())

# WHILE TRUE LOOP VOOR CONNECTION BEHOUDEN

client.close()