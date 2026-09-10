import socket
import threading
import json

class Server:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.connected_players = {}  # {player_id: [x, y]}
        self.clients = {}            # {player_id: conn}
        self.lock = threading.Lock()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")

    def broadcast_state(self):
        """Send current game state to all connected players."""
        with self.lock:
            payload = (json.dumps({
                "type": "state",
                "players": self.connected_players
            }) + '\n').encode('utf-8')
            
            dead_clients = []
            for player_id, conn in self.clients.items():
                try:
                    conn.sendall(payload)
                except socket.error:
                    dead_clients.append(player_id)
            
            for player_id in dead_clients:
                self.remove_player(player_id)

    def remove_player(self, player_id):
        if player_id in self.connected_players:
            del self.connected_players[player_id]
        if player_id in self.clients:
            try:
                self.clients[player_id].close()
            except:
                pass
            del self.clients[player_id]
        print(f"[PLAYER DISCONNECTED] {player_id}")

    def handle_connection(self, conn, addr):
        player_id = f"{addr[0]}:{addr[1]}"
        print(f"[NEW CONNECTION] {player_id}")

        with self.lock:
            self.connected_players[player_id] = [400, 300]
            self.clients[player_id] = conn

        # Send the player their unique ID on first connect
        init_payload = (json.dumps({
            "type": "init",
            "id": player_id
        }) + '\n').encode('utf-8')
        try:
            conn.sendall(init_payload)
        except socket.error:
            with self.lock:
                self.remove_player(player_id)
            return

        buffer = ""
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data

                # Process every full line delimited by '\n'
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if not line:
                        continue
                    
                    msg = json.loads(line)
                    with self.lock:
                        if player_id in self.connected_players:
                            self.connected_players[player_id] = [msg['x'], msg['y']]
                    
                    self.broadcast_state()

            except (socket.error, json.JSONDecodeError, KeyError):
                break

        with self.lock:
            self.remove_player(player_id)
        self.broadcast_state()

    def main_loop(self):
        while True:
            conn, addr = self.server.accept()
            t = threading.Thread(target=self.handle_connection, args=(conn, addr), daemon=True)
            t.start()

server = Server()
server.main_loop()
