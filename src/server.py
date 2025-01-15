import socket

HOST = "127.0.0.1"
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print("Server listening...")
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                print(f"Received {data.decode('utf-8')}")
