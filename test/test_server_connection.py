import socket
import json

HOST = "127.0.0.1"
PORT = 5555


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    join_message = {
        "action": "join",
        "name": "Player1"
    }

    client.send(json.dumps(join_message).encode())

    response = client.recv(1024).decode()
    print("Server Response:")
    print(response)

    roll_message = {
        "action": "roll"
    }

    client.send(json.dumps(roll_message).encode())

    response = client.recv(1024).decode()
    print("Roll Response:")
    print(response)

    client.close()


if __name__ == "__main__":
    main()