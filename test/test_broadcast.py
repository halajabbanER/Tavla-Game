import socket
import json
import threading

HOST = "127.0.0.1"
PORT = 5555


def listen(client, name):
    while True:
        try:
            response = client.recv(4096).decode()
            if not response:
                break

            print(f"\n{name} received:")
            print(response)

        except:
            break


def send(client, message):
    client.send(json.dumps(message).encode())


def main():
    # Client 1
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect((HOST, PORT))

    # Client 2
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.connect((HOST, PORT))

    # Listening Threads
    threading.Thread(
        target=listen,
        args=(client1, "Player1"),
        daemon=True
    ).start()

    threading.Thread(
        target=listen,
        args=(client2, "Player2"),
        daemon=True
    ).start()

    # Join
    send(client1, {
        "action": "join",
        "name": "Player1"
    })

    send(client2, {
        "action": "join",
        "name": "Player2"
    })

    input("\nPress Enter to roll dice...\n")

    # Roll
    send(client1, {
        "action": "roll"
    })

    input("\nPress Enter to exit...\n")

    client1.close()
    client2.close()


if __name__ == "__main__":
    main()