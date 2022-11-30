import socket

server_host = '10.0.0.1'
server_port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', server_port))
    s.listen(2)  # listen to two hosts at a time, renderer and controller
    conn, addr = s.accept()
    with conn:
        print("Connected to addr={0} \n Listening on port x={1}".format(
            addr, server_port))
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
