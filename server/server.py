import socket
import threading

from server.room import Room
from server.client_handler import ClientHandler


HOST = "0.0.0.0"
PORT = 5555


class Server:
    def __init__(self):
        self.room = Room()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

    def start(self):
        try:
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen()

            print(f"Server started on {HOST}:{PORT}", flush=True)

            while True:
                client_socket, address = self.server_socket.accept()
                print("Client connected:", address, flush=True)

                client_handler = ClientHandler(
                    client_socket,
                    address,
                    self.room
                )

                self.room.add_client(client_handler)

                thread = threading.Thread(
                    target=client_handler.handle,
                    daemon=True
                )
                thread.start()

        except OSError as e:
            print("Server error:", e, flush=True)
            print("Maybe the port is already used.", flush=True)

        except KeyboardInterrupt:
            print("\nServer stopped.", flush=True)

        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start()