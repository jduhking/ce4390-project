import socket

server_host = '127.0.0.1'  # IP of the server
server_port = 3333  # server port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_host, server_port))
    s.sendall(b'Hello!, world')
    data = s.recv(256)

print('Received', repr(data))
