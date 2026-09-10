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

    def update_players(self, conn):
        payload = json.dumps(self.connected_players).encode('utf-8')+b'\n'
        conn.sendall(payload)

    def handle_connection(self, conn, addr):
        addr_str = str(addr)
        self.connected_players[addr_str] = [0, 0]
        while True:
            try:
                raw_data = conn.recv(1024).decode('utf-8')
                if not raw_data:
                    break

                data_json = json.loads(raw_data.strip())
                self.connected_players[addr][0] = data_json[0]
                self.connected_players[addr][1] = data_json[1]

                self.update_players(conn)
            except socket.error:
                break
            except json.JSONDecodeError:
                break

        if addr in self.connected_players:
            del self.connected_players[addr]
        conn.close()

    def main_loop(self):
        while True:
            conn, addr = self.server.accept()
            # 1. Create the Thread object
            thread = threading.Thread(target=self.handle_connection, args=(conn, addr))
            # 2. Set daemon attribute (no parentheses)
            thread.daemon = True
            # 3. Start the thread
            thread.start()

server = Server()
server.main_loop()

