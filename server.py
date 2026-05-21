import socket
import threading
from common import decrypt_message, encrypt_message

clients = []
usernames = {}

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def send_user_list():
    user_list = ",".join(usernames.values())
    msg = encrypt_message(f"[USERS]{user_list}")
    for client in clients:
        try:
            client.send(msg)
        except:
            pass

def broadcast_system(msg):
    encrypted = encrypt_message(f"[SYSTEM] {msg}")
    for client in clients:
        try:
            client.send(encrypted)
        except:
            pass

def handle_client(conn, addr):
    print(f"[NEW] {addr}")
    clients.append(conn)

    try:
        username = decrypt_message(conn.recv(4096))
        usernames[conn] = username

        broadcast_system(f"{username} connected")
        send_user_list()

        while True:
            data = conn.recv(4096)
            if not data:
                break

            message = decrypt_message(data)
            print(f"[{username}] {message}")

            with open("chat.log", "a") as f:
                f.write(f"{username}: {message}\n")

            broadcast(data, conn)

    except:
        pass

    finally:
        clients.remove(conn)
        name = usernames.pop(conn, "Unknown")
        broadcast_system(f"{name} disconnected")
        send_user_list()
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen()

    print("[LISTENING] Port 5555...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start()