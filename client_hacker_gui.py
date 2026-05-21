import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from common import encrypt_message, decrypt_message

HOST = "127.0.0.1"
PORT = 5555

BG = "#000000"
FG = "#00FF00"
FONT = ("Courier", 11)

class HackerChat:
    def __init__(self, root):
        self.root = root
        self.root.title("SECURE TERMINAL v1.0")
        self.root.configure(bg=BG)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        self.username = simpledialog.askstring("Identity", "Enter codename:", parent=root)
        self.sock.send(encrypt_message(self.username))

        self.build_ui()

        threading.Thread(target=self.receive, daemon=True).start()

    def build_ui(self):
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill=tk.BOTH, expand=True)

        # Chat terminal
        self.chat = tk.Text(frame, bg=BG, fg=FG, insertbackground=FG,
                            font=FONT, state='disabled')
        self.chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # User list
        self.users = tk.Listbox(frame, bg=BG, fg=FG, font=FONT, width=20)
        self.users.pack(side=tk.RIGHT, fill=tk.Y)

        # Input
        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(fill=tk.X)

        self.entry = tk.Entry(bottom, bg=BG, fg=FG, insertbackground=FG, font=FONT)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.insert(0, "> ")
        self.entry.bind("<Return>", self.send)

    def write(self, msg):
        self.chat.config(state='normal')
        self.chat.insert(tk.END, msg + "\n")
        self.chat.config(state='disabled')
        self.chat.see(tk.END)

    def receive(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break

                msg = decrypt_message(data)

                if msg.startswith("[USERS]"):
                    users = msg.replace("[USERS]", "").split(",")
                    self.update_users(users)
                else:
                    self.write(msg)

            except:
                break

    def update_users(self, users):
        self.users.delete(0, tk.END)
        for u in users:
            self.users.insert(tk.END, f"> {u}")

    def send(self, event=None):
        msg = self.entry.get().replace("> ", "")
        if msg.strip() == "":
            return

        full = f"{self.username}: {msg}"
        self.sock.send(encrypt_message(full))

        self.entry.delete(0, tk.END)
        self.entry.insert(0, "> ")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    app = HackerChat(root)
    root.mainloop()