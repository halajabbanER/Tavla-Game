import socket
import json
import threading


class NetworkClient:
    def __init__(self, host="127.0.0.1", port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.on_message = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def listen(self):
        while True:
            try:
                data = self.socket.recv(4096).decode()
                if not data:
                    break

                message = json.loads(data)

                if self.on_message:
                    self.on_message(message)

            except Exception as e:
                print("Network error:", e)
                break

    def send(self, message):
        self.socket.send(json.dumps(message).encode())

    def join(self, name):
        self.send({
            "action": "join",
            "name": name
        })

    def roll(self):
        self.send({
            "action": "roll"
        })

    def move(self, from_pos, dice):
        self.send({
            "action": "move",
            "from": from_pos,
            "dice": dice
        })

    def get_state(self):
        self.send({
            "action": "state"
        })

    def close(self):
        if self.socket:
            self.socket.close()