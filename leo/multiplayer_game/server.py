import socket
import threading
import json
import random


class Server:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 5555
        self.connected_players = {}
        self.lock = threading.Lock()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started on {self.host}:{self.port}")

    def update_players(self, conn):
        with self.lock:
            payload = json.dumps(self.connected_players).encode('utf-8') + b'\n'
        conn.sendall(payload)

    def handle_connection(self, conn, addr):
        addr_str = str(addr)

        # 1. Generate a consistent random color ONCE when the client connects
        assigned_color = [
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        ]

        with self.lock:
            self.connected_players[addr_str] = [400, 300, assigned_color]

        print(f"Player connected: {addr_str} with color {assigned_color}")

        buffer = ""

        while True:
            try:
                raw_data = conn.recv(1024).decode('utf-8')
                if not raw_data:
                    break

                buffer += raw_data

                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if not line.strip():
                        continue

                    data_json = json.loads(line)

                    # 2. Update position coordinates while keeping the assigned color intact
                    with self.lock:
                        if addr_str in self.connected_players:
                            self.connected_players[addr_str][0] = data_json.get('y', 0)
                            self.connected_players[addr_str][1] = data_json.get('z', 0)
                            # assigned_color remains unchanged in index 2

                    self.update_players(conn)

                    print(self.connected_players)

            except (socket.error, json.JSONDecodeError) as e:
                break

        with self.lock:
            if addr_str in self.connected_players:
                del self.connected_players[addr_str]

        conn.close()
        print(f"Player disconnected: {addr_str}")

    def main_loop(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            thread.daemon = True
            thread.start()

server = Server()
server.main_loop()