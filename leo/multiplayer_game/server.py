import socket
import threading
import json


class Server:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 5555
        self.connected_players = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server started on {self.host}:{self.port}")

    def update_players(self, conn):
        payload = json.dumps(self.connected_players).encode('utf-8') + b'\n'
        conn.sendall(payload)

    def handle_connection(self, conn, addr):
        addr_str = str(addr)
        self.connected_players[addr_str] = [0, 0]
        print(f"Player connected: {addr_str}")

        while True:
            try:
                raw_data = conn.recv(1024).decode('utf-8')
                if not raw_data:
                    break

                data_json = json.loads(raw_data.strip())

                # Match client keys ('y' and 'z') and update using addr_str
                self.connected_players[addr_str][0] = data_json['y']
                self.connected_players[addr_str][1] = data_json['z']

                self.update_players(conn)
            except (socket.error, json.JSONDecodeError, KeyError) as e:
                break

        # Disconnect cleanup using addr_str
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