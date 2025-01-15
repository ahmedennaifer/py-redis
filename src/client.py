import socket
import logging


logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)


class client:
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


if __name__ == "__main__":
    c = client()
    while True:
        print("Sending data...")
        payload = input("")
        if payload != "":
            c.send_payload(payload)
        else:
            print("Payload cannot be empty\n")
