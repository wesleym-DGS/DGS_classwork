import socket
import sys
import json
import pygame


class Client:
    def __init__(self):
        pygame.init()
        self.server_address = ('127.0.0.1', 5555)
        self.screenW = 800
        self.screenH = 600
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))
        pygame.display.set_caption('Multiplayer Game')
        self.clock = pygame.time.Clock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(0.1)
        self.render_list = []  # Stores tuples: (Vector2(x, y), (r, g, b))
        self.game = True

        try:
            self.client.connect(self.server_address)
        except socket.error as e:
            print(f"Connection error: {e}")
            sys.exit()

    def receive(self):
        buffer = ''
        while '\n' not in buffer:
            try:
                chunk = self.client.recv(1024).decode('utf-8')
                if not chunk:
                    return None
                buffer += chunk
            except (socket.timeout, socket.error):
                return None
        return json.loads(buffer.strip())

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False

    def update_pos(self, player):
        # Client only sends position coordinates
        payload = json.dumps({
            "y": int(player.pos.x),
            "z": int(player.pos.y)
        }) + '\n'

        try:
            self.client.sendall(payload.encode('utf-8'))
            server_data = self.receive()
            if server_data:
                self.render_list.clear()
                # Server sends: { player_id: [x, y, [r, g, b]] }
                for addr_str, player_info in server_data.items():
                    pos = pygame.Vector2(player_info[0], player_info[1])
                    color = tuple(player_info[2])
                    self.render_list.append((pos, color))
        except socket.timeout:
            pass
        except (socket.error, json.JSONDecodeError):
            self.game = False

    def render(self):
        self.screen.fill((30, 30, 30))

        # Render each player using their position and assigned color
        for pos, color in self.render_list:
            pygame.draw.circle(self.screen, color, (int(pos.x), int(pos.y)), 15)

        pygame.display.flip()


class Player:
    def __init__(self, screenW, screenH):
        self.pos = pygame.Vector2(screenW / 2, screenH / 2)
        self.speed = 5

    def move(self):
        move_dir = pygame.Vector2(0, 0)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_dir.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_dir.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_dir.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_dir.y += 1

        if move_dir.length() > 0:
            move_dir = move_dir.normalize()
            self.pos += move_dir * self.speed

        self.pos.x = max(15, min(785, self.pos.x))
        self.pos.y = max(15, min(585, self.pos.y))


client = Client()
player = Player(client.screenW, client.screenH)

while client.game:
    client.clock.tick(60)
    client.check_quit()
    player.move()
    client.update_pos(player)
    client.render()

client.client.close()
pygame.quit()