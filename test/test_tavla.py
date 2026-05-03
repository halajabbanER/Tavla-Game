import socket
import json

HOST = "127.0.0.1"
PORT = 5555


def send_message(client, message):
    client.send(json.dumps(message).encode())
    response = client.recv(4096).decode()

    try:
        parsed = json.loads(response)
        print(json.dumps(parsed, indent=4))
    except:
        print(response)


def main():
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect((HOST, PORT))

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

    print("\n=== Player1 Move ===")
    send_message(client1, {
        "action": "move",
        "from": 0,
        "dice": 2
    })

    print("\n=== Game State ===")
    send_message(client1, {
        "action": "state"
    })

    client1.close()
    client2.close()


if __name__ == "__main__":
    main()