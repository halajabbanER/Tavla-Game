import socket
import json

HOST = "127.0.0.1"
PORT = 5555


def receive_message(client, title):
    try:
        response = client.recv(4096).decode()
        print(f"\n=== {title} ===")
        print(response)
    except:
        print(f"{title}: No response")


def main():
    # Client 1
    client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1.connect((HOST, PORT))
    receive_message(client1, "Client1 Connected")

    # Client 2
    client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client2.connect((HOST, PORT))
    receive_message(client2, "Client2 Connected")

    # Client 3
    client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client3.connect((HOST, PORT))
    receive_message(client3, "Client3 Connected")

    input("\nPress Enter to close Client1 and exit..\n")

    client1.close()

    receive_message(client3, "Client3 After Waiting")

    client2.close()
    client3.close()


if __name__ == "__main__":
    main()