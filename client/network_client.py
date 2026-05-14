import socket
import json
import threading


class NetworkClient:
    def __init__(self, host="18.232.175.37", port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.on_message = None
        self.connected = False

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True

            print("Connected to server")

            thread = threading.Thread(target=self.listen, daemon=True)
            thread.start()

            return True

        except Exception as e:
            print("Connection failed:", e)
            self.connected = False
            return False

    def listen(self):
        while self.connected:
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

        self.connected = False
        print("Disconnected from server")

    def send(self, message):
        if not self.connected:
            print("Not connected to server")
            return

        try:
            self.socket.sendall(json.dumps(message).encode())
        except Exception as e:
            print("Send error:", e)
            self.connected = False

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

    def skip(self, dice):
        self.send({
            "action": "skip",
            "dice": dice
        })

    def get_state(self):
        self.send({
            "action": "state"
        })

    def close(self):
        self.connected = False

        try:
            if self.socket:
                self.socket.close()
        except:
            pass