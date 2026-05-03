import socket
import threading
import json


class Client:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            return True
        except Exception as e:
            print("Connection failed:", e)
            return False

    def send(self, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)

            self.socket.send(message.encode())

        except Exception as e:
            print("Send failed:", e)

    def receive(self):
        try:
            data = self.socket.recv(4096).decode()
            if not data:
                return None

            try:
                return json.loads(data)
            except:
                return data

        except:
            return None

    def start_listening(self, callback):
        def listen():
            while True:
                data = self.receive()
                if data is None:
                    break

                # ❌ حذفنا الطباعة
                callback(data)

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def close(self):
        try:
            self.socket.close()
        except:
            pass