import socket
import threading
import json
import time

class Client:
    def __init__(self, port, host='localhost'):
        print(333)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.stop_flag = threading.Event()

    def quit(self):
        self.send_message("")
        self.stop()

    def llm_call(self, history, prompt, system):
        message = []

        if system:
            history.append((system, "Okay, I will play the game with you according to the rules."))

        for chat in history:
            message.extend(
                (
                    {"role": "user", "content": chat[0]},
                    {"role": "agent", "content": chat[1]},
                )
            )
        message.append({
            "role": "user",
            "content": prompt
        })
        #with open("client.txt", "a") as f:
        #    f.write(json.dumps(message) + "\n")
        self.send_message(json.dumps(message))
        return self.receive_messages()
    
    def receive_messages(self):
        while not self.stop_flag.is_set():
            if data := self.socket.recv(1000000).decode():
                return data

    def send_message(self, message):
        self.socket.sendall(message.encode())

    def stop(self):
        self.stop_flag.set()
        self.socket.close()