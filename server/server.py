import socket
import threading

from server.room import Room
from server.client_handler import ClientHandler


HOST = "127.0.0.1"
PORT = 5555


class Server:
    def __init__(self):
        self.room = Room()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()

        print(f"Server started on {HOST}:{PORT}")

        while True:
            client_socket, address = self.server_socket.accept()
            print("Client connected:", address)

            client_handler = ClientHandler(client_socket, address, self.room)
            self.room.add_client(client_handler)

            thread = threading.Thread(target=client_handler.handle)
            thread.start()


if __name__ == "__main__":
    server = Server()
    server.start()