import socket

server_host = '127.0.0.1'
server_port = 3333

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((server_host, server_port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if data:
                print("Data received is:", repr(data))
                # convert the bytes data object to string (utf-8)
                data = data.decode("utf-8")
                data = data.upper()  # upper case the data
                print("Uppercasing the data gives: " + data)
                data = data.encode()
            if not data:
                break
            conn.sendall(data)
