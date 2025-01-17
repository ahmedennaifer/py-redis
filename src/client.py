import socket
import logging
from parse import parse_command
from serialize import RESP

logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)


class Client:
    def __init__(self) -> None:
        self._HOST = "127.0.0.1"
        self._PORT = 65432
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self._HOST, self._PORT))
        logger.info("Initiated client")

    def get_payload_buffer_size(self, payload: str) -> int:
        return len(payload.encode("utf-8"))

    def send_payload(self, payload: str) -> None:
        self.socket.sendall(payload.encode("utf-8"))
        data = self.socket.recv(self.get_payload_buffer_size(payload))
        logger.info(f"Sent {data}")
        return data

if __name__ == "__main__":
    c = Client()
    while True:
        print("Sending data...")
        payload = input("")
        if payload != "":
            instr = parse_command(payload)
            resp = RESP(instr)
            s_instr = resp.serialize_to_resp()
            data = c.send_payload(s_instr)
            print(data.decode('utf-8'))
        else:
            print("Payload cannot be empty\n")
