import socket
import json

HOST = "127.0.0.1"
PORT = 5555


def send_message(client, message):
    client.send(json.dumps(message).encode())
    response = client.recv(1024).decode()
    print(response)


def main():
    # Client 1
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect((HOST, PORT))

    # Client 2
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.connect((HOST, PORT))

    print("=== Player1 Join ===")
    send_message(client1, {
        "action": "join",
        "name": "Player1"
    })

    print("\n=== Player2 Join ===")
    send_message(client2, {
        "action": "join",
        "name": "Player2"
    })

    print("\n=== Player1 Roll ===")
    send_message(client1, {
        "action": "roll"
    })

    print("\n=== Player1 Try Again (Should Fail) ===")
    send_message(client1, {
        "action": "roll"
    })

    print("\n=== Player2 Roll ===")
    send_message(client2, {
        "action": "roll"
    })

    client1.close()
    client2.close()


if __name__ == "__main__":
    main()