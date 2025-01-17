import socket
from store import KVStore 
from parse import Command, CommandResult

HOST = "127.0.0.1"
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    kv = KVStore()
    while True:
        print("Server listening...")
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data_str = data.decode('utf-8')
                decoded = kv.decode_resp_string(data_str)
                if decoded.command == Command.GET.value:
                    res = kv.get(decoded)
                elif decoded.command == Command.SET.value: 
                    res = kv.insert(decoded)
                elif decoded.command == Command.DEL.value:
                    res = kv.delete(decoded)
                conn.sendall(res.value.encode('utf-8'))
                print(f"Received {data.decode('utf-8')}")
