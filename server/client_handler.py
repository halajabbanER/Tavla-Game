import json


class ClientHandler:
    def __init__(self, client_socket, address, room):
        self.client_socket = client_socket
        self.address = address
        self.room = room
        self.player_id = str(address)

    def handle(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode()

                if not data:
                    break

                message = json.loads(data)
                response = self.room.handle_message(self, message)

                if response:
                    self.send(response)

        except Exception as e:
            print("Client error:", e)

        finally:
            self.room.remove_client(self)
            self.client_socket.close()

    def send(self, data):
        message = json.dumps(data)
        self.client_socket.send(message.encode())